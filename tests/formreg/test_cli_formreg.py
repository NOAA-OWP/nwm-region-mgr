"""Tests for nwm-region-mgr formreg CLI."""

import subprocess
from pathlib import Path

import pytest


@pytest.mark.slow
def test_cli_formreg(tmp_path, patched_config_dir):
    """Test nwm_region_mgr formreg CLI command."""
    repo_root = Path(__file__).resolve().parents[2]

    result = subprocess.run(
        ["python", "-m", "nwm_region_mgr", str(patched_config_dir), "formreg"],
        cwd=repo_root,
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0
