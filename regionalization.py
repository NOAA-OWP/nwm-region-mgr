"""Main script for parameter regionalization.

This script reads a configuration file and processes the parameter regionalization
using the specified algorithms and configurations.
"""

import argparse
import logging
from argparse import RawTextHelpFormatter
from pathlib import Path
from typing import Literal

import matplotlib

from nwm_region_mgr.formreg import config_schema as fcs
from nwm_region_mgr.formreg.process_config import FormulationRegionalizationProcessor
from nwm_region_mgr.parreg import config_schema as pcs
from nwm_region_mgr.parreg.manual_pairings import ManualPairer
from nwm_region_mgr.parreg.process_config import ParameterRegionalizationProcessor

logger = logging.getLogger(__name__)
matplotlib.use("Agg")


def main(
    config_dir: str | Path, config_files: list[str], mode: Literal["formreg", "region"]
) -> None:
    """Execute regionalization."""
    # Ensure mode is valid
    if mode not in {"formreg", "region"}:
        msg = (
            f"Invalid mode for regionalization: {mode}. Must be 'formreg' or 'region'."
        )
        logger.error(msg)
        raise ValueError(msg)

    # Build full paths to each config file
    config_paths = {file: config_dir / file for file in config_files}

    # Allow access to individual files
    file_general_config = config_paths["config_general.yaml"]
    file_formreg_config = config_paths["config_formreg.yaml"]
    file_parreg_config = config_paths["config_parreg.yaml"]

    # Check that all config files exist
    missing = [str(p) for p in config_paths.values() if not p.is_file()]
    if missing:
        raise FileNotFoundError(f"Missing required config files: {', '.join(missing)}")

    # Load and process the formulation regionalization config
    frp = FormulationRegionalizationProcessor(
        config_file=[file_general_config, file_formreg_config], config_schema=fcs.Config
    )

    # Load and process the parameter regionalization config
    rp = ParameterRegionalizationProcessor(
        config_file=[file_general_config, file_parreg_config],
        config_schema=pcs.Config,
        sample_size=None,
    )

    if mode == "formreg":
        # process formulation regionalization by VPU only
        for vpu in frp.config.general.vpu_list:
            frp.run_formreg_for_vpu(
                vpu,
                frp.get_output_file_path(
                    "formulation",
                    vpu,
                    use_stem_suffix=True,
                ),
            )
        return

    # process parameter regionalization by VPU (which also runs formulation regionalization)
    for vpu in rp.config.general.vpu_list:
        rp.run_parreg_for_vpu(vpu, frp)

    # If manual pairings are enabled, run the manual pairings
    mp = ManualPairer(rp.config)
    for vpu in rp.config.general.vpu_list:
        mp.run_manual_pairing(vpu)


if __name__ == "__main__":
    # Create the parser
    parser = argparse.ArgumentParser(formatter_class=RawTextHelpFormatter)

    config_files = ["config_general.yaml", "config_formreg.yaml", "config_parreg.yaml"]

    # Argument help text
    help_text = """Path to the folder containing the following three YAML config files:
    config_general.yaml: contains general settings for the regionalization process.
    config_formreg.yaml: contains specific settings for the formulation regionalization process.
    config_parreg.yaml: contains specific settings for the parameter regionalization process.

    Example usage:
    python regionalization.py /path/to/configs/ formreg
    python regionalization.py /path/to/configs/ region
    python regionalization.py /path/to/configs/

    """
    # Add the argument for the config directory
    parser.add_argument(
        "config_dir",
        type=str,
        help=help_text,
    )

    # Add argument to specify run mode: formreg or region; default is region
    parser.add_argument(
        "mode",
        nargs="?",
        choices=["formreg", "region"],
        default="region",
        help=(
            "Specify the run mode: 'formreg' for formulation regionalization only or 'region' for parameter "
            "regionalization, which runs both formulation and parameter regionalization (default: 'region')"
        ),
    )

    # Parse the arguments
    args = parser.parse_args()
    config_dir = Path(args.config_dir)
    main(config_dir, config_files, args.mode)
