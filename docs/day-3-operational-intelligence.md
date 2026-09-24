# Day 3 — Operational Intelligence

## Question

Can the digital twin distinguish different causes that produce the same operational outcome, explain its reasoning from evidence, and identify what should be verified next?

Day 3 deliberately consumes the deterministic Day-2 telemetry while keeping injected failure labels as hidden evaluation ground truth.

## Architecture

`Day-2 telemetry → evidence extraction → transparent hypothesis scoring → verification plan → operational comparison → report`

LLMs, RAG, embeddings/vector databases, Neo4j and generative/autonomous AI agents are outside the scope of this Operational Digital Twin. The intelligence layer is intentionally deterministic and testable, using explicit engineering knowledge, first-principles models, telemetry and evidence-based reasoning. The knowledge layer does not imply a graph database.

## 1. Evidence engine

`intelligence/evidence.py` reconstructs a pre/post-trip evidence window for an asset. Diagnostic inputs include observable values such as vibration trend, electrical-load trend, trip code, process demand and post-trip hydraulic consequence.

The injected `failure_cause` and `scenario` fields are explicitly excluded from the diagnostic view.

## 2. Diagnostic reasoning

`intelligence/diagnosis.py` uses transparent evidence scoring rather than an opaque classifier.

For the synthetic Day-2 experiment:

- P-101: rising vibration + rising electrical load + VSD overload supports a mechanical-load/bearing-degradation hypothesis.
- P-102: electrical excursion + electrical-fault trip + no material vibration rise supports an electrical-supply/cable hypothesis.
- P-103: the generic resilience-test trip has insufficient condition evidence for a cause diagnosis; the engine reports the hydraulic consequence without inventing a cause.

These are hypotheses derived from synthetic evidence, not real diagnostic thresholds.

## 3. Maintenance intelligence

`intelligence/maintenance.py` converts the leading hypothesis into verification checks. It does not issue automatic maintenance commands. Checks identify the additional evidence an engineer would need before acting.

`knowledge/failure_modes.yaml` records the current diagnostic reference knowledge and its limitations.

## 4. Operational and energy intelligence

`intelligence/operations.py` compares the 5-, 4-, 3- and 2-pump states against:

- hydraulic duty feasibility
- required speed
- flow/capacity margin
- estimated electrical power
- modelled specific energy consumption
- remaining pump-count resilience above the minimum three-pump sustainable state

A configuration that cannot meet the frozen 500 m3/h @ 38 mH2O duty is not considered feasible. Energy values remain conceptual because pump, motor and VSD efficiencies are model assumptions rather than measured/vendor performance maps.

The comparison is decision support, not an automatic optimizer or plant-control command.

## 5. Explainability and validation

The Day-3 output separates:

`OBSERVED → DERIVED → HYPOTHESIS → SUPPORTING EVIDENCE → MISSING EVIDENCE → SYSTEM CONSEQUENCE → VERIFICATION`

Tests verify that:

- P-101 and P-102 produce different evidence and diagnostic paths.
- P-103's capacity consequence is identified without inventing a cause.
- diagnostic code does not consume `failure_cause` or `scenario`.
- insufficient evidence does not become a maintenance claim.
- operating comparisons reject the two-pump state as unable to meet baseline duty.

## Run

```bash
python -m intelligence.report
pytest -q
```

The report generator writes `artifacts/day3_diagnostic_report.json` when run locally.

## Boundary

Day 3 is an educational/reference operational-intelligence layer. It does not validate real failure thresholds, replace engineering inspection, perform autonomous maintenance, or send commands to a PLC/VSD.


## Conclusion — from Day 1 to Day 3

The build started with a conceptual P&ID and a question: can software understand an industrial pumping system as engineering assets and relationships rather than only as a drawing?

Day 1 created that machine-readable plant definition. Day 2 added first-principles behaviour, resilience, synthetic telemetry, controlled fault scenarios and energy accounting. Day 3 converted those observable signals into an inspectable evidence-to-hypothesis-to-verification workflow while preserving the injected causes as hidden validation ground truth.

The resulting reference model can represent system topology, simulate hydraulic behaviour, test pump-availability scenarios, generate repeatable datasets, reconstruct event evidence, compare implemented synthetic diagnostic patterns, identify insufficient evidence, propose verification checks and compare feasible operating states. These capabilities are deterministic and automatically tested.

## Engineering and research use

Engineers, students and researchers can use the repository as a reproducible sandbox for pump-system studies, what-if simulation, resilience/capacity analysis, condition-monitoring logic, evidence-based diagnostics, instrumentation-gap studies, energy-metric studies, data-contract experiments and comparison of analytical methods against known simulated ground truth.

For a real installation, the architecture can be adapted but the reference assumptions cannot simply be reused. Site topology, vendor pump curves, measured electrical performance, instrumentation, protection logic, constraints and failure signatures must be replaced with validated real engineering data. Any diagnostic or maintenance use requires independent engineering validation.
