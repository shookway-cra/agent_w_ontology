"""Scenario definition: order of battle, platform/weapon kinematics and the scripted
engagement plan for the synthetic AFSIM run "BALTIC SHIELD".

This module is the single source of truth used by:
  * generate_sim_data.py  -> data/afsim_run.sqlite   (what the simulation *emits*)
  * build_orbat_ttl.py    -> ontology/scenario_orbat.ttl (what the ontology *knows*)

Only raw simulation strings (callsigns, sim type names, side) end up in the SQLite file.
Chain of command, nationality and type semantics end up only in the ontology.
"""
from dataclasses import dataclass, field

# ---------------------------------------------------------------------------
# Order of battle
# ---------------------------------------------------------------------------

@dataclass
class Unit:
    id: str
    label: str
    echelon: str              # bs:Echelon local name
    nation: str               # bs:Nation local name
    service: str              # Air | Land | Maritime
    children: list = field(default_factory=list)
    # (callsigns, sim platform type)
    platforms: list = field(default_factory=list)


def cs(prefix, *nums):
    return [f"{prefix}{n}" for n in nums]


BLUE = Unit("CJTF_BalticShield", "Combined Joint Task Force BALTIC SHIELD", "JointForce", "USA", "Land", children=[
    Unit("CFACC", "Combined Force Air Component Command", "Component", "USA", "Air", children=[
        Unit("FW388", "388th Fighter Wing", "Brigade", "USA", "Air", children=[
            Unit("FS4", "4th Fighter Squadron", "Battalion", "USA", "Air",
                 platforms=[(cs("LIGHTNING", 11, 12, 13, 14, 21, 22, 23, 24), "F-35A")]),
        ]),
        Unit("FW52", "52nd Fighter Wing", "Brigade", "USA", "Air", children=[
            Unit("FS480", "480th Fighter Squadron", "Battalion", "USA", "Air",
                 platforms=[(cs("WEASEL", 11, 12, 13, 14, 21, 22, 23, 24), "F-16CM_BLK50")]),
        ]),
        Unit("FW4", "4th Fighter Wing", "Brigade", "USA", "Air", children=[
            Unit("FS336", "336th Fighter Squadron", "Battalion", "USA", "Air",
                 platforms=[(cs("RAZOR", 11, 12, 13, 14), "F-15EX")]),
        ]),
        Unit("BW7", "7th Bomb Wing", "Brigade", "USA", "Air", children=[
            Unit("BS9", "9th Bomb Squadron", "Battalion", "USA", "Air",
                 platforms=[(cs("BONE", 11, 12), "B-1B")]),
        ]),
        Unit("ACW552", "552nd Air Control Wing", "Brigade", "USA", "Air", children=[
            Unit("AACS960", "960th Airborne Air Control Squadron", "Battalion", "USA", "Air",
                 platforms=[(["DARKSTAR01"], "E-3G")]),
        ]),
        Unit("ARW22", "22nd Air Refueling Wing", "Brigade", "USA", "Air", children=[
            Unit("ARS344", "344th Air Refueling Squadron", "Battalion", "USA", "Air",
                 platforms=[(["SHELL71"], "KC-46A")]),
        ]),
        Unit("WG432", "432nd Wing", "Brigade", "USA", "Air", children=[
            Unit("ATKS42", "42nd Attack Squadron", "Battalion", "USA", "Air",
                 platforms=[(cs("REAPER", 41, 42), "MQ-9A")]),
        ]),
        Unit("EAW140", "140 Expeditionary Air Wing (RAF)", "Brigade", "GBR", "Air", children=[
            Unit("SQN_IXB", "IX(B) Squadron RAF", "Battalion", "GBR", "Air",
                 platforms=[(cs("RAPIER", 1, 2, 3, 4), "EF2000_FGR4")]),
        ]),
        Unit("MOB_Northstar_Unit", "Main Operating Base NORTHSTAR", "Brigade", "USA", "Air",
             platforms=[(["MOB_NORTHSTAR"], "AIRBASE_FACILITY")]),
    ]),
    Unit("CFLCC", "Combined Force Land Component Command", "Component", "USA", "Land", children=[
        Unit("ID3", "3rd Infantry Division", "Division", "USA", "Land", children=[
            Unit("ABCT1", "1st Armored Brigade Combat Team, 3ID", "Brigade", "USA", "Land", children=[
                Unit("IN2_7", "2nd Battalion, 7th Infantry", "Battalion", "USA", "Land", children=[
                    Unit("IN2_7_A", "A Company, 2-7 IN", "Company", "USA", "Land",
                         platforms=[(cs("COBRA", 11, 12, 13, 14), "M2A4")]),
                    Unit("IN2_7_B", "B Company, 2-7 IN", "Company", "USA", "Land",
                         platforms=[(cs("BLADE", 11, 12, 13, 14), "M2A4")]),
                    Unit("IN2_7_LM", "Loitering Munition Section, 2-7 IN", "Platoon", "USA", "Land",
                         platforms=[(cs("LASSO", 11, 12), "SB600_TEAM")]),
                ]),
                Unit("AR3_69", "3rd Battalion, 69th Armor", "Battalion", "USA", "Land", children=[
                    Unit("AR3_69_A", "A Company, 3-69 AR", "Company", "USA", "Land",
                         platforms=[(cs("IRON", 11, 12, 13, 14), "M1A2_SEPV3")]),
                    Unit("AR3_69_B", "B Company, 3-69 AR", "Company", "USA", "Land",
                         platforms=[(cs("BANDIT", 11, 12, 13, 14), "M1A2_SEPV3")]),
                ]),
                Unit("FA1_10", "1st Battalion, 10th Field Artillery", "Battalion", "USA", "Land", children=[
                    Unit("FA1_10_A", "A Battery, 1-10 FA", "Company", "USA", "Land",
                         platforms=[(cs("THUNDER", 11, 12, 13, 14), "M109A7")]),
                    Unit("FA1_10_B", "B Battery, 1-10 FA", "Company", "USA", "Land",
                         platforms=[(cs("THUNDER", 21, 22, 23, 24), "M109A7")]),
                ]),
                Unit("ADA5_4_A", "A Battery, 5-4 ADA (M-SHORAD)", "Company", "USA", "Land",
                     platforms=[(cs("DRAGON", 11, 12, 13, 14), "M-SHORAD_INC1")]),
            ]),
            Unit("CAB3", "Combat Aviation Brigade, 3ID", "Brigade", "USA", "Land", children=[
                Unit("ATKRB1_3", "1-3 Attack Reconnaissance Battalion", "Battalion", "USA", "Land",
                     platforms=[(cs("WOLFPACK", 11, 12, 13, 14), "AH-64E")]),
            ]),
        ]),
        Unit("FAB41", "41st Field Artillery Brigade", "Brigade", "USA", "Land", children=[
            Unit("FA1_77", "1st Battalion, 77th Field Artillery", "Battalion", "USA", "Land", children=[
                Unit("FA1_77_A", "A Battery, 1-77 FA", "Company", "USA", "Land",
                     platforms=[(cs("HAMMER", 11, 12, 13, 14), "M142_HIMARS")]),
            ]),
        ]),
        Unit("AAMDC10", "10th Army Air and Missile Defense Command", "Brigade", "USA", "Land", children=[
            Unit("ADA5_7", "5th Battalion, 7th Air Defense Artillery", "Battalion", "USA", "Land", children=[
                Unit("ADA5_7_B", "B Battery, 5-7 ADA (Patriot)", "Company", "USA", "Land",
                     platforms=[(["WARLORD01"], "MPQ-65A_RADAR"), (["WARLORD02"], "MSQ-132_ECS"),
                                (cs("WARLORD", 11, 12, 13, 14), "M903_LS")]),
            ]),
        ]),
        Unit("ART11_POL", "11th Masurian Artillery Regiment (POL)", "Brigade", "POL", "Land", children=[
            Unit("ART11_POL_1", "1st Battery, 11th Artillery Regiment", "Company", "POL", "Land",
                 platforms=[(cs("KRAB", 31, 32, 33, 34), "AHS_KRAB")]),
        ]),
        Unit("ADBN_NOR", "Air Defence Battalion (NOR)", "Battalion", "NOR", "Land", children=[
            Unit("ADBN_NOR_1", "1st NASAMS Fire Unit (NOR)", "Company", "NOR", "Land",
                 platforms=[(["TROLL01"], "NASAMS_FDC"), (["TROLL02"], "SENTINEL_F1"),
                            (cs("TROLL", 11, 12, 13), "NASAMS_LCHR")]),
        ]),
        Unit("LSA_Harbor_Unit", "Logistics Support Area HARBOR", "Battalion", "USA", "Land",
             platforms=[(["LSA_HARBOR"], "PORT_FACILITY")]),
    ]),
    Unit("CFMCC", "Combined Force Maritime Component Command", "Component", "USA", "Maritime", children=[
        Unit("DESRON60", "Destroyer Squadron 60", "Brigade", "USA", "Maritime", children=[
            Unit("DDG71", "USS Ross (DDG-71)", "Battalion", "USA", "Maritime", platforms=[(["ROSS"], "DDG-51_FLT_IIA")]),
            Unit("DDG78", "USS Porter (DDG-78)", "Battalion", "USA", "Maritime", platforms=[(["PORTER"], "DDG-51_FLT_IIA")]),
            Unit("FFG62", "USS Constellation (FFG-62)", "Battalion", "USA", "Maritime", platforms=[(["CONSTELLATION"], "FFG-62")]),
        ]),
        Unit("SNMG1_NOR", "Royal Norwegian Navy contribution", "Brigade", "NOR", "Maritime", children=[
            Unit("F310", "HNoMS Fridtjof Nansen (F310)", "Battalion", "NOR", "Maritime", platforms=[(["NANSEN"], "NANSEN_CLASS_FFG")]),
        ]),
    ]),
])

RED = Unit("WOSC", "Western Operational-Strategic Command (Redland)", "JointForce", "RDL", "Land", children=[
    Unit("AirArmy6", "6th Air and Air Defence Army", "Component", "RDL", "Air", children=[
        Unit("IAP159", "159th Fighter Aviation Regiment", "Brigade", "RDL", "Air", children=[
            Unit("IAP159_1", "1st Squadron, 159 IAP", "Battalion", "RDL", "Air",
                 platforms=[(cs("SOKOL0", 1, 2, 3, 4, 5, 6, 7, 8), "SU-35S")]),
        ]),
        Unit("BAP47", "47th Bomber Aviation Regiment", "Brigade", "RDL", "Air", children=[
            Unit("BAP47_1", "1st Squadron, 47 BAP", "Battalion", "RDL", "Air",
                 platforms=[(cs("BERKUT0", 1, 2, 3, 4, 5, 6), "SU-34")]),
        ]),
        Unit("IAP790", "790th Interceptor Aviation Regiment", "Brigade", "RDL", "Air", children=[
            Unit("IAP790_1", "1st Squadron, 790 IAP", "Battalion", "RDL", "Air",
                 platforms=[(cs("KOBRA0", 1, 2), "MIG-31BM")]),
        ]),
        Unit("AEW_Det", "AEW&C Detachment, 6th Army", "Battalion", "RDL", "Air", platforms=[(["SHMEL01"], "A-50U")]),
        Unit("UAV_Sqn", "Independent UAV Squadron", "Battalion", "RDL", "Air", platforms=[(cs("STRIZH0", 1, 2), "INOKHODETS")]),
        Unit("ADD2", "2nd Air Defence Division", "Division", "RDL", "Air", children=[
            Unit("ZRP1544", "1544th Anti-Aircraft Missile Regiment (S-400)", "Brigade", "RDL", "Air", children=[
                Unit("ZRP1544_1", "1st S-400 Battalion, 1544 ZRP", "Battalion", "RDL", "Air",
                     platforms=[(["KREMEN10"], "55K6E_CP"), (["KREMEN11"], "91N6E_BIG_BIRD"),
                                (["KREMEN12"], "92N6E_GRAVE_STONE"), (cs("KREMEN", 13, 14, 15, 16), "5P85TE2_TEL")]),
                Unit("ZRP1544_2", "2nd S-400 Battalion, 1544 ZRP", "Battalion", "RDL", "Air",
                     platforms=[(["KREMEN20"], "55K6E_CP"), (["KREMEN21"], "91N6E_BIG_BIRD"),
                                (["KREMEN22"], "92N6E_GRAVE_STONE"), (cs("KREMEN", 23, 24, 25, 26), "5P85TE2_TEL")]),
                Unit("ZRP1544_PD", "Point Defence Battery, 1544 ZRP", "Company", "RDL", "Air",
                     platforms=[(cs("LIS", 41, 42, 43, 44), "96K6_PANTSIR-S1")]),
            ]),
            Unit("RTP3", "3rd Radio-Technical Regiment", "Brigade", "RDL", "Air", children=[
                Unit("RTP3_1", "1st Radar Battalion, 3 RTP", "Battalion", "RDL", "Air",
                     platforms=[(["MAYAK01"], "55ZH6M_NEBO-M")]),
            ]),
            Unit("ADD2_HQ", "2nd Air Defence Division Command Post", "Battalion", "RDL", "Air",
                 platforms=[(["OPLOT01"], "BAIKAL-1ME")]),
        ]),
        Unit("AB_Chkalovsk_Unit", "Chkalovsk Air Base", "Brigade", "RDL", "Air", platforms=[(["AB_CHKALOVSK"], "AIRBASE_FACILITY")]),
    ]),
    Unit("AK11", "11th Army Corps", "Corps", "RDL", "Land", children=[
        Unit("MRR7", "7th Motor Rifle Regiment", "Brigade", "RDL", "Land", children=[
            Unit("MRR7_1", "1st Motor Rifle Battalion, 7 MRR", "Battalion", "RDL", "Land", children=[
                Unit("MRR7_1_1", "1st Motor Rifle Company", "Company", "RDL", "Land", platforms=[(cs("TAIGA", 11, 12, 13, 14), "BMP-3")]),
                Unit("MRR7_1_AT", "Anti-Tank Platoon", "Platoon", "RDL", "Land", platforms=[(cs("KAMEN", 11, 12), "9P163_KORNET")]),
            ]),
            Unit("MRR7_TB", "Tank Battalion, 7 MRR", "Battalion", "RDL", "Land", children=[
                Unit("MRR7_TB_1", "1st Tank Company", "Company", "RDL", "Land", platforms=[(cs("TUNDRA", 11, 12, 13, 14), "T-90M")]),
            ]),
            Unit("MRR7_AD", "Air Defence Battalion, 7 MRR (Tor)", "Battalion", "RDL", "Land",
                 platforms=[(cs("YASTREB", 51, 52), "9K332_TOR-M2")]),
        ]),
        Unit("ZRBR53", "53rd Anti-Aircraft Missile Brigade (Buk-M3)", "Brigade", "RDL", "Land", children=[
            Unit("ZRBR53_1", "1st Buk Battalion, 53 ZRBR", "Battalion", "RDL", "Land",
                 platforms=[(["BEREZA10"], "9S18M1"), (["BEREZA11"], "9S36M"), (["BEREZA12"], "9S510M"),
                            (cs("BEREZA", 13, 14, 15), "9A317M_TELAR")]),
        ]),
        Unit("ABR244", "244th Artillery Brigade", "Brigade", "RDL", "Land", children=[
            Unit("ABR244_1", "1st Howitzer Battalion, 244 ABR", "Battalion", "RDL", "Land",
                 platforms=[(cs("VULKAN", 11, 12, 13, 14), "2S19M2")]),
            Unit("ABR244_2", "Rocket Artillery Battalion, 244 ABR", "Battalion", "RDL", "Land",
                 platforms=[(cs("METEL", 21, 22), "9A53-S")]),
            Unit("ABR244_LM", "Loitering Munition Detachment, 244 ABR", "Platoon", "RDL", "Land",
                 platforms=[(cs("OSKOL", 31, 32), "ZALA_LANCET_TEAM")]),
        ]),
        Unit("RBR152", "152nd Guards Missile Brigade", "Brigade", "RDL", "Land", children=[
            Unit("RBR152_1", "1st Missile Battalion, 152 RBR", "Battalion", "RDL", "Land",
                 platforms=[(cs("SHTORM0", 1, 2), "9P78-1")]),
        ]),
        Unit("OVP15", "15th Army Aviation Regiment", "Brigade", "RDL", "Land", children=[
            Unit("OVP15_1", "1st Attack Helicopter Squadron", "Battalion", "RDL", "Land",
                 platforms=[(cs("KRECHET0", 1, 2, 3, 4), "KA-52")]),
        ]),
        Unit("UAV_Strike_Det", "Long-Range Strike UAV Detachment", "Battalion", "RDL", "Land",
             platforms=[(cs("PTITSA0", 1, 2), "GERAN_LAUNCH_RAIL")]),
        Unit("Depot_Kalina_Unit", "Kalina Fuel Depot", "Battalion", "RDL", "Land", platforms=[(["DEPOT_KALINA"], "FUEL_DEPOT")]),
    ]),
    Unit("BalticFleet", "Redland Baltic Fleet", "Component", "RDL", "Maritime", children=[
        Unit("SSB36", "36th Surface Ship Brigade", "Brigade", "RDL", "Maritime", children=[
            Unit("SERPUKHOV_U", "Corvette Serpukhov", "Battalion", "RDL", "Maritime", platforms=[(["SERPUKHOV"], "PR21631_BUYAN-M")]),
            Unit("MYTISHCHI_U", "Corvette Mytishchi", "Battalion", "RDL", "Maritime", platforms=[(["MYTISHCHI"], "PR22800_KARAKURT")]),
        ]),
        Unit("OBRP25", "25th Coastal Missile Regiment", "Brigade", "RDL", "Maritime", children=[
            Unit("OBRP25_1", "1st Coastal Missile Battalion", "Battalion", "RDL", "Maritime",
                 platforms=[(cs("SKALA0", 1, 2), "K-300P_LAUNCHER")]),
        ]),
    ]),
])

NATIONS = {
    "USA": ("United States", "BlueCoalition"),
    "GBR": ("United Kingdom", "BlueCoalition"),
    "NOR": ("Norway", "BlueCoalition"),
    "POL": ("Poland", "BlueCoalition"),
    "RDL": ("Redland (notional)", "RedForce"),
}
COALITIONS = {"BlueCoalition": ("Blue Coalition", "blue"), "RedForce": ("Red Force", "red")}

# ---------------------------------------------------------------------------
# Platform kinematics / loadouts (sim type -> parameters).  This is information
# the *simulation engine* uses; none of it is written to the database except
# the resulting positions and inventories.
#   motion: air | rotary | uav | ground | sea | fixed
# ---------------------------------------------------------------------------

PTYPE = {
    # type: (motion, speed_mps, alt_m, fuel_kg, {weapon: qty})
    "F-35A":            ("air", 260, 9500, 8200, {"AIM-120D": 4, "GBU-31V3": 2, "GBU-53B": 4}),
    "F-16CM_BLK50":     ("air", 270, 8500, 3200, {"AGM-88G": 2, "AGM-88E": 2, "AIM-120C7": 2, "AIM-9X_BLK2": 2}),
    "F-15EX":           ("air", 280, 10000, 10000, {"AIM-120D": 6, "WPN_KESTREL": 6, "TRIDENT_GLIDE_KIT": 4, "GBU-39": 8}),
    "EF2000_FGR4":      ("air", 280, 10500, 5000, {"MBDA_METEOR": 4, "AIM-132": 2, "AIM-120C7": 2}),
    "B-1B":             ("air", 250, 9000, 88000, {"JASSM-ER": 12, "GBU-31V3": 8}),
    "E-3G":             ("air", 200, 9000, 70000, {}),
    "KC-46A":           ("air", 210, 8500, 90000, {}),
    "MQ-9A":            ("uav", 85, 7500, 1800, {"AGM-114R": 4, "GBU-12": 2}),
    "AH-64E":           ("rotary", 70, 60, 1100, {"AGM-179_JAGM": 8, "AGM-114R": 4, "APKWS_II": 14, "HYDRA70_M151": 14}),
    "M1A2_SEPV3":       ("ground", 6, 0, 1900, {"M829A4": 20, "M830A1": 20}),
    "M2A4":             ("ground", 6, 0, 680, {"BGM-71F": 7, "M919": 300}),
    "SB600_TEAM":       ("ground", 1, 0, 0, {"SB600": 6}),
    "M109A7":           ("ground", 3, 0, 1500, {"M795": 30, "M982A1": 6, "XM1113": 10}),
    "AHS_KRAB":         ("ground", 3, 0, 1500, {"M795": 40}),
    "M142_HIMARS":      ("ground", 4, 0, 400, {"M31A2": 6, "M30A2": 6, "PRSM_INC1": 2, "MGM-140B": 1}),
    "M-SHORAD_INC1":    ("ground", 5, 0, 600, {"FIM-92K": 8}),
    "MPQ-65A_RADAR":    ("fixed", 0, 0, 0, {}),
    "MSQ-132_ECS":      ("fixed", 0, 0, 0, {}),
    "M903_LS":          ("fixed", 0, 0, 0, {"PAC-3_MSE": 12, "GEM-T": 4}),
    "NASAMS_FDC":       ("fixed", 0, 0, 0, {}),
    "SENTINEL_F1":      ("fixed", 0, 0, 0, {}),
    "NASAMS_LCHR":      ("fixed", 0, 0, 0, {"AMRAAM-ER": 6}),
    "DDG-51_FLT_IIA":   ("sea", 8, 0, 1300000, {"SM-6_BLK1A": 12, "SM-2_BLK3C": 24, "RIM-162D": 24, "BGM-109E": 16}),
    "FFG-62":           ("sea", 8, 0, 700000, {"RGM-184A": 16, "RIM-162D": 32}),
    "NANSEN_CLASS_FFG": ("sea", 8, 0, 600000, {"NSM_BLK1A": 8, "RIM-162D": 32}),
    "AIRBASE_FACILITY": ("fixed", 0, 0, 0, {}),
    "PORT_FACILITY":    ("fixed", 0, 0, 0, {}),
    "FUEL_DEPOT":       ("fixed", 0, 0, 0, {}),
    # Red
    "SU-35S":           ("air", 270, 10000, 11000, {"R-77-1": 4, "R-73M": 2, "KH-31PD": 2}),
    "SU-34":            ("air", 240, 6000, 12000, {"KH-59MK2": 2, "KAB-500S": 4, "FAB-500M62": 4, "RBK-500_SPBE": 2}),
    "MIG-31BM":         ("air", 330, 15000, 16000, {"R-37M": 4}),
    "A-50U":            ("air", 190, 9000, 60000, {}),
    "INOKHODETS":       ("uav", 55, 6000, 400, {"KAB-20S": 4}),
    "KA-52":            ("rotary", 65, 50, 1500, {"9M127-1": 8, "S-8KOM": 40}),
    "55K6E_CP":         ("fixed", 0, 0, 0, {}),
    "91N6E_BIG_BIRD":   ("fixed", 0, 0, 0, {}),
    "92N6E_GRAVE_STONE": ("fixed", 0, 0, 0, {}),
    "5P85TE2_TEL":      ("fixed", 0, 0, 0, {"48N6E3": 2, "40N6E": 1, "9M96E2": 4}),
    "96K6_PANTSIR-S1":  ("ground", 4, 0, 500, {"57E6E": 12}),
    "55ZH6M_NEBO-M":    ("fixed", 0, 0, 0, {}),
    "BAIKAL-1ME":       ("fixed", 0, 0, 0, {}),
    "BMP-3":            ("ground", 6, 0, 690, {"9M117M1": 8, "3UBR8": 500}),
    "9P163_KORNET":     ("ground", 1, 0, 0, {"9M133M-2": 6}),
    "T-90M":            ("ground", 6, 0, 1600, {"3BM60": 18, "9M119M": 4, "3OF26": 18}),
    "9K332_TOR-M2":     ("ground", 4, 0, 500, {"9M338K": 16}),
    "9S18M1":           ("fixed", 0, 0, 0, {}),
    "9S36M":            ("fixed", 0, 0, 0, {}),
    "9S510M":           ("fixed", 0, 0, 0, {}),
    "9A317M_TELAR":     ("fixed", 0, 0, 0, {"9M317M": 4}),
    "2S19M2":           ("ground", 3, 0, 1200, {"3OF45": 30, "3OF39": 4, "3O23": 8}),
    "9A53-S":           ("ground", 4, 0, 900, {"9M55K": 12, "9M542": 12, "BURYA-12": 12}),
    "ZALA_LANCET_TEAM": ("ground", 1, 0, 0, {"LANCET-3": 6, "ZALA_LANCET3": 6, "VORON-K": 4}),
    "9P78-1":           ("ground", 3, 0, 900, {"9M723": 2, "9M728": 2}),
    "GERAN_LAUNCH_RAIL": ("fixed", 0, 0, 0, {"GERAN-2": 12}),
    "PR21631_BUYAN-M":  ("sea", 7, 0, 300000, {"3M14": 8}),
    "PR22800_KARAKURT": ("sea", 8, 0, 300000, {"3M54": 8}),
    "K-300P_LAUNCHER":  ("ground", 2, 0, 900, {"P-800": 2, "3M55": 2}),
}

# Per-platform loadout overrides: different federates / model libraries for the
# same airframe use different weapon type names for the same missile.
LOADOUT_OVERRIDE = {
    # 4 FS second flight was built from an older F-35 model that names AMRAAM differently
    **{c: {"WPN_AMRAAM_D": 4, "GBU-31V3": 2, "GBU-53B": 4} for c in cs("LIGHTNING", 21, 22, 23, 24)},
    "KOBRA02": {"IZDELIYE_610M": 4},
    "OSKOL32": {"ZALA_LANCET3": 8, "VORON-K": 4},
    "OSKOL31": {"LANCET-3": 8, "VORON-K": 2},
    "SKALA01": {"P-800": 4},
    "SKALA02": {"3M55": 4},
}

# ---------------------------------------------------------------------------
# Weapon kinematics:  weapon -> (speed_mps, base_pk, lethality, threat_class)
#   threat_class drives which defenders may try to intercept it in flight
# ---------------------------------------------------------------------------

WEAPON = {
    "AIM-120D": (1200, 0.55, 1.0, None), "WPN_AMRAAM_D": (1200, 0.55, 1.0, None),
    "AIM-120C7": (1150, 0.5, 1.0, None), "MBDA_METEOR": (1250, 0.6, 1.0, None),
    "AIM-9X_BLK2": (900, 0.7, 1.0, None), "AIM-132": (950, 0.7, 1.0, None),
    "WPN_KESTREL": (900, 0.65, 1.0, None),
    "R-77-1": (1150, 0.45, 1.0, None), "R-73M": (850, 0.55, 1.0, None),
    "R-37M": (1700, 0.4, 1.0, None), "IZDELIYE_610M": (1700, 0.4, 1.0, None),
    "48N6E3": (2000, 0.5, 1.0, None), "40N6E": (2200, 0.45, 1.0, None), "9M96E2": (1000, 0.6, 1.0, None),
    "9M317M": (1200, 0.5, 1.0, None), "57E6E": (1100, 0.55, 1.0, None), "9M338K": (850, 0.6, 1.0, None),
    "PAC-3_MSE": (1600, 0.75, 1.0, None), "GEM-T": (1500, 0.6, 1.0, None), "AMRAAM-ER": (1100, 0.6, 1.0, None),
    "FIM-92K": (750, 0.6, 1.0, None), "SM-2_BLK3C": (1100, 0.6, 1.0, None), "SM-6_BLK1A": (1200, 0.7, 1.0, None),
    "RIM-162D": (1000, 0.6, 1.0, None),
    "AGM-88E": (700, 0.6, 1.0, "fast"), "AGM-88G": (900, 0.65, 1.0, "fast"), "KH-31PD": (1000, 0.55, 1.0, "fast"),
    "JASSM-ER": (240, 0.85, 1.0, "cruise"), "KH-59MK2": (250, 0.8, 1.0, "cruise"), "BGM-109E": (245, 0.9, 1.0, "cruise"),
    "3M14": (250, 0.85, 1.0, "cruise"), "9M728": (260, 0.85, 1.0, "cruise"),
    "NSM_BLK1A": (300, 0.8, 0.7, "seaskim"), "RGM-184A": (300, 0.8, 0.7, "seaskim"),
    "P-800": (750, 0.8, 0.6, "seaskim"), "3M55": (750, 0.8, 0.6, "seaskim"), "3M54": (300, 0.8, 0.6, "seaskim"),
    "9M723": (2000, 0.9, 1.0, "ballistic"), "PRSM_INC1": (1700, 0.9, 1.0, "ballistic"), "MGM-140B": (1500, 0.9, 0.8, "ballistic"),
    "BGM-71F": (280, 0.75, 1.0, None), "9M133M-2": (300, 0.7, 1.0, None), "9M119M": (350, 0.65, 0.9, None),
    "9M117M1": (350, 0.6, 0.8, None), "AGM-114R": (420, 0.8, 1.0, None), "AGM-179_JAGM": (420, 0.85, 1.0, None),
    "9M127-1": (600, 0.7, 1.0, None),
    "GBU-12": (250, 0.8, 1.0, None), "GBU-31V3": (300, 0.85, 1.0, "glide"), "GBU-39": (250, 0.85, 0.6, "glide"),
    "GBU-53B": (250, 0.85, 0.6, "glide"), "TRIDENT_GLIDE_KIT": (230, 0.8, 0.8, "glide"),
    "KAB-500S": (280, 0.75, 1.0, "glide"), "KAB-20S": (200, 0.7, 0.4, None),
    "FAB-500M62": (280, 0.35, 1.0, None), "RBK-500_SPBE": (280, 0.6, 0.8, None),
    "APKWS_II": (600, 0.8, 0.5, None), "M31A2": (900, 0.85, 1.0, "rocket"), "M30A2": (900, 0.7, 0.7, "rocket"),
    "9M542": (900, 0.7, 0.8, "rocket"), "HYDRA70_M151": (600, 0.3, 0.5, None), "S-8KOM": (550, 0.3, 0.5, None),
    "9M55K": (900, 0.6, 0.7, "rocket"), "BURYA-12": (900, 0.55, 0.7, "rocket"),
    "M982A1": (600, 0.8, 0.8, None), "3OF39": (550, 0.7, 0.8, None),
    "M795": (550, 0.25, 0.5, None), "XM1113": (650, 0.2, 0.5, None), "3OF45": (550, 0.25, 0.5, None),
    "3O23": (550, 0.45, 0.6, None),
    "M829A4": (1650, 0.7, 1.0, None), "3BM60": (1700, 0.65, 1.0, None), "M919": (1400, 0.5, 0.4, None),
    "3UBR8": (1100, 0.45, 0.3, None), "M830A1": (1400, 0.6, 0.8, None), "3OF26": (900, 0.5, 0.5, None),
    "SB600": (50, 0.8, 1.0, "drone"), "LANCET-3": (35, 0.7, 0.9, "drone"), "ZALA_LANCET3": (35, 0.7, 0.9, "drone"),
    "VORON-K": (40, 0.7, 0.9, "drone"), "GERAN-2": (50, 0.6, 0.6, "drone"),
}

# Defensive fire: which defender platform types try to intercept which threat class,
# with which interceptor.  (defender sim type, interceptor, p_engage)
INTERCEPTORS = {
    "blue": {
        "ballistic": [("M903_LS", "PAC-3_MSE", 0.9), ("DDG-51_FLT_IIA", "SM-6_BLK1A", 0.5)],
        "cruise":    [("NASAMS_LCHR", "AMRAAM-ER", 0.7), ("M903_LS", "GEM-T", 0.5), ("DDG-51_FLT_IIA", "SM-2_BLK3C", 0.5)],
        "seaskim":   [("DDG-51_FLT_IIA", "SM-6_BLK1A", 0.6), ("DDG-51_FLT_IIA", "RIM-162D", 0.8),
                      ("FFG-62", "RIM-162D", 0.8), ("NANSEN_CLASS_FFG", "RIM-162D", 0.8)],
        "drone":     [("M-SHORAD_INC1", "FIM-92K", 0.7), ("NASAMS_LCHR", "AMRAAM-ER", 0.4)],
        "fast":      [("M903_LS", "PAC-3_MSE", 0.4)],
    },
    "red": {
        "ballistic": [("5P85TE2_TEL", "48N6E3", 0.5)],
        "cruise":    [("96K6_PANTSIR-S1", "57E6E", 0.8), ("5P85TE2_TEL", "9M96E2", 0.6), ("9A317M_TELAR", "9M317M", 0.4)],
        "glide":     [("96K6_PANTSIR-S1", "57E6E", 0.6), ("9K332_TOR-M2", "9M338K", 0.6)],
        "rocket":    [("96K6_PANTSIR-S1", "57E6E", 0.5), ("9K332_TOR-M2", "9M338K", 0.5)],
        "drone":     [("9K332_TOR-M2", "9M338K", 0.6), ("96K6_PANTSIR-S1", "57E6E", 0.5)],
        "fast":      [("96K6_PANTSIR-S1", "57E6E", 0.4)],
    },
}

# ---------------------------------------------------------------------------
# Engagement plan.  Each wave: (start_min, end_min, shooter callsign prefixes,
# weapon, target selector, number of engagements, salvo size)
# Target selectors:  ("cs", [prefixes]) | ("type", [sim types])
# ---------------------------------------------------------------------------

BLUE_AIR = ("cs", ["LIGHTNING", "WEASEL", "RAZOR", "BONE", "RAPIER", "DARKSTAR", "SHELL", "REAPER"])
BLUE_HVAA = ("cs", ["DARKSTAR", "SHELL"])
RED_AIR = ("cs", ["SOKOL", "BERKUT", "KOBRA", "SHMEL", "STRIZH"])
RED_FTR = ("cs", ["SOKOL", "KOBRA", "BERKUT"])
S400_PARTS = ("cs", ["KREMEN"])
RED_RADARS = ("cs", ["KREMEN11", "KREMEN12", "KREMEN21", "KREMEN22", "BEREZA10", "BEREZA11", "MAYAK01", "LIS", "YASTREB"])
RED_ARMOR = ("cs", ["TUNDRA", "TAIGA"])
RED_ARTY = ("cs", ["VULKAN", "METEL"])
RED_HIGHVALUE = ("cs", ["OPLOT01", "KREMEN10", "KREMEN20", "SHTORM", "AB_CHKALOVSK", "DEPOT_KALINA", "BEREZA12"])
RED_SHORAD = ("cs", ["LIS", "YASTREB"])
RED_LIGHT = ("cs", ["KAMEN", "OSKOL", "PTITSA"])
RED_SHIPS = ("cs", ["SERPUKHOV", "MYTISHCHI"])
BLUE_ARMOR = ("cs", ["IRON", "BANDIT", "COBRA", "BLADE"])
BLUE_ARTY = ("cs", ["THUNDER", "KRAB", "HAMMER"])
BLUE_GROUND_ALL = ("cs", ["IRON", "BANDIT", "COBRA", "BLADE", "THUNDER", "KRAB", "HAMMER", "DRAGON", "LASSO"])
BLUE_AD = ("cs", ["WARLORD", "TROLL"])
BLUE_FACILITIES = ("cs", ["MOB_NORTHSTAR", "LSA_HARBOR"])
BLUE_SHIPS = ("cs", ["ROSS", "PORTER", "CONSTELLATION", "NANSEN"])
BLUE_HELO = ("cs", ["WOLFPACK", "REAPER"])

WAVES = [
    # ---- Phase 1: Red opening strike (0-35 min) ------------------------------
    (1, 12, ["SHTORM"], "9M723", ("cs", ["MOB_NORTHSTAR", "LSA_HARBOR", "WARLORD01", "HAMMER"]), 4, 1),
    (3, 15, ["SHTORM"], "9M728", ("cs", ["MOB_NORTHSTAR", "WARLORD", "TROLL01"]), 4, 1),
    (2, 20, ["SERPUKHOV"], "3M14", ("cs", ["MOB_NORTHSTAR", "LSA_HARBOR", "TROLL", "WARLORD02"]), 6, 1),
    (2, 35, ["PTITSA"], "GERAN-2", ("cs", ["MOB_NORTHSTAR", "LSA_HARBOR", "TROLL", "WARLORD", "KRAB"]), 18, 1),
    (10, 40, ["SKALA"], "P-800", BLUE_SHIPS, 3, 1),
    (10, 40, ["SKALA"], "3M55", BLUE_SHIPS, 3, 1),
    (12, 40, ["MYTISHCHI"], "3M54", BLUE_SHIPS, 4, 1),
    (5, 30, ["KOBRA"], "R-37M", BLUE_HVAA, 2, 1),
    (5, 30, ["KOBRA"], "IZDELIYE_610M", ("cs", ["DARKSTAR", "SHELL", "RAPIER"]), 3, 1),
    (8, 45, ["SOKOL"], "R-77-1", ("cs", ["LIGHTNING", "RAPIER", "WEASEL", "RAZOR"]), 12, 1),
    (15, 45, ["SOKOL"], "R-73M", ("cs", ["RAPIER", "WEASEL", "RAZOR"]), 5, 1),
    (15, 50, ["SOKOL"], "KH-31PD", ("cs", ["WARLORD01", "TROLL02", "ROSS"]), 6, 1),
    (20, 60, ["BERKUT"], "KH-59MK2", ("cs", ["LSA_HARBOR", "MOB_NORTHSTAR", "WARLORD02", "TROLL01"]), 5, 1),
    # ---- Phase 2: Blue counter-air, SEAD/DEAD (15-110 min) ------------------
    (15, 60, ["LIGHTNING1"], "AIM-120D", RED_FTR, 8, 1),
    (15, 60, ["LIGHTNING2"], "WPN_AMRAAM_D", ("cs", ["SOKOL", "KOBRA", "BERKUT", "SHMEL"]), 8, 1),
    (15, 60, ["RAZOR"], "AIM-120D", RED_AIR, 8, 1),
    (25, 70, ["RAZOR"], "WPN_KESTREL", RED_FTR, 8, 1),
    (15, 60, ["RAPIER"], "MBDA_METEOR", RED_AIR, 7, 1),
    (25, 60, ["RAPIER"], "AIM-132", RED_FTR, 3, 1),
    (25, 60, ["RAPIER", "WEASEL"], "AIM-120C7", RED_FTR, 6, 1),
    (30, 70, ["WEASEL"], "AIM-9X_BLK2", RED_FTR, 4, 1),
    (25, 90, ["WEASEL"], "AGM-88G", RED_RADARS, 12, 1),
    (25, 90, ["WEASEL"], "AGM-88E", RED_RADARS, 10, 1),
    (35, 90, ["BONE"], "JASSM-ER", ("cs", ["OPLOT01", "KREMEN10", "KREMEN20", "SHTORM", "AB_CHKALOVSK", "DEPOT_KALINA", "BEREZA12", "KREMEN12", "KREMEN22"]), 18, 2),
    (30, 80, ["ROSS", "PORTER"], "BGM-109E", ("cs", ["OPLOT01", "AB_CHKALOVSK", "DEPOT_KALINA", "MAYAK01"]), 10, 2),
    (30, 100, ["HAMMER"], "PRSM_INC1", ("cs", ["KREMEN12", "KREMEN22", "KREMEN11", "SHTORM", "OPLOT01"]), 6, 1),
    (30, 100, ["HAMMER"], "M31A2", ("cs", ["LIS", "YASTREB", "BEREZA", "KREMEN1", "KREMEN2"]), 14, 2),
    (40, 110, ["HAMMER"], "MGM-140B", ("cs", ["AB_CHKALOVSK", "BEREZA", "KREMEN2"]), 3, 1),
    (40, 110, ["HAMMER"], "M30A2", ("cs", ["TAIGA", "KAMEN", "BEREZA1"]), 6, 2),
    (45, 110, ["LIGHTNING"], "GBU-53B", ("cs", ["KREMEN", "BEREZA", "LIS"]), 12, 2),
    (45, 110, ["LIGHTNING"], "GBU-31V3", ("cs", ["KREMEN", "BEREZA", "OPLOT01"]), 8, 1),
    (50, 110, ["RAZOR"], "TRIDENT_GLIDE_KIT", ("cs", ["BEREZA", "KREMEN2", "VULKAN", "METEL"]), 8, 2),
    (50, 110, ["RAZOR"], "GBU-39", ("cs", ["BEREZA", "LIS", "YASTREB", "VULKAN"]), 10, 2),
    (60, 120, ["BONE"], "GBU-31V3", ("cs", ["AB_CHKALOVSK", "DEPOT_KALINA", "BEREZA"]), 6, 2),
    # Red IADS against Blue aircraft
    (15, 110, ["KREMEN1", "KREMEN2"], "48N6E3", BLUE_AIR, 14, 2),
    (15, 110, ["KREMEN1", "KREMEN2"], "40N6E", ("cs", ["DARKSTAR", "SHELL", "BONE"]), 4, 1),
    (20, 110, ["BEREZA"], "9M317M", BLUE_AIR, 10, 2),
    # ---- Phase 3: land battle (80-210 min) ----------------------------------
    (80, 200, ["IRON", "BANDIT"], "M829A4", ("cs", ["TUNDRA", "TAIGA"]), 24, 1),
    (80, 200, ["IRON", "BANDIT"], "M830A1", ("cs", ["TAIGA", "KAMEN"]), 12, 1),
    (80, 200, ["COBRA", "BLADE"], "BGM-71F", RED_ARMOR, 14, 1),
    (80, 200, ["COBRA", "BLADE"], "M919", ("cs", ["TAIGA", "KAMEN"]), 18, 3),
    (90, 200, ["LASSO"], "SB600", ("cs", ["TUNDRA", "VULKAN", "METEL", "YASTREB"]), 8, 1),
    (80, 210, ["THUNDER"], "M795", ("cs", ["TAIGA", "TUNDRA", "KAMEN", "OSKOL"]), 24, 4),
    (80, 210, ["THUNDER"], "M982A1", ("cs", ["VULKAN", "METEL", "BEREZA", "YASTREB"]), 10, 1),
    (80, 210, ["THUNDER"], "XM1113", RED_ARTY, 8, 3),
    (80, 210, ["KRAB"], "M795", ("cs", ["TAIGA", "TUNDRA", "VULKAN", "KAMEN"]), 20, 4),
    (90, 200, ["WOLFPACK"], "AGM-179_JAGM", ("cs", ["TUNDRA", "TAIGA", "YASTREB", "LIS"]), 18, 1),
    (90, 200, ["WOLFPACK"], "AGM-114R", RED_ARMOR, 8, 1),
    (90, 200, ["WOLFPACK"], "APKWS_II", ("cs", ["KAMEN", "OSKOL", "TAIGA"]), 16, 2),
    (90, 200, ["WOLFPACK"], "HYDRA70_M151", ("cs", ["KAMEN", "OSKOL", "TAIGA"]), 8, 6),
    (60, 200, ["REAPER"], "AGM-114R", ("cs", ["KAMEN", "OSKOL", "SHTORM", "PTITSA"]), 8, 1),
    (60, 200, ["REAPER"], "GBU-12", ("cs", ["PTITSA", "SKALA", "METEL"]), 4, 1),
    (90, 200, ["DRAGON"], "FIM-92K", ("cs", ["KRECHET", "STRIZH"]), 10, 1),
    # Red ground and fires
    (80, 200, ["TUNDRA"], "3BM60", BLUE_ARMOR, 22, 1),
    (80, 200, ["TUNDRA"], "9M119M", BLUE_ARMOR, 10, 1),
    (80, 200, ["TUNDRA"], "3OF26", ("cs", ["COBRA", "BLADE", "LASSO"]), 10, 1),
    (80, 200, ["TAIGA"], "9M117M1", BLUE_ARMOR, 12, 1),
    (80, 200, ["TAIGA"], "3UBR8", ("cs", ["COBRA", "BLADE", "LASSO"]), 16, 3),
    (80, 200, ["KAMEN"], "9M133M-2", BLUE_ARMOR, 10, 1),
    (70, 210, ["VULKAN"], "3OF45", BLUE_GROUND_ALL, 24, 4),
    (70, 210, ["VULKAN"], "3OF39", ("cs", ["THUNDER", "KRAB", "HAMMER", "DRAGON"]), 10, 1),
    (70, 210, ["VULKAN"], "3O23", ("cs", ["COBRA", "BLADE", "IRON", "KRAB"]), 8, 2),
    (70, 210, ["METEL"], "9M55K", ("cs", ["THUNDER", "KRAB", "COBRA", "BLADE"]), 6, 4),
    (70, 210, ["METEL"], "9M542", ("cs", ["HAMMER", "THUNDER", "WARLORD", "TROLL"]), 8, 2),
    (70, 210, ["METEL"], "BURYA-12", ("cs", ["IRON", "BANDIT", "COBRA"]), 4, 3),
    (60, 210, ["OSKOL31"], "LANCET-3", ("cs", ["THUNDER", "HAMMER", "DRAGON", "KRAB"]), 8, 1),
    (60, 210, ["OSKOL32"], "ZALA_LANCET3", ("cs", ["THUNDER", "HAMMER", "KRAB", "IRON"]), 8, 1),
    (60, 210, ["OSKOL"], "VORON-K", ("cs", ["IRON", "BANDIT", "COBRA", "KRAB"]), 5, 1),
    (80, 200, ["KRECHET"], "9M127-1", BLUE_ARMOR, 14, 1),
    (80, 200, ["KRECHET"], "S-8KOM", ("cs", ["COBRA", "BLADE", "LASSO"]), 6, 8),
    (60, 200, ["STRIZH"], "KAB-20S", ("cs", ["THUNDER", "KRAB", "DRAGON", "LASSO"]), 6, 1),
    (50, 150, ["BERKUT"], "KAB-500S", ("cs", ["COBRA", "IRON", "THUNDER", "HAMMER"]), 10, 1),
    (50, 150, ["BERKUT"], "FAB-500M62", ("cs", ["COBRA", "BLADE", "IRON", "BANDIT"]), 8, 2),
    (60, 150, ["BERKUT"], "RBK-500_SPBE", ("cs", ["IRON", "BANDIT", "COBRA"]), 4, 1),
    # Red SHORAD vs low fliers
    (90, 200, ["LIS", "YASTREB"], "57E6E", BLUE_HELO, 6, 2),
    (90, 200, ["YASTREB"], "9M338K", BLUE_HELO, 6, 1),
    # ---- Phase 4: maritime (170-235 min) ------------------------------------
    (170, 230, ["NANSEN"], "NSM_BLK1A", RED_SHIPS, 6, 2),
    (170, 230, ["CONSTELLATION"], "RGM-184A", RED_SHIPS, 6, 2),
    (175, 230, ["ROSS"], "SM-6_BLK1A", ("cs", ["MYTISHCHI", "SERPUKHOV"]), 2, 1),
    (170, 230, ["SERPUKHOV"], "3M14", ("cs", ["LSA_HARBOR", "MOB_NORTHSTAR"]), 2, 1),
    (170, 230, ["MYTISHCHI"], "3M54", BLUE_SHIPS, 4, 1),
    (170, 230, ["SKALA"], "P-800", BLUE_SHIPS, 2, 1),
    (170, 230, ["SKALA"], "3M55", BLUE_SHIPS, 2, 1),
]

DURATION_S = 4 * 3600
STATUS_INTERVAL_S = 60
INVENTORY_INTERVAL_S = 600
SIM_START_UTC = "2026-03-14T04:00:00Z"
SEED = 20260347


def iter_units(root, parent=None):
    yield root, parent
    for c in root.children:
        yield from iter_units(c, root)


def iter_platforms(root):
    """Yield (callsign, sim_type, owning_unit, side) for every platform."""
    side = "blue" if root is BLUE else "red"
    for unit, _ in iter_units(root):
        for callsigns, ptype in unit.platforms:
            for c in callsigns:
                yield c, ptype, unit, side
