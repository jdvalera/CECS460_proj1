`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date:    18:57:40 09/06/2016 
// Design Name: 
// Module Name:    pulse_maker 
// Project Name: 
// Target Devices: 
// Tool versions: 
// Description: 
//
// Dependencies: 
//
// Revision: 
// Revision 0.01 - File Created
// Additional Comments: 
//
//////////////////////////////////////////////////////////////////////////////////
module pulse_maker(
		input wire sig, clk, reset,
		output wire pulse
    );
	 
	 wire dff1, dff2;
	 
	 DFF DFF1(.clk(clk), .reset(reset), .d(sig), .q(dff1));
	 DFF DFF2(.clk(clk), .reset(reset), .d(dff1), .q(dff2));
	 
	 assign pulse = dff1 & ~dff2;


endmodule
