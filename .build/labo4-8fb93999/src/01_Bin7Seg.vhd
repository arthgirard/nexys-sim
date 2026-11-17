----------------------------------------------------------------------------------
-- Company: 
-- Engineer: 
-- 
-- Create Date: 11/16/2026 11:02:50 AM
-- Design Name: 
-- Module Name: Bin7Seg - Behavioral
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
use IEEE.NUMERIC_STD.ALL;


entity Bin7Seg is
    Port (E : in  STD_LOGIC_VECTOR (3 downto 0);
          S : out STD_LOGIC_VECTOR (7 downto 0));
end Bin7Seg;

architecture Behavioral of Bin7Seg is

begin
    with E select
        S <= "11000000" when "0000",
             "11111001" when "0001",
             "10100100" when "0010",
             "10110000" when "0011",
             "10011001" when "0100",
             "10010010" when "0101",           
             "10000010" when "0110",
             "11111000" when "0111",
             "10000000" when "1000",
             "10010000" when "1001",
             "11111111" when others;

end Behavioral;
