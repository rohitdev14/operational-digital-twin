import pytest
from model.capacity import capacity_point

@pytest.mark.parametrize("n", [5,4,3])
def test_baseline_is_sustainable_with_three_or_more_pumps(n):
    assert capacity_point(n).achievable

def test_baseline_is_not_sustainable_with_two_pumps():
    p=capacity_point(2)
    assert not p.achievable
    assert p.required_speed_pu > 1.0

def test_capacity_margin_declines_as_pumps_are_lost():
    margins=[capacity_point(n).flow_margin_m3h for n in (5,4,3,2)]
    assert margins == sorted(margins, reverse=True)

def test_three_pumps_are_close_to_full_speed():
    assert capacity_point(3).required_speed_pu == pytest.approx(0.945279, rel=1e-4)
