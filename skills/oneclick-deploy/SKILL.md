---
name: oneclick-deploy
description: "Low-budget one-click deploy of customizable business websites for trades and commerce. Use when deploying to IONOS or cheap stable hosts, with many designs, LLM integration, personas, and automation models for Handwerk/Gewerbe."
type: workflow
lifecycle: active
allowed-tools:
  - Read
  - Write
  - Bash
---

# Oneclick Deploy — Low-Budget Business Sites for Trades

Enable easy, cheap, stable deployment of professional websites for Fachbetriebe (trades and commerce). Focus on IONOS shared hosting or VPS for low cost. Include multiple designs, AI/LLM features, trade-specific personas, and a database of automation models. Self-improving via postmortem updates to references.

Use for requests like: deploy a site for my electrician business, create one-click deploy for a painter with AI chat, low-budget host for bakery with booking automation.

## Core Workflow

1. **Identify business**: Ask or extract trade/field (e.g. Elektriker, Maler, Bäcker, Friseur, IT-Dienstleister). See `references/trades.md` for common Handwerk categories. Map to persona (professional, friendly local, expert, modern).

2. **Select design**: Choose from 10+ styles (modern minimal, classic trustworthy, bold industrial, warm craft, colorful service). Generate or adapt HTML/CSS. Prefer static sites for cheapest hosting. Use assets templates if present.

3. **Load automation models**: Consult `references/automations.md` for 50+ model ideas across fields (at least 20 per major category). Select 3-8 relevant (e.g. quote calculator, appointment booking, AI FAQ, lead form, simple inventory). Generate the features in the site.

4. **Integrate LLM**: Embed simple AI features – FAQ chatbot (link to Grok or generic), content generation notes, self-learning prompts. For self-learning: document successful configs in references for future use.

5. **Generate site**: Prefer the helper in `scripts/generate_site.py`. It maps the trade via `assets/trades.json`, embeds widgets from `assets/automations.json` (subset of `references/automations.md`), and applies `assets/base.css` plus `assets/template.html` / `assets/site.js`. Output is offline HTML/CSS/JS only — no network calls. Customize further if needed, then package as zip for upload.

6. **Deploy one-click style**:
   - Prefer IONOS Webhosting: Provide FTP upload instructions or generate ready-to-upload folder. Shared hosting is cheap (~5-15€/mo), stable for static/simple sites.
   - Alternatives: Netlify/Vercel free tier for static, or cheap VPS (IONOS, Hetzner) with Docker if more complex.
   - Health check: Verify after deploy (user provides URL).
   - See `references/hosting.md` for cheapest stable options and exact steps.

7. **Self-learning**: After successful deploy, update references with the new model/design combination. Suggest running postmortem for improvement.

Always confirm key choices (trade, design preference, must-have automations) if not clear. Aim for fully autonomous completion once basics are known. Output the files + clear deploy steps.

## Key Principles

- Low budget first: Static > dynamic. Shared hosting > VPS unless needed.
- Easy for everyone: Clear numbered steps, no complex CLI unless scripted.
- Stable/cheap servers: Prioritize IONOS, Hetzner, or free static hosts.
- Many designs/personas: Adapt to trade (e.g. robust for construction, elegant for services).
- Automation database: Expand on demand; core list in references.

## Resources

- `references/trades.md`: List of Handwerk/Gewerbe fields and personas.
- `references/automations.md`: Database of 50+ automation models, categorized.
- `references/hosting.md`: IONOS and low-cost deploy guides.
- `scripts/generate_site.py`: Trade-aware static scaffold (`--trade`, `--output`).
- `assets/`: `base.css`, `template.html`, `site.js`, `trades.json`, `automations.json`.

## Common Issues

| Problem | Fix |
|---------|-----|
| No trade specified | Ask for Fachgebiet or business type |
| Complex backend needed | Recommend VPS + Docker over shared |
| Auth/credentials | Guide user to set up IONOS FTP/SSH; never store secrets |
| Site too heavy | Stick to static HTML/CSS/JS |
| LLM costs | Use free tiers or simple rule-based first; note Grok integration options |
