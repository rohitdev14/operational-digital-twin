# Day 2 — Energy data prerequisites

Energy optimization is reserved for a later stage, but Day 2 must generate the measurements needed to evaluate candidate operating states.

## Added energy fields

The failure/resilience telemetry now records:

- shaft power per operating pump (kW)
- estimated electrical input power per pump (kW)
- system electrical input power (kW)
- incremental and cumulative electrical energy (kWh)
- incremental and cumulative delivered water volume (m³)
- instantaneous specific energy consumption, **kWh/m³**
- cumulative specific energy consumption, **kWh/m³**
- assumed motor and VSD efficiencies

For the conceptual model, motor efficiency is fixed at **93%** and VSD efficiency at **97%**. These are transparent modelling assumptions, not vendor curves or measured equipment values.

Electrical input is calculated as:

`P_electrical = P_shaft / (eta_motor × eta_VSD)`

Specific energy is:

`SEC = electrical power (kW) / delivered flow (m³/h)`

which is numerically equivalent to kWh/m³ for a steady one-hour basis.

## Why this belongs to Day 2

Day 2 generates and preserves operating evidence. Recording energy and delivered volume allows later work to compare operating configurations without retroactively inventing data.

No optimizer is implemented here. No configuration is ranked or selected. Day 2 only creates the reproducible energy dataset and metrics required for future optimization.

## Important limitation

Fixed motor/VSD efficiencies are sufficient for the current educational data pipeline but are not adequate for a real energy-optimization study. A deployment model should use measured electrical power and, where available, vendor or measured efficiency maps versus load and speed.
