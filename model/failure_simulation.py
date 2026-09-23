"""Day-2 resilience/failure simulation with energy-accounting prerequisites.

Conceptual synthetic data only. Energy values are model-derived, not vendor data.
"""
import csv
from pathlib import Path
from .capacity import BASELINE_FLOW_M3H, SETPOINT_HEAD_M, capacity_point
from .physics import PumpModel

PUMPS=[f"P-{n}" for n in range(101,106)]
MOTOR_EFFICIENCY=0.93
VSD_EFFICIENCY=0.97
DT_HOURS=1.0/3600.0

def scenario_at(t):
    if t < 120: return "S0_HEALTHY", []
    if t < 240: return "S1_P101_BEARING_VSD_TRIP", ["P-101"]
    if t < 360: return "S2_P102_CABLE_TRIP", ["P-101","P-102"]
    return "S3_THIRD_PUMP_TRIP_CAPACITY_DEFICIT", ["P-101","P-102","P-103"]

def failure_cause(pump,t):
    if pump=="P-101" and t>=120: return "bearing_failure_vsd_overload_trip"
    if pump=="P-102" and t>=240: return "cable_electrical_fault_trip"
    if pump=="P-103" and t>=360: return "generic_trip_for_resilience_test"
    return ""

def simulate_failures(duration_s=480):
    pump=PumpModel(); rows=[]; cumulative_kwh=0.0; cumulative_volume_m3=0.0
    for t in range(duration_s):
        scenario,failed=scenario_at(t); available=5-len(failed)
        cap=capacity_point(available)
        speed=min(cap.required_speed_pu,pump.max_speed_pu)
        maxflow=available*pump.flow_at_head_m3h(SETPOINT_HEAD_M,speed)
        delivered=min(BASELINE_FLOW_M3H,maxflow)
        head=SETPOINT_HEAD_M if cap.achievable else pump.head_m(BASELINE_FLOW_M3H/available,speed)
        deficit=BASELINE_FLOW_M3H-delivered
        q_each=delivered/available
        shaft_each=pump.shaft_power_kw(q_each,head,speed)
        electrical_each=shaft_each/(MOTOR_EFFICIENCY*VSD_EFFICIENCY)
        system_electrical_kw=electrical_each*available
        step_kwh=system_electrical_kw*DT_HOURS
        step_volume_m3=delivered/3600.0
        cumulative_kwh+=step_kwh; cumulative_volume_m3+=step_volume_m3
        sec=system_electrical_kw/delivered if delivered>0 else 0.0
        cumulative_sec=cumulative_kwh/cumulative_volume_m3 if cumulative_volume_m3>0 else 0.0
        common={"t_s":t,"scenario":scenario,"demand_m3h":BASELINE_FLOW_M3H,
                "delivered_flow_m3h":round(delivered,3),"flow_deficit_m3h":round(deficit,3),
                "header_head_m":round(head,3),"setpoint_head_m":SETPOINT_HEAD_M,
                "common_speed_ref_pu":round(speed,5),"pumps_available":available,
                "baseline_sustained":cap.achievable,
                "system_electrical_power_kw":round(system_electrical_kw,3),
                "step_energy_kwh":round(step_kwh,6),
                "cumulative_energy_kwh":round(cumulative_kwh,6),
                "step_delivered_volume_m3":round(step_volume_m3,6),
                "cumulative_delivered_volume_m3":round(cumulative_volume_m3,6),
                "specific_energy_kwh_m3":round(sec,6),
                "cumulative_specific_energy_kwh_m3":round(cumulative_sec,6)}
        for pid in PUMPS:
            tripped=pid in failed; q=0.0 if tripped else q_each
            shaft=0.0 if tripped else shaft_each
            electrical=0.0 if tripped else electrical_each
            vibration=0.0 if tripped else 2.0
            current_index=0.0 if tripped else electrical/pump.motor_kw
            trip_code=""
            if pid=="P-101" and 90<=t<120:
                vibration=2.0+0.10*(t-89); current_index=min(1.15,current_index+0.012*(t-89))
            if pid=="P-101" and t>=120: trip_code="VSD_OVERLOAD"
            if pid=="P-102" and 235<=t<240: current_index=min(1.3,current_index+0.18*(t-234))
            if pid=="P-102" and t>=240: trip_code="ELECTRICAL_FAULT"
            if pid=="P-103" and t>=360: trip_code="RESILIENCE_TEST_TRIP"
            row=dict(common)
            row.update({"asset_id":pid,"status":"TRIPPED" if tripped else "RUNNING",
                        "failure_cause":failure_cause(pid,t),"trip_code":trip_code,
                        "pump_flow_m3h":round(q,3),"shaft_power_kw":round(shaft,3),
                        "electrical_input_power_kw":round(electrical,3),
                        "motor_efficiency_assumed":MOTOR_EFFICIENCY,
                        "vsd_efficiency_assumed":VSD_EFFICIENCY,
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
    out,rows=write_csv(); print(f"Generated {len(rows)} asset telemetry rows -> {out}")
