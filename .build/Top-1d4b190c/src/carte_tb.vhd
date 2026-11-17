-- Généré par nexys_sim.py : ne pas modifier.
library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;
use std.textio.all;

entity carte_tb is
end entity carte_tb;

architecture sim of carte_tb is
  constant NB_IN  : integer := 22;
  constant NB_OUT : integer := 38;
  constant ACTIVE : string(1 to NB_OUT) := "11111111111111111111110000000000000000";
  type int_arr is array (natural range <>) of integer;
  signal clk   : std_logic := '0';
  signal b_in  : std_logic_vector(NB_IN - 1 downto 0) := (others => '0');
  signal b_out : std_logic_vector(NB_OUT - 1 downto 0);
  signal p_A : STD_LOGIC_VECTOR(4 downto 0);
  signal p_CLOCK : STD_LOGIC;
  signal p_SEVEN_SEG : STD_LOGIC_VECTOR(7 downto 0);
  signal p_A_N : STD_LOGIC_VECTOR(7 downto 0);
begin
  clk <= not clk after 5 ns;

  p_A(0) <= b_in(0);
  p_A(1) <= b_in(1);
  p_A(2) <= b_in(2);
  p_A(3) <= b_in(3);
  p_A(4) <= b_in(4);
  p_CLOCK <= clk;

  b_out(22) <= p_SEVEN_SEG(0);
  b_out(23) <= p_SEVEN_SEG(1);
  b_out(24) <= p_SEVEN_SEG(2);
  b_out(25) <= p_SEVEN_SEG(3);
  b_out(26) <= p_SEVEN_SEG(4);
  b_out(27) <= p_SEVEN_SEG(5);
  b_out(28) <= p_SEVEN_SEG(6);
  b_out(29) <= p_SEVEN_SEG(7);
  b_out(30) <= p_A_N(0);
  b_out(31) <= p_A_N(1);
  b_out(32) <= p_A_N(2);
  b_out(33) <= p_A_N(3);
  b_out(34) <= p_A_N(4);
  b_out(35) <= p_A_N(5);
  b_out(36) <= p_A_N(6);
  b_out(37) <= p_A_N(7);
  b_out(0) <= '0';
  b_out(1) <= '0';
  b_out(2) <= '0';
  b_out(3) <= '0';
  b_out(4) <= '0';
  b_out(5) <= '0';
  b_out(6) <= '0';
  b_out(7) <= '0';
  b_out(8) <= '0';
  b_out(9) <= '0';
  b_out(10) <= '0';
  b_out(11) <= '0';
  b_out(12) <= '0';
  b_out(13) <= '0';
  b_out(14) <= '0';
  b_out(15) <= '0';
  b_out(16) <= '0';
  b_out(17) <= '0';
  b_out(18) <= '0';
  b_out(19) <= '0';
  b_out(20) <= '0';
  b_out(21) <= '0';

  dut : entity work.Top
    port map (
      A => p_A,
      CLOCK => p_CLOCK,
      SEVEN_SEG => p_SEVEN_SEG,
      A_N => p_A_N
    );

  -- Protocole : lit "<22 bits d'entrée> <cycles>", simule, puis écrit
  -- "@@R <cycles> <temps actif par sortie (ns)...> <temps segment par afficheur...> <indéfinis>".
  monitor : process
    variable lin, lout : line;
    variable c         : character;
    variable ncyc      : integer;
    variable inv       : std_logic_vector(NB_IN - 1 downto 0);
    variable prev      : std_logic_vector(NB_OUT - 1 downto 0) := (others => 'U');
    variable act_t     : int_arr(0 to NB_OUT - 1);
    variable seg_t     : int_arr(0 to 63);
    variable undef     : string(1 to NB_OUT);
    variable t_last    : time := 0 ns;
    variable t_end     : time;
    variable dt        : integer;
  begin
    loop
      readline(input, lin);
      for i in 0 to NB_IN - 1 loop
        read(lin, c);
        if c = '1' then inv(i) := '1'; else inv(i) := '0'; end if;
      end loop;
      read(lin, ncyc);
      b_in <= inv;
      act_t := (others => 0);
      seg_t := (others => 0);
      undef := (others => '0');
      t_end := now + ncyc * 10 ns;
      loop
        wait on b_out for t_end - now;
        dt := (now - t_last) / 1 ns;
        if dt > 0 then
          for i in 0 to NB_OUT - 1 loop
            if prev(i) = '1' and ACTIVE(i + 1) = '1' then act_t(i) := act_t(i) + dt; end if;
            if prev(i) = '0' and ACTIVE(i + 1) = '0' then act_t(i) := act_t(i) + dt; end if;
          end loop;
          for d in 0 to 7 loop
            if prev(30 + d) = '0' then
              for s in 0 to 7 loop
                if prev(22 + s) = '0' then seg_t(d * 8 + s) := seg_t(d * 8 + s) + dt; end if;
              end loop;
            end if;
          end loop;
        end if;
        t_last := now;
        prev := b_out;
        for i in 0 to NB_OUT - 1 loop
          if b_out(i) /= '0' and b_out(i) /= '1' then undef(i + 1) := '1'; end if;
        end loop;
        exit when now >= t_end;
      end loop;
      write(lout, string'("@@R "));
      write(lout, ncyc);
      for i in 0 to NB_OUT - 1 loop write(lout, ' '); write(lout, act_t(i)); end loop;
      for i in 0 to 63 loop write(lout, ' '); write(lout, seg_t(i)); end loop;
      write(lout, ' ');
      write(lout, undef);
      writeline(output, lout);
    end loop;
  end process monitor;
end architecture sim;
