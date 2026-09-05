from __future__ import annotations

import logging
import types
import uuid
from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).resolve().parents[1]

def load_module(name: str, relative_path: str | Path):
    module_path = PROJECT_ROOT / Path(relative_path)
    source = module_path.read_text(encoding="utf-8")
    if "from __future__ import annotations" not in source:
        source = f"from __future__ import annotations\n{source}"

    module_name = f"tests_{name}_{uuid.uuid4().hex}"
    module = types.ModuleType(module_name)
    module.__file__ = str(module_path)
    module.__package__ = ""

    code = compile(source, str(module_path), "exec")
    exec(code, module.__dict__)
    return module

@pytest.fixture
def mediasorter_module():
    module = load_module("mediasorter", "scripts/mediasorter.py")
    logging.basicConfig(level=logging.INFO, force=True)
    return module

@pytest.fixture
def make_proofs_module():
    return load_module("make_proofs", "scripts/make_proofs.py")
