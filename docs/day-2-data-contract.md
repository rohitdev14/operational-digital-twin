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

## Knowledge/event layer

`knowledge/events.yaml` stores the small set of injected events, their affected assets, mechanisms, consequences and telemetry evidence windows.

The event file is **ground truth for the experiment**, not a diagnosis produced by the twin.

## Boundary for later work

Day 2 may compare commanded/expected operating capacity with simulated outcomes, but it must not infer an unknown failure cause or recommend maintenance. Those activities are intentionally reserved for a later stage.
