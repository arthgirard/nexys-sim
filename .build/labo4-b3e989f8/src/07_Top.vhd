----------------------------------------------------------------------------------
-- Company: 
-- Engineer: 
-- 
-- Create Date: 11/16/2026 08:48:06 AM
-- Design Name: 
-- Module Name: Top - Behavioral
-- Project Name: 
-- Target Devices: 
-- Tool Versions: 
-- Description: 
-- 
-- Dependencies: 
-- 
-- Revision:
-- Revision 0.01 - File Created
-- Additional Comments:
-- 
----------------------------------------------------------------------------------


library IEEE;
use IEEE.STD_LOGIC_1164.ALL;
entity Top is
    Port ( A         : in  STD_LOGIC_VECTOR(4 downto 0);
           CLOCK     : in  STD_LOGIC;
           SEVEN_SEG : out STD_LOGIC_VECTOR(7 downto 0);
           A_N       : out STD_LOGIC_VECTOR(7 downto 0));
end Top;

architecture Behavioral of Top is
    signal SCompl2   : STD_LOGIC_VECTOR(4 downto 0) := (others => '0');
    signal SBitShift : STD_LOGIC_VECTOR(4 downto 0) := (others => '0');
    signal SMux31    : STD_LOGIC_VECTOR(4 downto 0) := (others => '0');
    signal S0Bin2Dec : STD_LOGIC_VECTOR(3 downto 0) := (others => '0');
    signal S1Bin2Dec : STD_LOGIC_VECTOR(3 downto 0) := (others => '0');
    signal SMux21    : STD_LOGIC_VECTOR(3 downto 0) := (others => '0');
    signal SEL31     : STD_LOGIC_VECTOR(1 downto 0) := (others => '0');
    signal SEL21     : STD_LOGIC := '0';
begin
    CPL_2: entity work.Cplmt2
        port map (
            E => A,
            S => SCompl2 
            );
            
    BTSHFT: entity work.BitShift
        port map (
            E => A,
            S => SBitShift
            );
            
    MUX31: entity work.Mux31_5b
        port map (
            E_0 => A,
            E_1 => SCompl2,
            E_2 => SBitShift,
            SEL => SEL31,
            S => SMux31
            );
    
    BIN2DEC: entity work.BIN2DEC
        port map (
            E => SMux31,
            S_0 => S0Bin2Dec,
            S_1 => S1Bin2Dec
            );
    
    MUX21: entity work.Mux21_4b
        port map (
            E_0 => S0Bin2Dec,
            E_1 => S1Bin2Dec,
            SEL => SEL21,
            S => SMux21
            );
     
    BIN7SEG: entity work.Bin7Seg
        port map (
            E => SMux21,
            S => SEVEN_SEG
            );
     
    GESTAFFI: entity work.GestAffichage
        port map (
            CLK => CLOCK,
            MOD_SEL => SEL31,
            UNIT_SEL => SEL21,
            AN => A_N
            );



end Behavioral;
