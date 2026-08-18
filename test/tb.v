`default_nettype none
`timescale 1ns / 1ps

/* This testbench instantiates the module and sets up wires
   that can be driven/tested by the cocotb test.py script.
*/
module tb ();

  // Dump the signals to an FST file for GTKWave or Surfer waveform viewing
  initial begin
    $dumpfile("tb.fst");
    $dumpvars(0, tb);
    #1;
  end

  // Signal declarations
  reg clk;
  reg rst_n;
  reg ena;
  reg [7:0] ui_in;
  reg [7:0] uio_in;
  wire [7:0] uo_out;
  wire [7:0] uio_out;
  wire [7:0] uio_oe;

`ifdef GL_TEST
  wire VPWR = 1'b1;
  wire VGND = 1'b0;
`endif

  // Instantiation of HDC Classifier module
  tt_um_hdc_classifier user_project (

`ifdef GL_TEST
      .VPWR(VPWR),
      .VGND(VGND),
`endif

      .ui_in   (ui_in),    // Dedicated inputs
      .uo_out  (uo_out),   // Dedicated outputs
      .uio_in  (uio_in),   // IOs: Input path
      .uio_out (uio_out),  // IOs: Output path
      .uio_oe  (uio_oe),   // IOs: Enable path
      .ena     (ena),      // Design enable signal
      .clk     (clk),      // Clock
      .rst_n   (rst_n)     // Active-low reset
  );

endmodule
