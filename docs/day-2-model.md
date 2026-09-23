# Day 2 — Make the plant behave

Day 2 adds a transparent first-principles behaviour model to the Day-1 knowledge layer.

## Engineering question

Can a small deterministic model reproduce the expected response of the reference pumping system as demand changes?

## Public modelling assumptions

These are conceptual assumptions for learning and software validation. They are **not vendor pump data** and are not intended for equipment selection or plant design.

- Fluid: water, density 998 kg/m³.
- Five identical centrifugal pump packages, each with a 30 kW motor and VSD.
- Nominal-speed conceptual pump curve: `H = H0 - k Q²`.
- Shutoff head: 55 m.
- Reference point: 180 m³/h at 42 m head per pump.
- VSD operating range used in the demo: 45–100% speed.
- Parallel pumps share flow equally and operate at a common header head.
- Header-pressure setpoint: 38 m water column (~3.72 bar differential equivalent).
- A bounded efficiency approximation is used only to demonstrate hydraulic/shaft energy behaviour.
- Synthetic demand is imposed at the discharge header; it is not measured plant data.

## Physics implemented

Nominal pump curve: `H(Q) = H0 - k Q²`

Affinity-law scaling: `Q ∝ N`, `H ∝ N²`, `P ∝ N³`.

Calculated demo shaft power uses `Pshaft = ρ g Q H / η`.

For identical parallel pumps, total demanded flow is divided between running pumps and each pump operates at the common header head.

## Controls implemented

A deliberately simple PI-style pressure controller adjusts common VSD speed reference. When pressure cannot be maintained near maximum speed for a defined delay, another pump is staged. Pumps de-stage only after sustained lower-speed operation.

This is a conceptual control model, not production PLC logic. Real implementations require permissives, trips, lead/lag rotation, minimum run/off times, ramp limits, minimum-flow protection and equipment-specific constraints.

## Synthetic operating sequence

The demo applies:

`140 → 300 → 500 → 720 → 430 → 220 m³/h`

Expected response:

**Demand ↑ → header pressure tends to fall → controller increases VSD speed → additional pumps stage when required → capacity increases → power changes.**

## Run

```bash
python -m model.run_demo
python -m model.render_svg
pytest -q
```

The demo generates synthetic telemetry for demand, header head, setpoint, VSD speed, pumps running, per-pump flow, calculated shaft power and cumulative energy.

## Day-2 boundary

Day 2 models expected behaviour only. Fault injection, expected-vs-actual residuals and evidence-based diagnosis belong to Day 3.
