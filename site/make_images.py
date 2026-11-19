"""Pick the property photos and write AVIF + WebP sizes to site/img, plus img-meta.json.
Usage: python make_images.py"""
import json
from pathlib import Path
from PIL import Image, ImageOps

ROOT = Path(__file__).parent
RAW = ROOT.parent / "images" / "raw"
OUT = ROOT / "img"
# name: (source file, sizes, optional crop box as fractions l,t,r,b)
PICKS = {
    "hero-dusk": ("agoda-92fc44ac3c.jpg", [480, 800, 1280, 1600], None),
    "valley-balcony": ("exp-516fc429.jpg", [480, 800, 1280], None),
    "mist-balcony": ("ta-18-3a.jpg", [480, 800], None),
    "pool": ("wmg-1731252196_Pool.jpeg", [480, 800, 1280], (0.22, 0, 1, 1)),
    "lawn-night": ("wmg-1731252044_0F1A8625.JPG", [480, 800, 1280], (0.2, 0, 1, 1)),
    "stage-ring": ("wmg-1731252094_0F1A8626.JPG", [480, 800, 1280], (0.24, 0, 1, 1)),
    "lawn-day": ("wmg-2022-12-11-44pm.jpg", [480, 800, 1280], None),
    "hall-basilica": ("wmg-2022-12-11-38pm.jpg", [480, 800], (0.26, 0, 1, 1)),
    "hall-stage": ("wmg-2022-12-11-52pm__1_.jpg", [480, 800, 1280], None),
    "terrace-mandap": ("wmg-2022-12-11-45pm.jpg", [480, 800, 1280], None),
    "entrance-arch": ("wmg-1731252025_0F1A8384.JPG", [480, 800, 1280], None),
    "room-deluxe": ("agoda-59742ddab3.jpg", [480, 800, 1280], None),
    "room-balcony": ("ta-18-34.jpg", [480, 800], None),
    "room-cottage": ("agoda-9d163f5638.jpg", [480, 800, 1280], None),
    "bungalow-twin": ("agoda-bung-f73032ce6b.jpg", [480, 800, 1280], None),
    "bungalow-double": ("agoda-bung-1cff5d9f88.jpg", [480, 800, 1280], None),
    "restaurant": ("exp-83b4c743.jpg", [480, 800, 1280], None),
    "lobby": ("exp-51a83220.jpg", [480, 800, 1280], None),
    "courtyard": ("exp-a7656ae3.jpg", [480, 800, 1280], None),
    "garden-play": ("ta-17-86.jpg", [480, 800], None),
}

def main():
    import sys
    only = set(sys.argv[1:])
    OUT.mkdir(exist_ok=True)
    meta = json.loads((ROOT / "img-meta.json").read_text()) if only else {}
    for name, (src, sizes, crop) in PICKS.items():
        if only and name not in only:
            continue
        for old in OUT.glob(f"{name}-*"):
            old.unlink()
        im = ImageOps.exif_transpose(Image.open(RAW / src)).convert("RGB")
        if crop:
            w, h = im.size
            im = im.crop((int(crop[0]*w), int(crop[1]*h), int(crop[2]*w), int(crop[3]*h)))
        sizes = [s for s in sizes if s <= im.width] or [im.width]
        for s in sizes:
            r = im.resize((s, round(im.height * s / im.width)), Image.LANCZOS)
            r.save(OUT / f"{name}-{s}.webp", quality=72, method=6)
            r.save(OUT / f"{name}-{s}.avif", quality=52, speed=6)
        meta[name] = {"w": im.width, "h": im.height, "sizes": sizes, "src": src}
    (ROOT / "img-meta.json").write_text(json.dumps(meta, indent=1))
    print(len(meta), "images")

if __name__ == "__main__":
    main()
