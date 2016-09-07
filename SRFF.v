`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date:    19:08:32 09/06/2016 
// Design Name: 
// Module Name:    SRFF 
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
module SRFF(
		input wire clk, s, r, reset,
		output reg q
    );
	 
	 always @*
		if(r)
			q <= 0; else
		if(s)
			q <= 1; else
		if(reset)
			q <= 0;


endmodule
