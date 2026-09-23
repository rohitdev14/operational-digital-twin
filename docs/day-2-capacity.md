# Day 2 — Baseline duty and resilience envelope

## Frozen baseline V0.1

- Total demand: **500 m³/h**
- Common discharge-header target: **38 mH2O**
- Installed pumps: **5 × 30 kW VSD centrifugal pump packages**
- Normal mode for this experiment: **all available pumps run together**
- All available pumps receive the same speed reference.
- Pumps are assumed identical for the healthy capacity calculation.

The calculation uses the conceptual public pump curve already defined in `model/physics.py`: shutoff head 55 m and reference point 180 m³/h at 42 m at nominal speed.

## Pre-fault capacity calculation

Before injecting faults, the twin calculates the speed and per-pump flow required to hold 500 m³/h at 38 m as pumps become unavailable.

| Pumps available | Required flow/pump | Required speed | Maximum total flow at 38 m | Flow margin | Calculated shaft power/pump | Baseline sustainable? |
|---|---:|---:|---:|---:|---:|---|
| 5 | 100.0 m³/h | 87.4% | 1029.2 m³/h | +529.2 | 13.4 kW | Yes |
| 4 | 125.0 m³/h | 89.7% | 823.4 m³/h | +323.4 | 16.4 kW | Yes |
| 3 | 166.7 m³/h | 94.5% | 617.5 m³/h | +117.5 | 21.5 kW | Yes |
| 2 | 250.0 m³/h | 107.1% | 411.7 m³/h | -88.3 | >30 kW at required duty | No |
| 1 | 500.0 m³/h | 158.6% | 205.8 m³/h | -294.2 | outside model envelope | No |

These are model outputs, not measured equipment data.

## Interpretation

At the frozen baseline, loss of one pump should be recoverable by the remaining four. Loss of two pumps should also be recoverable, but the remaining three operate close to maximum speed and the flow-capacity margin falls substantially.

With only two pumps available, the model requires approximately 107% nominal speed to meet the duty point. Because the VSD model is capped at 100%, the requested baseline cannot be maintained. The expected symptom is a sustained header-pressure/flow deficit rather than successful recovery.

This creates a useful resilience sequence for the next simulation:

**5 healthy → P-101 fault/trip → 4-pump recovery → P-102 fault/trip → 3-pump recovery with reduced margin → third pump loss → capacity deficit.**

The failure mechanism is deliberately kept separate from the capacity calculation. Later scenarios can make a pump unavailable through bearing degradation/VSD overload, cable/electrical fault, or another evidence-backed event while preserving the same hydraulic consequence: loss of available pumping capacity.
