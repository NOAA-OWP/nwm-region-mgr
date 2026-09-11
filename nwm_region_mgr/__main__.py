"""Main entry point for formulation/parameter regionalization and NGEN simulation.

This module reads a set of configuration files and executes formulation
regionalization, parameter regionalization, or NGEN simulation depending
on the selected option.
"""

from __future__ import annotations

import argparse
import logging
from argparse import RawTextHelpFormatter
from dataclasses import dataclass
from pathlib import Path
from typing import Literal, get_args

import matplotlib

from nwm_region_mgr.formreg import config_schema as fcs
from nwm_region_mgr.formreg.process_config import FormulationRegionalizationProcessor
from nwm_region_mgr.parreg import config_schema as pcs
from nwm_region_mgr.parreg.manual_pairings import ManualPairer
from nwm_region_mgr.parreg.process_config import ParameterRegionalizationProcessor
from nwm_region_mgr.utils.config_utils import BaseConfigProcessor
from nwm_region_mgr.utils.logging_utils import setup_logging

logger = logging.getLogger("nwm_region_mgr.__main__")
matplotlib.use("Agg")


@dataclass(frozen=True)
class ConfigFiles:
    """Standard configuration file names."""

    general: str = "config_general.yaml"
    formreg: str = "config_formreg.yaml"
    parreg: str = "config_parreg.yaml"
    ngen: str = "config_ngen.yaml"


CONFIG = ConfigFiles()

# required config files for each option
OPTIONS = Literal["formreg", "parreg", "ngen"]
REQUIRED_CONFIG_FILES: dict[OPTIONS, tuple[str, ...]] = {
    "formreg": (
        CONFIG.general,
        CONFIG.formreg,
    ),
    "parreg": (
        CONFIG.general,
        CONFIG.formreg,
        CONFIG.parreg,
    ),
    "ngen": (
        CONFIG.general,
        CONFIG.ngen,
    ),
}


def _resolve_config_files(
    config_dir: Path,
    option: OPTIONS,
) -> dict[str, Path]:
    """Resolve and validate config files required for the given option."""
    required = REQUIRED_CONFIG_FILES[option]
    config_paths = [config_dir / name for name in required]

    missing = [str(p) for p in config_paths if not p.is_file()]
    if missing:
        raise FileNotFoundError(
            f"Missing required config files for option '{option}':\n"
            + "\n".join(missing)
        )

    return config_paths


def _run_formreg(
    frp: FormulationRegionalizationProcessor,
    vpu: str,
) -> None:
    """Run formulation regionalization."""
    logger.info("Running formulation regionalization for VPU %s", vpu)
    frp.run_formreg_for_vpu(
        vpu,
        frp.get_output_file_path(
            "formulation",
            vpu,
            use_stem_suffix=True,
        ),
    )


def _run_parreg(
    frp: FormulationRegionalizationProcessor,
    prp: ParameterRegionalizationProcessor,
    vpu: str,
) -> None:
    """Run parameter regionalization (includes formulation regionalization)."""
    logger.info("Running parameter regionalization for VPU %s", vpu)
    prp.run_parreg_for_vpu(vpu, frp)

    mp = ManualPairer(prp.config)
    mp.run_manual_pairing(vpu, prp, frp)


def _run_ngen(
    nsp: BaseConfigProcessor,
    vpu: str,
) -> None:
    """Run NGEN simulations."""
    logger.info("Running NGEN simulation for VPU %s", vpu)
    nsp.run_ngen_for_vpu(vpu)


def _build_formreg_processor(config_paths: list[Path]):
    """Build formulation regionalization processor."""
    return FormulationRegionalizationProcessor(config_paths, fcs.Config)


def _build_parreg_processor(config_paths: dict[str, Path]):
    """Build parameter regionalization processor."""
    return ParameterRegionalizationProcessor(config_paths, pcs.Config)


def _build_ngen_processor(config_paths: list[Path]):
    """Build NGEN simulation processor."""
    from nwm_region_mgr.ngen import config_schema as ncs
    from nwm_region_mgr.ngen.process_config import NgenSimulationProcessor

    return NgenSimulationProcessor(config_paths, ncs.Config)


def main(
    config_dir: Path,
    option: OPTIONS,
    sample_size: int | None = None,
) -> None:
    """Execute regionalization or NGEN simulation."""
    # create processor instances to validate configs and file paths before starting any processing
    if option == "formreg":
        pc = _build_formreg_processor(_resolve_config_files(config_dir, "formreg"))
    elif option == "parreg":
        fpc = _build_formreg_processor(_resolve_config_files(config_dir, "formreg"))
        pc = _build_parreg_processor(_resolve_config_files(config_dir, "parreg"))
    elif option == "ngen":
        pc = _build_ngen_processor(_resolve_config_files(config_dir, "ngen"))

    # set up logging
    log_file = getattr(pc.config.general.logging, "file", None)
    log_level = getattr(pc.config.general.logging, "level", "INFO")

    setup_logging(level=log_level, log_file=log_file)

    logger.info("Starting nwm_region_mgr")
    logger.info("Config directory: %s", config_dir)
    logger.info("Run option: %s", option)
    if log_file:
        logger.info("Log file: %s", log_file)
    if sample_size is not None:
        logger.info("Sample size: %d", sample_size)

    # run the selected option (formreg or parreg or ngen)
    vpu = pc.config.general.vpu if hasattr(pc.config.general, "vpu") else None
    if not vpu:
        logger.warning(
            "VPU is not specified in the configuration. Please set the 'vpu' field in the config_general.yaml file."
        )
        return

    if vpu:
        logger.info("Processing VPU: %s", vpu)

        if option == "formreg":
            _run_formreg(pc, vpu)

        elif option == "parreg":
            _run_parreg(fpc, pc, vpu)

        elif option == "ngen":
            _run_ngen(pc, vpu)

    logger.info("Completed %s", option)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(formatter_class=RawTextHelpFormatter)

    parser.add_argument(
        "config_dir",
        type=Path,
        help=(
            "Path to directory containing configuration files.\n\n"
            "Required files depend on mode:\n"
            f"  formreg : {CONFIG.general}, {CONFIG.formreg}\n"
            f"  parreg  : {CONFIG.general}, {CONFIG.formreg}, {CONFIG.parreg}\n"
            f"  ngen    : {CONFIG.general}, {CONFIG.ngen}\n"
        ),
    )

    parser.add_argument(
        "option",
        nargs="?",
        choices=get_args(OPTIONS),
        default="parreg",
        help=(
            "Run option:\n"
            "  formreg : formulation regionalization only\n"
            "  parreg  : formulation + parameter regionalization (default)\n"
            "  ngen    : NGEN simulation only"
        ),
    )

    parser.add_argument(
        "--sample-size",
        type=int,
        default=None,
        help="Sample size for parameter regionalization",
    )

    args = parser.parse_args()
    main(args.config_dir, args.option, sample_size=args.sample_size)
