"""Tests for nwm-region-mgr CLI parreg command."""

import subprocess
from pathlib import Path

import pytest
import yaml

ALGORITHMS = [
    "gower",
    "urf",
    "kmeans",
    "kmedoids",
    "hdbscan",
    "birch",
    "proximity",
]


@pytest.mark.slow
@pytest.mark.parametrize("algorithm", ALGORITHMS)
def test_cli_parreg_all_algorithms(tmp_path, algorithm, patched_config_dir):
    """Test nwm_region_mgr parreg CLI command for all algorithms."""
    repo_root = Path(__file__).resolve().parents[2]
    cfg_dir = patched_config_dir

    # patch algorithm list
    cfg_file = cfg_dir / "config_parreg.yaml"
    cfg = yaml.safe_load(cfg_file.read_text())
    cfg["general"]["algorithm_list"] = [algorithm]
    cfg_file.write_text(yaml.safe_dump(cfg))

    result = subprocess.run(
        ["python", "-m", "nwm_region_mgr", str(cfg_dir), "parreg"],
        cwd=repo_root,
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0
