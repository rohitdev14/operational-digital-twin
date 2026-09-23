"""Capacity/resilience calculations for the frozen Day-2 baseline.

Baseline demand: 500 m3/h
Header pressure target: 38 mH2O
All available pumps receive a common speed reference.
"""
from dataclasses import dataclass
from math import sqrt
from .physics import PumpModel

BASELINE_FLOW_M3H = 500.0
SETPOINT_HEAD_M = 38.0

@dataclass(frozen=True)
class CapacityPoint:
    pumps_available: int
    required_flow_per_pump_m3h: float
    required_speed_pu: float
    achievable: bool
    max_total_flow_at_setpoint_m3h: float
    flow_margin_m3h: float
    shaft_power_per_pump_kw: float
    total_shaft_power_kw: float
    motor_overload: bool

def required_speed(pump: PumpModel, flow_per_pump_m3h: float, head_m: float) -> float:
    return sqrt((head_m + pump.curve_k * flow_per_pump_m3h**2) / pump.shutoff_head_m)

def max_flow_per_pump_at_head(pump: PumpModel, head_m: float) -> float:
    return pump.flow_at_head_m3h(head_m, pump.max_speed_pu)

def capacity_point(pumps_available: int, demand_m3h: float = BASELINE_FLOW_M3H,
                   setpoint_head_m: float = SETPOINT_HEAD_M) -> CapacityPoint:
    pump = PumpModel()
    q_each = demand_m3h / pumps_available
    speed = required_speed(pump, q_each, setpoint_head_m)
    max_total = pumps_available * max_flow_per_pump_at_head(pump, setpoint_head_m)
    power_each = pump.shaft_power_kw(q_each, setpoint_head_m, min(speed, pump.max_speed_pu))
    motor_overload = power_each > pump.motor_kw
    achievable = speed <= pump.max_speed_pu and not motor_overload
    return CapacityPoint(
        pumps_available, q_each, speed, achievable, max_total,
        max_total-demand_m3h, power_each, power_each*pumps_available, motor_overload
    )

def capacity_table():
    return [capacity_point(n) for n in range(5, 0, -1)]

if __name__ == "__main__":
    print("Baseline: 500 m3/h @ 38 mH2O")
    print("pumps | q/pump | speed | max flow @ SP | margin | shaft kW/pump | sustainable")
    for p in capacity_table():
        print(f"{p.pumps_available:5d} | {p.required_flow_per_pump_m3h:6.1f} | "
              f"{p.required_speed_pu*100:5.1f}% | {p.max_total_flow_at_setpoint_m3h:13.1f} | "
              f"{p.flow_margin_m3h:6.1f} | {p.shaft_power_per_pump_kw:13.1f} | {p.achievable}")
