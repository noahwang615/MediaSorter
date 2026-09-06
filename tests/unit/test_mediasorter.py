from __future__ import annotations

from pathlib import Path

import pytest
pytestmark = pytest.mark.mediasort

def test_parse_exif_date_prefers_original_timestamp(mediasorter_module):
    exif_tag_lookup = {value: key for key, value in mediasorter_module.TAGS.items()}
    exif_data = {
        exif_tag_lookup["DateTime"]: "2023:01:02 03:04:05",
        exif_tag_lookup["DateTimeOriginal"]: "2024:05:06 07:08:09",
    }

    assert mediasorter_module.parse_exif_date(exif_data) == "2024-05-06"


def test_get_unique_filename_appends_counter(mediasorter_module, tmp_path: Path):
    target_dir = tmp_path / "photos"
    target_dir.mkdir()
    (target_dir / "trip.jpg").write_text("original")
    (target_dir / "trip_2.jpg").write_text("duplicate")

    unique_name = mediasorter_module.get_unique_filename(str(target_dir), "trip.jpg")

    assert unique_name == "trip_3.jpg"


def test_process_file_moves_photo_into_year_month_raw(mediasorter_module, monkeypatch, tmp_path: Path):
    source_file = tmp_path / "camera.jpg"
    source_file.write_text("image-data")
    image_target = tmp_path / "photos"

    monkeypatch.setattr(mediasorter_module, "IMAGE_TARGET_DIR", str(image_target))
    monkeypatch.setattr(mediasorter_module, "is_photo", lambda _: True)
    monkeypatch.setattr(mediasorter_module, "is_video", lambda _: False)
    monkeypatch.setattr(mediasorter_module, "get_media_date", lambda _: "2024-07-09")

    result = mediasorter_module.process_file(str(source_file))

    expected_destination = image_target / "2024" / "07" / "raw" / "camera.jpg"
    assert result == "moved"
    assert expected_destination.exists()
    assert not source_file.exists()


def test_process_file_skips_invalid_date(mediasorter_module, monkeypatch, tmp_path: Path):
    source_file = tmp_path / "camera.jpg"
    source_file.write_text("image-data")

    monkeypatch.setattr(mediasorter_module, "is_photo", lambda _: True)
    monkeypatch.setattr(mediasorter_module, "is_video", lambda _: False)
    monkeypatch.setattr(mediasorter_module, "get_media_date", lambda _: "unknown")

    result = mediasorter_module.process_file(str(source_file))

    assert result == "skipped"
    assert source_file.exists()


def test_main_exits_when_source_directory_is_missing(mediasorter_module, monkeypatch, tmp_path: Path):
    missing_source = tmp_path / "missing"

    monkeypatch.setattr(mediasorter_module, "SOURCE_DIR", str(missing_source))
    monkeypatch.setattr(mediasorter_module, "check_dependencies", lambda: None)

    with pytest.raises(SystemExit) as error:
        mediasorter_module.main()

    assert error.value.code == 1
