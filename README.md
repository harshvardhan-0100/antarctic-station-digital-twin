# Antarctic Station Digital Twin

A physics-informed Digital Twin for modelling the energy and infrastructure
of Antarctic research stations.

## Objective

The project aims to simulate and monitor the evolving operational state of
an Antarctic research station using environmental conditions, physical models,
and infrastructure constraints.

The initial implementation focuses on:

- Environmental modelling
- Building thermal dynamics
- Electrical load modelling
- CHP generator simulation
- Fuel consumption dynamics
- Generator dispatch optimisation
- Infrastructure resilience analysis
- What-if scenario simulation

## System Architecture

```text
Environmental Data
        ↓
Physics Simulation Core
        ↓
Station State
        ↓
Energy & Infrastructure Models
        ↓
Anomaly Detection / Optimisation
        ↓
Resilience Analysis