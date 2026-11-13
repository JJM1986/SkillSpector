# Low-Budget Stable Hosting Guide

Prioritize cheapest, reliable options for German users. Focus on IONOS.

## Recommended: IONOS Webhosting
- Cheap shared hosting: often 1-10€/mo first year, stable for static/simple sites.
- Supports HTML/CSS/JS, PHP, FTP/SFTP upload.
- Domain often included or cheap.
- Steps for one-click style:
  1. Generate static site files locally (`python3 scripts/generate_site.py --trade … --output ./site --zip`).
  2. Use the produced `site/site.zip` (index.html, styles.css, site.js, manifest.json) or zip the folder yourself.
  3. User logs into IONOS customer area → Webhosting → FTP or File Manager.
  4. Upload and extract to public_html or root.
  5. Test URL.
- For forms: Use simple PHP mail() or external service (Formspree free tier) to avoid backend complexity.
- SSL: Free Let's Encrypt usually available.

## Alternatives
- **Hetzner VPS**: Very cheap (~4€/mo), excellent stability. Use for Docker if needed. Guide: install Docker, docker-compose up.
- **Netlify / Vercel**: Free for static. Drag-and-drop deploy or CLI. Great for pure HTML/JS. One-click via their dashboard.
- **GitHub Pages**: Free static. Push to repo.
- **Cloudflare Pages**: Free, fast, good for static.

## Deploy Process Summary
- Static preferred: no server maintenance.
- Provide user with: zip file + numbered upload steps + "verify by visiting URL".
- For advanced: script in scripts/ to prepare package.
- Self-learning: Note which host worked best for which trade type.

Always warn: User must handle their own account credentials. Do not store passwords.
