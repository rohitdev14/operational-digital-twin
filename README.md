# Operational Digital Twin

[![Digital twin validation](https://github.com/rohitdev14/operational-digital-twin/actions/workflows/validate.yml/badge.svg)](https://github.com/rohitdev14/operational-digital-twin/actions/workflows/validate.yml)

A public engineering experiment to build an operational digital twin of a centrifugal pumping system from first principles: **P&ID → engineering knowledge → physics → controls behaviour → telemetry → faults → operational intelligence**.

The reference system is an open-loop water supply system with **5 × 30 kW VSD-driven centrifugal pump packages in parallel**, supplied from a common tank and discharging into a common variable-load header.

> Educational/reference implementation using generic equipment and synthetic data. Not for plant operation, control or construction.

## Build status

| Stage | Question | Status |
|---|---|---|
| **Day 1 — Make the plant understandable** | What exists, how is it connected, and what measures it? | ✅ Complete / validated |
| **Day 2 — Make the plant behave** | How should it behave physically, how resilient is it, and what operating evidence should we capture? | ✅ Complete / validated |
| **Day 3 — Operational Intelligence** | Can the twin use evidence to explain deviations, support maintenance analysis and evaluate operating optimization? | ⏳ Not started |

---

## Day 1 — Make the plant understandable

### Objective

Turn the P&ID from a picture into structured engineering knowledge that software can query deterministically.

### Achievements

- Defined the open-loop system boundary and engineering assumptions.
- Created an editable conceptual P&ID: `docs/pid/WSP-001_PID_V0.1.drawio`.
- Assigned persistent IDs to tanks, headers, valves, instruments and all five pump packages.
- Built `knowledge/assets.yaml` as the machine-readable asset registry.
- Built `knowledge/relationships.yaml` for physical, measurement and instrumentation relationships.
- Added deterministic engineering queries in `knowledge/query.py`.
- Added automated validation of assets, topology and queries.
- Added GitHub Actions CI.

Example queries:

```text
What monitors P-101?
→ PS-101, PD-101, VT-101, EM-101

What is upstream of P-101?
→ P-101 ← ST-101 ← XV-101-S ← SH-001 ← TK-001

Which pumps discharge into DH-001?
→ P-101, P-102, P-103, P-104, P-105
```

**Day 1 outcome:** the plant has a small, explicit engineering knowledge layer. Software no longer needs to infer the topology directly from the drawing.

---

## Day 2 — Make the plant behave

### Objective

Add deterministic first-principles behaviour to the Day-1 knowledge model and create the operating/resilience/energy dataset required for later intelligence.

### Frozen baseline V0.1

- **Installed capacity:** 5 × 30 kW VSD centrifugal pump packages
- **Baseline process demand:** 500 m³/h
- **Header pressure target:** 38 mH₂O
- **Normal experiment:** all available pumps operate together
- **Control concept:** common VSD speed reference to available pumps
- **Data:** synthetic/model-derived, not vendor or plant data

### Day 2 achievements

#### 1. First-principles pump behaviour
- Implemented conceptual pump curve and parallel-pump calculations.
- Modelled VSD speed effects and required operating speed.
- Calculated shaft power and approximate pump efficiency.
- Kept model assumptions explicit and testable.

#### 2. Capacity and resilience envelope

| Pumps available | Required flow/pump | Required speed | Capacity at baseline |
|---:|---:|---:|---|
| **5** | 100.0 m³/h | 87.4% | ✅ Sustainable |
| **4** | 125.0 m³/h | 89.7% | ✅ Sustainable |
| **3** | 166.7 m³/h | 94.5% | ✅ Sustainable, reduced margin |
| **2** | 250.0 m³/h | 107.1% required | ❌ Not sustainable within 100% VSD limit |

**Key result:** the frozen baseline survives the loss of one or two pumps. A third pump loss crosses the modelled resilience boundary.

#### 3. Failure simulation
A deterministic 480-second experiment now represents:

- 5 healthy pumps at baseline.
- P-101 bearing-degradation precursor followed by a synthetic VSD-overload trip.
- Four-pump recovery.
- P-102 cable/electrical-fault precursor followed by an electrical trip.
- Three-pump recovery with reduced capacity margin.
- P-103 resilience-test trip.
- Two-pump state where baseline duty can no longer be maintained.

The bearing and electrical scenarios deliberately leave **different evidence trails even though both ultimately make a pump unavailable**.

> Failure signatures and trip mechanisms are synthetic experiment assumptions, not validated diagnostic thresholds.

#### 4. Telemetry and maintenance evidence
The Day-2 dataset records:

- demand and delivered flow
- flow deficit
- header pressure and setpoint
- common speed reference
- pump availability and run/trip state
- per-pump flow
- shaft power
- synthetic vibration
- electrical-load proxy
- trip code and injected ground-truth failure mechanism

`knowledge/events.yaml` links the injected events to affected assets, consequences and telemetry evidence windows. Raw samples remain time-series data rather than becoming individual graph nodes.

#### 5. Energy-optimization prerequisites
Day 2 also records the data needed for later optimization:

- electrical input power per pump
- total system electrical power
- incremental and cumulative energy (kWh)
- delivered water volume (m³)
- specific energy consumption (**kWh/m³**)
- cumulative specific energy
- explicit motor/VSD efficiency assumptions

For V0.1 the model uses **93% motor efficiency** and **97% VSD efficiency** as transparent conceptual assumptions. Real deployment should replace these with measured power and appropriate efficiency maps.

**No optimizer is implemented in Day 2.** Day 2 creates the reproducible evidence needed to evaluate operating configurations later.

#### 6. Validation
Automated tests validate:

- Day-1 asset and relationship integrity
- pump physics and capacity calculations
- 5/4/3-pump baseline sustainability
- 2-pump capacity deficit
- distinct bearing/electrical precursor signatures
- trip-state behaviour
- electrical power and cumulative-energy accounting
- delivered volume and specific-energy metrics
- deterministic scenario checkpoints

The validation suite runs automatically through GitHub Actions.

### Day 2 outcome

The project has progressed from a machine-readable plant description to a deterministic plant-behaviour model that can answer:

- What should the pump system do at the baseline duty?
- Can the remaining pumps sustain the required duty after equipment loss?
- How much operating margin remains?
- What telemetry preceded a known injected event?
- What power and energy were required to deliver the useful hydraulic service?

**Day 2 is complete and validated.**

---

## Day 3 — Operational Intelligence

**Status: Not started.**

Day 3 is intentionally separated from the deterministic Day-2 ground truth. Planned work will evaluate evidence-based maintenance reasoning and operational/energy optimization without allowing AI-generated recommendations to silently become control commands.


---

## Repository guide

- `docs/system-definition.md` — system boundary and assumptions
- `docs/pid/WSP-001_PID_V0.1.drawio` — editable conceptual P&ID
- `docs/day-2-capacity.md` — frozen baseline and resilience envelope
- `docs/day-2-failure-simulation.md` — failure experiment
- `docs/day-2-data-contract.md` — Day-2 data and Day-3 boundary
- `docs/day-2-energy-data.md` — energy-data prerequisites
- `knowledge/assets.yaml` — asset registry
- `knowledge/relationships.yaml` — engineering relationships
- `knowledge/events.yaml` — injected events and evidence references
- `knowledge/query.py` — deterministic engineering queries
- `model/physics.py` — pump physics
- `model/capacity.py` — resilience calculations
- `model/failure_simulation.py` — sequential failure simulation
- `model/day2_summary.py` — deterministic scenario summary
- `tests/` — automated validation
- `.github/workflows/validate.yml` — CI

## Validate locally

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python knowledge/query.py
python -m model.failure_simulation
pytest -q
```

## Engineering principles

**Physics before AI.**  
**Explicit assumptions before inference.**  
**Evidence before diagnosis.**  
**Measured/calculated/estimated/inferred values remain distinguishable.**  
**AI recommendations never silently become control commands.**
