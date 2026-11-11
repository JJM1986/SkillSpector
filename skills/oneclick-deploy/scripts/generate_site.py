#!/usr/bin/env python3
"""
Simple scaffold for a static business site.
Usage: python3 generate_site.py --trade "Elektriker" --output ./site
Generates index.html with placeholders for persona and automations.
"""
import argparse
import os
from pathlib import Path

def generate(trade: str, output: str):
    Path(output).mkdir(parents=True, exist_ok=True)
    html = f"""<!DOCTYPE html>
<html lang="de">
<head>
  <meta charset="UTF-8">
  <title>{trade} - Fachbetrieb</title>
  <style>
    body {{ font-family: system-ui, sans-serif; max-width: 800px; margin: auto; padding: 20px; }}
    header {{ background: #1a365d; color: white; padding: 20px; }}
    .cta {{ background: #2b6cb0; color: white; padding: 10px 20px; text-decoration: none; }}
  </style>
</head>
<body>
  <header>
    <h1>{trade}</h1>
    <p>Professioneller Service in Ihrer Nähe</p>
  </header>
  <section>
    <h2>Unsere Leistungen</h2>
    <ul>
      <li>Installation & Reparatur</li>
      <li>Beratung & Angebot</li>
    </ul>
    <a href="#kontakt" class="cta">Jetzt Angebot anfordern</a>
  </section>
  <section id="kontakt">
    <h2>Kontakt</h2>
    <form>
      <input type="text" placeholder="Name" required><br>
      <input type="email" placeholder="E-Mail" required><br>
      <textarea placeholder="Nachricht"></textarea><br>
      <button type="submit">Senden</button>
    </form>
  </section>
  <footer>© {trade} – Low-Budget Deploy</footer>
</body>
</html>"""
    (Path(output) / "index.html").write_text(html, encoding="utf-8")
    print(f"Generated basic site for {trade} in {output}/index.html")
    print("Customize further, then zip for IONOS FTP upload.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--trade", default="Fachbetrieb", help="Trade or business name")
    parser.add_argument("--output", default="./site", help="Output directory")
    args = parser.parse_args()
    generate(args.trade, args.output)
