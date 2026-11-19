# Basilica Holiday Home: concept demo

A pitch demo website for **Basilica Holiday Home**, Raiwood, Lonavala. It is a concept demo prepared by Soham and is not the official website.

## Layout
- `BRIEF.md`: the researched facts with source links, and the placeholders.
- `NOTES.md`: photo picks, niche research, the two Stitch directions and the reasons for the pick, check results, and **the list of placeholders the owner must fill**.
- `images/raw/`: the property's own listing photos. `images/SOURCES.md` records where each one came from.
- `design/`: the Stitch design tokens ("Monsoon Ghats") and the Direction B thumbnail Stitch saved.
- `site/src/`: the page template, CSS, JS, `_headers` and `robots.txt`.
- `site/img/`, `site/fonts/`: AVIF/WebP image sizes (made by `site/make_images.py`) and the self-hosted fonts (Newsreader, Public Sans).
- `site/dist/`: the built site, ready to deploy.
- `screenshots/`: screenshots at 390 px and 1440 px.

## Build
Requires Python 3 with Pillow.
```
cd site
python make_images.py   # only when photos change
python build.py         # writes site/dist/
```

## Deploy: Cloudflare Pages
Either connect this repo (Workers & Pages → Create → Pages → Connect to Git, framework preset None, no build command, output directory `site/dist`) or upload directly:
```
npx wrangler login
npx wrangler pages deploy site/dist --project-name basilica-holiday-home-demo
```
`_headers` applies the CSP, nosniff, Referrer-Policy, Permissions-Policy, X-Frame-Options DENY and X-Robots-Tag noindex.

At launch: remove the noindex meta, the `X-Robots-Tag` line and the `robots.txt` Disallow, point the canonical, og:image and schema URLs at the real domain, and wire the two forms to a booking engine or WhatsApp.
