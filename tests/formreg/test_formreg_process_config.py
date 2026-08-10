"""Unit and integration tests for nwm_region_mgr.formreg.process_config.FormulationRegionalizationProcessor."""

import pytest


# -------------------------------Fixtures-------------------------------
@pytest.fixture
def processor():
    """Minimal FormulationRegionalizationProcessor instance with just enough wiring to test orchestration logic."""
    from nwm_region_mgr.formreg.process_config import (
        FormulationRegionalizationProcessor,
    )

    proc = FormulationRegionalizationProcessor.__new__(
        FormulationRegionalizationProcessor
    )

    # Minimal attributes used by run_formreg_for_vpu
    proc.config = object()

    # Stub methods inherited from BaseConfigProcessor
    proc.set_vpu = lambda vpu: None
    proc.get_vpu_gdf = lambda: "fake_gdf"

    # timing_block is a context manager; stub it cheaply
    class DummyTimer:
        def __enter__(self):
            return None

        def __exit__(self, *args):
            return False

    proc.timing_block = lambda name: DummyTimer()

    return proc


# --------------------------------Unit tests---------------------------
@pytest.mark.unit
def test_run_formreg_no_formulation_file_raises(processor):
    """Missing formulation file is a hard error."""
    with pytest.raises(ValueError, match="No formulation file provided"):
        processor.run_formreg_for_vpu("01", "")


@pytest.mark.unit
def test_run_formreg_existing_file_skips(processor, tmp_path, monkeypatch):
    """If the formulation file already exists, the processor must short-circuit and NOT call downstream logic."""
    formulation_file = tmp_path / "formulation.csv"
    formulation_file.touch()

    # If these are called, the test should fail
    monkeypatch.setattr(
        "nwm_region_mgr.formreg.summary_score.compute_summary_score",
        lambda *a, **k: (_ for _ in ()).throw(
            AssertionError("compute_summary_score should not be called")
        ),
    )

    monkeypatch.setattr(
        "nwm_region_mgr.formreg.select_formulation.select_formulation",
        lambda *a, **k: (_ for _ in ()).throw(
            AssertionError("select_formulation should not be called")
        ),
    )

    processor.run_formreg_for_vpu("01", str(formulation_file))


# --------------------------------Integration tests---------------------------
@pytest.mark.integration
def test_run_formreg_happy_path_calls_components(processor, monkeypatch):
    """Lightweight integration test to ensure orchestration works and correct calls are made."""
    dummy_score = object()

    called = {
        "compute": False,
        "select": False,
    }

    def fake_compute_summary_score(config, vpu):
        assert config is processor.config
        assert vpu == "01"
        called["compute"] = True
        return dummy_score

    def fake_select_formulation(config, vpu, score, gdf):
        assert config is processor.config
        assert vpu == "01"
        assert score is dummy_score
        assert gdf == "fake_gdf"
        called["select"] = True

    monkeypatch.setattr(
        "nwm_region_mgr.formreg.summary_score.compute_summary_score",
        fake_compute_summary_score,
    )

    monkeypatch.setattr(
        "nwm_region_mgr.formreg.select_formulation.select_formulation",
        fake_select_formulation,
    )

    processor.run_formreg_for_vpu("01", "nonexistent_formulation.csv")

    assert called["compute"] is True
    assert called["select"] is True
