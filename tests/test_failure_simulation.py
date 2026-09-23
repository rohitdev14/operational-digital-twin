from model.failure_simulation import simulate_failures

def at(rows,t,p="P-105"):
    return next(x for x in rows if x["t_s"]==t and x["asset_id"]==p)

def test_five_and_four_and_three_pumps_sustain_baseline():
    r=simulate_failures()
    assert at(r,0)["baseline_sustained"]
    assert at(r,120)["baseline_sustained"]
    assert at(r,240)["baseline_sustained"]

def test_two_pumps_cannot_sustain_baseline():
    r=simulate_failures(); x=at(r,360)
    assert not x["baseline_sustained"]
    assert x["flow_deficit_m3h"] > 0
    assert x["header_head_m"] < x["setpoint_head_m"]

def test_bearing_failure_has_vibration_precursor_and_overload_trip():
    r=simulate_failures()
    assert at(r,119,"P-101")["vibration_mm_s_rms"] > at(r,89,"P-101")["vibration_mm_s_rms"]
    assert at(r,120,"P-101")["trip_code"]=="VSD_OVERLOAD"

def test_cable_fault_has_no_vibration_precursor():
    r=simulate_failures()
    assert at(r,239,"P-102")["vibration_mm_s_rms"]==2.0
    assert at(r,240,"P-102")["trip_code"]=="ELECTRICAL_FAULT"

def test_trip_causal_histories_are_distinct():
    r=simulate_failures()
    assert at(r,120,"P-101")["failure_cause"] != at(r,240,"P-102")["failure_cause"]


def test_energy_accounting_is_positive_and_cumulative():
    r=simulate_failures()
    a=at(r,0); b=at(r,479)
    assert a["system_electrical_power_kw"] > 0
    assert b["cumulative_energy_kwh"] > a["cumulative_energy_kwh"]
    assert b["cumulative_delivered_volume_m3"] > a["cumulative_delivered_volume_m3"]

def test_specific_energy_is_computable_for_each_operating_state():
    r=simulate_failures()
    for t in (0,120,240,360):
        x=at(r,t)
        assert x["specific_energy_kwh_m3"] > 0

def test_tripped_pump_has_zero_electrical_input_power():
    r=simulate_failures()
    assert at(r,120,"P-101")["electrical_input_power_kw"] == 0
    assert at(r,240,"P-102")["electrical_input_power_kw"] == 0
