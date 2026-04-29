# SPDX-FileCopyrightText: © 2024 Tiny Tapeout
# SPDX-License-Identifier: Apache-2.0

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import ClockCycles
from cocotb.triggers import RisingEdge
from cocotb.triggers import ReadOnly


@cocotb.test()
async def test_project(dut):
    dut._log.info("Start")

    # Set the clock period to 40 ns (25 MHz)
    clock = Clock(dut.clk, 40, unit="ns")
    cocotb.start_soon(clock.start())

    # Reset
    dut._log.info("Reset")
    dut.ena.value = 1
    dut.ui_in.value = 0
    dut.uio_in.value = 0
    dut.rst_n.value = 0
    await ClockCycles(dut.clk, 10)
    dut.rst_n.value = 1
    await ClockCycles(dut.clk, 1000)

    dut._log.info("Test project behavior")
    
    # change test based on gate level or rtl sim since post-synth can't use
    # the internal signals needed for the functional test (??)
    try:
        snek = dut.user_project.ci.snek
        gl_test = False
        dut._log.info("hierarchical signals usable")
    except AttributeError:
        gl_test = True
        dut._log.info("only ports")
        
    # super simple test to simulate moving the snake forwards from the init state
    if not gl_test:    
        # hit the start game button
        print(snek.curr_state.value)
        dut.ui_in.value = 0b000_0000_1
        await ClockCycles(dut.clk, 5) # propagate btn input into dut

        print(snek.start_game.value)
        
        # wait for game_clk so start_game gets used
        while True:
            print("waiting for game_clk posedge")
            await RisingEdge(snek.game_clk)
            await ReadOnly()
            if(dut.user_project.ci.start_game.value == 1):
                print("both game_clk and start_game high, proceeding")
                break
        
        await ClockCycles(dut.clk, 5)
        print(f"curr_state: {snek.curr_state.value}")
        print(f"start_game: {dut.user_project.ci.start_game.value}")
        assert dut.user_project.ci.start_game.value == 1
        print(f"game_clk: {snek.game_clk.value}")
        # assert that the snake moved out of the idle state
        assert snek.curr_state.value != 0
    
    # even more basic test for gate-level sim
    # just checking that the vga is ... alive
    else:
        await ClockCycles(dut.clk, 1000)
        hs_seen = False
        
        # hs period is like 800 so this should be enough time...
        for i in range(1000):
            await ClockCycles(dut.clk, 100)
            if int(dut.uo_out.value) & 0b10:  # VGA_HS on uo[1]
                print("hs has gone high!")
                hs_seen = True
                break
        
        assert hs_seen
        
        

    ##  Testbenches for when you want to sit around forever :) ## 
    # wait for snake to die (takes a while since game_clk takes forever...)
    # game_clk_cnt = 0
    # while True:
    #     print("waiting for game_clk posedge")
    #     print("game_clk_cnt: ", game_clk_cnt)
    #     await RisingEdge(snek.game_clk)
    #     await ReadOnly()
    #     game_clk_cnt = game_clk_cnt + 1
    #     if(snek.collision.value == 1):
    #         print("both game_clk and collision high, proceeding")
    #         break
    
    # await ClockCycles(dut.clk, 5)
    # print(f"curr_state: {snek.curr_state.value}")
    # print(f"collision: {snek.collision.value}")
    # assert snek.collision.value == 1
    # print(f"game_clk: {snek.game_clk.value}")
    
    # # snake should eat an egg by just moving forwards, wait until that happens
    # print("wait for score to increment")
    # print(snek.curr_state.value)
    # while(snek.curr_score.value == 0):
    #     await RisingEdge(snek.game_clk)
    #     pass
    
    # # check that score incremented and snake grew
    # assert snek.curr_score.value == 1
    # print("score incremented")
    # assert snek.snake_length.value == 4
    # print("snake length increased")
    
    # # turn off start_game button
    # dut.ui_in.value = 0b000_0000_0
    # print("turning off start_game button")
    
    # print("waiting for snake to die")
    # print(snek.curr_state.value)
    # # now the snake should die by just moving forwards and crashing into the wall
    # while(snek.collision.value == 0):
    #     await RisingEdge(snek.game_clk) # just step the clock
    #     pass

    # assert snek.collision.value == 1
    # print("snake has died")
    # await RisingEdge(snek.game_clk)
    
    # assert snek.snake_length.value == 3
    # print("snake has gone back to length 3")
    

