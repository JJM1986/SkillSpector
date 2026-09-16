# SkillSpector v2.11.3

Release status: candidate; publication pending.

## Summary

SkillSpector 2.11.3 fixes false AE1 incomplete-analysis results caused by ordinary Markdown and JSON documentation. It also makes discovery and requested-analysis gaps explicit, preserves distinct findings and their source locations, detects letter-spaced prompt instructions, and adds an opt-in CLI gate for any active finding. Oversized files now produce an explicit coverage finding and bounded LLM input.

## Highlights

- Recognize complete JSON strings and Markdown code spans in their document context, avoiding false analysis limits while retaining analysis of their contents.
- Keep delimiter pairing within Markdown blocks and table cells so unrelated documentation cannot hide unresolved runtime commands.
- Scan JSON quote candidates in linear time and retain cancellation handling.
- Preserve distinct full-evidence and rule identities, including findings with identical shortened previews, and retain precise locations for repeated occurrences.
- Keep requested but unavailable or incomplete semantic analysis visible in completeness metadata and strict CLI/MCP decisions.

## Added

- `SKILLSPECTOR_MAX_STATIC_ANALYSIS_SECONDS_PER_ARTIFACT` configures the static pattern and YARA time allowance per artifact; its default increases from 30 to 300 seconds. The remaining workflow deadline still bounds both analyzers.
- `skillspector scan --fail-on-findings` exits with code 1 when a scan reports any active finding, including findings below the default risk-score threshold. It applies to single-skill, recursive, and MCP registry scans. Skill scans evaluate active findings after suppression ([#469](https://github.com/NVIDIA/SkillSpector/pull/469)).

## Changed

- Align provider setup guidance and update research background documentation.
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
- Skip symlink test cases when the platform refuses symlink creation ([#501](https://github.com/NVIDIA/SkillSpector/pull/501)).

## Security

- Genuine removal instructions remain reportable. The covered unresolved-runtime-command controls retain incomplete coverage and fail strict CLI/MCP installation gates, including when semantic analysis succeeds. Additional runtime-selected command variants remain under investigation (see Known Limitations).
- JSON string ownership preserves source evidence and does not exempt string contents from analysis.
- Findings and exit status can change after upgrading: oversized files can add HIGH AE7 findings, letter-spaced instructions can produce P3/P4 or AE6 findings, and previously collapsed distinct matches can increase the retained finding count and risk score. Missing requested analysis remains incomplete even when static analysis finishes.

## Breaking Changes and Migration

- No new configuration is required. Static analysis can now run longer within the existing workflow deadline. Set `SKILLSPECTOR_MAX_STATIC_ANALYSIS_SECONDS_PER_ARTIFACT=30` to retain the previous per-artifact allowance, and restart the SkillSpector process after changing the setting ([#522](https://github.com/NVIDIA/SkillSpector/pull/522)).
- `--fail-on-findings` is opt-in. Combine it with `--fail-on-incomplete` when CI must reject either active findings or incomplete coverage. Code 2 still denotes an input or execution error; a nonzero exit alone does not identify which condition occurred.
- Consumers should retain completeness/degradation metadata and inspect findings as well as exit status. Explicitly use `--no-llm` for an intended static-only scan; requesting LLM analysis without an available provider is incomplete.
- Third-party dependency versions are unchanged from 2.11.2.

## Deprecations

- None.

## Validation

The release candidate includes main commit `0a8b80c36cad7c503f98548d0fa166f90a50294c`. Validation is being repeated against the resulting 2.11.3 artifact after the merges listed above. Earlier results apply only to their recorded commits and are not current-candidate certification.

[Release PR #550](https://github.com/NVIDIA/SkillSpector/pull/550) records the candidate commit, artifact identity, regression and integration results, and remaining release gates.

## Known Limitations

- Local sanity checks cover the tested inputs and environment; live provider and deployment behavior depend on their configuration.
- Incomplete inspection is a reportable result. Unsupported inputs, unavailable requested analysis, and resource limits must remain visible; these conditions cannot be treated as a clean scan.
- The release remains a draft while current-candidate validation and outstanding release issues are assessed. Proposed fixes in unmerged PRs are not included in this candidate.
- Current validation found that public report serialization can repeat the first occurrence's columns for other matches; SARIF does not yet preserve these column coordinates. The internal occurrence improvements in #409 do not establish correct locations in every output format. See [release validation](https://github.com/NVIDIA/SkillSpector/pull/550) for the tracked report defect.
- Some runtime-selected command variants and Markdown reference destinations still have open completeness defects. Proposed fixes [#514](https://github.com/NVIDIA/SkillSpector/pull/514) and [#553](https://github.com/NVIDIA/SkillSpector/pull/553) are not included in this candidate.

## References

- [Changes since v2.11.2](https://github.com/NVIDIA/SkillSpector/compare/v2.11.2...v2.11.3)
- [AE1 documentation fix #516](https://github.com/NVIDIA/SkillSpector/pull/516)
- [Static analysis time allowance #522](https://github.com/NVIDIA/SkillSpector/pull/522)

Prepared by Codex for Mohit Gupta.
