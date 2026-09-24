"""Compare feasible operating states using hydraulic service, energy and resilience metrics."""
from model.capacity import capacity_point, BASELINE_FLOW_M3H, SETPOINT_HEAD_M
from model.physics import PumpModel
from model.failure_simulation import MOTOR_EFFICIENCY,VSD_EFFICIENCY

def configuration_comparison():
    pump=PumpModel(); result=[]
    for n in (5,4,3,2):
        c=capacity_point(n)
        speed=min(c.required_speed_pu,1.0)
        delivered=BASELINE_FLOW_M3H if c.achievable else c.max_total_flow_at_setpoint_m3h
        q_each=delivered/n
        shaft_each=pump.shaft_power_kw(q_each,SETPOINT_HEAD_M,speed)
        electrical_kw=shaft_each*n/(MOTOR_EFFICIENCY*VSD_EFFICIENCY)
        sec=electrical_kw/delivered if delivered else None
        result.append({"pumps_available":n,"required_speed_pu":round(c.required_speed_pu,5),
          "hydraulic_duty_met":c.achievable,"flow_margin_m3h":round(c.flow_margin_m3h,3),
          "estimated_electrical_kw":round(electrical_kw,3),"specific_energy_kwh_m3":round(sec,6) if sec is not None else None,
          "pumps_above_minimum_sustainable":max(0,n-3),"model_only":True})
    return result

def feasible_configurations():
    return [r for r in configuration_comparison() if r["hydraulic_duty_met"]]
