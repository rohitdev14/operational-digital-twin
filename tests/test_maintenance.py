from intelligence.maintenance import verification_plan

def test_no_evidence_means_no_maintenance_claim():
    p=verification_plan({"asset_id":"P-103","hypotheses":[]})
    assert p["status"]=="insufficient_evidence"
    assert p["checks"]==[]
