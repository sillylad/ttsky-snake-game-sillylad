# SPDX-FileCopyrightText: © 2024 Tiny Tapeout
# SPDX-License-Identifier: Apache-2.0

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import ClockCycles


@cocotb.test()
async def test_project(dut):
    dut._log.info("Start")

    # Set the clock period to 10 us (100 KHz)
    clock = Clock(dut.clk, 10, unit="us")
    cocotb.start_soon(clock.start())

    # Reset
    dut._log.info("Reset")
    dut.ena.value = 1
    dut.ui_in.value = 0
    dut.uio_in.value = 0
    dut.rst_n.value = 0
    await ClockCycles(dut.clk, 10)
    dut.rst_n.value = 1

    dut._log.info("Test project behavior")

    # Set the input values you want to test
    
    # simple test to simulate crashing into the wall and dying after eating 
    # the first egg

    # hit the start game button
    dut.ui_in.value = 0b000_0000_1
    
    # snake should eat an egg by just moving forwards, wait until that happens
    while(dut.ci.snek.curr_score == 0):
        await ClockCycles(dut.clk, 1) # just step the clock
        pass
    
    # check that score incremented and snake grew
    assert dut.ci.snek.curr_score == 1
    assert dut.ci.snek.snake_length == 4
    
    # turn off start_game button
    dut.ui_in.value = 0b000_0000_0
    
    # now the snake should die by just moving forwards and crashing into the wall
    while(dut.ci.snek.collision == 0):
        await ClockCycles(dut.clk, 1) # just step the clock
        pass
    
    assert dut.ci.snek.collision == 1
    await ClockCycles(dut.clk, 10000)
    
    assert dut.ci.snek.snake_length == 3
    
    

    # The following assersion is just an example of how to check the output values.
    # Change it to match the actual expected output of your module:
    # assert dut.uo_out.value == 50

    # Keep testing the module by changing the input values, waiting for
    # one or more clock cycles, and asserting the expected output values.
