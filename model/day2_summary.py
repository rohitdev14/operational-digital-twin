"""Create a deterministic Day-2 scenario summary. No diagnosis or Day-3 reasoning."""
import csv
from pathlib import Path
from .failure_simulation import simulate_failures

CHECKPOINTS=[0,119,120,239,240,359,360,479]

def checkpoint_rows():
    rows=simulate_failures()
    result=[]
    for t in CHECKPOINTS:
        group=[r for r in rows if r["t_s"]==t]
        ref=next(r for r in group if r["asset_id"]=="P-105")
        result.append({
            "t_s":t,
            "scenario":ref["scenario"],
            "pumps_available":ref["pumps_available"],
            "speed_ref_pct":round(ref["common_speed_ref_pu"]*100,2),
            "delivered_flow_m3h":ref["delivered_flow_m3h"],
            "header_head_m":ref["header_head_m"],
            "flow_deficit_m3h":ref["flow_deficit_m3h"],
            "baseline_sustained":ref["baseline_sustained"],
            "tripped_assets":";".join(r["asset_id"] for r in group if r["status"]=="TRIPPED"),
        })
    return result

def write_summary(path="artifacts/day2_scenario_summary.csv"):
    data=checkpoint_rows(); out=Path(path); out.parent.mkdir(parents=True,exist_ok=True)
    with out.open("w",newline="") as f:
        w=csv.DictWriter(f,fieldnames=data[0].keys()); w.writeheader(); w.writerows(data)
    return out

if __name__=="__main__":
    out=write_summary()
    print(f"Wrote {out}")
    for r in checkpoint_rows(): print(r)
