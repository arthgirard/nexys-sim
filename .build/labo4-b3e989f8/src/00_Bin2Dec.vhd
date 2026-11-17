----------------------------------------------------------------------------------
-- Company: 
-- Engineer: 
-- 
-- Create Date: 11/16/2026 10:12:05 AM
-- Design Name: 
-- Module Name: Bin2Dec - Behavioral
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

-- Uncomment the following library declaration if using
-- arithmetic functions with Signed or Unsigned values
use IEEE.NUMERIC_STD.ALL;



entity Bin2Dec is
    Port ( E    : in STD_LOGIC_VECTOR (4 downto 0);
           S_0    : out STD_LOGIC_VECTOR (3 downto 0);
           S_1    : out STD_LOGIC_VECTOR (3 downto 0));
end Bin2Dec;

architecture Behavioral of Bin2Dec is
    signal E_integer : integer range 0 to 32;
begin
    E_integer <= to_integer(unsigned(E));
    
    S_1 <= std_logic_vector(to_unsigned((E_integer / 10),4));
    S_0 <= std_logic_vector(to_unsigned(E_integer mod 10,4));

end Behavioral;
