----------------------------------------------------------------------------------
-- Company: 
-- Engineer: 
-- 
-- Create Date: 11/16/2026 09:44:31 AM
-- Design Name: 
-- Module Name: BitShift - Behavioral
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



entity BitShift is
    Port ( E    : in STD_LOGIC_VECTOR (4 downto 0);
           S    : out STD_LOGIC_VECTOR (4 downto 0));
end BitShift;

architecture Behavioral of BitShift is

begin

S <= std_logic_vector(shift_left(signed(E),1));

end Behavioral;
