"""
EVS II Ü8 — 380 kV, three-node delta (Übertragungsnetz + Kraftwerke/Industrie).
Recreates the Netzschema: Bus 1 = slack, Buses 2–3 = gen + load.
"""

import numpy as np
import pandapower as pp

# Base power for the network (MW/MVA in tables are consistent with 100 MVA if you convert to pu)
S_BASE_MVA = 100.0
U_N_KV = 380.0

# Line data (Tabelle 1): R, C vernachlässigt; only series reactance
X_OHM_PER_KM = 0.3
R_OHM_PER_KM = 0.0
C_NF_PER_KM = 0.0
I_THERMAL_KA = 0.55  # 550 A

# Injections (cos φ = 1 → no reactive in loads/gens)
P_GEN_A_MW = 400.0
P_GEN_B_MW = 500.0
P_LOAD_A_MW = 100.0
P_LOAD_B_MW = 100.0

net = pp.create_empty_network(name="EVS2_A8__380kV", sn_mva=S_BASE_MVA)

# Buses: diagram labels 1, 2, 3 (internal indices will be 0, 1, 2)
b1 = pp.create_bus(net, vn_kv=U_N_KV, name="Bus1_Uebertragungsnetz")
b2 = pp.create_bus(net, vn_kv=U_N_KV, name="Bus2")
b3 = pp.create_bus(net, vn_kv=U_N_KV, name="Bus3")

# Bus 1: reference (starr), θ = 0°, |V| = 1.0 pu
pp.create_ext_grid(
    net,
    bus=b1,
    vm_pu=1.0,
    va_degree=0.0,
    name="ExtGrid_Slack",
)

# Bus 2: Kraftwerk A + Industrie A
pp.create_gen(
    net,
    bus=b2,
    p_mw=P_GEN_A_MW,
    vm_pu=1.0,  # nominal |V| as in the sheet
    name="Kraftwerk_A",
)
pp.create_load(
    net,
    bus=b2,
    p_mw=P_LOAD_A_MW,
    q_mvar=0.0,
    name="Industrie_A",
)

# Bus 3: Kraftwerk B + Industrie B
pp.create_gen(
    net,
    bus=b3,
    p_mw=P_GEN_B_MW,
    vm_pu=1.0,
    name="Kraftwerk_B",
)
pp.create_load(
    net,
    bus=b3,
    p_mw=P_LOAD_B_MW,
    q_mvar=0.0,
    name="Industrie_B",
)

# Three lines: delta — 1–2: 50 km, 1–3: 100 km, 2–3: 150 km
pp.create_line_from_parameters(
    net,
    from_bus=b1,
    to_bus=b2,
    length_km=50.0,
    r_ohm_per_km=R_OHM_PER_KM,
    x_ohm_per_km=X_OHM_PER_KM,
    c_nf_per_km=C_NF_PER_KM,
    max_i_ka=I_THERMAL_KA,
    name="Line_1-2_50km",
)
pp.create_line_from_parameters(
    net,
    from_bus=b1,
    to_bus=b3,
    length_km=100.0,
    r_ohm_per_km=R_OHM_PER_KM,
    x_ohm_per_km=X_OHM_PER_KM,
    c_nf_per_km=C_NF_PER_KM,
    max_i_ka=I_THERMAL_KA,
    name="Line_1-3_100km",
)
pp.create_line_from_parameters(
    net,
    from_bus=b2,
    to_bus=b3,
    length_km=150.0,
    r_ohm_per_km=R_OHM_PER_KM,
    x_ohm_per_km=X_OHM_PER_KM,
    c_nf_per_km=C_NF_PER_KM,
    max_i_ka=I_THERMAL_KA,
    name="Line_2-3_150km",
)

if __name__ == "__main__":
    print(net)
    pp.runpp(net, numba=False)
    theta_rad = np.deg2rad(net.res_bus["va_degree"])
    print("\n", net.res_bus)
    print(
        "\nKnotenwinkel theta_rad (Vergleich Handrechnung, Slack=0):",
        np.asarray(theta_rad),
    )
    print(
        f"  Bus2: {theta_rad[b2]:.6f} rad, Bus3: {theta_rad[b3]:.6f} rad"
    )
    print("\n", net.res_line)
