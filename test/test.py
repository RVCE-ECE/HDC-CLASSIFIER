# SPDX-FileCopyrightText: © 2024 Tiny Tapeout
# SPDX-License-Identifier: Apache-2.0

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import ClockCycles


@cocotb.test()
async def test_project(dut):

    dut._log.info("Start HDC Classifier Test")

    # ---------------------------------------------------------
    # Clock
    # 10 us period = 100 KHz
    # ---------------------------------------------------------

    clock = Clock(dut.clk, 10, unit="us")
    cocotb.start_soon(clock.start())

    # ---------------------------------------------------------
    # Reset
    # ---------------------------------------------------------

    dut._log.info("Reset")

    dut.ena.value = 1
    dut.ui_in.value = 0
    dut.uio_in.value = 0
    dut.rst_n.value = 0

    await ClockCycles(dut.clk, 10)

    dut.rst_n.value = 1

    await ClockCycles(dut.clk, 2)

    # ---------------------------------------------------------
    # LOAD CLASS A
    #
    # mode       = 0
    # class_sel  = 0
    # valid_in   = 1
    # start_query = 0
    #
    # uio_in = 00000100
    # ---------------------------------------------------------

    dut._log.info("Loading Class A")

    class_a = [
        0x10,
        0x20,
        0x30,
        0x40,
        0x50,
        0x60,
        0x70,
        0x80
    ]

    for value in class_a:

        dut.ui_in.value = value

        # mode = 0
        # class_sel = 0
        # valid_in = 1
        # start_query = 0

        dut.uio_in.value = 0b00000100

        await ClockCycles(dut.clk, 1)

    # Stop Class A loading
    dut.ui_in.value = 0
    dut.uio_in.value = 0

    await ClockCycles(dut.clk, 1)

    # ---------------------------------------------------------
    # LOAD CLASS B
    #
    # mode       = 0
    # class_sel  = 1
    # valid_in   = 1
    # start_query = 0
    #
    # uio_in = 00000110
    # ---------------------------------------------------------

    dut._log.info("Loading Class B")

    class_b = [
        0xFF,
        0xEE,
        0xDD,
        0xCC,
        0xBB,
        0xAA,
        0x99,
        0x88
    ]

    for value in class_b:

        dut.ui_in.value = value

        # mode = 0
        # class_sel = 1
        # valid_in = 1
        # start_query = 0

        dut.uio_in.value = 0b00000110

        await ClockCycles(dut.clk, 1)

    # Stop Class B loading
    dut.ui_in.value = 0
    dut.uio_in.value = 0

    await ClockCycles(dut.clk, 1)

    # ---------------------------------------------------------
    # START QUERY
    #
    # IMPORTANT:
    # start_query gets its own clock cycle.
    # No query data is sent during this cycle.
    #
    # mode       = 1
    # start_query = 1
    #
    # uio_in = 00001001
    # ---------------------------------------------------------

    dut._log.info("Starting Query")

    dut.ui_in.value = 0
    dut.uio_in.value = 0b00001001

    await ClockCycles(dut.clk, 1)

    # ---------------------------------------------------------
    # QUERY DATA
    #
    # Query is identical to Class A.
    #
    # mode       = 1
    # valid_in   = 1
    # start_query = 0
    #
    # uio_in = 00000101
    # ---------------------------------------------------------

    dut._log.info("Sending Query")

    query = [
        0x10,
        0x20,
        0x30,
        0x40,
        0x50,
        0x60,
        0x70,
        0x80
    ]

    for value in query:

        dut.ui_in.value = value

        # mode = 1
        # class_sel = 0
        # valid_in = 1
        # start_query = 0

        dut.uio_in.value = 0b00000101

        await ClockCycles(dut.clk, 1)

    # ---------------------------------------------------------
    # Stop inputs
    # ---------------------------------------------------------

    dut.ui_in.value = 0
    dut.uio_in.value = 0

    # Give the design some time to update outputs
    await ClockCycles(dut.clk, 2)

    # ---------------------------------------------------------
    # READ OUTPUT
    #
    # uo_out[7]   = done
    # uo_out[6]   = winner
    # uo_out[5:0] = winning distance
    # ---------------------------------------------------------

    result = int(dut.uo_out.value)

    done = (result >> 7) & 1
    winner = (result >> 6) & 1
    distance = result & 0x3F

    dut._log.info("--------------------------------")
    dut._log.info(f"uo_out   = {result:08b}")
    dut._log.info(f"Done     = {done}")
    dut._log.info(f"Winner   = {winner}")
    dut._log.info(f"Distance = {distance}")
    dut._log.info("--------------------------------")

    # ---------------------------------------------------------
    # EXPECTED RESULT
    #
    # Query = Class A
    #
    # Therefore:
    #
    # Distance A = 0
    # Distance B = 64
    # Class A wins
    #
    # done     = 1
    # winner   = 0
    # distance = 0
    #
    # Expected uo_out:
    #
    # 10000000
    # ---------------------------------------------------------

    assert done == 1, \
        "Classification did not complete"

    assert winner == 0, \
        "Class B incorrectly selected"

    assert distance == 0, \
        "Distance to Class A should be zero"

    dut._log.info("HDC Classifier Test PASSED")
