"""Pytest fixtures for nwm-region-mgr tests."""

import shutil
from pathlib import Path

import pytest
import yaml


@pytest.fixture
def patched_config_dir(tmp_path, monkeypatch):
    """Create a config directory in tmp_path and patch environment variables."""
    repo_root = Path(__file__).resolve().parents[1]

    # copy configs
    cfg_src = repo_root / "configs"
    cfg_dir = tmp_path / "configs"
    shutil.copytree(cfg_src, cfg_dir, dirs_exist_ok=True)

    # set env vars
    monkeypatch.setenv("WORK_DIR", str(tmp_path))
    monkeypatch.setenv("REPOS_COMMON_ROOT__HOST", str(repo_root.parent))

    # set n_procs to 2 in general config
    general_cfg_file = cfg_dir / "config_general.yaml"
    general_cfg = yaml.safe_load(general_cfg_file.read_text())
    general_cfg["general"]["n_procs"] = 2
    general_cfg_file.write_text(yaml.safe_dump(general_cfg))

    return cfg_dir
