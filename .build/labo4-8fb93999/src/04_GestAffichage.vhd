library IEEE;
use IEEE.STD_LOGIC_1164.ALL;
use IEEE.NUMERIC_STD.ALL;

entity GestAffichage is
    Port ( CLK      : in  STD_LOGIC;
           MOD_SEL  : out STD_LOGIC_VECTOR (1 downto 0);
           UNIT_SEL : out STD_LOGIC;
           AN       : out STD_LOGIC_VECTOR (7 downto 0));
end GestAffichage;

architecture Behavioral of GestAffichage is
    signal cpt : unsigned(19 downto 0) := (others => '0');
    signal sel : unsigned(2 downto 0) := (others => '0');
begin
    -- Compteur libre
    process (CLK)
    begin
        if rising_edge(CLK) then
            cpt <= cpt + 1;
        end if;
    end process;

    -- Afficheur courant : bits [19:17] -> 2^17 cycles par afficheur
    -- à 100 MHz : ~1,3 ms par afficheur, ~95 Hz pour un tour complet
    sel <= cpt(19 downto 17);

    -- Afficheurs 0-1 -> module 0, 2-3 -> module 1, etc.
    MOD_SEL  <= std_logic_vector(sel(2 downto 1));
    UNIT_SEL <= sel(0);

    -- Anodes actives à 0, une seule à la fois
    process (sel)
    begin
        AN <= (others => '1');
        AN(to_integer(sel)) <= '0';
    end process;
end Behavioral;