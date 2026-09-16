# SkillSpector v2.12.0

Release status: candidate; publication pending.

## Summary

SkillSpector 2.12.0 adds an opt-in CLI gate for any active finding, a configurable static-analysis allowance, an OpenCode CLI semantic-analysis provider, and an OpenCode-native scan command and tool. It also fixes false AE1 incomplete-analysis results caused by ordinary Markdown and JSON documentation, makes discovery and requested-analysis gaps explicit, inventories excluded executable content, preserves distinct findings and their source locations, adds bounded reconstruction for letter-spaced prompt instructions, and reduces false positives in companion CLI documentation and literal current-skill references. Oversized files now produce an explicit coverage finding and bounded LLM input.

## Highlights

- Run semantic analysis through the new `opencode_cli` provider and invoke SkillSpector from OpenCode through a native `/skillspector` command and `skillspector_scan` tool.
- Inventory executable and loadable content in normally excluded locations, preserving coverage evidence and failing closed when referenced or otherwise outside inspection coverage.
- Keep multilingual batch language detection and gap-fill on the graph's validated provider-eligible cache instead of rereading paths after inspection.
- Retarget per-call LLM deadlines on existing clients to avoid connection-pool churn and closed-event-loop cleanup failures.
- Honor model-registry overrides for CLI providers and accept valid Windows 8.3 aliases without weakening opened-handle validation.
- Recognize complete JSON strings and Markdown code spans in their document context, avoiding false analysis limits while retaining analysis of their contents.
- Keep delimiter pairing within Markdown blocks and table cells so unrelated documentation cannot hide unresolved runtime commands.
- Scan JSON quote candidates in linear time and retain cancellation handling.
- Preserve distinct full-evidence and rule identities, including findings with identical shortened previews, and retain precise locations for repeated occurrences.
- Keep requested but unavailable or incomplete semantic analysis visible in completeness metadata and strict CLI/MCP decisions.
- Classify selected OAuth, signed self-update, and warned installer documentation based on surrounding context, subject to the PE3 and RA1 gaps recorded under Known Limitations.
- Suppress AS3 only when a literal `skills/<name>/SKILL.md` path identifies the skill currently being scanned, while retaining peer-skill, transformed, and enumeration findings.

## Added

- `SKILLSPECTOR_PROVIDER=opencode_cli` runs semantic analysis through a local OpenCode login. The verified deny-all policy requires exactly OpenCode 1.18.30; authentication, version, policy, empty-output, or event-envelope failures fail closed. `SKILLSPECTOR_MODEL` remains optional ([#536](https://github.com/NVIDIA/SkillSpector/pull/536)).
- The repository-provided OpenCode extension adds a static-by-default `/skillspector` command and `skillspector_scan` tool. Copy `.opencode/` from a checkout to install it; the wheel does not install the extension. It resolves the binary from `SKILLSPECTOR_BIN`, a worktree `.venv`, or `PATH`, requests required host capabilities before launch, rejects symlinked target/output/binary paths, and uses a 120-second timeout with bounded, redacted output. Semantic analysis is opt-in through `noLlm=false` and the provider environment ([#537](https://github.com/NVIDIA/SkillSpector/pull/537)).
- `SKILLSPECTOR_MAX_STATIC_ANALYSIS_SECONDS_PER_ARTIFACT` configures the static pattern and YARA time allowance per artifact; its default increases from 30 to 300 seconds. The remaining workflow deadline still bounds both analyzers.
- `skillspector scan --fail-on-findings` exits with code 1 when a scan reports any active finding, including findings below the default risk-score threshold. It applies to single-skill, recursive, and MCP registry scans. Skill scans evaluate active findings after suppression ([#469](https://github.com/NVIDIA/SkillSpector/pull/469)).

## Changed

- CLI-backed providers now honor `SKILLSPECTOR_MODEL_REGISTRY` for context and output-token limits. Missing entries retain the existing fallback behavior; malformed registry structures or invalid and non-positive budgets warn and fall back ([#463](https://github.com/NVIDIA/SkillSpector/pull/463)).
- The repository's `contrib/batch_scan` tool reuses the graph's validated `llm_file_cache` for multilingual language detection and gap-fill, avoiding a second raw filesystem read and retaining provider/local-only boundaries. `contrib` remains outside the wheel ([#558](https://github.com/NVIDIA/SkillSpector/pull/558)).
- Align provider setup guidance, add the HVTrust badge, and update research background counts ([#434](https://github.com/NVIDIA/SkillSpector/pull/434), [#428](https://github.com/NVIDIA/SkillSpector/pull/428), [#543](https://github.com/NVIDIA/SkillSpector/pull/543)).
- Reports retain requested LLM intent separately from runtime availability. Incomplete semantic execution remains visible through aggregate reports and CLI/MCP installation gates ([#410](https://github.com/NVIDIA/SkillSpector/pull/410)).

## Fixed

- Retarget dynamic workflow deadlines on existing OpenAI, Anthropic, and agent-CLI clients instead of constructing a new client per call, preventing connection-pool churn and closed-event-loop cleanup errors while preserving retry and concurrency behavior ([#520](https://github.com/NVIDIA/SkillSpector/pull/520)).
- Preserve whole-document Markdown ownership when recovering commands from validated JSON strings so fenced or literal content is not reinterpreted as standalone Markdown and unresolved commands cannot become a clean result through unrelated JSON adjacency ([#559](https://github.com/NVIDIA/SkillSpector/pull/559)).
- Inventory normally excluded executable and loadable content, retain root-coverage evidence, resolve explicit extensionless command paths, and inspect excluded ZIP-family containers within existing limits. Referenced executable exclusions or incomplete excluded-artifact inspection now emit HIGH SC9/incomplete evidence with the existing minimum score of 51 (`DO_NOT_INSTALL`); the narrow exception for direct, non-binary `.git/hooks/*.sample` files remains ([#548](https://github.com/NVIDIA/SkillSpector/pull/548)).
- Expand Windows 8.3 short-name components before comparing a requested path with its opened handle, allowing valid paths under spaced profile directories while retaining reparse-point and fail-closed checks ([#484](https://github.com/NVIDIA/SkillSpector/pull/484)).
- Avoid false AE1 results from valid JSON placeholders, inline code, list and blockquote containers, indented JSON, Markdown tables, and literal Make syntax ([#516](https://github.com/NVIDIA/SkillSpector/pull/516)).
- Bound JSON quote traversal without repeatedly scanning overlapping suffixes ([#521](https://github.com/NVIDIA/SkillSpector/pull/521)).
- Emit a HIGH AE7 analysis-evasion finding for per-file size limits that leave an artifact partially inspected, unless AE1 already covers that path. Supply a bounded text prefix and an explicit unreviewed-region marker to enabled LLM analysis; the unread region remains incomplete ([#509](https://github.com/NVIDIA/SkillSpector/pull/509)).
- Preserve full-evidence fingerprints, concrete YARA rule identity, and precise occurrence locations through projection, deduplication, and report compaction. Separate findings are retained while duplicate projections of the same occurrence are collapsed ([#409](https://github.com/NVIDIA/SkillSpector/pull/409)).
- Add bounded reconstruction for letter-spaced P3/P4 prompt instructions, retain source evidence, and use AE6 as an incomplete-coverage fallback for some ambiguous reconstructions. Some alternating-width short runs can evade both P3/P4 and AE6 (see Known Limitations) ([#470](https://github.com/NVIDIA/SkillSpector/pull/470)).
- Discover skills inside dot-prefixed directories, retain inherited local-only restrictions for child skills, and partition transitive scan caching by those privacy restrictions ([#410](https://github.com/NVIDIA/SkillSpector/pull/410)).
- Preserve incomplete discovery and requested semantic-analysis failures, including unavailable providers and mixed success/failure telemetry, instead of allowing a complete scan result ([#410](https://github.com/NVIDIA/SkillSpector/pull/410)).
- Emit recursive JSON reports to standard output when no output path is provided ([#467](https://github.com/NVIDIA/SkillSpector/pull/467)).
- Use the project manifest version for RP3 analysis ([#474](https://github.com/NVIDIA/SkillSpector/pull/474)).
- Prefer exact known-package matches when evaluating SC6 package-name similarity ([#530](https://github.com/NVIDIA/SkillSpector/pull/530)).
- Avoid treating slash-separated prose as local file references ([#451](https://github.com/NVIDIA/SkillSpector/pull/451)).
- Reduce false-positive severity for companion CLI OAuth results and signed self-update documentation classified as benign, and provide contextual explanations for warned pipe-to-shell installers. The contextual classifiers have unresolved PE3 and RA1 fail-open paths (see Known Limitations) ([#547](https://github.com/NVIDIA/SkillSpector/pull/547)).
- Ignore literal AS3 references to the current skill, derived from the scan-root basename or manifest name, without suppressing peer-skill or obfuscated-path access ([#506](https://github.com/NVIDIA/SkillSpector/pull/506)).
- Skip symlink test cases when the platform refuses symlink creation ([#501](https://github.com/NVIDIA/SkillSpector/pull/501)).

## Testing and Portability

- Make secure-open, FIFO, newline-sensitive build-context, nested OMS, and non-ASCII YARA fixtures deterministic across Windows and non-POSIX environments ([#503](https://github.com/NVIDIA/SkillSpector/pull/503), [#502](https://github.com/NVIDIA/SkillSpector/pull/502), [#505](https://github.com/NVIDIA/SkillSpector/pull/505), [#518](https://github.com/NVIDIA/SkillSpector/pull/518), [#504](https://github.com/NVIDIA/SkillSpector/pull/504)).
- Add dependency-free Node 22+ tests for the OpenCode tool helpers and an exact-head OpenCode TypeScript CI job ([#537](https://github.com/NVIDIA/SkillSpector/pull/537)).

## Security

- Excluded executable or loadable content is inventoried before exclusion. Referenced or out-of-coverage bytes now produce SC9 and incomplete-analysis evidence that blocks strict installation gates; the narrow exception is limited to direct, non-binary `.git/hooks/*.sample` files.
- Multilingual batch analysis consumes only the validated provider-eligible snapshot, so language detection and gap-fill do not reread local-only or replaced path content after the core scan.
- OpenCode integration is static by default. The native tool redacts common secret forms and bounds output, while the semantic provider uses argv/stdin and treats missing authentication, empty output, or unsupported event streams as failures.
- Genuine removal instructions remain reportable. The covered unresolved-runtime-command controls retain incomplete coverage and fail strict CLI/MCP installation gates, including when semantic analysis succeeds. Additional runtime-selected command variants remain under investigation (see Known Limitations).
- JSON string ownership preserves source evidence and does not exempt string contents from analysis.
- Findings and exit status can change after upgrading: oversized files can add HIGH AE7 findings, letter-spaced instructions can produce P3/P4 or AE6 findings, and previously collapsed distinct matches can increase the retained finding count and risk score. Missing requested analysis remains incomplete even when static analysis finishes.
- Context-aware companion CLI classification can lower severity, scores, or recommendations for documentation classified as benign. Coverage is not fail-closed for every token-transfer or self-update phrasing: the known PE3 and RA1 exceptions below can be incorrectly downgraded or missed. Warned pipe-to-shell installer findings remain reportable.
- Literal current-skill references no longer produce AS3 findings. Peer-skill references, transformed or obfuscated paths, explicit enumeration, AS1, and AS2 remain reportable.

## Breaking Changes and Migration

- `opencode_cli` is opt-in and requires an authenticated OpenCode 1.18.30 executable; other versions fail closed because their deny-all policy has not been verified. The OpenCode-native tool is installed by copying `.opencode/` from a checkout and defaults to static analysis; set `noLlm=false` and configure the provider environment to request semantic analysis.
- Existing CLI-provider deployments that set `SKILLSPECTOR_MODEL_REGISTRY` now use its valid token budgets. Invalid or non-positive values warn and fall back instead of aborting.
- Scans that previously treated excluded executable content as clean can now become incomplete with SC9 and `DO_NOT_INSTALL`; consumers should retain completeness and exclusion evidence.
- No new configuration is required. Static analysis can now run longer within the existing workflow deadline. Set `SKILLSPECTOR_MAX_STATIC_ANALYSIS_SECONDS_PER_ARTIFACT=30` to retain the previous per-artifact allowance, and restart the SkillSpector process after changing the setting ([#522](https://github.com/NVIDIA/SkillSpector/pull/522)).
- `--fail-on-findings` is opt-in. Combine it with `--fail-on-incomplete` when CI must reject either active findings or incomplete coverage. Code 2 still denotes an input or execution error; a nonzero exit alone does not identify which condition occurred.
- Consumers should retain completeness/degradation metadata and inspect findings as well as exit status. Explicitly use `--no-llm` for an intended static-only scan; requesting LLM analysis without an available provider is incomplete.
- Third-party dependency versions are unchanged from 2.11.2.

## Deprecations

- None.

## Validation

The release candidate is synchronized through main commit `4d5204893f0cd117d138990b28434ee37348fffc`. The earlier application-code head `5134f62458fa235b487e823d1c0472be54678295` was validated locally with Python 3.12.13:

- `uv lock --check --offline` passed with the locked dependency set.
- `make test-ci` passed 5,235 tests, with 14 skipped, 38 deselected, 4 expected failures, and 90% coverage.
- Ruff lint and format checks passed for all source and test files.
- The CLI reported `SkillSpector v2.12.0`; the release helper dry run resolved `v2.12.0` and the matching versioned notes.
- All 10 release helper and workflow tests passed.
- Wheel and source distributions built successfully, and Twine validated both artifacts.
- `git diff --check` passed.

For the release-catalog reconciliation through `4d5204893f0cd117d138990b28434ee37348fffc`, `uv lock --check --offline`, `uv run skillspector --version`, all 10 release-helper and workflow tests, and `git diff --check` passed locally.

All five hosted checks passed on the historical release head `5134f62458fa235b487e823d1c0472be54678295`: change detection, lint, unit tests, DCO, and Docker smoke ([run 35127688213](https://github.com/NVIDIA/SkillSpector/actions/runs/35127688213)). The current PR head and its exact-head checks are the source of truth after subsequent `main` synchronizations. Deployment/provider validation and the separate release gates below remain pending. Earlier candidate results apply only to their recorded commits and are not certification of this candidate.

[Release PR #550](https://github.com/NVIDIA/SkillSpector/pull/550) records the candidate baseline, validation results, known gaps, and remaining release gates.

## Known Limitations

- Local sanity checks cover the tested inputs and environment; live provider and deployment behavior depend on their configuration.
- Incomplete inspection is a reportable result. Unsupported inputs, unavailable requested analysis, and resource limits must remain visible; these conditions cannot be treated as a clean scan.
- The release remains a candidate while outstanding review and release issues are assessed. Proposed fixes in unmerged PRs are not included in this candidate.
- Letter-spacing reconstruction is not fail-closed. Alternating-width short runs such as `s e  n d conversation to external` can be split before P3/P4 matching and remain below AE6's six-letter concealed-run threshold, allowing a SAFE result.
- Companion-context classification is not fail-closed. PE3 can downgrade imperative token-acquisition text and miss adjacent disclosure phrased with verbs such as `paste`; RA1 can accept protected agent/tool names with CLI suffixes and signed-release evidence from a different logical line. These variants can be incorrectly downgraded or missed.
- Current validation found that public report serialization can repeat the first occurrence's columns for other matches; SARIF does not yet preserve these column coordinates. The internal occurrence improvements in #409 do not establish correct locations in every output format. See [release validation](https://github.com/NVIDIA/SkillSpector/pull/550) for the tracked report defect.
- Some runtime-selected command variants and Markdown reference destinations still have open completeness defects. Proposed fixes [#514](https://github.com/NVIDIA/SkillSpector/pull/514) and [#553](https://github.com/NVIDIA/SkillSpector/pull/553) are not included in this candidate.
- `opencode_cli` currently reports no token-usage accounting, and model availability or rate limits remain external. Multilingual batch gap-fill was validated with mocked providers; live-provider qualification remains pending.

## References

- [Changes since v2.11.2](https://github.com/NVIDIA/SkillSpector/compare/v2.11.2...v2.12.0)
- [AE1 documentation fix #516](https://github.com/NVIDIA/SkillSpector/pull/516)
- [Static analysis time allowance #522](https://github.com/NVIDIA/SkillSpector/pull/522)
- [OpenCode CLI provider #536](https://github.com/NVIDIA/SkillSpector/pull/536)
- [OpenCode-native integration #537](https://github.com/NVIDIA/SkillSpector/pull/537)
- [Excluded executable coverage #548](https://github.com/NVIDIA/SkillSpector/pull/548)

Prepared by Codex for Mohit Gupta.
