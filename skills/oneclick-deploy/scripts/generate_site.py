#!/usr/bin/env python3
"""Scaffold a static trade site from assets/ (offline, no network).

Usage (from skills/oneclick-deploy):
  python3 scripts/generate_site.py --trade Elektriker --output ./site
"""
from __future__ import annotations

import argparse
import json
import re
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ASSETS = ROOT / "assets"


def norm(trade: str) -> str:
    t = trade.strip().lower()
    t = t.replace("ü", "ue").replace("ä", "ae").replace("ö", "oe").replace("ß", "ss")
    t = re.sub(r"[^a-z0-9\-]+", " ", t).strip()
    return t.split()[0] if t else "default"


def load_json(name: str) -> dict:
    return json.loads((ASSETS / name).read_text(encoding="utf-8"))


def resolve_profile(trade: str, catalog: dict) -> dict:
    key = norm(trade)
    aliases = catalog.get("aliases", {})
    mapped = aliases.get(key, aliases.get(trade.strip().lower(), key))
    trades = catalog.get("trades", {})
    if mapped in trades:
        profile = dict(trades[mapped])
    else:
        profile = dict(catalog["default"])
        if trade.strip():
            profile["label"] = trade.strip()
    return profile


def build_faq(label: str, chosen: list[str]) -> dict:
    """FAQ copy only references widgets actually embedded on the page."""
    has = set(chosen)
    has_lead = "lead_form" in has
    contact = "das Kontaktformular" if has_lead else "uns"
    faq = {
        "default": (
            f"Danke für Ihre Frage zu {label}. Schreiben Sie uns über {contact}."
            if has_lead
            else f"Danke für Ihre Frage zu {label}."
        ),
    }
    if "emergency_call" in has:
        faq["notdienst"] = (
            "Für Notfälle nutzen Sie den Notdienst-Button oder rufen Sie uns an."
        )
    if "quote_calculator" in has:
        faq["preis"] = (
            "Eine grobe Kostenschätzung finden Sie im Rechner; "
            "verbindliche Angebote nach Besichtigung."
        )
    elif has_lead:
        faq["preis"] = (
            f"Preise für {label} nennen wir gerne nach kurzer Abstimmung "
            "über das Kontaktformular."
        )
    if "booking" in has:
        faq["termin"] = (
            "Nutzen Sie die Terminbuchung oder das Kontaktformular."
            if has_lead
            else "Nutzen Sie die Terminbuchung."
        )
    elif has_lead:
        faq["termin"] = "Termine stimmen wir über das Kontaktformular ab."
    return faq


def generate(trade: str, output: str) -> Path:
    out = Path(output)
    out.mkdir(parents=True, exist_ok=True)

    catalog = load_json("trades.json")
    autos = load_json("automations.json")
    profile = resolve_profile(trade, catalog)
    chosen = [a for a in profile["automations"] if a in autos]

    services = "\n".join(f"        <li>{s}</li>" for s in profile["services"])
    auto_list = "\n".join(
        f'        <li>{autos[a]["title"]} <small>({autos[a]["ref"]})</small></li>'
        for a in chosen
    )
    widgets = "\n".join(autos[a]["html"] for a in chosen)

    site = {
        "trade": profile["label"],
        "persona": profile["persona"],
        "automations": chosen,
        "rates": {"hourly": 65, "per_km": 0.8},
        "faq": build_faq(profile["label"], chosen),
    }

    html = (ASSETS / "template.html").read_text(encoding="utf-8")
    html = (
        html.replace("{{LABEL}}", profile["label"])
        .replace("{{TAGLINE}}", profile["tagline"])
        .replace("{{PERSONA}}", profile["persona"])
        .replace("{{SERVICES}}", services)
        .replace("{{AUTO_LIST}}", auto_list)
        .replace("{{WIDGETS}}", widgets)
        .replace("{{SITE_JSON}}", json.dumps(site, ensure_ascii=False))
    )
    (out / "index.html").write_text(html, encoding="utf-8")
    shutil.copyfile(ASSETS / "base.css", out / "styles.css")
    shutil.copyfile(ASSETS / "site.js", out / "site.js")
    (out / "manifest.json").write_text(
        json.dumps(
            {
                "trade": profile["label"],
                "persona": profile["persona"],
                "automations": chosen,
                "files": ["index.html", "styles.css", "site.js"],
            },
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    return out


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate static trade site")
    parser.add_argument("--trade", default="Fachbetrieb")
    parser.add_argument("--output", default="./site")
    args = parser.parse_args()
    out = generate(args.trade, args.output)
    print(f"Generated site for {args.trade} in {out}")
    print("Files: index.html, styles.css, site.js, manifest.json")


if __name__ == "__main__":
    main()
