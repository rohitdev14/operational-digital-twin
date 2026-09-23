"""Day-2 resilience/failure simulation.

Conceptual synthetic data only. All five healthy pumps run together at the
frozen 500 m3/h, 38 mH2O baseline. Failures remove pumps sequentially.
"""
import csv
from pathlib import Path
from .capacity import BASELINE_FLOW_M3H, SETPOINT_HEAD_M, capacity_point
from .physics import PumpModel

PUMPS=[f"P-{n}" for n in range(101,106)]

def scenario_at(t):
    if t < 120:
        return "S0_HEALTHY", []
    if t < 240:
        return "S1_P101_BEARING_VSD_TRIP", ["P-101"]
    if t < 360:
        return "S2_P102_CABLE_TRIP", ["P-101","P-102"]
    return "S3_THIRD_PUMP_TRIP_CAPACITY_DEFICIT", ["P-101","P-102","P-103"]

def failure_cause(pump,t):
    if pump=="P-101" and t>=120: return "bearing_failure_vsd_overload_trip"
    if pump=="P-102" and t>=240: return "cable_electrical_fault_trip"
    if pump=="P-103" and t>=360: return "generic_trip_for_resilience_test"
    return ""

def simulate_failures(duration_s=480):
    pump=PumpModel(); rows=[]
    for t in range(duration_s):
        scenario,failed=scenario_at(t); available=5-len(failed)
        cap=capacity_point(available)
        speed=min(cap.required_speed_pu,pump.max_speed_pu)
        maxflow=available*pump.flow_at_head_m3h(SETPOINT_HEAD_M,speed)
        delivered=min(BASELINE_FLOW_M3H,maxflow)
        # If capacity is insufficient, hold demanded flow as the process requirement
        # and report the maximum head the available pumps can develop at that flow.
        head=SETPOINT_HEAD_M if cap.achievable else pump.head_m(BASELINE_FLOW_M3H/available,speed)
        deficit=BASELINE_FLOW_M3H-delivered
        common={"t_s":t,"scenario":scenario,"demand_m3h":BASELINE_FLOW_M3H,
                "delivered_flow_m3h":round(delivered,3),"flow_deficit_m3h":round(deficit,3),
                "header_head_m":round(head,3),"setpoint_head_m":SETPOINT_HEAD_M,
                "common_speed_ref_pu":round(speed,5),"pumps_available":available,
                "baseline_sustained":cap.achievable}
        for pid in PUMPS:
            tripped=pid in failed
            q=0.0 if tripped else delivered/available
            power=0.0 if tripped else pump.shaft_power_kw(q,head,speed)
            # Synthetic evidence signals distinguish causal histories.
            vibration=0.0 if tripped else 2.0
            current_index=0.0 if tripped else power/pump.motor_kw
            trip_code=""
            if pid=="P-101" and 90<=t<120:
                vibration=2.0 + 0.10*(t-89)
                current_index=min(1.15,current_index+0.012*(t-89))
            if pid=="P-101" and t>=120: trip_code="VSD_OVERLOAD"
            if pid=="P-102" and 235<=t<240:
                current_index=min(1.3,current_index+0.18*(t-234))
            if pid=="P-102" and t>=240: trip_code="ELECTRICAL_FAULT"
            if pid=="P-103" and t>=360: trip_code="RESILIENCE_TEST_TRIP"
            row=dict(common)
            row.update({"asset_id":pid,"status":"TRIPPED" if tripped else "RUNNING",
                        "failure_cause":failure_cause(pid,t),"trip_code":trip_code,
                        "pump_flow_m3h":round(q,3),"shaft_power_kw":round(power,3),
                        "vibration_mm_s_rms":round(vibration,3),
                        "current_load_index":round(current_index,4)})
            rows.append(row)
    return rows

def write_csv(path="artifacts/day2_failure_telemetry.csv"):
    rows=simulate_failures(); out=Path(path); out.parent.mkdir(parents=True,exist_ok=True)
    with out.open("w",newline="") as f:
        w=csv.DictWriter(f,fieldnames=rows[0].keys()); w.writeheader(); w.writerows(rows)
    return out,rows

if __name__=="__main__":
    out,rows=write_csv()
    print(f"Generated {len(rows)} asset telemetry rows -> {out}")
    for t in (0,120,240,360):
        r=next(x for x in rows if x["t_s"]==t and x["asset_id"]=="P-105")
        print(t,r["scenario"],r["pumps_available"],r["common_speed_ref_pu"],
              r["delivered_flow_m3h"],r["header_head_m"],r["baseline_sustained"])
