<!---

This file is used to generate your project datasheet. Please fill in the information below and delete any unused
sections.

You can also include images in this folder and reference them in the markdown. Each image must be less than
512 kb in size, and the combined size of all images must be less than 1 MB.
-->

## How it works

This project implements an 8-bit Hyperdimensional Computing (HDC) classifier with two class prototypes.

The 8-bit input data is provided through the `ui_in[7:0]` pins. The classifier processes the input and compares it with the stored prototypes to determine the closest class.

The classifier provides the following outputs:

- `uo[5:0]` - 6-bit distance between the input and the selected prototype
- `uo[6]` - Winner class
- `uo[7]` - Done signal indicating that classification is complete

The bidirectional pins are used as control inputs:

- `uio[0]` - MODE
- `uio[1]` - CLASS_SEL
- `uio[2]` - VALID
- `uio[3]` - START
- `uio[7:4]` - Unused

The design operates synchronously with the `clk` signal and uses `rst_n` for active-low reset.

## How to test

The project includes a Cocotb-based testbench for functional verification.

From the project directory, run:

```bash
cd ~/tinytapeout/my_project
make -C test
