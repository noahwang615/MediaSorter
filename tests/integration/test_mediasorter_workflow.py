from __future__ import annotations

from pathlib import Path


def test_main_moves_media_and_leaves_unsupported_files(
    mediasorter_module,
    monkeypatch,
    tmp_path: Path,
    caplog,
):
    source_dir = tmp_path / "mediadump"
    image_target = tmp_path / "photos"
    video_target = tmp_path / "videos"
    source_dir.mkdir()

    (source_dir / "family.jpg").write_text("photo")
    (source_dir / "vacation.mp4").write_text("video")
    (source_dir / "notes.txt").write_text("unsupported")

    monkeypatch.setattr(mediasorter_module, "SOURCE_DIR", str(source_dir))
    monkeypatch.setattr(mediasorter_module, "IMAGE_TARGET_DIR", str(image_target))
    monkeypatch.setattr(mediasorter_module, "VIDEO_TARGET_DIR", str(video_target))
    monkeypatch.setattr(mediasorter_module, "check_dependencies", lambda: None)
    monkeypatch.setattr(
        mediasorter_module,
        "get_media_date",
        lambda file_path: "2024-03-01" if file_path.endswith(".jpg") else "2023-11-15",
    )

    caplog.set_level("INFO")
    mediasorter_module.main()

    assert (image_target / "2024" / "03" / "raw" / "family.jpg").exists()
    assert (video_target / "2023" / "11" / "vacation.mp4").exists()
    assert (source_dir / "notes.txt").exists()
    assert "Finished MediaSorter: moved=2 skipped=1 failed=0" in caplog.text
