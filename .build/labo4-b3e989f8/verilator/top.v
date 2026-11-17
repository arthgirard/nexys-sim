module gestaffichage_Bbehavioral_Lxil_defaultlib
  (input  clk,
   output [1:0] mod_sel,
   output unit_sel,
   output [7:0] an);
  reg [19:0] cpt;
  reg [2:0] sel;
  wire [19:0] n102;
  wire [2:0] n105;
  wire [1:0] n106;
  wire n107;
  localparam [7:0] n112 = 8'b11111111;
  reg [19:0] n117;
  wire n118;
  wire n119;
  wire n120;
  wire n121;
  wire n122;
  wire n123;
  wire n124;
  wire n125;
  wire n126;
  wire n127;
  wire n128;
  wire n129;
  wire n130;
  wire n131;
  wire n132;
  wire n133;
  wire n134;
  wire n135;
  wire n136;
  wire n137;
  wire n138;
  wire n139;
  wire n140;
  wire n141;
  wire n142;
  wire n143;
  wire n144;
  wire n145;
  wire n146;
  wire n147;
  wire n148;
  wire n149;
  wire n150;
  wire n151;
  wire [7:0] n152;
  assign mod_sel = n106; //(module output)
  assign unit_sel = n107; //(module output)
  assign an = n152; //(module output)
  /*# ../src/04_GestAffichage.vhd:13:12 */
  always @*
    cpt = n117; // (isignal)
  /*# ../src/04_GestAffichage.vhd:14:12 */
  always @*
    sel = n105; // (isignal)
  /*# ../src/04_GestAffichage.vhd:20:24 */
  assign n102 = cpt + 20'b00000000000000000001;
  /*# ../src/04_GestAffichage.vhd:26:15 */
  assign n105 = cpt[19:17]; // extract
  /*# ../src/04_GestAffichage.vhd:29:37 */
  assign n106 = sel[2:1]; // extract
  /*# ../src/04_GestAffichage.vhd:30:20 */
  assign n107 = sel[0]; // extract
  /*# ../src/04_GestAffichage.vhd:19:9 */
  always @(posedge clk)
    n117 <= n102;
  initial
    n117 = 20'b00000000000000000000;
  /*# ../src/04_GestAffichage.vhd:36:9 */
  assign n118 = sel[2]; // extract
  /*# ../src/04_GestAffichage.vhd:36:9 */
  assign n119 = ~n118;
  /*# ../src/04_GestAffichage.vhd:36:9 */
  assign n120 = sel[1]; // extract
  /*# ../src/04_GestAffichage.vhd:36:9 */
  assign n121 = ~n120;
  /*# ../src/04_GestAffichage.vhd:36:9 */
  assign n122 = n119 & n121;
  /*# ../src/04_GestAffichage.vhd:36:9 */
  assign n123 = n119 & n120;
  /*# ../src/04_GestAffichage.vhd:36:9 */
  assign n124 = n118 & n121;
  /*# ../src/04_GestAffichage.vhd:36:9 */
  assign n125 = n118 & n120;
  /*# ../src/04_GestAffichage.vhd:36:9 */
  assign n126 = sel[0]; // extract
  /*# ../src/04_GestAffichage.vhd:36:9 */
  assign n127 = ~n126;
  /*# ../src/04_GestAffichage.vhd:36:9 */
  assign n128 = n122 & n127;
  /*# ../src/04_GestAffichage.vhd:36:9 */
  assign n129 = n122 & n126;
  /*# ../src/04_GestAffichage.vhd:36:9 */
  assign n130 = n123 & n127;
  /*# ../src/04_GestAffichage.vhd:36:9 */
  assign n131 = n123 & n126;
  /*# ../src/04_GestAffichage.vhd:36:9 */
  assign n132 = n124 & n127;
  /*# ../src/04_GestAffichage.vhd:36:9 */
  assign n133 = n124 & n126;
  /*# ../src/04_GestAffichage.vhd:36:9 */
  assign n134 = n125 & n127;
  /*# ../src/04_GestAffichage.vhd:36:9 */
  assign n135 = n125 & n126;
  /*# ../src/04_GestAffichage.vhd:36:9 */
  assign n136 = n112[0]; // extract
  /*# ../src/04_GestAffichage.vhd:36:9 */
  assign n137 = n128 ? 1'b0 : n136;
  /*# ../src/04_GestAffichage.vhd:36:9 */
  assign n138 = n112[1]; // extract
  /*# ../src/04_GestAffichage.vhd:36:9 */
  assign n139 = n129 ? 1'b0 : n138;
  /*# ../src/04_GestAffichage.vhd:36:9 */
  assign n140 = n112[2]; // extract
  /*# ../src/04_GestAffichage.vhd:36:9 */
  assign n141 = n130 ? 1'b0 : n140;
  /*# ../src/04_GestAffichage.vhd:36:9 */
  assign n142 = n112[3]; // extract
  /*# ../src/04_GestAffichage.vhd:36:9 */
  assign n143 = n131 ? 1'b0 : n142;
  /*# ../src/04_GestAffichage.vhd:36:9 */
  assign n144 = n112[4]; // extract
  /*# ../src/04_GestAffichage.vhd:36:9 */
  assign n145 = n132 ? 1'b0 : n144;
  /*# ../src/04_GestAffichage.vhd:36:9 */
  assign n146 = n112[5]; // extract
  /*# ../src/04_GestAffichage.vhd:36:9 */
  assign n147 = n133 ? 1'b0 : n146;
  /*# ../src/04_GestAffichage.vhd:36:9 */
  assign n148 = n112[6]; // extract
  /*# ../src/04_GestAffichage.vhd:36:9 */
  assign n149 = n134 ? 1'b0 : n148;
  /*# ../src/04_GestAffichage.vhd:36:9 */
  assign n150 = n112[7]; // extract
  /*# ../src/04_GestAffichage.vhd:36:9 */
  assign n151 = n135 ? 1'b0 : n150;
  /*# ../src/04_GestAffichage.vhd:36:9 */
  assign n152 = {n151, n149, n147, n145, n143, n141, n139, n137};
endmodule

module bin7seg_Bbehavioral_Lxil_defaultlib
  (input  [3:0] e,
   output [7:0] s);
  wire n62;
  wire n65;
  wire n68;
  wire n71;
  wire n74;
  wire n77;
  wire n80;
  wire n83;
  wire n86;
  wire n89;
  wire [9:0] n91;
  reg [7:0] n92;
  assign s = n92; //(module output)
  /*# ../src/01_Bin7Seg.vhd:36:25 */
  assign n62 = e == 4'b0000;
  /*# ../src/01_Bin7Seg.vhd:37:25 */
  assign n65 = e == 4'b0001;
  /*# ../src/01_Bin7Seg.vhd:38:25 */
  assign n68 = e == 4'b0010;
  /*# ../src/01_Bin7Seg.vhd:39:25 */
  assign n71 = e == 4'b0011;
  /*# ../src/01_Bin7Seg.vhd:40:25 */
  assign n74 = e == 4'b0100;
  /*# ../src/01_Bin7Seg.vhd:41:25 */
  assign n77 = e == 4'b0101;
  /*# ../src/01_Bin7Seg.vhd:42:25 */
  assign n80 = e == 4'b0110;
  /*# ../src/01_Bin7Seg.vhd:43:25 */
  assign n83 = e == 4'b0111;
  /*# ../src/01_Bin7Seg.vhd:44:25 */
  assign n86 = e == 4'b1000;
  /*# ../src/01_Bin7Seg.vhd:45:25 */
  assign n89 = e == 4'b1001;
  /*# ../src/01_Bin7Seg.vhd:35:5 */
  assign n91 = {n89, n86, n83, n80, n77, n74, n71, n68, n65, n62};
  /*# ../src/01_Bin7Seg.vhd:35:5 */
  always @*
    case (n91)
      10'b1000000000: n92 = 8'b10010000;
      10'b0100000000: n92 = 8'b10000000;
      10'b0010000000: n92 = 8'b11111000;
      10'b0001000000: n92 = 8'b10000010;
      10'b0000100000: n92 = 8'b10010010;
      10'b0000010000: n92 = 8'b10011001;
      10'b0000001000: n92 = 8'b10110000;
      10'b0000000100: n92 = 8'b10100100;
      10'b0000000010: n92 = 8'b11111001;
      10'b0000000001: n92 = 8'b11000000;
      default: n92 = 8'b11111111;
    endcase
endmodule

module mux21_4b_Bbehavioral_Lxil_defaultlib
  (input  [3:0] e_0,
   input  [3:0] e_1,
   input  sel,
   output [3:0] s);
  wire n53;
  wire n55;
  wire [1:0] n57;
  reg [3:0] n58;
  assign s = n58; //(module output)
  /*# ../src/05_Mux21_4b.vhd:36:18 */
  assign n53 = sel == 1'b0;
  /*# ../src/05_Mux21_4b.vhd:37:18 */
  assign n55 = sel == 1'b1;
  /*# ../src/05_Mux21_4b.vhd:35:5 */
  assign n57 = {n55, n53};
  /*# ../src/05_Mux21_4b.vhd:35:5 */
  always @*
    case (n57)
      2'b10: n58 = e_1;
      2'b01: n58 = e_0;
      default: n58 = 4'b0000;
    endcase
endmodule

module bin2dec_Bbehavioral_Lxil_defaultlib
  (input  [4:0] e,
   output [3:0] s_0,
   output [3:0] s_1);
  wire [5:0] e_integer;
  wire [5:0] n40;
  wire [31:0] n41;
  wire [31:0] n43;
  wire [30:0] n44;
  wire [3:0] n45;
  wire [31:0] n46;
  wire [31:0] n48;
  wire [30:0] n49;
  wire [3:0] n50;
  assign s_0 = n50; //(module output)
  assign s_1 = n45; //(module output)
  /*# ../src/00_Bin2Dec.vhd:38:12 */
  assign e_integer = n40; // (signal)
  /*# ../src/00_Bin2Dec.vhd:40:18 */
  assign n40 = {1'b0, e};  // uext
  /*# ../src/00_Bin2Dec.vhd:42:52 */
  assign n41 = {26'b0, e_integer};  // uext
  /*# ../src/00_Bin2Dec.vhd:42:52 */
  assign n43 = $signed(n41) / $signed(32'b00000000000000000000000000001010); // sdiv
  /*# ../src/00_Bin2Dec.vhd:42:41 */
  assign n44 = n43[30:0];  // trunc
  /*# ../src/00_Bin2Dec.vhd:42:29 */
  assign n45 = n44[3:0];  // trunc
  /*# ../src/00_Bin2Dec.vhd:43:51 */
  assign n46 = {26'b0, e_integer};  // uext
  /*# ../src/00_Bin2Dec.vhd:43:51 */
  assign n48 = n46 % 32'b00000000000000000000000000001010; // smod
  /*# ../src/00_Bin2Dec.vhd:43:41 */
  assign n49 = n48[30:0];  // trunc
  /*# ../src/00_Bin2Dec.vhd:43:29 */
  assign n50 = n49[3:0];  // trunc
endmodule

module mux31_5b_Bbehavioral_Lxil_defaultlib
  (input  [4:0] e_0,
   input  [4:0] e_1,
   input  [4:0] e_2,
   input  [1:0] sel,
   output [4:0] s);
  wire n29;
  wire n31;
  wire n33;
  wire [2:0] n35;
  reg [4:0] n36;
  assign s = n36; //(module output)
  /*# ../src/06_Mux31_5b.vhd:36:18 */
  assign n29 = sel == 2'b00;
  /*# ../src/06_Mux31_5b.vhd:37:18 */
  assign n31 = sel == 2'b01;
  /*# ../src/06_Mux31_5b.vhd:38:18 */
  assign n33 = sel == 2'b10;
  /*# ../src/06_Mux31_5b.vhd:35:5 */
  assign n35 = {n33, n31, n29};
  /*# ../src/06_Mux31_5b.vhd:35:5 */
  always @*
    case (n35)
      3'b100: n36 = e_2;
      3'b010: n36 = e_1;
      3'b001: n36 = e_0;
      default: n36 = 5'b00000;
    endcase
endmodule

module bitshift_Bbehavioral_Lxil_defaultlib
  (input  [4:0] e,
   output [4:0] s);
  wire [4:0] n26;
  assign s = n26; //(module output)
  /*# ../src/02_BitShift.vhd:40:23 */
  assign n26 = e << 31'b0000000000000000000000000000001;
endmodule

module cplmt2_Bbehavioral_Lxil_defaultlib
  (input  [4:0] e,
   output [4:0] s);
  wire [4:0] n21;
  wire [4:0] n23;
  assign s = n23; //(module output)
  /*# ../src/03_Cplmt2.vhd:33:36 */
  assign n21 = ~e;
  /*# ../src/03_Cplmt2.vhd:33:43 */
  assign n23 = n21 + 5'b00001;
endmodule

module Top
  (input  [4:0] A,
   input  CLOCK,
   output [7:0] SEVEN_SEG,
   output [7:0] A_N);
  reg [4:0] scompl2;
  reg [4:0] sbitshift;
  reg [4:0] smux31;
  reg [3:0] s0bin2dec;
  reg [3:0] s1bin2dec;
  reg [3:0] smux21;
  reg [1:0] sel31;
  reg sel21;
  wire [4:0] \cpl_2.s ;
  wire [4:0] \btshft.s ;
  wire [4:0] \mux31.s ;
  wire [3:0] \bin2dec.s_0 ;
  wire [3:0] \bin2dec.s_1 ;
  wire [3:0] \mux21.s ;
  wire [7:0] \bin7seg.s ;
  wire [1:0] \gestaffi.mod_sel ;
  wire \gestaffi.unit_sel ;
  wire [7:0] \gestaffi.an ;
  assign SEVEN_SEG = \bin7seg.s ; //(module output)
  assign A_N = \gestaffi.an ; //(module output)
  /*# ../src/07_Top.vhd:32:12 */
  always @*
    scompl2 = \cpl_2.s ; // (isignal)
  /*# ../src/07_Top.vhd:33:12 */
  always @*
    sbitshift = \btshft.s ; // (isignal)
  /*# ../src/07_Top.vhd:34:12 */
  always @*
    smux31 = \mux31.s ; // (isignal)
  /*# ../src/07_Top.vhd:35:12 */
  always @*
    s0bin2dec = \bin2dec.s_0 ; // (isignal)
  /*# ../src/07_Top.vhd:36:12 */
  always @*
    s1bin2dec = \bin2dec.s_1 ; // (isignal)
  /*# ../src/07_Top.vhd:37:12 */
  always @*
    smux21 = \mux21.s ; // (isignal)
  /*# ../src/07_Top.vhd:38:12 */
  always @*
    sel31 = \gestaffi.mod_sel ; // (isignal)
  /*# ../src/07_Top.vhd:39:12 */
  always @*
    sel21 = \gestaffi.unit_sel ; // (isignal)
  /*# ../src/07_Top.vhd:41:5 */
  cplmt2_Bbehavioral_Lxil_defaultlib cpl_2 (
    .e(A),
    .s(\cpl_2.s ));
  /*# ../src/07_Top.vhd:47:5 */
  bitshift_Bbehavioral_Lxil_defaultlib btshft (
    .e(A),
    .s(\btshft.s ));
  /*# ../src/07_Top.vhd:53:5 */
  mux31_5b_Bbehavioral_Lxil_defaultlib mux31 (
    .e_0(A),
    .e_1(scompl2),
    .e_2(sbitshift),
    .sel(sel31),
    .s(\mux31.s ));
  /*# ../src/07_Top.vhd:62:5 */
  bin2dec_Bbehavioral_Lxil_defaultlib bin2dec (
    .e(smux31),
    .s_0(\bin2dec.s_0 ),
    .s_1(\bin2dec.s_1 ));
  /*# ../src/07_Top.vhd:69:5 */
  mux21_4b_Bbehavioral_Lxil_defaultlib mux21 (
    .e_0(s0bin2dec),
    .e_1(s1bin2dec),
    .sel(sel21),
    .s(\mux21.s ));
  /*# ../src/07_Top.vhd:77:5 */
  bin7seg_Bbehavioral_Lxil_defaultlib bin7seg (
    .e(smux21),
    .s(\bin7seg.s ));
  /*# ../src/07_Top.vhd:83:5 */
  gestaffichage_Bbehavioral_Lxil_defaultlib gestaffi (
    .clk(CLOCK),
    .mod_sel(\gestaffi.mod_sel ),
    .unit_sel(\gestaffi.unit_sel ),
    .an(\gestaffi.an ));
endmodule

