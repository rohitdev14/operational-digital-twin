from knowledge.query import instruments_monitoring, pumps_discharge_to, upstream_path


def ids(items):
    return {item["id"] for item in items}


def test_p101_monitoring_instruments():
    assert ids(instruments_monitoring("P-101")) == {
        "PS-101", "PD-101", "VT-101", "EM-101"
    }


def test_p101_upstream_path():
    path = [item["id"] for item in upstream_path("P-101")]
    assert path[:4] == ["ST-101", "XV-101-S", "SH-001", "TK-001"]


def test_all_five_pumps_discharge_to_header():
    assert ids(pumps_discharge_to("DH-001")) == {
        "P-101", "P-102", "P-103", "P-104", "P-105"
    }
