# SkillSpector v2.12.0

Release status: candidate; publication pending.

## Summary

SkillSpector 2.12.0 adds an opt-in CLI gate for any active finding and a configurable static-analysis allowance. It also fixes false AE1 incomplete-analysis results caused by ordinary Markdown and JSON documentation, makes discovery and requested-analysis gaps explicit, preserves distinct findings and their source locations, detects letter-spaced prompt instructions, and reduces false positives in companion CLI documentation and literal current-skill references. Oversized files now produce an explicit coverage finding and bounded LLM input.

## Highlights

- Recognize complete JSON strings and Markdown code spans in their document context, avoiding false analysis limits while retaining analysis of their contents.
- Keep delimiter pairing within Markdown blocks and table cells so unrelated documentation cannot hide unresolved runtime commands.
- Scan JSON quote candidates in linear time and retain cancellation handling.
- Preserve distinct full-evidence and rule identities, including findings with identical shortened previews, and retain precise locations for repeated occurrences.
- Keep requested but unavailable or incomplete semantic analysis visible in completeness metadata and strict CLI/MCP decisions.
- Classify narrowly proven OAuth, signed self-update, and warned installer documentation in context while retaining the underlying findings and fail-closed controls.
- Suppress AS3 only when a literal `skills/<name>/SKILL.md` path identifies the skill currently being scanned, while retaining peer-skill, transformed, and enumeration findings.

## Added

- `SKILLSPECTOR_MAX_STATIC_ANALYSIS_SECONDS_PER_ARTIFACT` configures the static pattern and YARA time allowance per artifact; its default increases from 30 to 300 seconds. The remaining workflow deadline still bounds both analyzers.
- `skillspector scan --fail-on-findings` exits with code 1 when a scan reports any active finding, including findings below the default risk-score threshold. It applies to single-skill, recursive, and MCP registry scans. Skill scans evaluate active findings after suppression ([#469](https://github.com/NVIDIA/SkillSpector/pull/469)).

## Changed

- Align provider setup guidance, add the HVTrust badge, and update research background counts ([#434](https://github.com/NVIDIA/SkillSpector/pull/434), [#428](https://github.com/NVIDIA/SkillSpector/pull/428), [#543](https://github.com/NVIDIA/SkillSpector/pull/543)).
- Reports retain requested LLM intent separately from runtime availability. Incomplete semantic execution remains visible through aggregate reports and CLI/MCP installation gates ([#410](https://github.com/NVIDIA/SkillSpector/pull/410)).

## Fixed

- Avoid false AE1 results from valid JSON placeholders, inline code, list and blockquote containers, indented JSON, Markdown tables, and literal Make syntax ([#516](https://github.com/NVIDIA/SkillSpector/pull/516)).
- Bound JSON quote traversal without repeatedly scanning overlapping suffixes ([#521](https://github.com/NVIDIA/SkillSpector/pull/521)).
- Emit a HIGH AE7 analysis-evasion finding for per-file size limits that leave an artifact partially inspected, unless AE1 already covers that path. Supply a bounded text prefix and an explicit unreviewed-region marker to enabled LLM analysis; the unread region remains incomplete ([#509](https://github.com/NVIDIA/SkillSpector/pull/509)).
- Preserve full-evidence fingerprints, concrete YARA rule identity, and precise occurrence locations through projection, deduplication, and report compaction. Separate findings are retained while duplicate projections of the same occurrence are collapsed ([#409](https://github.com/NVIDIA/SkillSpector/pull/409)).
- Detect letter-spaced P3/P4 prompt instructions through bounded reconstruction, retain source evidence, and report ambiguous or irregular letter-spacing reconstruction as AE6 incomplete coverage ([#470](https://github.com/NVIDIA/SkillSpector/pull/470)).
- Discover skills inside dot-prefixed directories, retain inherited local-only restrictions for child skills, and partition transitive scan caching by those privacy restrictions ([#410](https://github.com/NVIDIA/SkillSpector/pull/410)).
- Preserve incomplete discovery and requested semantic-analysis failures, including unavailable providers and mixed success/failure telemetry, instead of allowing a complete scan result ([#410](https://github.com/NVIDIA/SkillSpector/pull/410)).
- Emit recursive JSON reports to standard output when no output path is provided ([#467](https://github.com/NVIDIA/SkillSpector/pull/467)).
- Use the project manifest version for RP3 analysis ([#474](https://github.com/NVIDIA/SkillSpector/pull/474)).
- Prefer exact known-package matches when evaluating SC6 package-name similarity ([#530](https://github.com/NVIDIA/SkillSpector/pull/530)).
- Avoid treating slash-separated prose as local file references ([#451](https://github.com/NVIDIA/SkillSpector/pull/451)).
- Reduce false-positive severity for narrowly proven companion CLI OAuth results and signed self-update documentation while preserving risky findings, and provide contextual explanations for warned pipe-to-shell installers ([#547](https://github.com/NVIDIA/SkillSpector/pull/547)).
- Ignore literal AS3 references to the current skill, derived from the scan-root basename or manifest name, without suppressing peer-skill or obfuscated-path access ([#506](https://github.com/NVIDIA/SkillSpector/pull/506)).
- Skip symlink test cases when the platform refuses symlink creation ([#501](https://github.com/NVIDIA/SkillSpector/pull/501)).

## Security

- Genuine removal instructions remain reportable. The covered unresolved-runtime-command controls retain incomplete coverage and fail strict CLI/MCP installation gates, including when semantic analysis succeeds. Additional runtime-selected command variants remain under investigation (see Known Limitations).
- JSON string ownership preserves source evidence and does not exempt string contents from analysis.
- Findings and exit status can change after upgrading: oversized files can add HIGH AE7 findings, letter-spaced instructions can produce P3/P4 or AE6 findings, and previously collapsed distinct matches can increase the retained finding count and risk score. Missing requested analysis remains incomplete even when static analysis finishes.
- Context-aware companion CLI classification can lower severity, scores, or recommendations for narrowly proven benign documentation. Risky token transfers, unsafe self-update variants, and pipe-to-shell installers remain reportable.
- Literal current-skill references no longer produce AS3 findings. Peer-skill references, transformed or obfuscated paths, explicit enumeration, AS1, and AS2 remain reportable.

## Breaking Changes and Migration

- No new configuration is required. Static analysis can now run longer within the existing workflow deadline. Set `SKILLSPECTOR_MAX_STATIC_ANALYSIS_SECONDS_PER_ARTIFACT=30` to retain the previous per-artifact allowance, and restart the SkillSpector process after changing the setting ([#522](https://github.com/NVIDIA/SkillSpector/pull/522)).
- `--fail-on-findings` is opt-in. Combine it with `--fail-on-incomplete` when CI must reject either active findings or incomplete coverage. Code 2 still denotes an input or execution error; a nonzero exit alone does not identify which condition occurred.
- Consumers should retain completeness/degradation metadata and inspect findings as well as exit status. Explicitly use `--no-llm` for an intended static-only scan; requesting LLM analysis without an available provider is incomplete.
- Third-party dependency versions are unchanged from 2.11.2.

## Deprecations

- None.

## Validation

The release candidate includes main commit `9e078093eb8e621852e937cdc1757dca1c41ad05`. Validated locally with Python 3.12.13:

- `uv lock --check --offline` passed with the locked dependency set.
- `make test-ci` passed 5,235 tests, with 14 skipped, 38 deselected, 4 expected failures, and 90% coverage.
- Ruff lint and format checks passed for all source and test files.
- The CLI reported `SkillSpector v2.12.0`; the release helper dry run resolved `v2.12.0` and the matching versioned notes.
- All 10 release helper and workflow tests passed.
- Wheel and source distributions built successfully, and Twine validated both artifacts.
- `git diff --check` passed.

Hosted checks, deployment/provider validation, and the separate release gates below remain pending for the final PR head. Earlier candidate results apply only to their recorded commits and are not certification of this candidate.

[Release PR #550](https://github.com/NVIDIA/SkillSpector/pull/550) records the candidate baseline, validation results, known gaps, and remaining release gates.

## Known Limitations

- Local sanity checks cover the tested inputs and environment; live provider and deployment behavior depend on their configuration.
- Incomplete inspection is a reportable result. Unsupported inputs, unavailable requested analysis, and resource limits must remain visible; these conditions cannot be treated as a clean scan.
- The release remains a candidate while current-head CI and outstanding release issues are assessed. Proposed fixes in unmerged PRs are not included in this candidate.
- Current validation found that public report serialization can repeat the first occurrence's columns for other matches; SARIF does not yet preserve these column coordinates. The internal occurrence improvements in #409 do not establish correct locations in every output format. See [release validation](https://github.com/NVIDIA/SkillSpector/pull/550) for the tracked report defect.
- Some runtime-selected command variants and Markdown reference destinations still have open completeness defects. Proposed fixes [#514](https://github.com/NVIDIA/SkillSpector/pull/514) and [#553](https://github.com/NVIDIA/SkillSpector/pull/553) are not included in this candidate.

## References

- [Changes since v2.11.2](https://github.com/NVIDIA/SkillSpector/compare/v2.11.2...v2.12.0)
- [AE1 documentation fix #516](https://github.com/NVIDIA/SkillSpector/pull/516)
- [Static analysis time allowance #522](https://github.com/NVIDIA/SkillSpector/pull/522)

Prepared by Codex for Mohit Gupta.
