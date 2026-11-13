#!/usr/bin/env python3
"""Scaffold a static trade site from assets/ (offline, no network).

Usage (from skills/oneclick-deploy):
  python3 scripts/generate_site.py --trade Elektriker --output ./site
  python3 scripts/generate_site.py --trade Friseur --output ./site --zip
"""
from __future__ import annotations

import argparse
import json
import re
import shutil
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ASSETS = ROOT / "assets"
THEMES = ASSETS / "themes"

PERSONA_THEME = {
    "Professional & Trustworthy": "professional",
    "Friendly Local Hero": "friendly",
    "Modern Expert": "modern",
    "Classic Craft": "classic",
    "Energetic Service": "energetic",
}


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


def theme_for(persona: str) -> str:
    return PERSONA_THEME.get(persona, "professional")


def write_styles(out: Path, theme_id: str) -> None:
    base = (ASSETS / "base.css").read_text(encoding="utf-8")
    theme_path = THEMES / f"{theme_id}.css"
    theme = theme_path.read_text(encoding="utf-8") if theme_path.is_file() else ""
    (out / "styles.css").write_text(
        base + "\n\n/* theme: " + theme_id + " */\n" + theme,
        encoding="utf-8",
    )


def package_zip(out: Path) -> Path:
    """Write <dirname>.zip next to the site folder; tolerate `.` / empty names."""
    out = out.resolve()
    folder_name = out.name if out.name not in {"", ".", ".."} else "site"
    zip_path = out.parent / f"{folder_name}.zip"
    files = ["index.html", "styles.css", "site.js", "manifest.json"]
    with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        for name in files:
            path = out / name
            if path.is_file():
                zf.write(path, arcname=name)
    return zip_path


def generate(trade: str, output: str, *, make_zip: bool = False) -> tuple[Path, Path | None]:
    out = Path(output).resolve()
    out.mkdir(parents=True, exist_ok=True)

    catalog = load_json("trades.json")
    autos = load_json("automations.json")
    profile = resolve_profile(trade, catalog)
    chosen = [a for a in profile["automations"] if a in autos]
    theme_id = theme_for(profile["persona"])

    services = "\n".join(f"        <li>{s}</li>" for s in profile["services"])
    auto_list = "\n".join(
        f'        <li>{autos[a]["title"]} <small>({autos[a]["ref"]})</small></li>'
        for a in chosen
    )
    widgets = "\n".join(autos[a]["html"] for a in chosen)

    site = {
        "trade": profile["label"],
        "persona": profile["persona"],
        "theme": theme_id,
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
    write_styles(out, theme_id)
    shutil.copyfile(ASSETS / "site.js", out / "site.js")
    (out / "manifest.json").write_text(
        json.dumps(
            {
                "trade": profile["label"],
                "persona": profile["persona"],
                "theme": theme_id,
                "automations": chosen,
                "files": ["index.html", "styles.css", "site.js"],
            },
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    zip_path = package_zip(out) if make_zip else None
    return out, zip_path


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate static trade site")
    parser.add_argument("--trade", default="Fachbetrieb")
    parser.add_argument("--output", default="./site")
    parser.add_argument(
        "--zip",
        action="store_true",
        help="Also write <output>.zip for IONOS/File-Manager upload",
    )
    args = parser.parse_args()
    out, zip_path = generate(args.trade, args.output, make_zip=args.zip)
    print(f"Generated site for {args.trade} in {out}")
    print("Files: index.html, styles.css, site.js, manifest.json")
    if zip_path is not None:
        print(f"Upload package: {zip_path}")


if __name__ == "__main__":
    main()
