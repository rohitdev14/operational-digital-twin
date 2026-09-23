from model.simulation import simulate

def test_simulation_generates_one_row_per_second():
    assert len(simulate(120))==120

def test_controller_stages_multiple_pumps_for_high_demand():
    assert max(r["pumps_running"] for r in simulate())>=3

def test_speed_remains_within_vsd_limits():
    assert all(0.45<=r["speed_pu"]<=1.0 for r in simulate())

def test_energy_accumulates_monotonically():
    e=[r["energy_kwh"] for r in simulate()]; assert all(b>=a for a,b in zip(e,e[1:]))

def test_pressure_recovers_near_setpoint_during_steady_period():
    r=simulate(); s=r[170:180]; mean=sum(x["header_head_m"] for x in s)/len(s); assert abs(mean-38.0)<2.0

def test_controller_destages_after_demand_falls():
    r=simulate(); assert r[-1]["pumps_running"]<max(x["pumps_running"] for x in r)
