"""Process configuration to conduct NGEN simulation with regionalized formulations and parameters.

Classes:
    - NgenSimulationProcessor: Processor to run NGEN simulation for regionalization.
Functions:
    - log_run_info: Log the run information.
    - create_mswm_config: Create MSWM config file based on template.
    - verify_ngen_run_inputs: Verify that necessary input files for NGEN run exist.
    - run_mswm: Run MSWM RealizationBuilder to build realization and BMI config files.
    - build_ngen_command: Build the NGEN command string.
    - run_ngen: Run NGEN as a subprocess and log output.
    - ngen_work_dir: Get NGEN work directory (work_dir field in MSWM config file).
    - ngen_data_dir: Get directory for NGEN inputs and outputs for a given VPU and algorithm.
    - ngen_vpu_workflow: Run the main workflow to execute MSWM and NGEN simulations.
"""

import logging
import os
import subprocess
from datetime import datetime
from pathlib import Path

from mswm.build_inputs import RealizationBuilder

from nwm_region_mgr.ngen.config_schema import TIMESTAMP_FMT, TIMESTAMP_FMT1
from nwm_region_mgr.utils import BaseConfigProcessor

logger = logging.getLogger(__name__)


class NgenSimulationProcessor(BaseConfigProcessor):
    """NGEN simulation processor."""

    def log_run_info(self, vpu: str, algo: str):
        """Log the run information."""
        logger.info("====== Settings for Current NGEN Regionalization Run ======")
        logger.info(f"VPU:            {vpu}")
        logger.info(f"Algorithm:      {algo}")
        logger.info(f"Run name:       {self.config.general.run_name}")
        logger.info(
            f"Time range:     {self.config.general.start_time} → {self.config.general.end_time}"
        )
        logger.info(f"Working dir:    {self.config.general.base_dir}")
        logger.info(
            f"Parameter file:   {self.config.general.par_file.get(f'{vpu}_{algo}', None)}"
        )
        logger.info(
            f"Pair file:        {self.config.general.pair_file.get(f'{vpu}_{algo}', None)}"
        )
        logger.info(
            f"GeoPackage file:  {self.config.general.ngen_hydrofabric_file.get(f'{vpu}', None)}"
        )
        logger.info(f"MSWM template file:  {self.config.general.config_template}")
        logger.info(f"NGEN input dir:      {self.ngen_data_dir(vpu, algo)}/Input")
        logger.info(f"NGEN output dir:     {self.ngen_data_dir(vpu, algo)}/Output")
        logger.info(f"Number of procs:     {self.config.general.n_procs}")
        logger.info("================================================")

    def resolve_num_processes(self, n: int):
        """Resolve number of processes to use for NGEN run."""
        if n == -1:
            return os.cpu_count() or 1
        return max(1, n)

    def create_mswm_config(self, vpu: str, algo: str) -> Path:
        """Create MSWM config file based on template."""
        with open(self.config.general.config_template, "r") as f:
            template_content = f.read()

        # format start and end times (as required by MSWM)
        start_time = datetime.strptime(self.config.general.start_time, TIMESTAMP_FMT)
        end_time = datetime.strptime(self.config.general.end_time, TIMESTAMP_FMT)
        self.config.general.start_time = start_time.strftime(TIMESTAMP_FMT1)
        self.config.general.end_time = end_time.strftime(TIMESTAMP_FMT1)

        # global_domain for ngen-forcing
        domain_map = {
            "conus": "CONUS",
            "ak": "Alaska",
            "hi": "Hawaii",
            "prvi": "Puerto_Rico",
            "gl": "gl",
        }

        domain = self.config.general.domain.lower()

        try:
            general_domain = domain_map[domain].lower()
            # forcing_domain = domain_map[domain]
        except KeyError:
            raise ValueError(
                f"Unsupported domain: {domain}. "
                f"Supported options: {', '.join(domain_map.keys())}."
            )

        forcing_source = "aorc" if domain == "conus" else "nwm"

        # Replace placeholders in the template
        config_content = template_content.format(
            vpu="vpu_" + vpu,
            run_name=self.config.general.run_name + "_" + algo,
            start_time=self.config.general.start_time,
            end_time=self.config.general.end_time,
            par_file=self.config.general.par_file.get(f"{vpu}_{algo}", None),
            pair_file=self.config.general.pair_file.get(f"{vpu}_{algo}", None),
            gpkg_file=self.config.general.ngen_hydrofabric_file.get(f"{vpu}", None),
            work_dir=self.ngen_work_dir,
            nprocs=self.resolve_num_processes(self.config.general.n_procs),
            static_data_dir=self.config.general.static_data_dir,
            domain=general_domain,
            # global_domain=forcing_domain,
            forcing_configuration=forcing_source,
        )

        # Write the new config file
        config_path = (
            self.ngen_work_dir.parent
            / f"mswm.config_{self.config.general.run_name}_{algo}_vpu{vpu}"
        )
        with open(config_path, "w") as f:
            f.write(config_content)

        logger.info(f"Created MSWM config file at: {config_path}")

        return config_path

    def verify_ngen_run_inputs(
        self,
        vpu: str,
        algo: str,
    ) -> tuple[Path, Path, Path, Path]:
        """Verify that necessary input files for NGEN run exist."""
        input_dir = self.ngen_data_dir(vpu, algo) / "Input"
        ngen_exe = input_dir / "ngen"
        real_file = (
            self.ngen_data_dir(vpu, algo)
            / f"vpu_{vpu}_realization_config_bmi_region.json"
        )
        real_file = real_file.resolve()
        partition_file = input_dir / f"vpu_{vpu}_partition_config.json"
        hydrofab_file = input_dir / self.config.general.ngen_hydrofabric_file.get(
            f"{vpu}", None
        )

        # command line argument validation
        if not ngen_exe.is_file():
            raise FileNotFoundError(f"NGEN executable not found: {ngen_exe}")
        if not real_file.is_file():
            raise FileNotFoundError(f"Realization config file not found: {real_file}")
        if not partition_file.is_file() and self.config.general.n_procs > 1:
            raise FileNotFoundError(f"Partition file not found: {partition_file}")
        if not hydrofab_file.is_file():
            raise FileNotFoundError(f"Hydrofabric file not found: {hydrofab_file}")
        logger.info("All NGEN command-line arguments verified.")

        return ngen_exe, real_file, partition_file, hydrofab_file

    def run_mswm(self, config_path, log_level=logging.INFO):
        """Run MSWM RealizationBuilder to build realization and BMI config files."""
        root_logger = logging.getLogger()
        saved_handlers = root_logger.handlers.copy()

        # Dedicated MSWM logger
        mswm_logger = logging.getLogger("mswm")
        mswm_logger.setLevel(log_level)
        mswm_logger.propagate = False
        mswm_logger.handlers.clear()
        for h in saved_handlers:
            mswm_logger.addHandler(h)

        # Disable propagation on all mswm sub-loggers to avoid double logging
        for name, logger_obj in logging.root.manager.loggerDict.items():
            if name.startswith("mswm") and isinstance(logger_obj, logging.Logger):
                logger_obj.handlers = mswm_logger.handlers
                logger_obj.propagate = False

        # Call MSWM
        rb = RealizationBuilder(config_path)
        rb.build_region_realization()

        # Restore root logger
        root_logger.handlers.clear()
        for h in saved_handlers:
            root_logger.addHandler(h)
        logging.getLogger("main").info("MSWM finished, logging restored.")

    def build_ngen_command(self, vpu: str, algo: str) -> str:
        """Build the NGEN command string."""
        ngen_exe, real_file, partition_file, hydrofab_file = (
            self.verify_ngen_run_inputs(vpu, algo)
        )

        n_procs = self.resolve_num_processes(self.config.general.n_procs)

        # Precompute the output directory path safely
        output_dir = self.ngen_data_dir(vpu, algo) / "Output"
        output_dir.mkdir(parents=True, exist_ok=True)

        # Base command string
        if n_procs == 1:
            logger.info("Running NGEN in serial mode.")
            cmd_str = (
                f'cd "{output_dir}"\n'
                f"{ngen_exe} {hydrofab_file} all {hydrofab_file} all {real_file}"
            )
        else:
            logger.info(f"Running NGEN in parallel mode with {n_procs} processors.")
            cmd_str = (
                f'cd "{output_dir}"\n'
                f"mpirun --allow-run-as-root -n {n_procs} {ngen_exe} "
                f"{hydrofab_file} all {hydrofab_file} all {real_file} {partition_file}"
            )

        return cmd_str

    def run_ngen(self, vpu: str, algo: str):
        """Run NGEN as a subprocess and log output.

        Args:
            vpu (str): The VPU identifier.
            algo (str): The algorithm name.

        """
        cmd = ["bash", "-c", self.build_ngen_command(vpu, algo)]
        logger.info(f"Running command: {cmd}")
        subprocess.run(cmd, check=True)
        logger.info(f"Command finished: {cmd}")

    @property
    def ngen_work_dir(self) -> Path:
        """Get NGEN work directory (work_dir field in MSWM config file)."""
        return Path(self.config.output.ngen.path)

    def ngen_data_dir(self, vpu: str, algo: str) -> Path:
        """Get directory for NGEN inputs and outputs for a given VPU and algorithm."""
        return (
            self.ngen_work_dir
            / "regionalization"
            / (self.config.general.run_name + "_" + algo)
            / ("vpu_" + vpu)
        )

    def run_ngen_for_vpu(
        self,
        vpu: str,
    ):
        """Run the main workflow to execute MSWM and NGEN simulations for a given VPU.

        Args:
            vpu (str): The VPU identifier.

        """
        # iterate over algorithms
        for algo in self.config.general.algorithm_list:
            # log run info
            self.log_run_info(vpu, algo)

            # create MSWM config file based on template
            mswm_config_path = self.create_mswm_config(vpu, algo)

            # Run MSWM to build realization and module BMI config files
            with self.timing_block("Run MSWM RealizationBuilder"):
                self.run_mswm(mswm_config_path)

            # Run NGEN simulation
            with self.timing_block("Run NGEN simulation"):
                self.run_ngen(vpu, algo)
