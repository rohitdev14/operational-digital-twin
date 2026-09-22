# Operational Digital Twin

Building a machine-readable engineering representation of a centrifugal pump system from first principles.

## Day 1 — Building the knowledge layer

The reference system is a water supply system with five parallel 30 kW VSD-driven centrifugal pump packages supplied from a common tank and discharging into a common variable-load header.

Today's objective is deliberately narrow:

> Turn a P&ID from a picture into structured engineering knowledge.

The first layer captures assets, instruments and explicit relationships between them. It does **not** yet contain pump simulation, PID simulation, fault diagnosis, RAG or an AI agent.

## Day 1 structure

- `docs/system-definition.md` — reference-system boundary and engineering assumptions
- `docs/pid/README.md` — P&ID tagging and source placeholder
- `knowledge/assets.yaml` — machine-readable asset registry
- `knowledge/relationships.yaml` — explicit topology and instrumentation relationships
- `tests/test_knowledge_model.py` — lightweight validation of the knowledge model

## Principle

**P&ID → assets → relationships → knowledge**

Every physical component receives a persistent identity. Measurements are linked to the assets or process properties they observe. This creates a foundation that later engineering models can build on without treating the P&ID as only an image.

## Status

Day 1 — knowledge layer under construction.

> Educational/reference implementation. Not for plant operation, control or construction.
