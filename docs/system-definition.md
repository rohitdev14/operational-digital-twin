# System Definition — Day 1

## Boundary

The reference system is an open-loop water supply system:

**Makeup source → TK-001 → SH-001 → five parallel pump branches → DH-001 → variable process/users**

Water delivered to the users does not return to TK-001 in this version.

## Major equipment

- TK-001 — supply tank
- SH-001 — common suction header
- P-101 … P-105 — centrifugal pump + 30 kW motor + VSD functional packages
- DH-001 — common discharge header

## Makeup water

Makeup water may originate from another water loop or a metered city-water connection.

- FM-001 measures makeup-water flow.
- MV-001 modulates makeup flow.
- LT-001 measures TK-001 level.

## Pump branch pattern

Each pump branch contains:

suction isolation valve → suction strainer → strainer differential-pressure measurement → pump package → discharge non-return valve → manual discharge isolation valve.

The VSD, rather than a pneumatic discharge throttling valve, is the normal capacity-control element. The non-return valve prevents reverse flow through an idle parallel pump. The manual discharge valve provides maintenance isolation.

## Common measurements

- PT-001 — discharge-header pressure
- FT-001 — discharge-header flow
- PIC-001 — header pressure controller
- EM-001 — system energy-metering function

Pump-specific condition/performance measurements include suction pressure, discharge pressure, vibration and electrical energy/power channels.

## Day 1 scope

Day 1 represents topology and engineering semantics only. Dynamic hydraulics, controls simulation, energy modelling and fault reasoning are intentionally outside this commit.
