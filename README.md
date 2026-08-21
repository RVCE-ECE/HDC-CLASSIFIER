# 8-bit Hyperdimensional Computing (HDC) Classifier

**Tiny Tapeout submission, SkyWater 130nm, TTSKY26c shuttle**

- [Read the full project documentation](docs/info.md)
- [Project information](info.yaml)

## What is this?

This project implements an **8-bit Hyperdimensional Computing (HDC) Classifier** in digital logic. It receives an 8-bit input vector and compares it with two class prototypes to determine the most similar class.

The classification is based on **Hamming distance**, which measures the number of differing bits between the input vector and each class prototype. The class with the smaller distance is selected as the winner.

The design provides a compact hardware implementation of an HDC classification operation suitable for ASIC implementation through the Tiny Tapeout flow.

## Design summary

- **Top module:** `tt_um_hdc_classifier`
- **Technology:** SkyWater 130nm (SKY130)
- **Language:** Verilog
- **Input data:** 8 bits
- **Number of classes:** 2
- **Classification method:** Hamming distance
- **Clock:** 10 MHz
- **Tile size:** 1×1
- **Tiny Tapeout shuttle:** TTSKY26c
- **Physical verification:** GDS generation, precheck, gate-level test and viewer checks completed successfully

## How it works

The classifier receives an 8-bit input vector and compares it with two stored class prototypes.

For each class, the Hamming distance is calculated by determining the number of bit positions that differ between the input vector and the corresponding prototype.

The two distances are then compared:

- A smaller Hamming distance indicates a closer match.
- The class with the smaller distance is selected as the winner.
- The calculated distance is provided through the `DIST` output.
- The selected class is indicated by `WINNER`.
- `DONE` indicates completion of the classification operation.

