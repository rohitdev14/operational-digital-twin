"""Day 1 knowledge-layer query demo.

No graph database is required at this stage. The YAML files remain the source
of truth and this module exposes a few deterministic engineering queries.
"""

from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parents[1]


def load_model():
    assets_doc = yaml.safe_load((ROOT / "knowledge/assets.yaml").read_text())
    rel_doc = yaml.safe_load((ROOT / "knowledge/relationships.yaml").read_text())
    assets = {a["id"]: a for a in assets_doc["assets"]}
    return assets, rel_doc["relationships"]


def relationships_for(asset_id):
    _, relationships = load_model()
    return [
        r for r in relationships
        if r["subject"] == asset_id or r["object"] == asset_id
    ]


def instruments_monitoring(asset_id):
    assets, relationships = load_model()
    predicates = {
        "monitors_vibration_of",
        "measures_suction_pressure_of",
        "measures_discharge_pressure_of",
        "measures_energy_of",
    }
    ids = [
        r["subject"] for r in relationships
        if r["object"] == asset_id and r["predicate"] in predicates
    ]
    return [assets[i] for i in ids]


def pumps_discharge_to(header_id="DH-001"):
    assets, relationships = load_model()
    # Trace each discharge isolation valve back through NRV to its pump.
    pumps = []
    discharge_valves = {
        r["subject"] for r in relationships
        if r["predicate"] == "discharges_to" and r["object"] == header_id
    }
    for valve in discharge_valves:
        nrvs = [
            r["subject"] for r in relationships
            if r["predicate"] == "feeds" and r["object"] == valve
        ]
        for nrv in nrvs:
            candidates = [
                r["subject"] for r in relationships
                if r["predicate"] == "discharges_through" and r["object"] == nrv
            ]
            pumps.extend(p for p in candidates if assets[p]["type"] == "pump_package")
    return [assets[p] for p in sorted(set(pumps))]


def upstream_path(asset_id, max_hops=10):
    """Return one deterministic upstream path using physical-flow predicates."""
    assets, relationships = load_model()
    reverse = {}
    for r in relationships:
        if r["predicate"] in {"feeds", "discharges_through", "discharges_to"}:
            reverse.setdefault(r["object"], []).append(r["subject"])

    path, current, seen = [], asset_id, {asset_id}
    for _ in range(max_hops):
        parents = sorted(reverse.get(current, []))
        if not parents:
            break
        current = parents[0]
        if current in seen:
            break
        seen.add(current)
        path.append(assets[current])
    return path


if __name__ == "__main__":
    print("What monitors P-101?")
    print("  " + ", ".join(a["id"] for a in instruments_monitoring("P-101")))

    print("\nWhat is upstream of P-101?")
    print("  " + " <- ".join(["P-101"] + [a["id"] for a in upstream_path("P-101")]))

    print("\nWhich pumps discharge into DH-001?")
    print("  " + ", ".join(a["id"] for a in pumps_discharge_to("DH-001")))
