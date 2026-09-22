from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
ASSETS = (ROOT / "knowledge/assets.yaml").read_text()
REL = (ROOT / "knowledge/relationships.yaml").read_text()

def asset_ids():
    return set(re.findall(r"id:\s*([^,}\n]+)", ASSETS))

def test_five_pump_packages_exist():
    ids = asset_ids()
    assert all(f"P-{n}" in ids for n in range(101, 106))

def test_each_pump_is_30_kw():
    for n in range(101, 106):
        assert re.search(rf"id:\s*P-{n}.*motor_kw:\s*30", ASSETS)

def test_each_pump_discharges_to_common_header():
    for n in range(101, 106):
        assert f"subject: XV-{n}-D, predicate: discharges_to, object: DH-001" in REL

def test_each_strainer_has_dp_measurement():
    for n in range(101, 106):
        assert f"subject: DPT-{n}, predicate: measures_dp_across, object: ST-{n}" in REL

def test_each_pump_has_vibration_and_energy_relationships():
    for n in range(101, 106):
        assert f"subject: VT-{n}, predicate: monitors_vibration_of, object: P-{n}" in REL
        assert f"subject: EM-{n}, predicate: measures_energy_of, object: P-{n}" in REL
