"""Add photos to the gallery.

Put original photos in photos-raw/ (not committed), then run:

    python3 tools/add_photos.py

For each photo not yet in _data/photos.yml, this writes a full-size copy to
assets/photos/ and a thumbnail to assets/photos/thumb/, both with metadata
(including GPS location) removed, and appends an entry to _data/photos.yml.
Fill in `place` for the new entries afterwards.
"""

import re
import sys
from pathlib import Path

from PIL import Image, ImageOps

ROOT = Path(__file__).resolve().parent.parent
RAW = ROOT / "photos-raw"
FULL = ROOT / "assets" / "photos"
THUMB = FULL / "thumb"
DATA = ROOT / "_data" / "photos.yml"

FULL_LONG_EDGE = 2400
THUMB_HEIGHT = 600
EXTENSIONS = {".jpg", ".jpeg", ".png", ".tif", ".tiff"}
DATETIME_ORIGINAL = 0x9003


def slug(path):
    return re.sub(r"[^a-z0-9]+", "-", path.stem.lower()).strip("-") + ".jpg"


def date_taken(img):
    # "2025:12:03 14:21:07" -> "2025.12"
    value = img.getexif().get_ifd(0x8769).get(DATETIME_ORIGINAL, "")
    return value[:7].replace(":", ".") if value else ""


def main():
    if not RAW.is_dir():
        sys.exit(f"Put photos in {RAW.relative_to(ROOT)}/ first.")

    THUMB.mkdir(parents=True, exist_ok=True)
    existing = set(re.findall(r"^- file: (\S+)", DATA.read_text(), re.M))
    entries = []

    for src in sorted(RAW.iterdir()):
        if src.suffix.lower() not in EXTENSIONS or slug(src) in existing:
            continue
        name = slug(src)
        with Image.open(src) as img:
            date = date_taken(img)
            img = ImageOps.exif_transpose(img).convert("RGB")

            full = img.copy()
            full.thumbnail((FULL_LONG_EDGE, FULL_LONG_EDGE), Image.LANCZOS)
            full.save(FULL / name, quality=85, optimize=True, progressive=True)

            thumb = img.copy()
            thumb.thumbnail((THUMB_HEIGHT * 4, THUMB_HEIGHT), Image.LANCZOS)
            thumb.save(THUMB / name, quality=80, optimize=True, progressive=True)

        entries.append(
            f"\n- file: {name}\n"
            f"  width: {full.width}\n"
            f"  height: {full.height}\n"
            "  place: \n"
            f'  date: "{date}"\n'
        )
        print(f"added {name} ({full.width}x{full.height})")

    if not entries:
        print("No new photos.")
        return
    with DATA.open("a") as f:
        f.writelines(entries)
    print(f"Now fill in `place` for the new entries in {DATA.relative_to(ROOT)}.")


if __name__ == "__main__":
    main()
