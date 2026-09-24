"""Generate a compact deterministic Day-3 report from Day-2 telemetry."""
import json
from pathlib import Path
from model.failure_simulation import simulate_failures
from .evidence import event_evidence
from .diagnosis import diagnose
from .maintenance import verification_plan
from .operations import configuration_comparison

EVENTS=[("P-101",120),("P-102",240),("P-103",360)]

def build_report():
    rows=simulate_failures(start_utc=__import__("datetime").datetime(2026,1,1,tzinfo=__import__("datetime").timezone.utc))
    events=[]
    for asset,t in EVENTS:
        evidence=event_evidence(rows,asset,t)
        diagnosis=diagnose(evidence)
        events.append({"evidence":evidence,"diagnosis":diagnosis,"verification":verification_plan(diagnosis)})
    return {"day":3,"title":"Operational Intelligence","ground_truth_used_for_diagnosis":False,
            "events":events,"operating_configurations":configuration_comparison()}

def write_report(path="artifacts/day3_diagnostic_report.json"):
    out=Path(path); out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text(json.dumps(build_report(),indent=2),encoding="utf-8")
    return out

if __name__=="__main__": print(write_report())
