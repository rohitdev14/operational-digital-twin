from model.day2_summary import checkpoint_rows

def test_day2_summary_has_frozen_checkpoints():
    assert [r["t_s"] for r in checkpoint_rows()] == [0,119,120,239,240,359,360,479]

def test_capacity_deficit_only_after_third_trip_in_summary():
    rows=checkpoint_rows()
    assert all(r["baseline_sustained"] for r in rows if r["t_s"] < 360)
    assert all(not r["baseline_sustained"] for r in rows if r["t_s"] >= 360)

def test_summary_records_progressive_loss_of_assets():
    by_t={r["t_s"]:r for r in checkpoint_rows()}
    assert by_t[0]["tripped_assets"]==""
    assert by_t[120]["tripped_assets"]=="P-101"
    assert by_t[240]["tripped_assets"]=="P-101;P-102"
    assert by_t[360]["tripped_assets"]=="P-101;P-102;P-103"
