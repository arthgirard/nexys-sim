// Généré par nexys_sim.py : ne pas modifier.
// Même protocole que le banc VHDL : lit "<entrées> <cycles>", écrit "@@R ...".
#include "Vtop.h"
#include "verilated.h"
#include <cstdint>
#include <cstdio>
#include <cstdlib>
#include <memory>

static const int NB_IN = 22, NB_OUT = 38, SEG0 = 22, AN0 = 30;
static const uint64_t ACTIVE_HIGH = 4194303ULL;  // bit k = 1 : sortie k active à '1'
static Vtop* top;

static inline void drive(uint32_t in, int clk) {
  top->A = ((uint64_t)((in >> 0) & 1) << 0) | ((uint64_t)((in >> 1) & 1) << 1) | ((uint64_t)((in >> 2) & 1) << 2) | ((uint64_t)((in >> 3) & 1) << 3) | ((uint64_t)((in >> 4) & 1) << 4);
  top->CLOCK = (uint64_t)clk;
}

static inline uint64_t pack() {
  uint64_t v = 0ULL;
  v |= (((uint64_t)top->SEVEN_SEG >> 0) & 1) << 22;
  v |= (((uint64_t)top->SEVEN_SEG >> 1) & 1) << 23;
  v |= (((uint64_t)top->SEVEN_SEG >> 2) & 1) << 24;
  v |= (((uint64_t)top->SEVEN_SEG >> 3) & 1) << 25;
  v |= (((uint64_t)top->SEVEN_SEG >> 4) & 1) << 26;
  v |= (((uint64_t)top->SEVEN_SEG >> 5) & 1) << 27;
  v |= (((uint64_t)top->SEVEN_SEG >> 6) & 1) << 28;
  v |= (((uint64_t)top->SEVEN_SEG >> 7) & 1) << 29;
  v |= (((uint64_t)top->A_N >> 0) & 1) << 30;
  v |= (((uint64_t)top->A_N >> 1) & 1) << 31;
  v |= (((uint64_t)top->A_N >> 2) & 1) << 32;
  v |= (((uint64_t)top->A_N >> 3) & 1) << 33;
  v |= (((uint64_t)top->A_N >> 4) & 1) << 34;
  v |= (((uint64_t)top->A_N >> 5) & 1) << 35;
  v |= (((uint64_t)top->A_N >> 6) & 1) << 36;
  v |= (((uint64_t)top->A_N >> 7) & 1) << 37;
  return v;
}

int main() {
  auto ctx = std::make_unique<VerilatedContext>();
  top = new Vtop{ctx.get()};
  drive(0, 0);
  top->eval();
  uint64_t prev = pack();
  static char line[512];
  while (fgets(line, sizeof line, stdin)) {
    uint32_t in = 0;
    for (int i = 0; i < NB_IN; i++) if (line[i] == '1') in |= 1u << i;
    long long ncyc = strtoll(line + NB_IN, nullptr, 10);
    long long act[NB_OUT] = {0}, seg[64] = {0};
    long long t_last = 0;
    auto account = [&](long long now) {
      long long dt = now - t_last;
      if (dt > 0) {
        uint64_t on = ~(prev ^ ACTIVE_HIGH);  // bit = 1 si la sortie est à son niveau actif
        for (int i = 0; i < NB_OUT; i++) if ((on >> i) & 1) act[i] += dt;
        for (int d = 0; d < 8; d++)
          if (!((prev >> (AN0 + d)) & 1))
            for (int s = 0; s < 8; s++)
              if (!((prev >> (SEG0 + s)) & 1)) seg[d * 8 + s] += dt;
      }
      t_last = now;
    };
    drive(in, 0);
    top->eval();
    prev = pack();
    if (true) {
      for (long long c = 0; c < ncyc; c++) {
        long long t0 = c * 10;
        drive(in, 1); top->eval();
        uint64_t cur = pack();
        if (cur != prev) { account(t0 + 5); prev = cur; }
        drive(in, 0); top->eval();
        cur = pack();
        if (cur != prev) { account(t0 + 10); prev = cur; }
      }
    }
    account(ncyc * 10);
    printf("@@R %lld", ncyc);
    for (int i = 0; i < NB_OUT; i++) printf(" %lld", act[i]);
    for (int i = 0; i < 64; i++) printf(" %lld", seg[i]);
    printf(" ");
    for (int i = 0; i < NB_OUT; i++) putchar('0');
    putchar('\n');
    fflush(stdout);
  }
  top->final();
  delete top;
  return 0;
}
