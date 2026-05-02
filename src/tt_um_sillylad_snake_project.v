/*
 * Copyright (c) 2024 Your Name
 * SPDX-License-Identifier: Apache-2.0
 */

`default_nettype none

module tt_um_sillylad_top (
    input  wire [7:0] ui_in,    // Dedicated inputs
    output wire [7:0] uo_out,   // Dedicated outputs
    input  wire [7:0] uio_in,   // IOs: Input path
    output wire [7:0] uio_out,  // IOs: Output path
    output wire [7:0] uio_oe,   // IOs: Enable path (active high: 0=input, 1=output)
    input  wire       ena,      // always 1 when the design is powered, so you can ignore it
    input  wire       clk,      // clock
    input  wire       rst_n     // reset_n - low to reset
);

  // All output pins must be assigned. If not used, assign to 0.
  assign uio_oe  = '1; // all output pins used by design

  // List all unused inputs to prevent warnings
  wire _unused = &{ena, ui_in[7], ui_in[6], ui_in[5], uio_in, 1'b0};

  // hook up "buttons" to the user input pins
  wire [6:0] btn;
  assign btn[0] = rst_n;        // design reset button
  assign btn[6:3] = ui_in[4:1]; // snake direction controls (right, left, down, up)
  assign btn[1] = ui_in[0];     // start_game control

  // set the last button to zero since it's not being used (only 6 buttons needed)
  assign btn[2] = 1'b0;

// uo_out[7:0]  -> 6-bit RGB and VGA VS and HS signals
// uio_out[7]   -> blank signal for VGA (redundant)
// uio_out[6:0] -> led outputs displaying button directions
ChipInterface ci (.clk(clk), .btn(btn),
                  .R0(uo_out[4]), .R1(uo_out[0]),
                  .G0(uo_out[5]), .G1(uo_out[1]),
                  .B0(uo_out[6]), .B1(uo_out[2]),
                  .VGA_HS(uo_out[7]), .VGA_VS(uo_out[3]), .blank(uio_out[7]),
                  .led(uio_out[6:0]));

endmodule