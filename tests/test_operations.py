from intelligence.operations import configuration_comparison,feasible_configurations

def test_operational_comparison_respects_hydraulic_constraint():
    rows=configuration_comparison()
    assert [r["hydraulic_duty_met"] for r in rows]==[True,True,True,False]
    assert [r["pumps_available"] for r in feasible_configurations()]==[5,4,3]
    assert all(r["model_only"] for r in rows)
