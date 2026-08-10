"""Unit and integration tests for parreg.process_config.ParameterRegionalizationProcessor."""

from types import SimpleNamespace

import pandas as pd
import pytest

from nwm_region_mgr.parreg.process_config import (
    ParameterRegionalizationProcessor as PRP,
)


@pytest.fixture
def minimal_donors_df():
    """Minimal donor gages dataframe."""
    return pd.DataFrame(
        {
            "gage_id": ["G1", "G2"],
            "longitude": [-105.0, -104.5],
            "latitude": [40.0, 40.5],
        }
    )


@pytest.fixture
def gage_crosswalk_df():
    """Minimal gage crosswalk dataframe."""
    return pd.DataFrame(
        {
            "gage_id": ["G1", "G2"],
            "div_id": ["D1", "D2"],
            "vpu_id": ["01", "01"],
        }
    )


@pytest.fixture
def fake_config():
    """Minimal config object with the attributes the processor expects."""
    cfg = SimpleNamespace()
    cfg.general = SimpleNamespace(
        base_dir="/fake/base/dir",
        donor_gage_file="donor_gages.csv",
        gage_divide_cwt_file="gage_divide_crosswalk.parquet",
        id_col={"gage": "gage_id", "divide": "div_id"},
    )
    return cfg


@pytest.fixture
def processor(minimal_donors_df, gage_crosswalk_df, fake_config, monkeypatch):
    """ParameterRegionalizationProcessor with minimal injected data."""
    proc = PRP.__new__(PRP)

    # Inject only what the tested methods need
    proc._donor_gages = minimal_donors_df
    proc._gage_crosswalk = gage_crosswalk_df
    proc.config = fake_config

    # Monkeypatch donors_df to minimal_donors_df
    monkeypatch.setattr(
        PRP,
        "donors_df",
        property(lambda self: minimal_donors_df),
    )
    return proc


@pytest.fixture
def temp_hydrofabric_dir(tmp_path):
    """Temporary hydrofabric directory structure."""
    hf = tmp_path / "hydrofabric" / "01"
    hf.mkdir(parents=True)
    (hf / "divides.gpkg").touch()
    return tmp_path


@pytest.mark.unit
def test_donors_df_valid(processor, minimal_donors_df):
    """Test donors_df property."""
    df = processor.donors_df
    assert df.equals(minimal_donors_df)


@pytest.mark.unit
def test_donors_df_missing_coordinates_raises(monkeypatch):
    """Test that donors_df raises ValueError if coordinates are missing."""
    # Create a fresh processor instance (no monkeypatch applied)
    proc = PRP.__new__(PRP)

    # Minimal fake config
    proc.config = SimpleNamespace(
        general=SimpleNamespace(
            donor_gage_file="dummy.csv",
            id_col=SimpleNamespace(gage="gage_id", divide="div_id"),
        )
    )

    # Stub donor_gages to a DataFrame missing coordinates
    monkeypatch.setattr(
        PRP, "donor_gages", property(lambda self: pd.DataFrame({"gage_id": ["G1"]}))
    )

    # Now test
    with pytest.raises(ValueError, match="longitude.*latitude"):
        _ = proc.donors_df


@pytest.mark.unit
def test_donors_df_empty(monkeypatch):
    """Test that donors_df raises ValueError if no donors are found."""
    monkeypatch.setattr(
        PRP,
        "donor_gages",
        property(
            lambda self: pd.DataFrame(columns=["gage_id", "longitude", "latitude"])
        ),
    )

    proc = PRP.__new__(PRP)
    proc.config = SimpleNamespace(
        general=SimpleNamespace(
            donor_gage_file="dummy.csv",
            id_col=SimpleNamespace(gage="gage_id", divide="div_id"),
        )
    )
    with pytest.raises(ValueError, match="No donors found"):
        _ = proc.donors_df


@pytest.mark.unit
@pytest.mark.parametrize("missing_col", ["longitude", "latitude"])
def test_donors_df_missing_columns_raises(missing_col, monkeypatch):
    """Parametrized test for missing longitude/latitude columns."""
    df = pd.DataFrame({"gage_id": ["G1"], "longitude": [0.0], "latitude": [0.0]})
    df = df.drop(columns=[missing_col])

    monkeypatch.setattr(PRP, "donor_gages", property(lambda self: df))

    proc = PRP.__new__(PRP)
    proc.config = SimpleNamespace(
        general=SimpleNamespace(
            donor_gage_file="dummy.csv",
            id_col=SimpleNamespace(gage="gage_id", divide="div_id"),
        )
    )

    with pytest.raises(ValueError, match=missing_col):
        _ = proc.donors_df


@pytest.mark.unit
def test_donors_df_invalid_coordinates(monkeypatch):
    """Test that donors_df raises ValueError if coordinates are out of bounds."""
    df = pd.DataFrame(
        {
            "gage_id": ["G1"],
            "longitude": [200.0],  # invalid
            "latitude": [95.0],  # invalid
        }
    )
    monkeypatch.setattr(PRP, "donor_gages", property(lambda self: df))

    proc = PRP.__new__(PRP)
    proc.config = SimpleNamespace(
        general=SimpleNamespace(
            donor_gage_file="dummy.csv",
            id_col=SimpleNamespace(gage="gage_id", divide="div_id"),
        )
    )

    with pytest.raises(ValueError, match="invalid coordinates"):
        _ = proc.donors_df


@pytest.mark.integration
def test_parreg_pipeline_smoke(
    processor,
    minimal_donors_df,
    gage_crosswalk_df,
    monkeypatch,
):
    """Smoke test for a small piece of the parameter regionalization pipeline.

    Avoids reading real files by monkeypatching donors, crosswalks, and hydrofabric.
    """
    # Monkeypatch properties to bypass file I/O
    monkeypatch.setattr(PRP, "donors_df", property(lambda self: minimal_donors_df))
    monkeypatch.setattr(PRP, "donor_gages", property(lambda self: minimal_donors_df))
    monkeypatch.setattr(PRP, "gage_crosswalk", property(lambda self: gage_crosswalk_df))
    monkeypatch.setattr(PRP, "donor_basins_all", property(lambda self: ["G1", "G2"]))

    # Run a small piece of the pipeline
    donors = processor.donors_df
    donor_df = processor.get_initial_donor_df("01")

    # Assertions: contracts, not internals
    assert not donors.empty
    assert set(donor_df.columns) >= {"div_id", "gage_id"}
    assert len(donor_df) == 2
    assert donor_df["gage_id"].tolist() == ["G1", "G2"]
