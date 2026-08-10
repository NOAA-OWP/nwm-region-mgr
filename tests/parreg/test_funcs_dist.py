"""Unit and integration tests for distance-based pairing functions (funcs_dist.py)."""

import pandas as pd
import pytest

from nwm_region_mgr.parreg.funcs_dist import (
    DistancePairer,
    GowerPairer,
    ProximityPairer,
    URFPairer,
)


# -----------------------------Fixtures----------------------------------------
@pytest.fixture
def minimal_attr_df():
    """Small attribute dataframe with donors and receivers."""
    return pd.DataFrame(
        {
            "div_id": ["d1", "d2", "r1", "r2"],
            "is_donor": [True, True, False, False],
            "snowy": [1, 0, 1, 0],
            "attr1": [0.1, 0.2, 0.15, 0.25],
            "attr2": [10, 20, 15, 30],
        }
    )


@pytest.fixture
def minimal_spatial_dist():
    """Receiver-to-donor spatial distance matrix."""
    return pd.DataFrame(
        {
            "d1": [5.0, 50.0],
            "d2": [20.0, 10.0],
        },
        index=["r1", "r2"],
    )


@pytest.fixture
def minimal_config():
    """Minimal config dictionary used by pairers."""
    return {
        "attrs": {"main": ["attr1", "attr2"], "base": ["attr1"]},
        "non_attr_cols": ["div_id", "is_donor", "snowy"],
        "min_spa_dist": 0,
        "max_spa_dist": 200,
        "zero_spa_dist": 10,
        "max_attr_dist": 999,
        "min_attr_dist": 0,
        "njobs": 1,
        "pca": False,
        "n_trees": 5,
        "max_depth": 3,
    }


@pytest.fixture
def dummy_pairer(minimal_attr_df, minimal_spatial_dist, minimal_config):
    """DistancePairer with injected minimal state."""
    p = DistancePairer(
        config=minimal_config,
        df_attr_all=minimal_attr_df,
        dist_spatial=minimal_spatial_dist,
    )
    return p


# ----------------------------Unit tests (pure logic)--------------------------------
@pytest.mark.unit
def test_get_receivers_to_process_empty_processed(dummy_pairer):
    """If no receivers have been processed yet, all receivers should be returned."""
    out = dummy_pairer.get_receivers_to_process(pd.DataFrame())
    assert set(out) == {"r1", "r2"}


@pytest.mark.unit
def test_get_receivers_to_process_excludes_processed(dummy_pairer):
    """If some receivers have been processed, they should be excluded."""
    processed = pd.DataFrame({"div_id": ["r1"]})
    out = dummy_pairer.get_receivers_to_process(processed)
    assert out == ["r2"]


@pytest.mark.unit
def test_get_donors_in_same_snow_category(dummy_pairer, minimal_attr_df):
    """Donors in the same snowy category as the receiver are returned."""
    donors = dummy_pairer.get_donors_in_receivers_snow_category(minimal_attr_df, "r1")
    assert donors == ["d1"]


@pytest.mark.unit
def test_update_columns_index_rounding(dummy_pairer):
    """Test that update_columns_index correctly updates DataFrame indices and columns."""
    df = pd.DataFrame([[0.12345, 1.98765]])
    out = dummy_pairer.update_columns_index(["d1", "d2"], ["r1"], df)
    assert list(out.columns) == ["d1", "d2"]
    assert list(out.index) == ["r1"]
    assert out.iloc[0, 0] == pytest.approx(0.123, rel=1e-3)
    assert out.iloc[0, 1] == pytest.approx(1.988, rel=1e-3)


@pytest.mark.unit
def test_get_receivers_to_process_for_round(dummy_pairer):
    """Test that get_receivers_to_process_for_round returns the correct receivers."""
    recs = ["r1", "r2"]
    processed = ["r1"]
    round_recs = ["r1", "r2"]
    out = dummy_pairer.get_receivers_to_process_for_round(recs, processed, round_recs)
    assert out == ["r2"]


# -------------------------Integration tests — component interaction--------------------------
@pytest.mark.integration
def test_gower_process_shape(minimal_attr_df, minimal_config):
    """Test that GowerPairer.process returns correct shape."""
    p = GowerPairer.model_construct(
        config=minimal_config,
        df_attr_all=minimal_attr_df,
    )

    donors = ["d1", "d2"]
    receivers = ["r1", "r2"]

    df_round = minimal_attr_df[minimal_config["non_attr_cols"] + ["attr1", "attr2"]]

    out = p.process(df_round, donors, receivers)
    assert out.shape == (len(receivers), len(donors))


@pytest.mark.integration
def test_urf_process_shape(minimal_attr_df, minimal_config):
    """Test that URFPairer.process returns correct shape."""
    p = URFPairer.model_construct(
        config=minimal_config,
        df_attr_all=minimal_attr_df,
    )

    donors = ["d1", "d2"]
    receivers = ["r1", "r2"]

    df_round = minimal_attr_df[minimal_config["non_attr_cols"] + ["attr1", "attr2"]]

    out = p.process(df_round, donors, receivers)
    assert out.shape == (len(receivers), len(donors))
    assert list(out.index) == receivers
    assert list(out.columns) == donors


# -------------------------Functional tests — end-to-end pairing--------------------------
@pytest.mark.functional
def test_proximity_pairer_end_to_end(
    minimal_attr_df, minimal_spatial_dist, minimal_config, monkeypatch
):
    """End-to-end proximity pairing with assign_donors mocked."""
    from nwm_region_mgr.parreg import utils_algo

    def fake_assign(
        run, donors, receivers, config, dist_attr, dist_spatial, *_args, **_kwargs
    ):
        rows = []
        # for each receiver, assign the nearest donor based on dist_spatial
        for r in receivers:
            nearest_donor = dist_spatial.loc[r].idxmin()
            rows.append({"div_id": r, "donor_id": nearest_donor})
        return pd.DataFrame(rows)

    monkeypatch.setattr(utils_algo, "assign_donors", fake_assign)

    p = ProximityPairer.model_construct(
        config=minimal_config,
        df_attr_all=minimal_attr_df,
        dist_spatial=minimal_spatial_dist,
    )

    out = p.pair()
    assert set(out["div_id"]) == {"r1", "r2"}
    assert "donor_id" in out.columns
    assert out.loc[out["div_id"] == "r1", "donor_id"].iloc[0] == "d1"
    assert out.loc[out["div_id"] == "r2", "donor_id"].iloc[0] == "d2"
