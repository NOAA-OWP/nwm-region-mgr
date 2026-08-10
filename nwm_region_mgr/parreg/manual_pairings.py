"""Module to provide functionality for handling manual pairings of donor-receiver pairings."""

import logging
from functools import lru_cache
from pathlib import Path

import pandas as pd

from nwm_region_mgr.utils import read_table, save_data

logger = logging.getLogger(__name__)


class ManualPairer:
    """Class to handle manual pairings of donor-receiver pairings based on user input."""

    def __init__(self, config: dict):
        """Initialize the ManualPairer."""
        self.config = config

    @property
    def manual_pairings_file(self):
        """Path to the manual pairings file."""
        return self.config.general.manual_pairings_file

    @property
    def divide_col(self):
        """Get the divide column name from the configuration."""
        return getattr(self.config.general.id_col, "divide", "divide_id")

    @property
    def donor_col(self):
        """Get the donor column name from the configuration."""
        return getattr(self.config.general.id_col, "donor", "donor")

    @property
    def gage_col(self):
        """Get the gage column name from the configuration."""
        return getattr(self.config.general.id_col, "gage", "gage_id")

    @property
    @lru_cache
    def manual_pairings_df(self) -> pd.DataFrame:
        """Load and return the manual pairings DataFrame."""
        if not self.manual_pairings_file:
            return
        else:
            return read_table(self.manual_pairings_file, dtype={self.gage_col: str})

    def regionalization_df(
        self, regionalization_output_file: str | Path
    ) -> pd.DataFrame:
        """Get the regionalization DataFrame based on manual pairings."""
        return read_table(regionalization_output_file)

    def manually_update_pairings(
        self, regionalization_output_file: str | Path
    ) -> pd.DataFrame:
        """Update the regionalization DataFrame with manual pairings."""
        if self.manual_pairings_df is None:
            return
        df = self.regionalization_df(regionalization_output_file)

        self.check_donor_column()
        self.check_manual_pairings_overlaps()

        if self.gage_col in self.manual_pairings_df.columns:
            df = self.update_by_gage(df)
        if self.divide_col in self.manual_pairings_df.columns:
            df = self.update_by_divide(df)

        return df

    def check_donor_column(self):
        """Check if the donor column exists in the manual pairings DataFrame."""
        if self.donor_col not in self.manual_pairings_df.columns:
            raise ValueError(
                f"Donor column '{self.donor_col}' not found in manual pairings DataFrame."
            )

    @property
    @lru_cache
    def cwt_df(self) -> pd.DataFrame:
        """Load and return the CWT DataFrame."""
        return read_table(
            self.config.general.gage_divide_cwt_file, dtype={self.gage_col: str}
        )

    def update_by_divide(self, df: pd.DataFrame) -> pd.DataFrame:
        """Update the pairings DataFrame by divide."""
        df = df.merge(
            self.manual_pairings_df[[self.divide_col, self.donor_col]],
            on=self.divide_col,
            how="left",
            suffixes=("", "_manual"),
        )
        df[self.donor_col] = df[f"{self.donor_col}_manual"].combine_first(
            df[self.donor_col]
        )

        return df.drop(columns=[f"{self.donor_col}_manual"])

    def update_by_gage(self, df: pd.DataFrame) -> pd.DataFrame:
        """Update the pairings DataFrame by gage."""
        for _, row in self.manual_pairings_df.loc[
            self.manual_pairings_df[self.gage_col].notnull()
        ].iterrows():
            gage = row[self.gage_col]
            logger.info(f"Updating pairings for gage: {gage}")
            if gage in self.cwt_df[self.gage_col].values:
                divide_ids_for_gage = self.cwt_df.loc[
                    self.cwt_df[self.gage_col] == gage, self.divide_col
                ]
                logger.debug(f"Updating gage: {gage} with donor: {row[self.donor_col]}")
                df.loc[
                    df[self.divide_col].isin(divide_ids_for_gage), self.donor_col
                ] = row[self.donor_col]
        return df

    @property
    @lru_cache
    def divides_from_gages(self) -> list[str]:
        """Get a list of divides from the gages in the CWT DataFrame."""
        return self.cwt_df.loc[
            self.cwt_df[self.gage_col].isin(self.manual_pairings_df[self.gage_col]),
            self.divide_col,
        ].tolist()

    @property
    @lru_cache
    def divides_from_manual(self) -> list[str]:
        """Get a list of divides from the manual pairings DataFrame."""
        return self.manual_pairings_df[self.divide_col].tolist()

    def check_manual_pairings_overlaps(self) -> bool:
        """Check if there are multiple manual pairings for the same divide."""
        if len(set(self.divides_from_manual + self.divides_from_gages)) != len(
            self.divides_from_manual + self.divides_from_gages
        ):
            raise ValueError(
                f"There are multiple manual pairings for the same divide:{list(set(self.divides_from_manual).intersection(self.divides_from_gages))} "
                "Please check your manual pairings file."
            )

    def get_regionalization_output_file(self, vpu: str, algorithm: str) -> Path:
        """Construct the path to the regionalization output file for a given VPU."""
        out = getattr(self.config.output, "pairs", None)
        if out is None:
            msg = "Output configuration for 'pairs' is not defined."
            logger.error(msg)
            raise ValueError(msg)
        return out.get_file_path(vpu=vpu, algorithm=algorithm)

    def run_manual_pairing(self, vpu: str):
        """Run the manual pairing process and save the updated DataFrame."""
        if not self.manual_pairings_file:
            logger.debug("No manual pairings file provided. Skipping manual pairings.")
            return

        for algorithm in self.config.general.algorithm_list:
            logger.info(
                f"Running manual pairings for VPU: {vpu} | Algorithm: {algorithm}"
            )
            regionalization_output_file = self.get_regionalization_output_file(
                vpu, algorithm
            )
            save_data(
                self.manually_update_pairings(regionalization_output_file),
                regionalization_output_file,
                index=True,
            )
