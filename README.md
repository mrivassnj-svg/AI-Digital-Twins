# AI Digital Twins

## ITAI 4371 — Module 1: Digital Twin Verisimilitude

This repository documents my Module 1 conceptual digital-twin design work.

## Technical Plate Set

The `technical_plates/` directory contains six conceptual isometric technical models and an index plate. The series progresses from descriptive physical geometry, through live monitoring concepts, to predictive computational simulation.

| Model | Twin category | Conceptual subject |
|---|---|---|
| 01 | Low verisimilitude | Autodesk BIM / IFC structural model |
| 02 | Low verisimilitude | Minute Maid Park ballpark and retractable-roof study |
| 03 | Medium verisimilitude | Charles H. Wright Museum rotunda environmental monitoring |
| 04 | Medium verisimilitude | George R. Brown Convention Center operations monitoring |
| 05 | High verisimilitude | NASA National Airspace System conflict and reroute simulation |
| 06 | High verisimilitude | Buffalo Bayou hydrology and inundation simulation |

## Repository Contents

- `digital_twin_technical_plates.py` — reproducible Python rendering pipeline.
- `technical_plates/00_digital_twin_matrix_index.png` — overview/index visual.
- `technical_plates/01_*.png` through `06_*.png` — detailed model plates.

## Reproduce the Visuals

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install numpy matplotlib
python digital_twin_technical_plates.py
```

## Conceptual-Design Notice

These visuals are conceptual assignment designs. Landmark-inspired forms, architectural cues, device placements, dimensions, readings, identifiers, and predictive scenarios are illustrative. They are not surveyed drawings, engineering documents, facility-control systems, or live operational models.
