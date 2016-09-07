`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date:    18:32:38 09/06/2016 
// Design Name: 
// Module Name:    DFF 
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
module DFF(
	input wire clk, reset, d,
	output reg q
    );
	 
	 always @(posedge clk, posedge reset)
		if (reset)
			q <= 1'b0;
		else
			q <= d;

endmodule
