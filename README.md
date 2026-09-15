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
