# Day 2 — Failure and resilience simulation

This experiment holds the frozen process requirement at **500 m³/h and 38 mH2O** and progressively removes pumping capacity.

## Timeline

| Time | State | Mechanism | Expected response |
|---|---|---|---|
| 0–89 s | 5 healthy pumps | none | baseline |
| 90–119 s | P-101 degrading | synthetic bearing deterioration | vibration and current/load proxy rise |
| 120 s | P-101 trips | VSD overload | four pumps recover baseline |
| 235–239 s | P-102 electrical precursor | synthetic cable/electrical fault | electrical proxy excursion without vibration rise |
| 240 s | P-102 trips | electrical fault | three pumps recover baseline at reduced margin |
| 360 s | P-103 trips | resilience-test trip | only two pumps remain; baseline cannot be sustained |

## Ground-truth results from the deterministic model

- 5 pumps: baseline sustainable; common speed reference ≈ 87.4%.
- 4 pumps: baseline sustainable; common speed reference ≈ 89.7%.
- 3 pumps: baseline sustainable; common speed reference ≈ 94.5%.
- 2 pumps: baseline not sustainable within the 100% VSD-speed limit. At the requested 500 m³/h, the model predicts header head falls below the 38 m setpoint; the capacity calculation also reports a flow-capacity deficit at 38 m.

## Maintenance evidence

The simulation deliberately gives two trips different causal histories.

**P-101 bearing path:** rising VT-101 vibration + rising electrical load proxy → VSD overload trip → P-101 unavailable.

**P-102 cable/electrical path:** electrical proxy excursion without preceding vibration increase → electrical-fault trip → P-102 unavailable.

Both produce the same hydraulic state (one less available pump), but the evidence is different.

## Storage architecture

Raw high-frequency/synthetic telemetry belongs in a time-series dataset. The engineering knowledge layer stores assets, relationships, events, failure mechanisms and references to the relevant evidence windows. See `knowledge/events.yaml`.

This avoids turning every telemetry sample into a graph node while preserving the provenance needed for later maintenance reasoning.

## Run

```bash
python -m model.failure_simulation
pytest -q
```

The simulation writes `artifacts/day2_failure_telemetry.csv` when run locally. Generated telemetry is treated as a reproducible artifact; source model, event definitions and tests remain version controlled.

> All failure signatures are synthetic conceptual assumptions for the public experiment. They are not validated diagnostic thresholds and must not be used for real equipment protection or maintenance decisions.
