// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Design implementation internals
// See Vtop.h for the primary calling header

#include "Vtop__pch.h"

VL_ATTR_COLD void Vtop___024root___eval_static(Vtop___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vtop___024root___eval_static\n"); );
    Vtop__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    vlSelfRef.__Vtrigprevexpr___TOP__CLOCK__0 = vlSelfRef.CLOCK;
}

VL_ATTR_COLD void Vtop___024root___eval_initial(Vtop___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vtop___024root___eval_initial\n"); );
    Vtop__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    vlSelfRef.Top__DOT__gestaffi__DOT__n117 = 0U;
}

VL_ATTR_COLD void Vtop___024root___eval_initial__TOP(Vtop___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vtop___024root___eval_initial__TOP\n"); );
    Vtop__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    vlSelfRef.Top__DOT__gestaffi__DOT__n117 = 0U;
}

VL_ATTR_COLD void Vtop___024root___eval_final(Vtop___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vtop___024root___eval_final\n"); );
    Vtop__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
}

#ifdef VL_DEBUG
VL_ATTR_COLD void Vtop___024root___dump_triggers__stl(const VlUnpacked<QData/*63:0*/, 1> &triggers, const std::string &tag);
#endif  // VL_DEBUG
VL_ATTR_COLD bool Vtop___024root___eval_phase__stl(Vtop___024root* vlSelf);

VL_ATTR_COLD void Vtop___024root___eval_settle(Vtop___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vtop___024root___eval_settle\n"); );
    Vtop__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Locals
    IData/*31:0*/ __VstlIterCount;
    // Body
    __VstlIterCount = 0U;
    vlSelfRef.__VstlFirstIteration = 1U;
    do {
        if (VL_UNLIKELY(((0x00000064U < __VstlIterCount)))) {
#ifdef VL_DEBUG
            Vtop___024root___dump_triggers__stl(vlSelfRef.__VstlTriggered, "stl"s);
#endif
            VL_FATAL_MT("/home/arth/Documents/Outils/nexys-sim/.build/labo4-b3e989f8/verilator/top.v", 312, "", "DIDNOTCONVERGE: Settle region did not converge after '--converge-limit' of 100 tries");
        }
        __VstlIterCount = ((IData)(1U) + __VstlIterCount);
        vlSelfRef.__VstlPhaseResult = Vtop___024root___eval_phase__stl(vlSelf);
        vlSelfRef.__VstlFirstIteration = 0U;
    } while (vlSelfRef.__VstlPhaseResult);
}

VL_ATTR_COLD void Vtop___024root___eval_triggers_vec__stl(Vtop___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vtop___024root___eval_triggers_vec__stl\n"); );
    Vtop__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    vlSelfRef.__VstlTriggered[0U] = ((0xfffffffffffffffeULL 
                                      & vlSelfRef.__VstlTriggered[0U]) 
                                     | (IData)((IData)(vlSelfRef.__VstlFirstIteration)));
}

VL_ATTR_COLD bool Vtop___024root___trigger_anySet__stl(const VlUnpacked<QData/*63:0*/, 1> &in);

#ifdef VL_DEBUG
VL_ATTR_COLD void Vtop___024root___dump_triggers__stl(const VlUnpacked<QData/*63:0*/, 1> &triggers, const std::string &tag) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vtop___024root___dump_triggers__stl\n"); );
    // Body
    if ((1U & (~ (IData)(Vtop___024root___trigger_anySet__stl(triggers))))) {
        VL_DBG_MSGS("         No '" + tag + "' region triggers active\n");
    }
    if ((1U & (IData)(triggers[0U]))) {
        VL_DBG_MSGS("         '" + tag + "' region trigger index 0 is active: Internal 'stl' trigger - first iteration\n");
    }
}
#endif  // VL_DEBUG

VL_ATTR_COLD bool Vtop___024root___trigger_anySet__stl(const VlUnpacked<QData/*63:0*/, 1> &in) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vtop___024root___trigger_anySet__stl\n"); );
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

VL_ATTR_COLD void Vtop___024root___stl_sequent__TOP__0(Vtop___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vtop___024root___stl_sequent__TOP__0\n"); );
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

VL_ATTR_COLD void Vtop___024root___eval_stl(Vtop___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vtop___024root___eval_stl\n"); );
    Vtop__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    if ((1ULL & vlSelfRef.__VstlTriggered[0U])) {
        Vtop___024root___stl_sequent__TOP__0(vlSelf);
    }
}

VL_ATTR_COLD bool Vtop___024root___eval_phase__stl(Vtop___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vtop___024root___eval_phase__stl\n"); );
    Vtop__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Locals
    CData/*0:0*/ __VstlExecute;
    // Body
    Vtop___024root___eval_triggers_vec__stl(vlSelf);
#ifdef VL_DEBUG
    if (VL_UNLIKELY(vlSymsp->_vm_contextp__->debug())) {
        Vtop___024root___dump_triggers__stl(vlSelfRef.__VstlTriggered, "stl"s);
    }
#endif
    __VstlExecute = Vtop___024root___trigger_anySet__stl(vlSelfRef.__VstlTriggered);
    if (__VstlExecute) {
        Vtop___024root___eval_stl(vlSelf);
    }
    return (__VstlExecute);
}

bool Vtop___024root___trigger_anySet__ico(const VlUnpacked<QData/*63:0*/, 1> &in);

#ifdef VL_DEBUG
VL_ATTR_COLD void Vtop___024root___dump_triggers__ico(const VlUnpacked<QData/*63:0*/, 1> &triggers, const std::string &tag) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vtop___024root___dump_triggers__ico\n"); );
    // Body
    if ((1U & (~ (IData)(Vtop___024root___trigger_anySet__ico(triggers))))) {
        VL_DBG_MSGS("         No '" + tag + "' region triggers active\n");
    }
    if ((1U & (IData)(triggers[0U]))) {
        VL_DBG_MSGS("         '" + tag + "' region trigger index 0 is active: Internal 'ico' trigger - first iteration\n");
    }
}
#endif  // VL_DEBUG

bool Vtop___024root___trigger_anySet__act(const VlUnpacked<QData/*63:0*/, 1> &in);

#ifdef VL_DEBUG
VL_ATTR_COLD void Vtop___024root___dump_triggers__act(const VlUnpacked<QData/*63:0*/, 1> &triggers, const std::string &tag) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vtop___024root___dump_triggers__act\n"); );
    // Body
    if ((1U & (~ (IData)(Vtop___024root___trigger_anySet__act(triggers))))) {
        VL_DBG_MSGS("         No '" + tag + "' region triggers active\n");
    }
    if ((1U & (IData)(triggers[0U]))) {
        VL_DBG_MSGS("         '" + tag + "' region trigger index 0 is active: @(posedge CLOCK)\n");
    }
}
#endif  // VL_DEBUG

VL_ATTR_COLD void Vtop___024root___ctor_var_reset(Vtop___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vtop___024root___ctor_var_reset\n"); );
    Vtop__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    const uint64_t __VscopeHash = VL_MURMUR64_HASH(vlSelf->vlNamep);
    vlSelf->A = VL_SCOPED_RAND_RESET_I(5, __VscopeHash, 3969090544990846983ull);
    vlSelf->CLOCK = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 16934430937139784228ull);
    vlSelf->SEVEN_SEG = VL_SCOPED_RAND_RESET_I(8, __VscopeHash, 13154064712951660143ull);
    vlSelf->A_N = VL_SCOPED_RAND_RESET_I(8, __VscopeHash, 7522602863178325244ull);
    vlSelf->Top__DOT__mux31__DOT__n35 = VL_SCOPED_RAND_RESET_I(3, __VscopeHash, 5597302996148216490ull);
    vlSelf->Top__DOT__mux21__DOT__n57 = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 13924848201662234758ull);
    vlSelf->Top__DOT__gestaffi__DOT__n102 = VL_SCOPED_RAND_RESET_I(20, __VscopeHash, 3759347201973850082ull);
    vlSelf->Top__DOT__gestaffi__DOT__n117 = VL_SCOPED_RAND_RESET_I(20, __VscopeHash, 5425948665998756901ull);
    for (int __Vi0 = 0; __Vi0 < 1; ++__Vi0) {
        vlSelf->__VstlTriggered[__Vi0] = 0;
    }
    for (int __Vi0 = 0; __Vi0 < 1; ++__Vi0) {
        vlSelf->__VicoTriggered[__Vi0] = 0;
    }
    for (int __Vi0 = 0; __Vi0 < 1; ++__Vi0) {
        vlSelf->__VactTriggered[__Vi0] = 0;
    }
    vlSelf->__Vtrigprevexpr___TOP__CLOCK__0 = 0;
    for (int __Vi0 = 0; __Vi0 < 1; ++__Vi0) {
        vlSelf->__VnbaTriggered[__Vi0] = 0;
    }
}
