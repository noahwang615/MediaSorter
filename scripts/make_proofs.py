from pathlib import Path
import os

from dotenv import load_dotenv
from PIL import Image, ImageOps
from pillow_heif import register_heif_opener

SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent
load_dotenv(PROJECT_ROOT / ".env")

PHOTO_DEST = Path(os.getenv("PHOTO_DEST") or PROJECT_ROOT / "data" / "photos").expanduser()
if not PHOTO_DEST.is_absolute():
    PHOTO_DEST = PROJECT_ROOT / PHOTO_DEST
register_heif_opener()

PROOF_SIZE = (2000, 2000)
PROOF_QUALITY = 50
PHOTO_EXTENSIONS = {
    ".jpg", ".jpeg", ".tif", ".tiff", ".nef", ".png", ".gif", ".bmp",
    ".webp", ".heic", ".heif",
}


def create_proof(raw_path: Path, proof_path: Path) -> bool:
    if proof_path.exists():
        return False

    try:
        with Image.open(raw_path) as image:
            image = ImageOps.exif_transpose(image)
            image.thumbnail(PROOF_SIZE)
            image.convert("RGB").save(proof_path, "JPEG", quality=PROOF_QUALITY)
        return True
    except OSError as error:
        print(f"ERROR: can't create proof for {raw_path}: {error}")
        return False


def iter_photo_directories() -> list[tuple[Path, Path]]:
    """Return source/proof pairs for current raw and legacy month layouts."""
    directories = []
    if not PHOTO_DEST.is_dir():
        return directories

    for year_dir in PHOTO_DEST.iterdir():
        if not year_dir.is_dir() or year_dir.name in {"raw", "proof"}:
            continue
        for month_dir in year_dir.iterdir():
            if not month_dir.is_dir() or month_dir.name in {"raw", "proof"}:
                continue
            proof_dir = month_dir / "proof"
            raw_dir = month_dir / "raw"
            if raw_dir.is_dir():
                directories.append((raw_dir, proof_dir))
            directories.append((month_dir, proof_dir))
    return directories


def main() -> None:
    created = 0
    skipped = 0
    failed = 0

    for source_dir, proof_dir in iter_photo_directories():
        proof_dir.mkdir(parents=True, exist_ok=True)
        source_files = sorted(source_dir.iterdir())
        for photo_path in source_files:
            if not photo_path.is_file() or photo_path.suffix.lower() not in PHOTO_EXTENSIONS:
                continue
            proof_path = proof_dir / f"{photo_path.stem}_proof.jpg"
            if proof_path.exists():
                skipped += 1
                continue
            if photo_path.suffix.lower() == ".nef":
                source_names = {path.name.lower() for path in source_files}
                jpeg_variants = {
                    photo_path.with_suffix(".jpg").name.lower(),
                    photo_path.with_suffix(".jpeg").name.lower(),
                }
                if jpeg_variants.intersection(source_names):
                    skipped += 1
                    continue
            if create_proof(photo_path, proof_path):
                created += 1
            else:
                failed += 1

    print(f"Created {created} proofs; skipped {skipped}; failed {failed}.")


if __name__ == "__main__":
    main()
