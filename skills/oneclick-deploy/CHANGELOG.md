# Changelog
## 2026-11-13
- Map personas to theme CSS under `assets/themes/` (professional, friendly, modern, classic, energetic) and compose them into generated `styles.css`.
- Add `--zip` to `scripts/generate_site.py` for a ready-to-upload static archive (IONOS File Manager / FTP).
- Derive CTA hover colors from theme accent variables; harden zip naming for `.` / empty output paths.

## 2026-11-12
- Wire `scripts/generate_site.py` to trade personas and automation widgets via `assets/trades.json` + `assets/automations.json` (aligned with `references/trades.md` / `references/automations.md`).
- Add usable design assets: `assets/base.css`, `assets/template.html`, `assets/site.js`; generator emits offline `index.html` + copied CSS/JS + `manifest.json` (no network calls).
- Document the generator workflow in `SKILL.md`; keep `allowed-tools: Read, Write, Bash`.
- FAQ hints only reference embedded widgets; emergency FAQ matching gated on `notdienst` hint.

## 2026-11-11
- Declare Agent Skills `allowed-tools` (`Read`, `Write`, `Bash`) so file-write scaffolding in `scripts/generate_site.py` is covered and SkillSpector LP3 no longer fires.

## 2026-11-10
- Initial skill creation for low-budget one-click deploy of business sites for trades and commerce, focused on IONOS and similar cheap stable hosts, with LLM integration, designs, and automation models.
