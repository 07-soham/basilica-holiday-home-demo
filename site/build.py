"""Build the static demo: src/ + img/ + fonts/ -> dist/.

Usage: python build.py
Expands {{IMG:name|alt|sizes|eager|lazy}}, {{ROOMS}}, {{SPACES}}, {{LATTICE}}, {{SCHEMA}} and inline SVG icons.
"""
import html
import json
import re
import shutil
from pathlib import Path

ROOT = Path(__file__).parent
SRC, DIST = ROOT / "src", ROOT / "dist"
META = json.loads((ROOT / "img-meta.json").read_text())

PHONE_DISPLAY = "080807 86083"
PHONE_TEL = "+918080786083"
WA_NUMBER = "918080786083"

WA = ('<svg viewBox="0 0 24 24" aria-hidden="true" fill="currentColor"><path d="M12 2a10 10 0 0 0-8.6 15.1L2 22l5-1.3A10 10 0 1 0 12 2zm0 18.2a8.2 8.2 0 0 1-4.2-1.2l-.3-.2-3 .8.8-2.9-.2-.3A8.2 8.2 0 1 1 12 20.2zm4.5-6.1c-.2-.1-1.5-.7-1.7-.8-.2-.1-.4-.1-.6.1l-.8 1c-.1.2-.3.2-.5.1a6.7 6.7 0 0 1-3.3-2.9c-.3-.4.3-.4.7-1.4.1-.2 0-.3 0-.4l-.8-1.8c-.2-.5-.4-.4-.6-.4h-.5a1 1 0 0 0-.7.3 3 3 0 0 0-.9 2.2 5.2 5.2 0 0 0 1.1 2.7 11.8 11.8 0 0 0 4.5 4c1.7.7 2.3.8 3.2.6.5-.1 1.5-.6 1.7-1.2.2-.6.2-1.1.2-1.2-.1-.1-.2-.2-.5-.3z"/></svg>')
PHONE = ('<svg viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="2" stroke-linejoin="round"><path d="M5 3h4l2 5-2.5 1.5a11 11 0 0 0 6 6L16 13l5 2v4a2 2 0 0 1-2 2A16 16 0 0 1 3 5a2 2 0 0 1 2-2z"/></svg>')
PIN = ('<svg viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 22s7-6.2 7-12a7 7 0 0 0-14 0c0 5.8 7 12 7 12z"/><circle cx="12" cy="10" r="2.5"/></svg>')
STAR = '<svg viewBox="0 0 24 24" aria-hidden="true" fill="currentColor"><path d="M12 2.5l2.9 6.1 6.6.8-4.9 4.6 1.3 6.6L12 17.3l-5.9 3.3 1.3-6.6-4.9-4.6 6.6-.8z"/></svg>'


def lattice(cols=14, rows=2, cls="lattice"):
    """The facade's breeze-block panel: rows of punched circles in square cells."""
    cell = 16
    w, h = cols * cell, rows * cell
    circles = []
    i = 0
    for r in range(rows):
        for c in range(cols):
            circles.append(f'<circle cx="{c*cell+8}" cy="{r*cell+8}" r="5.2" style="--i:{c + r*2}"/>')
            i += 1
    return (f'<svg class="{cls}" viewBox="0 0 {w} {h}" preserveAspectRatio="xMinYMid slice" aria-hidden="true" focusable="false">'
            + "".join(circles) + "</svg>")


FAVICON = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32"><rect width="32" height="32" rx="6" fill="#183324"/>'
           + "".join(f'<circle cx="{x}" cy="{y}" r="4.2" fill="#F8FAFC"/>' for x in (9, 23) for y in (9, 23))
           + '<circle cx="16" cy="16" r="4.2" fill="#C2533F"/></svg>')

# (image, title, sleeps, detail, price or None, option value, alt, photo_note)
ROOMS = [
    ("room-deluxe", "Deluxe room, garden view", "Sleeps 3", "King bed and a sofa bed, about 20 m²", 2500, "deluxe",
     "A deluxe room with a white double bed, red cushions, towel swans, a wall-mounted TV and cream curtains", None),
    ("room-cottage", "Cottage room", "Sleeps 5", "Larger room for a family", None, "cottage",
     "A room with a double bed and purple runner, a dressing table and yellow curtains lit by the sun", "photo match to confirm"),
    ("room-balcony", "1-bedroom with terrace", "Sleeps 5", "Bedroom, hall and kitchen with a terrace", None, "1bhk",
     "A bright bedroom with a double bed and red cushions, its glass door open to a balcony with iron chairs", "photo match to confirm"),
    ("bungalow-double", "3-bedroom bungalow", "Sleeps 11", "One room downstairs, two upstairs", None, "3br",
     "A bungalow bedroom with a double bed, green bed runner and an orange feature wall", None),
    ("bungalow-twin", "4-bedroom bungalow", "Sleeps 15", "The whole house for a big group", None, "4br",
     "A bungalow bedroom with a padded leather headboard, two beds and green curtains", None),
]

# (name, where, seated, floating, note, image or None, alt)
SPACES = [
    ("The Lawn", "Outdoor, under the palms", 700, 1000, "Weddings, receptions and sangeet nights", "lawn-night",
     "The Lawn at night: rows of chairs in black covers face a lit stage, with a red carpet down the middle and palm trees above"),
    ("Basilica", "Indoor hall", 400, 600, "The largest hall, for receptions and conferences", "hall-basilica",
     "A large white banquet hall set with round tables in black and lilac cloths"),
    ("Tulip", "Indoor hall", 200, 300, "Engagements, birthdays and mid-size parties", None, ""),
    ("Orchid", "Indoor, terrace level", 70, 100, "Kitty parties, haldi and small family functions", None, ""),
]


def picture(name, alt, sizes, mode, cls=""):
    m = META[name]
    ws = m["sizes"]
    h = round(m["h"] * ws[-1] / m["w"])

    def ss(ext):
        return ", ".join(f"img/{name}-{w}.{ext} {w}w" for w in ws)
    attrs = 'fetchpriority="high" decoding="async"' if mode == "eager" else 'loading="lazy" decoding="async"'
    c = f' class="{cls}"' if cls else ""
    return (f'<picture><source type="image/avif" srcset="{ss("avif")}" sizes="{sizes}">'
            f'<source type="image/webp" srcset="{ss("webp")}" sizes="{sizes}">'
            f'<img{c} src="img/{name}-{ws[min(1, len(ws)-1)]}.webp" alt="{html.escape(alt)}" width="{ws[-1]}" height="{h}" {attrs}></picture>')


def rooms():
    out = []
    for img, title, sleeps, detail, price, val, alt, note in ROOMS:
        if price:
            p = (f'<p class="room-price"><span class="from">from</span> ₹{price:,}<span class="unit"> a night</span></p>'
                 f'<p class="ph-tag">Listed rate, owner to confirm</p>')
        else:
            p = ('<p class="room-price room-price--ask">Rate on request</p>'
                 '<p class="ph-tag">Owner to add direct rate</p>')
        n = f'<p class="ph-tag">{note}</p>' if note else ""
        out.append(
            f'<li class="room">{picture(img, alt, "(min-width: 1100px) 26vw, (min-width: 700px) 42vw, 78vw", "lazy")}'
            f'<div class="room-body"><h3>{title}</h3><p class="room-meta"><strong>{sleeps}</strong> · {detail}</p>{n}'
            f'<div class="room-foot">{p}'
            f'<a class="btn btn-ghost" href="#book" data-room="{val}">Check dates</a></div></div></li>')
    return "\n        ".join(out)


def spaces():
    out = []
    for name, where, seat, flo, note, img, alt in SPACES:
        fig = picture(img, alt, "(min-width: 900px) 30vw, 90vw", "lazy") if img else lattice(6, 4, "lattice lattice--card")
        out.append(
            f'<li class="space"><div class="space-media">{fig}</div><div class="space-body">'
            f'<h3>{name}</h3><p class="space-where">{where}</p>'
            f'<dl class="cap"><div><dt>Seated</dt><dd>{seat:,}</dd></div><div><dt>Standing</dt><dd>{flo:,}</dd></div></dl>'
            f'<p class="space-note">{note}</p></div></li>')
    return "\n        ".join(out)


def schema():
    return json.dumps({
        "@context": "https://schema.org",
        "@type": "Hotel",
        "name": "Basilica Holiday Home",
        "description": "3-star holiday home in Raiwood, Lonavala with about 50 air-conditioned rooms, family bungalows, an outdoor pool, a restaurant and four event spaces for weddings and parties.",
        "url": "https://07-soham.github.io/basilica-holiday-home-demo/",
        "image": "https://07-soham.github.io/basilica-holiday-home-demo/img/hero-dusk-1280.webp",
        "telephone": "+91-80807-86083",
        "foundingDate": "2014",
        "starRating": {"@type": "Rating", "ratingValue": "3"},
        "priceRange": "Rooms from ₹2,500 a night",
        "address": {"@type": "PostalAddress",
                    "streetAddress": "Plot No. 13 & 14, near Hanuman Temple, Thombrewadi, Raiwood",
                    "addressLocality": "Lonavala", "addressRegion": "Maharashtra", "postalCode": "410401",
                    "addressCountry": "IN"},
        "geo": {"@type": "GeoCoordinates", "latitude": 18.749394, "longitude": 73.392601},
        "checkinTime": "12:00", "checkoutTime": "10:00",
        "petsAllowed": False,
        "numberOfRooms": 50,
        "amenityFeature": [{"@type": "LocationFeatureSpecification", "name": n, "value": True} for n in
                           ["Outdoor pool", "Restaurant", "Room service", "Free parking", "Free Wi-Fi",
                            "24-hour front desk", "Laundry", "Garden", "Meeting rooms", "Banquet halls"]],
        "aggregateRating": {"@type": "AggregateRating", "ratingValue": 4.4, "reviewCount": 935, "bestRating": 5},
        "sameAs": ["https://www.instagram.com/basilica_holidayhomes/", "https://www.facebook.com/1829897583930218"],
    }, ensure_ascii=False)


def build():
    if DIST.exists():
        shutil.rmtree(DIST)
    DIST.mkdir()
    page = (SRC / "index.html").read_text(encoding="utf-8")
    page = (page.replace("{{ROOMS}}", rooms()).replace("{{SPACES}}", spaces()).replace("{{SCHEMA}}", schema())
            .replace("{{LATTICE}}", lattice(100, 2)).replace("{{LATTICE_SM}}", lattice(10, 1, "lattice lattice--rule"))
            .replace("{{WA}}", WA).replace("{{PHONE}}", PHONE).replace("{{PIN}}", PIN).replace("{{STAR}}", STAR)
            .replace("{{TEL}}", PHONE_TEL).replace("{{PHONE_DISPLAY}}", PHONE_DISPLAY).replace("{{WA_NUMBER}}", WA_NUMBER))
    page = re.sub(r"\{\{IMG:([^|]+)\|([^|]+)\|([^|]+)\|(eager|lazy)(?:\|([^}]*))?\}\}",
                  lambda m: picture(m[1], m[2], m[3], m[4], m[5] or ""), page)
    assert "{{" not in page, re.findall(r"\{\{[^}]*\}\}", page)
    (DIST / "index.html").write_text(page, encoding="utf-8")
    for f in ("styles.css", "app.js", "_headers", "robots.txt"):
        shutil.copy(SRC / f, DIST / f)
    (DIST / "favicon.svg").write_text(FAVICON, encoding="utf-8")
    shutil.copytree(ROOT / "img", DIST / "img")
    shutil.copytree(ROOT / "fonts", DIST / "fonts")
    print("built", DIST, len(page) // 1024, "KB html")


if __name__ == "__main__":
    build()
