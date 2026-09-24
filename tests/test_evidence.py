from model.failure_simulation import simulate_failures
from intelligence.evidence import event_evidence,diagnostic_view,HIDDEN_FIELDS

def test_evidence_reconstructs_distinct_precursors():
    rows=simulate_failures()
    p101=event_evidence(rows,"P-101",120)
    p102=event_evidence(rows,"P-102",240)
    assert p101["vibration_delta_mm_s"]>1.0
    assert p102["vibration_delta_mm_s"]==0.0
    assert p101["trip_code"]=="VSD_OVERLOAD"
    assert p102["trip_code"]=="ELECTRICAL_FAULT"

def test_diagnostic_view_hides_ground_truth():
    row=simulate_failures(duration_s=121)[-5]
    view=diagnostic_view(row)
    assert not (HIDDEN_FIELDS & set(view))
