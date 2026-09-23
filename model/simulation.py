"""Closed-loop pressure-control simulation with pump staging for Day 2."""
from dataclasses import dataclass
from .physics import PumpModel, parallel_header_head_m

@dataclass
class ControlConfig:
    setpoint_head_m: float = 38.0
    kp: float = 0.006
    ki: float = 0.0012
    stage_speed_pu: float = 0.95
    destage_speed_pu: float = 0.86
    stage_delay_s: int = 10
    destage_delay_s: int = 20
    max_pumps: int = 5

def demand_profile(t_s: int) -> float:
    if t_s < 60: return 140.0
    if t_s < 120: return 300.0
    if t_s < 180: return 500.0
    if t_s < 240: return 720.0
    if t_s < 300: return 430.0
    return 220.0

def simulate(duration_s: int = 360, dt_s: float = 1.0):
    pump=PumpModel(); cfg=ControlConfig(); speed=0.85; pumps_running=1
    integral=0.0; high_timer=low_timer=0.0; energy_kwh=0.0; rows=[]
    for step in range(int(duration_s/dt_s)):
        t_s=int(step*dt_s); demand=demand_profile(t_s)
        head=parallel_header_head_m(pump,demand,pumps_running,speed)
        error=cfg.setpoint_head_m-head
        integral=max(-100.0,min(100.0,integral+error*dt_s))
        speed += cfg.kp*error + cfg.ki*integral*dt_s
        speed=max(pump.min_speed_pu,min(pump.max_speed_pu,speed))

        if speed>=cfg.stage_speed_pu and head<cfg.setpoint_head_m-1.0 and pumps_running<cfg.max_pumps:
            high_timer += dt_s
        else: high_timer=0.0
        if high_timer>=cfg.stage_delay_s:
            pumps_running+=1; high_timer=0.0; integral=0.0

        if speed<=cfg.destage_speed_pu and pumps_running>1:
            low_timer += dt_s
        else: low_timer=0.0
        if low_timer>=cfg.destage_delay_s:
            pumps_running-=1; low_timer=0.0; integral=0.0

        head=parallel_header_head_m(pump,demand,pumps_running,speed)
        per_pump_flow=demand/pumps_running
        per_pump_kw=pump.shaft_power_kw(per_pump_flow,head,speed)
        total_kw=per_pump_kw*pumps_running
        energy_kwh += total_kw*dt_s/3600.0
        rows.append({"t_s":t_s,"demand_m3h":round(demand,3),"header_head_m":round(head,3),
          "setpoint_head_m":cfg.setpoint_head_m,"speed_pu":round(speed,4),
          "pumps_running":pumps_running,"per_pump_flow_m3h":round(per_pump_flow,3),
          "total_power_kw":round(total_kw,3),"energy_kwh":round(energy_kwh,5)})
    return rows
