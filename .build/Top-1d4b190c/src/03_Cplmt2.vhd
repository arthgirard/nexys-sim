----------------------------------------------------------------------------------
-- Company: 
-- Engineer: 
-- 
-- Create Date: 11/16/2026 09:05:21 AM
-- Design Name: 
-- Module Name: Cplmt2 - Behavioral
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

entity Cplmt2 is
    Port ( E : in STD_LOGIC_VECTOR(4 downto 0);
           S : out STD_LOGIC_VECTOR(4 downto 0));  
end Cplmt2;

architecture Behavioral of Cplmt2 is
begin
    S <= std_logic_vector(unsigned(not E) + 1);
end Behavioral;
