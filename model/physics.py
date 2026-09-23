"""First-principles hydraulic model for the Day-2 reference system.

All values are conceptual/public engineering assumptions, not vendor data.
Flow is m3/h, head is m water column, speed is per-unit of nominal speed.
"""
from dataclasses import dataclass
from math import sqrt

RHO_WATER = 998.0
G = 9.80665

@dataclass(frozen=True)
class PumpModel:
    shutoff_head_m: float = 55.0
    rated_flow_m3h: float = 180.0
    rated_head_m: float = 42.0
    motor_kw: float = 30.0
    min_speed_pu: float = 0.45
    max_speed_pu: float = 1.00

    @property
    def curve_k(self) -> float:
        return (self.shutoff_head_m - self.rated_head_m) / self.rated_flow_m3h**2

    def head_m(self, flow_m3h: float, speed_pu: float = 1.0) -> float:
        speed = max(0.0, speed_pu)
        return max(0.0, speed**2 * self.shutoff_head_m - self.curve_k * flow_m3h**2)

    def flow_at_head_m3h(self, head_m: float, speed_pu: float = 1.0) -> float:
        available = speed_pu**2 * self.shutoff_head_m - head_m
        return sqrt(max(0.0, available) / self.curve_k)

    def efficiency(self, flow_m3h: float, speed_pu: float = 1.0) -> float:
        if speed_pu <= 0:
            return 0.0
        equivalent_nominal_flow = flow_m3h / speed_pu
        deviation = (equivalent_nominal_flow - self.rated_flow_m3h) / self.rated_flow_m3h
        return max(0.55, min(0.80, 0.80 - 0.22 * deviation**2))

    def shaft_power_kw(self, flow_m3h: float, head_m: float, speed_pu: float = 1.0) -> float:
        eta = self.efficiency(flow_m3h, speed_pu)
        if eta <= 0 or flow_m3h <= 0 or head_m <= 0:
            return 0.0
        q_m3s = flow_m3h / 3600.0
        return RHO_WATER * G * q_m3s * head_m / eta / 1000.0

def parallel_header_head_m(pump: PumpModel, total_flow_m3h: float, pumps_running: int, speed_pu: float) -> float:
    if pumps_running < 1:
        return 0.0
    return pump.head_m(total_flow_m3h / pumps_running, speed_pu)
