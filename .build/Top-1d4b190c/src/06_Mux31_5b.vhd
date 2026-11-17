----------------------------------------------------------------------------------
-- Company: 
-- Engineer: 
-- 
-- Create Date: 11/16/2026 10:05:21 AM
-- Design Name: 
-- Module Name: Mux31_5b - Behavioral
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

entity Mux31_5b is
    Port ( E_0 : in  STD_LOGIC_VECTOR(4 downto 0);
           E_1 : in  STD_LOGIC_VECTOR(4 downto 0);
           E_2 : in  STD_LOGIC_VECTOR(4 downto 0);
           SEL : in  STD_LOGIC_VECTOR(1 downto 0);
           S   : out STD_LOGIC_VECTOR(4 downto 0));  
end Mux31_5b;

architecture Behavioral of Mux31_5b is
begin
    with SEL select
        S <= E_0 when "00",
             E_1 when "01",
             E_2 when "10",
             "00000" when others;
end Behavioral;
