`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date:    18:36:12 09/06/2016 
// Design Name: 
// Module Name:    AISO 
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
module AISO(
		input wire reset, clk,
		output wire rst_sync
    );
	 
	 //signals
	 wire dff1, dff2;
	 
	 DFF DFF1(.clk(clk), .reset(reset), .d(1'b1), .q(dff1));
	 DFF DFF2(.clk(clk), .reset(reset), .d(dff1), .q(dff2));
	
	 assign rst_sync = ~dff2;

endmodule
