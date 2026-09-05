from __future__ import annotations

import shutil
import subprocess
import uuid
from pathlib import Path

import pytest
from PIL import Image

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DOCKERFILE = PROJECT_ROOT / "docker_install" / "Dockerfile"
TEST_IMAGE = f"mediasorter-smoke:{uuid.uuid4().hex[:12]}"

pytestmark = pytest.mark.docker

def docker_available() -> bool:
    if shutil.which("docker") is None:
        return False

    result = subprocess.run(
        ["docker", "info"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        text=True,
        check=False,
    )
    return result.returncode == 0

@pytest.fixture(scope="session")
def docker_image() -> str:
    if not docker_available():
        pytest.skip("Docker CLI or daemon is unavailable")

    build_result = subprocess.run(
        ["docker", "build", "-t", TEST_IMAGE, "-f", str(DOCKERFILE), "."],
        cwd=PROJECT_ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    assert build_result.returncode == 0, build_result.stderr or build_result.stdout

    yield TEST_IMAGE

    subprocess.run(["docker", "image", "rm", "-f", TEST_IMAGE], check=False)

def run_container(command: list[str], *, env: dict[str, str], mounts: list[tuple[Path, str]], image: str) -> subprocess.CompletedProcess[str]:
    docker_command = ["docker", "run", "--rm"]

    for host_path, container_path in mounts:
        docker_command.extend(["-v", f"{host_path}:{container_path}"])

    for key, value in env.items():
        docker_command.extend(["-e", f"{key}={value}"])

    docker_command.extend(["--entrypoint", "python", image, *command])
    return subprocess.run(docker_command, capture_output=True, text=True, check=False)

def test_mediasorter_container_moves_files_once(docker_image: str, tmp_path: Path):
    source_dir = tmp_path / "mediadump"
    photo_dir = tmp_path / "photos"
    video_dir = tmp_path / "videos"
    logs_dir = tmp_path / "logs"
    source_dir.mkdir()
    photo_dir.mkdir()
    video_dir.mkdir()
    logs_dir.mkdir()

    (source_dir / "family.jpg").write_text("photo")
    (source_dir / "vacation.mp4").write_text("video")
    (source_dir / "notes.txt").write_text("unsupported")

    result = run_container(
        ["/app/scripts/mediasorter.py"],
        env={
            "MEDIA_SRC": "/data/mediadump",
            "PHOTO_DEST": "/data/photos",
            "VIDEO_DEST": "/data/videos",
        },
        mounts=[
            (source_dir, "/data/mediadump"),
            (photo_dir, "/data/photos"),
            (video_dir, "/data/videos"),
            (logs_dir, "/app/logs"),
        ],
        image=docker_image,
    )

    assert result.returncode == 0, result.stderr or result.stdout
    photo_matches = list(photo_dir.glob("*/*/raw/family.jpg"))
    video_matches = list(video_dir.glob("*/*/vacation.mp4"))
    assert len(photo_matches) == 1
    assert len(video_matches) == 1
    assert (source_dir / "notes.txt").exists()
    assert "Finished MediaSorter: moved=2 skipped=1 failed=0" in result.stdout
    assert (logs_dir / "mediasorter.log").exists()

def test_make_proofs_container_creates_proof(docker_image: str, tmp_path: Path):
    photo_dir = tmp_path / "photos"
    logs_dir = tmp_path / "logs"
    raw_dir = photo_dir / "2024" / "08" / "raw"
    proof_dir = photo_dir / "2024" / "08" / "proof"
    raw_dir.mkdir(parents=True)
    logs_dir.mkdir()

    source_image = raw_dir / "sample.jpg"
    Image.new("RGB", (20, 20), color="red").save(source_image, "JPEG")

    result = run_container(
        ["/app/scripts/make_proofs.py"],
        env={"PHOTO_DEST": "/data/photos"},
        mounts=[
            (photo_dir, "/data/photos"),
            (logs_dir, "/app/logs"),
        ],
        image=docker_image,
    )

    assert result.returncode == 0, result.stderr or result.stdout
    assert (proof_dir / "sample_proof.jpg").exists()
    assert "Created 1 proofs; skipped 0; failed 0." in result.stdout
