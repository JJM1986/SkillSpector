# SPDX-FileCopyrightText: Copyright (c) 2026 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

"""Perl host-string boundaries must not invent shell parse failures."""

import sys
import time
from pathlib import Path

import pytest

from skillspector.graph import graph
from skillspector.inspection_ledger import LedgerOutcome, LedgerReason
from skillspector.nodes.analyzers import static_patterns_tool_misuse as tm
from skillspector.nodes.analyzers import static_runner


def _scan(content: str) -> dict:
    return static_runner.run_static_patterns_with_ledger(
        {"components": ["scripts/helper.pl"], "file_cache": {"scripts/helper.pl": content}},
        [tm],
    )


@pytest.mark.parametrize(
    "statement",
    [
        'print "Use rm to remove a project\\n";',
        "print 'Use rm to remove a project';",
        '    print("Use rm to remove a project\\n");',
        'print STDERR "Use rm to remove a project\\n";',
        'print "Use rm to remove a project\\n"; # usage text',
        'print "Use rm to remove a \\"project\\"\\n";',
        'my $q = 1;\nprint "Use rm to remove a project\\n";',
        'my $text = "a multiline\nstring";\nprint "Use rm to remove a project\\n";',
        'if ($help) {\n    print "Use rm to remove a project\\n";\n}',
    ],
)
def test_literal_perl_help_has_complete_analysis(statement: str) -> None:
    result = _scan("#!/usr/bin/env perl\nuse strict;\nuse warnings;\n" + statement + "\n")

    assert result["findings"] == []
    assert all(row["outcome"] is LedgerOutcome.COMPLETED for row in result["inspection_ledger"])


def test_referenced_perl_help_does_not_emit_ae1(tmp_path: Path) -> None:
    (tmp_path / "scripts").mkdir()
    (tmp_path / "SKILL.md").write_text(
        "---\nname: perl-help\ndescription: Print help for a project tool.\n---\n\n"
        "Run `scripts/helper.pl`.\n\nSee `scripts/helper.pl`.\n"
    )
    (tmp_path / "scripts/helper.pl").write_text(
        '#!/usr/bin/env perl\nuse strict;\nuse warnings;\nprint "Use rm to remove a project\\n";\n'
    )

    result = graph.invoke({"input_path": str(tmp_path), "use_llm": False, "output_format": "json"})

    assert result["analysis_completeness"]["status"] == "complete"
    assert not any(finding.rule_id == "AE1" for finding in result["findings"])


@pytest.mark.parametrize(
    "statement",
    [
        'system("rm -rf /");',
        'exec("rm -rf /");',
        "my $output = `rm -rf /`;",
        "my $output = qx(rm -rf /);",
        "print \"${\\system('rm -rf /')}\";",
        'print "Use rm -rf *";',
        'print "Use rm -rf /";',
        'print "Use rm to remove a project\\n";\nsystem("rm -rf /");',
    ],
)
def test_executable_and_printed_dangerous_commands_remain_visible(statement: str) -> None:
    result = _scan(statement + "\n")

    assert any(finding.rule_id == "TM1" for finding in result["findings"])


@pytest.mark.parametrize(
    "content",
    [
        'print "Use rm $project\\n";',
        'print "Use rm @projects\\n";',
        'print "Use rm `command`\\n";',
        'system("sudo rm -rf *");',
        'my $message = "Use rm to remove a project\\n";',
        'my $message = \'unclosed\nprint "Use rm to remove a project\\n";',
        'my $message = q{\nprint "Use rm to remove a project\\n";\n};',
        'my $message = <<END;\nprint "Use rm to remove a project\\n";\nEND',
    ],
)
def test_unsupported_or_ambiguous_source_keeps_conservative_parse_status(content: str) -> None:
    assert tm.has_bounded_parse_exhaustion(content, lambda: None, file_type="perl") is True


@pytest.mark.parametrize(
    "content",
    [
        'print "Use rm to remove a project;',
        'print "Use rm to remove a project\\";',
        "my $text = '\nprint \"Use rm to remove a project\\n\";\n';",
        'print "Use rm to remove a project\\n"; print "another value";',
    ],
)
def test_unproven_literal_delimiters_do_not_acquire_ownership(content: str) -> None:
    assert tm._perl_literal_print_shell_text(content, lambda: None) == content
    assert tm.has_bounded_parse_exhaustion(content, lambda: None, file_type="perl") == (
        tm.has_bounded_parse_exhaustion(content, lambda: None, file_type="shell")
    )


@pytest.mark.parametrize("operator", ["q", "qq", "qx", "qr", "m", "s", "tr", "y"])
@pytest.mark.parametrize("prefix", ["", "CORE::"])
def test_word_delimited_quote_operator_does_not_grant_print_ownership(
    operator: str, prefix: str
) -> None:
    # Perl accepts a word delimiter when whitespace separates it from the
    # operator. In particular, qx can contain an executable shell program.
    content = f'my $value = {prefix}{operator} X\nprint "Use rm to remove a project\\n";\nX;\n'
    assert tm._perl_literal_print_shell_text(content, lambda: None) == content
    assert tm.has_bounded_parse_exhaustion(content, lambda: None, file_type="perl") is True


@pytest.mark.parametrize("operator", ["q", "qq", "qx", "qr"])
def test_core_quote_operator_does_not_grant_print_ownership(operator: str) -> None:
    content = f'my $value = CORE::{operator}{{\nprint "Use rm to remove a project\\n";\n}};\n'
    assert tm._perl_literal_print_shell_text(content, lambda: None) == content
    assert tm.has_bounded_parse_exhaustion(content, lambda: None, file_type="perl") is True


def test_host_ownership_honors_runtime_checks_inside_long_literals() -> None:
    content = 'print "Use rm ' + "safe " * 20_000 + '";\n'
    checks = 0

    def check_runtime() -> None:
        nonlocal checks
        checks += 1
        if checks >= 20:
            raise TimeoutError("test runtime bound")

    with pytest.raises(TimeoutError, match="test runtime bound"):
        tm.has_bounded_parse_exhaustion(content, check_runtime, file_type="perl")


def test_nonmatching_print_whitespace_prepass_is_linear_and_checks_runtime() -> None:
    content = "print" + " " * 100_000 + "x\n"
    checks = 0

    def check_runtime() -> None:
        nonlocal checks
        checks += 1
        if checks == 2:
            raise TimeoutError("test runtime bound after prepass")

    started = time.perf_counter()
    with pytest.raises(TimeoutError, match="test runtime bound after prepass"):
        tm._perl_literal_print_shell_text(content, check_runtime)
    assert time.perf_counter() - started < (12.0 if sys.gettrace() is not None else 2.0)


def test_print_literal_does_not_bypass_shell_parser_bounds() -> None:
    content = 'print "Use rm ' + "safe " * 2_000 + '-rf *";\n'
    result = _scan(content)

    assert any(
        row["outcome"] is LedgerOutcome.PARTIAL
        and row["reason_code"] is LedgerReason.STATIC_PARSE_LIMIT
        for row in result["inspection_ledger"]
    )


@pytest.mark.parametrize("file_type,complete_context", [("shell", True), ("perl", False)])
def test_only_complete_perl_source_can_grant_host_quote_ownership(
    file_type: str, complete_context: bool
) -> None:
    assert (
        tm.has_bounded_parse_exhaustion(
            'print "Use rm to remove a project\\n";',
            lambda: None,
            file_type=file_type,
            complete_context=complete_context,
        )
        is True
    )
