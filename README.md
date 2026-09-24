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
| **Day 3 — Operational Intelligence** | Can the twin use evidence to explain deviations, support maintenance analysis and evaluate operating optimization? | ✅ Complete / validated |

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

### Objective

Use Day-2 telemetry as observable evidence, keep injected failure labels hidden, and test whether the twin can produce transparent diagnostic hypotheses, verification checks and operational decision support.

### Where Day 3 started

At the end of Day 2 the twin could describe the plant, calculate its expected hydraulic behaviour, simulate progressive loss of pumping capacity, generate synthetic condition/energy telemetry and preserve known injected events. It could answer **what happened operationally**, but it did not independently interpret an unknown event or explain which observations supported a maintenance hypothesis.

Day 3 therefore started with a deliberate separation between **observable evidence** and **experiment ground truth**. The injected `failure_cause` and `scenario` fields remain available for validation, but are not diagnostic inputs.

### Day 3 achievements

#### 1. Evidence engine
- Added `intelligence/evidence.py` to reconstruct pre/post-event evidence windows.
- Extracts vibration/load trends, trip code, process demand and post-trip hydraulic consequence.
- Explicitly removes injected `failure_cause` and `scenario` from the diagnostic view.

#### 2. Transparent diagnostic reasoning
- Added deterministic, inspectable evidence scoring in `intelligence/diagnosis.py`.
- P-101's synthetic rising-vibration + rising-load + VSD-overload evidence follows a mechanical-load/bearing-degradation hypothesis path.
- P-102's electrical excursion + electrical-fault trip + no material vibration rise follows an electrical-supply/cable hypothesis path.
- P-103 has insufficient condition evidence for a cause diagnosis, so the engine reports the capacity consequence without inventing a cause.
- Absence of a signal by itself is not allowed to create a fault hypothesis; positive supporting evidence is required.

#### 3. Maintenance verification support
- Added `knowledge/failure_modes.yaml` and `intelligence/maintenance.py`.
- Leading hypotheses produce explicit verification checks and missing-evidence requirements rather than automatic maintenance commands.
- The output separates observed evidence, hypothesis and required engineering verification.

#### 4. Operational and energy intelligence
- Added `intelligence/operations.py` to compare 5-, 4-, 3- and 2-pump configurations.
- Comparison includes hydraulic feasibility, required speed, capacity margin, estimated electrical power, specific energy and remaining pump-count resilience.
- Configurations that cannot meet the frozen **500 m³/h @ 38 mH₂O** duty are excluded from the feasible set.
- Energy conclusions remain model-only because efficiency curves are conceptual assumptions.

#### 5. Explainability and validation
The Day-3 reasoning chain is deliberately inspectable:

`OBSERVED → DERIVED → HYPOTHESIS → SUPPORTING EVIDENCE → MISSING EVIDENCE → SYSTEM CONSEQUENCE → VERIFICATION`

Automated tests verify distinct diagnostic paths, insufficient-evidence behaviour, hydraulic feasibility and — critically — that diagnostic code does **not** consume the injected failure cause or scenario label.

`intelligence/report.py` generates a deterministic Day-3 diagnostic/operational report from the Day-2 telemetry.

### Where the three-day build ended

The repository now contains an end-to-end, deterministic operational digital-twin reference model:

`P&ID / system definition → machine-readable assets and relationships → first-principles pump behaviour → synthetic telemetry → resilience and energy calculations → event evidence → diagnostic hypotheses → engineering verification → operational comparison`

The progression is:

**Day 1 — What is the plant?**  
**Day 2 — How does it behave?**  
**Day 3 — Why might it be behaving this way, what evidence supports that hypothesis, and what should be verified next?**

### Model capability

Within its frozen conceptual assumptions, the model can:

- represent a five-pump parallel water-supply system as queryable engineering assets and relationships;
- calculate pump/head/flow behaviour and VSD-speed requirements from first-principles equations;
- evaluate whether 5, 4, 3 or 2 available pumps can sustain the baseline hydraulic duty;
- generate reproducible synthetic operating, condition and energy telemetry;
- inject controlled fault/resilience scenarios while retaining hidden experiment ground truth;
- reconstruct evidence around an event without exposing its injected cause;
- distinguish the two implemented synthetic evidence patterns and refuse to invent a cause when evidence is insufficient;
- identify the hydraulic consequence and remaining capacity after equipment loss;
- produce engineering verification checks from explicit failure-mode knowledge;
- compare feasible operating states using hydraulic service, capacity margin, estimated electrical power and specific energy;
- generate deterministic reports and validate behaviour automatically in CI.

### How engineers and researchers can use it

The repository is intended as a transparent engineering study and simulation platform. It can be used to:

- teach and study the connection between P&IDs, asset models, pump physics, telemetry, faults and operational decisions;
- run repeatable what-if studies by changing demand, duty point, pump assumptions, availability or fault timing;
- study redundancy and capacity margin under progressive equipment loss;
- develop and test condition-monitoring or diagnostic logic against controlled synthetic evidence;
- examine what additional instrumentation would be needed to discriminate between competing failure hypotheses;
- study energy metrics and operating-state trade-offs before applying measured/vendor performance data;
- prototype data contracts, event/evidence structures and deterministic engineering analytics;
- compare analytical methods against a known simulated ground truth;
- provide a software plant model that can later be adapted to real measured telemetry, provided the conceptual parameters and synthetic diagnostic assumptions are replaced and independently validated.

### Real-life use boundary

The repository is **not** a validated plant model, protection system, maintenance authority or control application. Applying the architecture to a real installation requires site-specific P&IDs and topology, actual pump/vendor curves, measured electrical performance, calibrated instrumentation, real protection logic, validated failure signatures, operating constraints and engineering review.

The useful real-life pattern is therefore not to copy the current numerical assumptions. It is to reuse the architecture and replace the synthetic/reference inputs with validated engineering data.

### Scope boundary — no generative-AI stack

**LLMs, RAG, embeddings/vector databases, Neo4j and generative/autonomous AI agents are outside the scope of this Operational Digital Twin.**

The operational-intelligence layer is intentionally based on:

`explicit engineering knowledge + first-principles models + telemetry + deterministic evidence-based reasoning`

The project does not require an LLM to function as a digital twin. The term **knowledge layer** in this repository describes structured engineering assets, relationships, events and failure-mode knowledge; it does not imply a graph database.

Day 3 remains decision support. It does not validate real failure thresholds, autonomously perform maintenance, or send control commands.

**Day 3 operational-intelligence layer: complete and validated.**

---

## Repository guide

- `docs/system-definition.md` — system boundary and assumptions
- `docs/pid/WSP-001_PID_V0.1.drawio` — editable conceptual P&ID
- `docs/day-2-capacity.md` — frozen baseline and resilience envelope
- `docs/day-2-failure-simulation.md` — failure experiment
- `docs/day-2-data-contract.md` — Day-2 data and Day-3 boundary
- `docs/day-2-energy-data.md` — energy-data prerequisites
- `docs/day-3-operational-intelligence.md` — Day-3 architecture, reasoning and boundaries
- `knowledge/assets.yaml` — asset registry
- `knowledge/relationships.yaml` — engineering relationships
- `knowledge/events.yaml` — injected events and evidence references
- `knowledge/failure_modes.yaml` — diagnostic reference knowledge and limitations
- `knowledge/query.py` — deterministic engineering queries
- `model/physics.py` — pump physics
- `model/capacity.py` — resilience calculations
- `model/failure_simulation.py` — sequential failure simulation
- `model/day2_summary.py` — deterministic scenario summary
- `intelligence/evidence.py` — observable event-evidence extraction
- `intelligence/diagnosis.py` — transparent hypothesis scoring
- `intelligence/maintenance.py` — verification-plan generation
- `intelligence/operations.py` — hydraulic/energy/resilience comparison
- `intelligence/report.py` — deterministic Day-3 report
- `tests/` — automated validation
- `.github/workflows/validate.yml` — CI

## Validate locally

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python knowledge/query.py
python -m model.failure_simulation
python -m intelligence.report
pytest -q
```

## Engineering principles

**Physics before AI.**  
**Explicit assumptions before inference.**  
**Evidence before diagnosis.**  
**Measured/calculated/estimated/inferred values remain distinguishable.**  
**AI recommendations never silently become control commands.**
