// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Design implementation internals
// See Vtop.h for the primary calling header

#include "Vtop__pch.h"

void Vtop___024root___eval_triggers_vec__ico(Vtop___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vtop___024root___eval_triggers_vec__ico\n"); );
    Vtop__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    vlSelfRef.__VicoTriggered[0U] = ((0xfffffffffffffffeULL 
                                      & vlSelfRef.__VicoTriggered[0U]) 
                                     | (IData)((IData)(vlSelfRef.__VicoFirstIteration)));
}

bool Vtop___024root___trigger_anySet__ico(const VlUnpacked<QData/*63:0*/, 1> &in) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vtop___024root___trigger_anySet__ico\n"); );
    // Locals
    IData/*31:0*/ n;
    // Body
    n = 0U;
    do {
        if (in[n]) {
            return (1U);
        }
        n = ((IData)(1U) + n);
    } while ((1U > n));
    return (0U);
}

extern const VlUnpacked<SData/*9:0*/, 16> Vtop__ConstPool__TABLE_h34bcea03_0;
extern const VlUnpacked<CData/*7:0*/, 1024> Vtop__ConstPool__TABLE_h4c73514b_0;

void Vtop___024root___ico_sequent__TOP__0(Vtop___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vtop___024root___ico_sequent__TOP__0\n"); );
    Vtop__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Locals
    IData/*31:0*/ Top__DOT__bin2dec__DOT__n41;
    Top__DOT__bin2dec__DOT__n41 = 0;
    SData/*9:0*/ Top__DOT__bin7seg__DOT__n91;
    Top__DOT__bin7seg__DOT__n91 = 0;
    CData/*7:0*/ Top__DOT__bin7seg__DOT__n92;
    Top__DOT__bin7seg__DOT__n92 = 0;
    SData/*9:0*/ __Vtableidx1;
    __Vtableidx1 = 0;
    CData/*3:0*/ __Vtableidx2;
    __Vtableidx2 = 0;
    // Body
    Top__DOT__bin2dec__DOT__n41 = (0x0000001fU & ((4U 
                                                   == (IData)(vlSelfRef.Top__DOT__mux31__DOT__n35))
                                                   ? 
                                                  VL_SHIFTL_III(5,5,31, (IData)(vlSelfRef.A), 1U)
                                                   : 
                                                  ((2U 
                                                    == (IData)(vlSelfRef.Top__DOT__mux31__DOT__n35))
                                                    ? 
                                                   ((IData)(1U) 
                                                    + 
                                                    (~ (IData)(vlSelfRef.A)))
                                                    : 
                                                   ((1U 
                                                     == (IData)(vlSelfRef.Top__DOT__mux31__DOT__n35))
                                                     ? (IData)(vlSelfRef.A)
                                                     : 0U))));
    __Vtableidx2 = (0x0000000fU & ((2U == (IData)(vlSelfRef.Top__DOT__mux21__DOT__n57))
                                    ? VL_DIVS_III(32, Top__DOT__bin2dec__DOT__n41, (IData)(0x0000000aU))
                                    : ((1U == (IData)(vlSelfRef.Top__DOT__mux21__DOT__n57))
                                        ? VL_MODDIV_III(32, Top__DOT__bin2dec__DOT__n41, (IData)(0x0000000aU))
                                        : 0U)));
    Top__DOT__bin7seg__DOT__n91 = Vtop__ConstPool__TABLE_h34bcea03_0
        [__Vtableidx2];
    __Vtableidx1 = Top__DOT__bin7seg__DOT__n91;
    Top__DOT__bin7seg__DOT__n92 = Vtop__ConstPool__TABLE_h4c73514b_0
        [__Vtableidx1];
    vlSelfRef.SEVEN_SEG = Top__DOT__bin7seg__DOT__n92;
}

void Vtop___024root___eval_ico(Vtop___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vtop___024root___eval_ico\n"); );
    Vtop__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Locals
    IData/*31:0*/ __Vinline__ico_sequent__TOP__0_Top__DOT__bin2dec__DOT__n41;
    __Vinline__ico_sequent__TOP__0_Top__DOT__bin2dec__DOT__n41 = 0;
    SData/*9:0*/ __Vinline__ico_sequent__TOP__0_Top__DOT__bin7seg__DOT__n91;
    __Vinline__ico_sequent__TOP__0_Top__DOT__bin7seg__DOT__n91 = 0;
    CData/*7:0*/ __Vinline__ico_sequent__TOP__0_Top__DOT__bin7seg__DOT__n92;
    __Vinline__ico_sequent__TOP__0_Top__DOT__bin7seg__DOT__n92 = 0;
    SData/*9:0*/ __Vinline__ico_sequent__TOP__0___Vtableidx1;
    __Vinline__ico_sequent__TOP__0___Vtableidx1 = 0;
    CData/*3:0*/ __Vinline__ico_sequent__TOP__0___Vtableidx2;
    __Vinline__ico_sequent__TOP__0___Vtableidx2 = 0;
    // Body
    if ((1ULL & vlSelfRef.__VicoTriggered[0U])) {
        __Vinline__ico_sequent__TOP__0_Top__DOT__bin2dec__DOT__n41 
            = (0x0000001fU & ((4U == (IData)(vlSelfRef.Top__DOT__mux31__DOT__n35))
                               ? VL_SHIFTL_III(5,5,31, (IData)(vlSelfRef.A), 1U)
                               : ((2U == (IData)(vlSelfRef.Top__DOT__mux31__DOT__n35))
                                   ? ((IData)(1U) + 
                                      (~ (IData)(vlSelfRef.A)))
                                   : ((1U == (IData)(vlSelfRef.Top__DOT__mux31__DOT__n35))
                                       ? (IData)(vlSelfRef.A)
                                       : 0U))));
        __Vinline__ico_sequent__TOP__0___Vtableidx2 
            = (0x0000000fU & ((2U == (IData)(vlSelfRef.Top__DOT__mux21__DOT__n57))
                               ? VL_DIVS_III(32, __Vinline__ico_sequent__TOP__0_Top__DOT__bin2dec__DOT__n41, (IData)(0x0000000aU))
                               : ((1U == (IData)(vlSelfRef.Top__DOT__mux21__DOT__n57))
                                   ? VL_MODDIV_III(32, __Vinline__ico_sequent__TOP__0_Top__DOT__bin2dec__DOT__n41, (IData)(0x0000000aU))
                                   : 0U)));
        __Vinline__ico_sequent__TOP__0_Top__DOT__bin7seg__DOT__n91 
            = Vtop__ConstPool__TABLE_h34bcea03_0[__Vinline__ico_sequent__TOP__0___Vtableidx2];
        __Vinline__ico_sequent__TOP__0___Vtableidx1 
            = __Vinline__ico_sequent__TOP__0_Top__DOT__bin7seg__DOT__n91;
        __Vinline__ico_sequent__TOP__0_Top__DOT__bin7seg__DOT__n92 
            = Vtop__ConstPool__TABLE_h4c73514b_0[__Vinline__ico_sequent__TOP__0___Vtableidx1];
        vlSelfRef.SEVEN_SEG = __Vinline__ico_sequent__TOP__0_Top__DOT__bin7seg__DOT__n92;
    }
}

#ifdef VL_DEBUG
VL_ATTR_COLD void Vtop___024root___dump_triggers__ico(const VlUnpacked<QData/*63:0*/, 1> &triggers, const std::string &tag);
#endif  // VL_DEBUG

bool Vtop___024root___eval_phase__ico(Vtop___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vtop___024root___eval_phase__ico\n"); );
    Vtop__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Locals
    CData/*0:0*/ __VicoExecute;
    // Body
    Vtop___024root___eval_triggers_vec__ico(vlSelf);
#ifdef VL_DEBUG
    if (VL_UNLIKELY(vlSymsp->_vm_contextp__->debug())) {
        Vtop___024root___dump_triggers__ico(vlSelfRef.__VicoTriggered, "ico"s);
    }
#endif
    __VicoExecute = Vtop___024root___trigger_anySet__ico(vlSelfRef.__VicoTriggered);
    if (__VicoExecute) {
        Vtop___024root___eval_ico(vlSelf);
    }
    return (__VicoExecute);
}

void Vtop___024root___eval_triggers_vec__act(Vtop___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vtop___024root___eval_triggers_vec__act\n"); );
    Vtop__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    vlSelfRef.__VactTriggered[0U] = (QData)((IData)(
                                                    ((IData)(vlSelfRef.CLOCK) 
                                                     & (~ (IData)(vlSelfRef.__Vtrigprevexpr___TOP__CLOCK__0)))));
    vlSelfRef.__Vtrigprevexpr___TOP__CLOCK__0 = vlSelfRef.CLOCK;
}

bool Vtop___024root___trigger_anySet__act(const VlUnpacked<QData/*63:0*/, 1> &in) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vtop___024root___trigger_anySet__act\n"); );
    // Locals
    IData/*31:0*/ n;
    // Body
    n = 0U;
    do {
        if (in[n]) {
            return (1U);
        }
        n = ((IData)(1U) + n);
    } while ((1U > n));
    return (0U);
}

void Vtop___024root___nba_sequent__TOP__0(Vtop___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vtop___024root___nba_sequent__TOP__0\n"); );
    Vtop__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Locals
    IData/*31:0*/ Top__DOT__bin2dec__DOT__n41;
    Top__DOT__bin2dec__DOT__n41 = 0;
    SData/*9:0*/ Top__DOT__bin7seg__DOT__n91;
    Top__DOT__bin7seg__DOT__n91 = 0;
    CData/*7:0*/ Top__DOT__bin7seg__DOT__n92;
    Top__DOT__bin7seg__DOT__n92 = 0;
    CData/*0:0*/ Top__DOT__gestaffi__DOT__n122;
    Top__DOT__gestaffi__DOT__n122 = 0;
    CData/*0:0*/ Top__DOT__gestaffi__DOT__n123;
    Top__DOT__gestaffi__DOT__n123 = 0;
    CData/*0:0*/ Top__DOT__gestaffi__DOT__n124;
    Top__DOT__gestaffi__DOT__n124 = 0;
    CData/*0:0*/ Top__DOT__gestaffi__DOT__n125;
    Top__DOT__gestaffi__DOT__n125 = 0;
    SData/*9:0*/ __Vtableidx1;
    __Vtableidx1 = 0;
    CData/*3:0*/ __Vtableidx2;
    __Vtableidx2 = 0;
    // Body
    vlSelfRef.Top__DOT__gestaffi__DOT__n117 = vlSelfRef.Top__DOT__gestaffi__DOT__n102;
    vlSelfRef.Top__DOT__gestaffi__DOT__n102 = (0x000fffffU 
                                               & ((IData)(1U) 
                                                  + vlSelfRef.Top__DOT__gestaffi__DOT__n117));
    Top__DOT__gestaffi__DOT__n125 = (IData)((0x000c0000U 
                                             == (0x000c0000U 
                                                 & vlSelfRef.Top__DOT__gestaffi__DOT__n117)));
    Top__DOT__gestaffi__DOT__n124 = (IData)((0x00080000U 
                                             == (0x000c0000U 
                                                 & vlSelfRef.Top__DOT__gestaffi__DOT__n117)));
    Top__DOT__gestaffi__DOT__n123 = (IData)((0x00040000U 
                                             == (0x000c0000U 
                                                 & vlSelfRef.Top__DOT__gestaffi__DOT__n117)));
    Top__DOT__gestaffi__DOT__n122 = (IData)((0U == 
                                             (0x000c0000U 
                                              & vlSelfRef.Top__DOT__gestaffi__DOT__n117)));
    vlSelfRef.Top__DOT__mux21__DOT__n57 = ((2U & (vlSelfRef.Top__DOT__gestaffi__DOT__n117 
                                                  >> 0x00000010U)) 
                                           | (1U & 
                                              (~ (vlSelfRef.Top__DOT__gestaffi__DOT__n117 
                                                  >> 0x00000011U))));
    vlSelfRef.Top__DOT__mux31__DOT__n35 = (((2U == 
                                             (3U & 
                                              (vlSelfRef.Top__DOT__gestaffi__DOT__n117 
                                               >> 0x00000012U))) 
                                            << 2U) 
                                           | (((1U 
                                                == 
                                                (3U 
                                                 & (vlSelfRef.Top__DOT__gestaffi__DOT__n117 
                                                    >> 0x00000012U))) 
                                               << 1U) 
                                              | (0U 
                                                 == 
                                                 (3U 
                                                  & (vlSelfRef.Top__DOT__gestaffi__DOT__n117 
                                                     >> 0x00000012U)))));
    vlSelfRef.A_N = (0x000000ffU & (~ (((((0x0000fffeU 
                                           & (((IData)(Top__DOT__gestaffi__DOT__n125) 
                                               << 1U) 
                                              & (vlSelfRef.Top__DOT__gestaffi__DOT__n117 
                                                 >> 0x00000010U))) 
                                          | ((~ (vlSelfRef.Top__DOT__gestaffi__DOT__n117 
                                                 >> 0x00000011U)) 
                                             & (IData)(Top__DOT__gestaffi__DOT__n125))) 
                                         << 6U) | (
                                                   ((0x0000fffeU 
                                                     & (((IData)(Top__DOT__gestaffi__DOT__n124) 
                                                         << 1U) 
                                                        & (vlSelfRef.Top__DOT__gestaffi__DOT__n117 
                                                           >> 0x00000010U))) 
                                                    | ((~ 
                                                        (vlSelfRef.Top__DOT__gestaffi__DOT__n117 
                                                         >> 0x00000011U)) 
                                                       & (IData)(Top__DOT__gestaffi__DOT__n124))) 
                                                   << 4U)) 
                                       | ((((0x0000fffeU 
                                             & (((IData)(Top__DOT__gestaffi__DOT__n123) 
                                                 << 1U) 
                                                & (vlSelfRef.Top__DOT__gestaffi__DOT__n117 
                                                   >> 0x00000010U))) 
                                            | ((~ (vlSelfRef.Top__DOT__gestaffi__DOT__n117 
                                                   >> 0x00000011U)) 
                                               & (IData)(Top__DOT__gestaffi__DOT__n123))) 
                                           << 2U) | 
                                          ((0x0000fffeU 
                                            & (((IData)(Top__DOT__gestaffi__DOT__n122) 
                                                << 1U) 
                                               & (vlSelfRef.Top__DOT__gestaffi__DOT__n117 
                                                  >> 0x00000010U))) 
                                           | ((~ (vlSelfRef.Top__DOT__gestaffi__DOT__n117 
                                                  >> 0x00000011U)) 
                                              & (IData)(Top__DOT__gestaffi__DOT__n122)))))));
    Top__DOT__bin2dec__DOT__n41 = (0x0000001fU & ((4U 
                                                   == (IData)(vlSelfRef.Top__DOT__mux31__DOT__n35))
                                                   ? 
                                                  VL_SHIFTL_III(5,5,31, (IData)(vlSelfRef.A), 1U)
                                                   : 
                                                  ((2U 
                                                    == (IData)(vlSelfRef.Top__DOT__mux31__DOT__n35))
                                                    ? 
                                                   ((IData)(1U) 
                                                    + 
                                                    (~ (IData)(vlSelfRef.A)))
                                                    : 
                                                   ((1U 
                                                     == (IData)(vlSelfRef.Top__DOT__mux31__DOT__n35))
                                                     ? (IData)(vlSelfRef.A)
                                                     : 0U))));
    __Vtableidx2 = (0x0000000fU & ((2U == (IData)(vlSelfRef.Top__DOT__mux21__DOT__n57))
                                    ? VL_DIVS_III(32, Top__DOT__bin2dec__DOT__n41, (IData)(0x0000000aU))
                                    : ((1U == (IData)(vlSelfRef.Top__DOT__mux21__DOT__n57))
                                        ? VL_MODDIV_III(32, Top__DOT__bin2dec__DOT__n41, (IData)(0x0000000aU))
                                        : 0U)));
    Top__DOT__bin7seg__DOT__n91 = Vtop__ConstPool__TABLE_h34bcea03_0
        [__Vtableidx2];
    __Vtableidx1 = Top__DOT__bin7seg__DOT__n91;
    Top__DOT__bin7seg__DOT__n92 = Vtop__ConstPool__TABLE_h4c73514b_0
        [__Vtableidx1];
    vlSelfRef.SEVEN_SEG = Top__DOT__bin7seg__DOT__n92;
}

void Vtop___024root___eval_nba(Vtop___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vtop___024root___eval_nba\n"); );
    Vtop__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    if ((1ULL & vlSelfRef.__VnbaTriggered[0U])) {
        Vtop___024root___nba_sequent__TOP__0(vlSelf);
    }
}

void Vtop___024root___trigger_orInto__act_vec_vec(VlUnpacked<QData/*63:0*/, 1> &out, const VlUnpacked<QData/*63:0*/, 1> &in) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vtop___024root___trigger_orInto__act_vec_vec\n"); );
    // Locals
    IData/*31:0*/ n;
    // Body
    n = 0U;
    do {
        out[n] = (out[n] | in[n]);
        n = ((IData)(1U) + n);
    } while ((0U >= n));
}

#ifdef VL_DEBUG
VL_ATTR_COLD void Vtop___024root___dump_triggers__act(const VlUnpacked<QData/*63:0*/, 1> &triggers, const std::string &tag);
#endif  // VL_DEBUG

bool Vtop___024root___eval_phase__act(Vtop___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vtop___024root___eval_phase__act\n"); );
    Vtop__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    Vtop___024root___eval_triggers_vec__act(vlSelf);
#ifdef VL_DEBUG
    if (VL_UNLIKELY(vlSymsp->_vm_contextp__->debug())) {
        Vtop___024root___dump_triggers__act(vlSelfRef.__VactTriggered, "act"s);
    }
#endif
    Vtop___024root___trigger_orInto__act_vec_vec(vlSelfRef.__VnbaTriggered, vlSelfRef.__VactTriggered);
    return (0U);
}

void Vtop___024root___trigger_clear__act(VlUnpacked<QData/*63:0*/, 1> &out) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vtop___024root___trigger_clear__act\n"); );
    // Locals
    IData/*31:0*/ n;
    // Body
    n = 0U;
    do {
        out[n] = 0ULL;
        n = ((IData)(1U) + n);
    } while ((1U > n));
}

bool Vtop___024root___eval_phase__nba(Vtop___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vtop___024root___eval_phase__nba\n"); );
    Vtop__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Locals
    CData/*0:0*/ __VnbaExecute;
    // Body
    __VnbaExecute = Vtop___024root___trigger_anySet__act(vlSelfRef.__VnbaTriggered);
    if (__VnbaExecute) {
        Vtop___024root___eval_nba(vlSelf);
        Vtop___024root___trigger_clear__act(vlSelfRef.__VnbaTriggered);
    }
    return (__VnbaExecute);
}

void Vtop___024root___eval(Vtop___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vtop___024root___eval\n"); );
    Vtop__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Locals
    IData/*31:0*/ __VicoIterCount;
    IData/*31:0*/ __VnbaIterCount;
    // Body
    __VicoIterCount = 0U;
    vlSelfRef.__VicoFirstIteration = 1U;
    do {
        if (VL_UNLIKELY(((0x00000064U < __VicoIterCount)))) {
#ifdef VL_DEBUG
            Vtop___024root___dump_triggers__ico(vlSelfRef.__VicoTriggered, "ico"s);
#endif
            VL_FATAL_MT("/home/arth/Documents/Outils/nexys-sim/.build/labo4-8fb93999/verilator/top.v", 312, "", "DIDNOTCONVERGE: Input combinational region did not converge after '--converge-limit' of 100 tries");
        }
        __VicoIterCount = ((IData)(1U) + __VicoIterCount);
        vlSelfRef.__VicoPhaseResult = Vtop___024root___eval_phase__ico(vlSelf);
        vlSelfRef.__VicoFirstIteration = 0U;
    } while (vlSelfRef.__VicoPhaseResult);
    __VnbaIterCount = 0U;
    do {
        if (VL_UNLIKELY(((0x00000064U < __VnbaIterCount)))) {
#ifdef VL_DEBUG
            Vtop___024root___dump_triggers__act(vlSelfRef.__VnbaTriggered, "nba"s);
#endif
            VL_FATAL_MT("/home/arth/Documents/Outils/nexys-sim/.build/labo4-8fb93999/verilator/top.v", 312, "", "DIDNOTCONVERGE: NBA region did not converge after '--converge-limit' of 100 tries");
        }
        __VnbaIterCount = ((IData)(1U) + __VnbaIterCount);
        vlSelfRef.__VactIterCount = 0U;
        do {
            if (VL_UNLIKELY(((0x00000064U < vlSelfRef.__VactIterCount)))) {
#ifdef VL_DEBUG
                Vtop___024root___dump_triggers__act(vlSelfRef.__VactTriggered, "act"s);
#endif
                VL_FATAL_MT("/home/arth/Documents/Outils/nexys-sim/.build/labo4-8fb93999/verilator/top.v", 312, "", "DIDNOTCONVERGE: Active region did not converge after '--converge-limit' of 100 tries");
            }
            vlSelfRef.__VactIterCount = ((IData)(1U) 
                                         + vlSelfRef.__VactIterCount);
            vlSelfRef.__VactPhaseResult = Vtop___024root___eval_phase__act(vlSelf);
        } while (vlSelfRef.__VactPhaseResult);
        vlSelfRef.__VnbaPhaseResult = Vtop___024root___eval_phase__nba(vlSelf);
    } while (vlSelfRef.__VnbaPhaseResult);
}

#ifdef VL_DEBUG
void Vtop___024root___eval_debug_assertions(Vtop___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vtop___024root___eval_debug_assertions\n"); );
    Vtop__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    if (VL_UNLIKELY(((vlSelfRef.A & 0xe0U)))) {
        Verilated::overWidthError("A");
    }
    if (VL_UNLIKELY(((vlSelfRef.CLOCK & 0xfeU)))) {
        Verilated::overWidthError("CLOCK");
    }
}
#endif  // VL_DEBUG
