from model.failure_simulation import simulate_failures
from intelligence.evidence import event_evidence
from intelligence.diagnosis import diagnose

def test_p101_and_p102_take_different_diagnostic_paths():
    rows=simulate_failures()
    d1=diagnose(event_evidence(rows,"P-101",120))
    d2=diagnose(event_evidence(rows,"P-102",240))
    assert d1["hypotheses"][0]["hypothesis"]=="mechanical_load_or_bearing_degradation"
    assert d2["hypotheses"][0]["hypothesis"]=="electrical_supply_or_cable_fault"

def test_third_trip_reports_capacity_consequence_without_inventing_cause():
    d=diagnose(event_evidence(simulate_failures(),"P-103",360))
    assert d["system_consequence"]["baseline_sustained"] is False
    assert d["system_consequence"]["flow_deficit_m3h"]>0
    assert d["hypotheses"]==[]
