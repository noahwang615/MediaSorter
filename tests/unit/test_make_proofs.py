from __future__ import annotations
from pathlib import Path

import pytest
pytestmark = pytest.mark.makeproofs

def test_iter_photo_directories_supports_raw_and_legacy_layout(make_proofs_module, monkeypatch, tmp_path: Path):
    photo_dest = tmp_path / "photos"
    raw_month = photo_dest / "2024" / "08"
    legacy_month = photo_dest / "2024" / "09"
    (raw_month / "raw").mkdir(parents=True)
    legacy_month.mkdir(parents=True)

    monkeypatch.setattr(make_proofs_module, "PHOTO_DEST", photo_dest)

    directories = make_proofs_module.iter_photo_directories()

    assert (raw_month / "raw", raw_month / "proof") in directories
    assert (raw_month, raw_month / "proof") in directories
    assert (legacy_month, legacy_month / "proof") in directories


def test_create_proof_returns_false_when_proof_already_exists(make_proofs_module, tmp_path: Path):
    raw_path = tmp_path / "raw.jpg"
    proof_path = tmp_path / "proof.jpg"
    proof_path.write_text("existing")

    result = make_proofs_module.create_proof(raw_path, proof_path)

    assert result is False


def test_main_skips_nef_when_matching_jpeg_exists(make_proofs_module, monkeypatch, tmp_path: Path, capsys):
    source_dir = tmp_path / "2024" / "08" / "raw"
    proof_dir = tmp_path / "2024" / "08" / "proof"
    source_dir.mkdir(parents=True)
    (source_dir / "IMG_0001.jpg").write_text("jpeg")
    (source_dir / "IMG_0001.nef").write_text("raw")

    create_calls: list[Path] = []

    monkeypatch.setattr(make_proofs_module, "iter_photo_directories", lambda: [(source_dir, proof_dir)])

    def fake_create_proof(raw_path: Path, proof_path: Path) -> bool:
        create_calls.append(raw_path)
        proof_path.write_text("proof")
        return True

    monkeypatch.setattr(make_proofs_module, "create_proof", fake_create_proof)

    make_proofs_module.main()
    captured = capsys.readouterr()

    assert create_calls == [source_dir / "IMG_0001.jpg"]
    assert "Created 1 proofs; skipped 1; failed 0." in captured.out
