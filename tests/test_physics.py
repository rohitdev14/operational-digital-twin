import pytest
from model.physics import PumpModel, parallel_header_head_m

def test_rated_point_matches_assumption():
    assert PumpModel().head_m(180.0,1.0)==pytest.approx(42.0)

def test_affinity_law_shutoff_head_scales_with_speed_squared():
    p=PumpModel(); assert p.head_m(0.0,0.8)==pytest.approx(0.8**2*p.shutoff_head_m)

def test_parallel_pumps_share_flow_at_common_head():
    p=PumpModel(); assert parallel_header_head_m(p,360.0,2,1.0)==pytest.approx(p.head_m(180.0,1.0))

def test_power_is_positive_and_below_motor_rating_at_rated_point():
    p=PumpModel(); power=p.shaft_power_kw(180.0,42.0,1.0); assert 0<power<p.motor_kw
