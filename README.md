# CAM-Software-test
Testing CAM software development. 
# CAM Software Build Test

Starter repository for a CAM software project that imports 3D CAD files, generates machining toolpaths, and outputs controller-ready G-code.

## Goal

Build a CAM application that can:
- Import 3D CAD geometry
- Define stock, tools, and machine setup
- Generate toolpaths for common milling operations
- Simulate operations before export
- Post-process into G-code for selected CNC controllers

## MVP Scope

The first version should support:
- Single 3D CAD input format
- 3-axis milling
- Basic operations:
  - facing
  - pocketing
  - profiling
  - drilling
  - simple finishing passes
- One G-code post-processor
- Basic toolpath preview or backplot

## Proposed Repository Structure

```text
docs/
  requirements.md
  architecture.md
  mvp-plan.md
src/
tests/
```

## Current Implementation

This repository now includes a modular Python CAM pipeline under `src/cam` that supports:

- CAD parsing for STL (ASCII + binary) and OBJ
- Extensible parser registry for future formats (DXF/STEP/etc.)
- Geometry analysis and mesh validation
- Roughing, finishing, and adaptive toolpath generation
- Machine profiles:
  - 2-axis mill
  - 3-axis mill
  - 4-axis mill
  - 2-axis lathe
- G-code generation with tool change, spindle, feed, and export support
- API + CLI workflow for file selection, machine selection, and parameter configuration

### Quick CLI Example

```bash
python -m src.cam.cli input.stl output.nc --machine 3_axis_mill --tool-number 2 --tool-diameter 8.0
