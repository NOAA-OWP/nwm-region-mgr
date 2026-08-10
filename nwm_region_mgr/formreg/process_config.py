"""Process configuration to conduct formulation regionalization.

process_config.py

Functions:
    - run_formreg_for_vpu: Run the formulation regionalization process for a given VPU.

"""

import logging
from pathlib import Path

from nwm_region_mgr.formreg import select_formulation as sf
from nwm_region_mgr.formreg import summary_score as ss
from nwm_region_mgr.utils import BaseConfigProcessor

logger = logging.getLogger(__name__)


class FormulationRegionalizationProcessor(BaseConfigProcessor):
    """Formulation regionalization processor."""

    def run_formreg_for_vpu(self, vpu: str, formulation_file: str) -> None:
        """Run the formulation regionalization process for a given VPU.

        Args:
            vpu (str): The VPU for which to run the formulation regionalization.
            formulation_file (str): Path to the formulation file for the VPU.

        """
        # set the VPU for processing
        self.set_vpu(vpu)

        if not formulation_file:
            msg = f"No formulation file provided for VPU {vpu}."
            logger.error(msg)
            raise ValueError(msg)

        if Path(formulation_file).exists():
            logger.info(
                f"Formulation file already exists for VPU {vpu}, skipping formulation regionalization."
            )
            return

        logger.info(
            f"--------- Processing formulation regionalization for VPU: {vpu} ---------"
        )

        # compute the summary score for the VPU
        with self.timing_block("compute_summary_score"):
            df_score = ss.compute_summary_score(self.config, vpu)

        # select the best formulation based on the summary score and optionally costs
        with self.timing_block("select_formulation"):
            sf.select_formulation(self.config, vpu, df_score, self.get_vpu_gdf())

        logger.info(f"Formulation regionalization for VPU {vpu} completed.")
