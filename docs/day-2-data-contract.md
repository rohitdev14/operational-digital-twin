# Day 2 data contract

Day 2 stops at deterministic simulation, synthetic telemetry, resilience calculations and event recording. It does **not** perform diagnosis, causal inference, maintenance recommendations, RAG or AI reasoning.

## Telemetry layer

The reproducible simulation emits one row per pump per second with:

- time and scenario ground truth
- demanded and delivered system flow
- flow deficit
- header head and setpoint
- common VSD speed reference
- number of pumps available
- baseline-sustained flag
- asset ID and run/trip state
- injected failure cause and trip code
- pump flow and calculated shaft power
- synthetic vibration and electrical-load proxy

## Cross-project timestamp contract

To correlate operational-twin data with the Open Partial Discharge Monitor, integration records shall use:

- `timestamp_utc` — ISO 8601 UTC timestamp, e.g. `2026-09-23T11:30:15.123456Z`
- `asset_id` — persistent equipment ID, e.g. `M-101` or `P-101`
- `run_id` — shared experiment identifier, e.g. `DT-PD-20260923-001`
- `source` — producer identifier, e.g. `operational-digital-twin` or `pd-simulator`

The same `run_id` shall be used by both repositories for a synchronized experiment. This provides a deterministic join key for VSD speed, flow, head, power/energy and PD waveform/PRPD evidence.

For reproducibility, an experiment record should also capture the commit SHA of each repository and configuration version used for the run.

## Knowledge/event layer

`knowledge/events.yaml` stores the small set of injected events, their affected assets, mechanisms, consequences and telemetry evidence windows.

The event file is **ground truth for the experiment**, not a diagnosis produced by the twin.

## Boundary for later work

Day 2 may compare commanded/expected operating capacity with simulated outcomes, but it must not infer an unknown failure cause or recommend maintenance. Those activities are intentionally reserved for a later stage.
