"""Module to provide functionality for handling manual pairings of donor-receiver pairings."""

import logging
from functools import lru_cache
from pathlib import Path

import pandas as pd
import pyarrow.parquet as pq

from nwm_region_mgr.formreg.process_config import (
    FormulationRegionalizationProcessor as FRP,
)
from nwm_region_mgr.parreg.process_config import (
    ParameterRegionalizationProcessor as PRP,
)
from nwm_region_mgr.utils import read_table

logger = logging.getLogger(__name__)


class ManualPairer:
    """Class to handle manual pairings of donor-receiver pairings based on user input."""

    def __init__(self, config: dict):
        """Initialize the ManualPairer."""
        self.config = config

    @property
    def manual_pairings_file(self) -> Path:
        """Path to the manual pairings file."""
        files = getattr(self.config.general, "manual_pairings_file", None)
        if files is None:
            return None

        return files[self.vpu]

    @property
    def divide_col(self):
        """Get the divide column name from the configuration."""
        return getattr(self.config.general.id_col, "divide", "div_id")

    @property
    def donor_col(self):
        """Get the donor column name from the configuration."""
        return getattr(self.config.general.id_col, "donor", "donor")

    @property
    def gage_col(self):
        """Get the gage column name from the configuration."""
        return getattr(self.config.general.id_col, "gage", "gage_id")

    @property
    def manual_pairings_df(self) -> pd.DataFrame:
        """Load and return the manual pairings DataFrame."""
        if not self.manual_pairings_file:
            return pd.DataFrame()
        else:
            dtype_dict = {
                f"receiver_{self.divide_col}": str,
                f"donor_{self.divide_col}": str,
                f"receiver_{self.gage_col}": str,
                f"donor_{self.gage_col}": str,
            }
            return read_table(self.manual_pairings_file, dtype=dtype_dict, refresh=True)

    def set_vpu(self, vpu: str):
        """Set the vpu."""
        self.vpu = vpu

    def regionalization_df(
        self, regionalization_output_file: str | Path
    ) -> pd.DataFrame:
        """Get the regionalization DataFrame based on manual pairings."""
        return read_table(regionalization_output_file)

    def check_manual_pairing_columns(self, df: pd.DataFrame) -> None:
        """Check that the manual pairings dataframe has the required columns.

        The column names must include one of the following pairs:
        - f"receiver_{self.divide_col}" and f"donor_{self.divide_col}"
        - f"receiver_{self.gage_col}" and f"donor_{self.gage_col}"
        - f"receiver_{self.divide_col}" and f"donor_{self.gage_col}"
        - f"receiver_{self.gage_col}" and f"donor_{self.divide_col}"

        Additionally, each row in the file must have exactly one receiver column and one donor column populated.

        """
        # make sure the file contains at least one receiver column and one donor column with valid naming convention
        receiver_cols = [f"receiver_{self.divide_col}", f"receiver_{self.gage_col}"]
        donor_cols = [f"donor_{self.divide_col}", f"donor_{self.gage_col}"]
        valid_pairs = [
            {receiver_cols[0], donor_cols[0]},
            {receiver_cols[1], donor_cols[1]},
            {receiver_cols[0], donor_cols[1]},
            {receiver_cols[1], donor_cols[0]},
        ]
        if not any(pair.issubset(df.columns) for pair in valid_pairs):
            msg = (
                f"Manual pairings file {self.manual_pairings_file} must contain at least one of {receiver_cols} "
                f"and one of {donor_cols} as column names. Please correct the column names to match the required "
                f"naming convention."
            )
            logger.error(msg)
            raise ValueError(msg)

        # make sure every row in the file has exactly one receiver and one donor column populated
        receiver_cols_present = [c for c in receiver_cols if c in df.columns]
        donor_cols_present = [c for c in donor_cols if c in df.columns]
        receiver_counts = df[receiver_cols_present].notna().sum(axis=1)
        donor_counts = df[donor_cols_present].notna().sum(axis=1)
        invalid_rows = (receiver_counts != 1) | (donor_counts != 1)

        if invalid_rows.any():
            bad_idx = df.index[invalid_rows].tolist()
            msg = (
                f"Row {bad_idx} in manual pairings file {self.manual_pairings_file} must have exactly one receiver "
                f"column and one donor column populated. "
            )
            logger.error(msg)
            raise ValueError(msg)

    def _extract_pairing_cases(self):
        """Extract the four different cases of manual receiver/donor pairings."""
        df = self.manual_pairings_df

        def extract(cols):
            if all(c in df.columns for c in cols):
                return df[cols].dropna(how="any")
            return pd.DataFrame(columns=cols)

        df1 = extract([f"receiver_{self.divide_col}", f"donor_{self.divide_col}"])
        df2 = extract([f"receiver_{self.gage_col}", f"donor_{self.gage_col}"])
        df3 = extract([f"receiver_{self.divide_col}", f"donor_{self.gage_col}"])
        df4 = extract([f"receiver_{self.gage_col}", f"donor_{self.divide_col}"])

        return df1, df2, df3, df4

    def _get_required_donor_divides(self, df1, df2, df3, df4):
        """Get the required donor divides based on the manual pairings."""
        donor_gages = set(df2[f"donor_{self.gage_col}"].dropna()) | set(
            df3[f"donor_{self.gage_col}"].dropna()
        )

        donor_divides = set(
            self.cwt_df.loc[
                self.cwt_df[self.gage_col].isin(donor_gages), self.divide_col
            ]
        )

        donor_divides |= set(df1[f"donor_{self.divide_col}"].dropna())
        donor_divides |= set(df4[f"donor_{self.divide_col}"].dropna())

        return donor_divides

    def _process_gage_gage_pairs(self, df, dist_spatial):
        """Process gage/gage pairings.

        For each receiver divide associated with the receiver gage, assign the nearest donor divide
        associated with the donor gage based on spatial proximity.

        """
        rows = []

        for _, row in df.iterrows():
            receiver_gage = row[f"receiver_{self.gage_col}"]
            donor_gage = row[f"donor_{self.gage_col}"]

            receiver_divides = self.cwt_df.loc[
                self.cwt_df[self.gage_col] == receiver_gage, self.divide_col
            ]
            receiver_divides = [r for r in receiver_divides if r in dist_spatial.index]
            if not receiver_divides:
                logger.warning(
                    f"Invalid manual pairing for receiver gage {receiver_gage}. Skipping this pairing."
                )
                continue

            donor_divides = self.cwt_df.loc[
                self.cwt_df[self.gage_col] == donor_gage, self.divide_col
            ]
            donor_divides = [d for d in donor_divides if d in dist_spatial.columns]
            if not donor_divides:
                logger.warning(
                    f"Invalid manual pairing for donor gage {donor_gage}. Skipping this pairing."
                )
                continue

            for r in receiver_divides:
                d = dist_spatial.loc[r, donor_divides].idxmin()
                rows.append({self.divide_col: r, "donor": d})

        return pd.DataFrame(rows)

    def _process_divide_gage_pairs(self, df, dist_spatial):
        """Process divide/gage pairings.

        For each receiver divide, assign the nearest donor divide associated with the donor gage
        based on spatial proximity.
        """
        rows = []

        for _, row in df.iterrows():
            receiver_divide = row[f"receiver_{self.divide_col}"]

            # Check receiver exists
            if receiver_divide not in dist_spatial.index:
                logger.warning(
                    f"Invalid manual pairing for receiver divide {receiver_divide}. Skipping this pairing."
                )
                continue

            donor_gage = row[f"donor_{self.gage_col}"]

            donor_divides = self.cwt_df.loc[
                self.cwt_df[self.gage_col] == donor_gage, self.divide_col
            ]
            valid_donors = [d for d in donor_divides if d in dist_spatial.columns]

            if not valid_donors:
                logger.warning(
                    f"Invalid manual pairing for receiver divide {receiver_divide}. Skipping this pairing."
                )
                continue

            series = dist_spatial.loc[receiver_divide, valid_donors]
            if series.empty:
                logger.warning(
                    f"No spatial distances found for receiver divide {receiver_divide}"
                )
                continue

            d = series.idxmin()

            rows.append({self.divide_col: receiver_divide, "donor": d})

        return pd.DataFrame(rows)

    def _process_gage_divide_pairs(self, df):
        """Process gage/divide pairings.

        Assign the donor divide to all receiver divides associated with the receiver gage.
        """
        rows = []

        for _, row in df.iterrows():
            receiver_gage = row[f"receiver_{self.gage_col}"]
            donor_divide = row[f"donor_{self.divide_col}"]

            receiver_divides = self.cwt_df.loc[
                self.cwt_df[self.gage_col] == receiver_gage, self.divide_col
            ]

            for r in receiver_divides:
                rows.append({self.divide_col: r, "donor": donor_divide})

        return pd.DataFrame(rows)

    def _add_spatial_distance_column(self, df_manual, dist_spatial):
        """Add a spatial distance column to the manual pairings DataFrame based on the distance matrix."""
        row_idx = dist_spatial.index.get_indexer(df_manual[self.divide_col])
        col_idx = dist_spatial.columns.get_indexer(df_manual["donor"])

        missing_rows = df_manual[self.divide_col][row_idx < 0]
        missing_cols = df_manual["donor"][col_idx < 0]

        if len(missing_rows) > 0 or len(missing_cols) > 0:
            raise ValueError(
                f"Missing receivers in distance matrix: {missing_rows.unique()[:5]}, "
                f"Missing donors in distance matrix: {missing_cols.unique()[:5]}"
            )

        values = dist_spatial.to_numpy()
        df_manual["distSpatial"] = values[row_idx, col_idx]

        return df_manual

    def _add_manual_tag_column(self, df_manual):
        """Add a "manual" tag column to the manual pairings DataFrame."""
        df_manual["tag"] = "manual"
        return df_manual

    def _remove_duplicate_receivers(self, df_manual):
        """If there are duplicate receiver divides, keep the one with the smallest spatial distance."""
        # Check for duplicated receivers
        dup_receivers = df_manual[self.divide_col].duplicated(keep=False)

        if dup_receivers.any():
            n_dup = df_manual.loc[dup_receivers, self.divide_col].nunique()
            logger.info(
                f"{n_dup} receivers have multiple donors specified; selecting the closest donor based on 'distSpatial'."
            )

        df_manual = (
            df_manual.sort_values("distSpatial")
            .drop_duplicates(subset=self.divide_col, keep="first")
            .reset_index(drop=True)
        )

        return df_manual

    def get_manual_pairs_for_divide(self, dist_file: str | Path) -> pd.DataFrame:
        """Resolve manual receiver/donor pairings.

        Handle the four different cases of manual receiver/donor pairings:
        - divide/divide,
        - divide/gage,
        - gage/divide,
        - gage/gage

        """
        if self.manual_pairings_df is None:
            return pd.DataFrame()

        df1_raw, df2_raw, df3_raw, df4_raw = self._extract_pairing_cases()

        # gather donor divides needed for spatial distance lookup
        donor_divides = self._get_required_donor_divides(
            df1_raw, df2_raw, df3_raw, df4_raw
        )

        # get valid donors (columns in the distance matrix)
        schema = pq.read_schema(dist_file)
        available_cols = set(schema.names)
        valid_cols = [c for c in donor_divides if c in available_cols]

        missing = set(donor_divides) - available_cols
        if missing:
            logger.warning(
                f"The following donor divides specified in the manual pairings file are not present in the distance matrix: {missing}"
            )

        dist_spatial = pd.read_parquet(dist_file, columns=valid_cols)

        # initialize empty dataframes with correct columns
        df1 = df2 = df3 = df4 = pd.DataFrame(columns=[self.divide_col, "donor"])

        # Case 1: divide/divide pairings (no extra processing needed, except renaming columns)
        if not df1_raw.empty:
            df1 = df1_raw.rename(
                columns={
                    f"receiver_{self.divide_col}": self.divide_col,
                    f"donor_{self.divide_col}": "donor",
                }
            )

        # Process the other three cases which require crosswalk and/or spatial distance lookups
        # to resolve donor divides for receiver divides
        if not df2_raw.empty:
            df2 = self._process_gage_gage_pairs(df2_raw, dist_spatial)
        if not df3_raw.empty:
            df3 = self._process_divide_gage_pairs(df3_raw, dist_spatial)
        if not df4_raw.empty:
            df4 = self._process_gage_divide_pairs(df4_raw)

        # concatenate all manual pairings together
        df_manual = pd.concat([df1, df2, df3, df4], ignore_index=True)

        df_manual = self._add_spatial_distance_column(df_manual, dist_spatial)
        df_manual = self._add_manual_tag_column(df_manual)
        df_manual = self._remove_duplicate_receivers(df_manual)

        return df_manual

    def update_pairings(
        self, regionalization_output_file: str | Path, df_manual: pd.DataFrame
    ) -> pd.DataFrame:
        """Update the regionalization DataFrame with manual pairings."""
        # original pairings from algorithm-based pairings
        df = self.regionalization_df(regionalization_output_file)

        # keep only rows not manually specified
        df_non_manual = df[~df[self.divide_col].isin(df_manual[self.divide_col])]

        # align manual dataframe to match original columns (missing columns filled with NaN)
        df_manual = df_manual.reindex(columns=df.columns)

        # combine and sort by divide column
        df_updated = (
            pd.concat([df_non_manual, df_manual], ignore_index=True)
            .sort_values(self.divide_col)
            .reset_index(drop=True)
        )

        return df_updated

    @property
    @lru_cache
    def cwt_df(self) -> pd.DataFrame:
        """Load and return the CWT DataFrame."""
        return read_table(
            self.config.general.gage_divide_cwt_file, dtype={self.gage_col: str}
        )

    def get_pairs_output_file(
        self, vpu: str, algorithm: str, use_stem_suffix: bool = False
    ) -> Path:
        """Construct the path to the regionalization output file for a given VPU."""
        out = getattr(self.config.output, "pairs", None)
        if out is None:
            msg = "Output configuration for 'pairs' is not defined."
            logger.error(msg)
            raise ValueError(msg)
        return out.get_file_path(
            vpu=vpu, algorithm=algorithm, use_stem_suffix=use_stem_suffix
        )

    def get_param_output_file(
        self, vpu: str, algorithm: str, use_stem_suffix: bool = False
    ) -> Path:
        """Construct the path to the parameter output file for a given VPU."""
        out = getattr(self.config.output, "params", None)
        if out is None:
            msg = "Output configuration for 'params' is not defined."
            logger.error(msg)
            raise ValueError(msg)
        return out.get_file_path(
            vpu=vpu, algorithm=algorithm, use_stem_suffix=use_stem_suffix
        )

    def create_backup_pair_param_files(
        self,
        vpu: str,
        algorithm: str,
    ) -> None:
        """Create backup copies of the original regionalization output files before applying manual pairings.

        These include: the full pairs file, MSWM pairs file (csv), and parameter output file (if they exist).
        The backup files will have the same name with '_original' added to the stem.

        """
        pairs_file = self.get_pairs_output_file(vpu, algorithm)
        mswm_pairs_file = self.get_pairs_output_file(
            vpu=vpu, algorithm=algorithm, use_stem_suffix=True
        ).with_suffix(".csv")  # MSWM pairs file is in csv format
        params_output_file = self.get_param_output_file(vpu, algorithm)

        def backup_file(file: Path) -> None:
            if not file.exists():
                return

            # create backup file path by adding '_original' to the stem of the original file name
            stem = file.stem
            if "_original" not in stem:
                backup_path = file.with_name(f"{stem}_original{file.suffix}")
            else:
                backup_path = file  # already has '_original', so backup is itself

            # Remove old backup if exists (overwrite)
            if backup_path.exists() and backup_path != file:
                logger.info(
                    f"Existing backup file already found for {backup_path}. Overwriting the existing backup."
                )
                backup_path.unlink()

            # Rename original to backup if necessary
            if backup_path != file:
                file.rename(backup_path)
                logger.info(f"Created backup of original file at: {backup_path}")

        backup_file(pairs_file)
        backup_file(mswm_pairs_file)
        backup_file(params_output_file)

    def run_manual_pairing(self, vpu: str, prp: PRP, frp: FRP) -> None:
        """Run the manual pairing process and save the updated DataFrame."""
        # set the VPU for processing
        self.set_vpu(vpu)

        if not self.manual_pairings_file:
            logger.debug("No manual pairings file provided. Skipping manual pairings.")
            return

        # check that the manual pairings file has the required columns and valid formatting
        self.check_manual_pairing_columns(self.manual_pairings_df)

        # make sure distances file exists
        dist_file = prp.dist_file
        if not dist_file.is_file():
            msg = f"Spatial distance file not found at expected location: {dist_file}"
            logger.error(msg)
            raise FileNotFoundError(msg)

        # resolve manual pairings to get the final dataframe of receiver-divide to donor-divide pairings
        df_manual = self.get_manual_pairs_for_divide(dist_file)
        if df_manual.empty:
            logger.info(
                "No valid manual pairings found after processing. Skipping manual pairings."
            )
            return

        # loop through each algorithm's regionalization output file to apply manual pairings
        for algorithm in self.config.general.algorithm_list:
            logger.info(
                f"******* Running manual pairings for VPU: {vpu} | Algorithm: {algorithm} *******"
            )

            # read in the regionalization output file and update with manual pairings
            df_updated = self.update_pairings(
                self.get_pairs_output_file(vpu, algorithm), df_manual
            )

            # keep a backup of the original regionalization output files before overwriting with manual pairings
            self.create_backup_pair_param_files(vpu, algorithm)

            # save the updated pairs file with manual pairings
            prp.save_pairing_results(df_updated, algorithm)

            # save the updated params files
            prp.create_formulation_parameter_file(
                getattr(frp.config.output, "formulation", None), algorithm
            )

            logger.info(
                f"Completed manual pairings for VPU: {vpu} | Algorithm: {algorithm}"
            )
