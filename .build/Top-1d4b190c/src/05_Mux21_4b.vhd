----------------------------------------------------------------------------------
-- Company: 
-- Engineer: 
-- 
-- Create Date: 11/16/2026 10:40:50 AM
-- Design Name: 
-- Module Name: Mux21_4b - Behavioral
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


entity Mux21_4b is
    Port ( E_0 : in  STD_LOGIC_VECTOR(3 downto 0);
           E_1 : in  STD_LOGIC_VECTOR(3 downto 0);
           SEL : in  STD_LOGIC;
           S   : out STD_LOGIC_VECTOR(3 downto 0));
end Mux21_4b;

architecture Behavioral of Mux21_4b is
begin
    with SEL select
        S <= E_0 when '0',
             E_1 when '1',
             "0000" when others;
    

end Behavioral;
