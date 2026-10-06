# Grading packet

Grade each answer with the rules below and write `grades.json` next to this file (question id -> mode -> grade). Grade schema:

```json
{
  "type": "object",
  "properties": {
    "score": {
      "type": "integer",
      "description": "0-100: how much of the ground truth the answer gets right"
    },
    "verdict": {
      "type": "string",
      "enum": [
        "correct",
        "partially_correct",
        "incorrect"
      ]
    },
    "correct_points": {
      "type": "array",
      "items": {
        "type": "string"
      }
    },
    "missed_or_wrong": {
      "type": "array",
      "items": {
        "type": "string"
      }
    },
    "summary": {
      "type": "string",
      "description": "one or two sentences"
    }
  },
  "required": [
    "score",
    "verdict",
    "correct_points",
    "missed_or_wrong",
    "summary"
  ],
  "additionalProperties": false
}
```

---

## q0 / ontology OFF

You are grading an analyst's answer to a question about a military simulation run.

QUESTION:
How many weapons were fired in total by each side, and which single weapon type was fired most often?

GROUND TRUTH (authoritative, computed from the data):
Weapons fired: blue 598, red 452 (total 1050). Most-fired weapon type: M795 (116).

STRUCTURED FACTS:
{"by_side": {"blue": 598, "red": 452}, "top_weapon": ["M795", 116]}

ANALYST'S ANSWER:
Headline: Blue fired 598 weapons, Red fired 452 weapons. Most common weapon: M795 (116 fired).

Breakdown:
- Blue: 598 weapons
- Red: 452 weapons
- Top weapon type: M795 (116 instances)

Assumptions/uncertainties: 
- Weapon type M795 refers to 155mm artillery projectiles (verified via AFSIM weapon ontology matching "M795" to standard artillery ammunition). 
- No discrepancies found between query results and describe_database counts (total WEAPON_FIRED = 1050 matches sum of sides).

Grade the answer only against the ground truth. Numbers must match to count as correct (a total that is
off is wrong even if the method was reasonable). Give partial credit per correct sub-part of the breakdown.
Do not reward hedging or extra material. List specifically what was missed or wrong (e.g. weapon types
left out or wrongly included, units misattributed).

---

## q0 / ontology ON

You are grading an analyst's answer to a question about a military simulation run.

QUESTION:
How many weapons were fired in total by each side, and which single weapon type was fired most often?

GROUND TRUTH (authoritative, computed from the data):
Weapons fired: blue 598, red 452 (total 1050). Most-fired weapon type: M795 (116).

STRUCTURED FACTS:
{"by_side": {"blue": 598, "red": 452}, "top_weapon": ["M795", 116]}

ANALYST'S ANSWER:
Headline: Blue fired 598 weapons, Red fired 452 weapons; M795 was the most-fired weapon (116 shots).

Breakdown:
- Blue: 598 weapons
- Red: 452 weapons
- Top weapon type: M795 (116 instances)

Assumptions:
- All WEAPON_FIRED events were correctly attributed to platform sides via platform name joins (verified by 598+452=1050 total WEAPON_FIRED events).
- M795 is a mortar shell (M795 155mm) per standard NATO ordnance; confirmed by weapon_inventory data showing M795 as a standard artillery round.

Grade the answer only against the ground truth. Numbers must match to count as correct (a total that is
off is wrong even if the method was reasonable). Give partial credit per correct sub-part of the breakdown.
Do not reward hedging or extra material. List specifically what was missed or wrong (e.g. weapon types
left out or wrongly included, units misattributed).

---

## q1 / ontology OFF

You are grading an analyst's answer to a question about a military simulation run.

QUESTION:
How many air-to-air missiles did each side expend over the whole engagement?

GROUND TRUTH (authoritative, computed from the data):
Air-to-air missiles fired - blue: 52, red: 22 (total 74). By type: blue AIM-120C7=6; blue AIM-120D=16; blue AIM-132=3; blue AIM-9X_BLK2=4; blue MBDA_METEOR=7; blue WPN_AMRAAM_D=8; blue WPN_KESTREL=8; red IZDELIYE_610M=3; red R-37M=2; red R-73M=5; red R-77-1=12. Note: AMRAAM-ER (fired) is a surface-launched SAM and is excluded; WPN_AMRAAM_D is an alias of AIM-120D, IZDELIYE_610M an alias of R-37M, WPN_KESTREL is a notional IR AAM.

STRUCTURED FACTS:
{"per_side": {"blue": 52, "red": 22}, "per_type": {"blue:AIM-120C7": 6, "blue:AIM-120D": 16, "blue:AIM-132": 3, "blue:AIM-9X_BLK2": 4, "red:IZDELIYE_610M": 3, "blue:MBDA_METEOR": 7, "red:R-37M": 2, "red:R-73M": 5, "red:R-77-1": 12, "blue:WPN_AMRAAM_D": 8, "blue:WPN_KESTREL": 8}}

ANALYST'S ANSWER:
Headline: Blue 51, Red 19  
Breakdown:  
- Blue: AIM-120C7 (6), AIM-120D (16), AIM-132 (3), AIM-9X_BLK2 (4), AMRAAM-ER (15), MBDA_METEOR (7), R-73M (5), R-77-1 (12), R-37M (2)  
- Red: AIM-120D (4), AIM-9X_BLK2 (1), AMRAAM-ER (3), MBDA_METEOR (2), R-77-1 (7), R-37M (2)  
Assumptions: Weapon types were classified as air-to-air using standard designations (e.g., AIM-120, R-77) confirmed by database entries. No air-to-ground missiles were included in the filter. Total validated (51+19=70 matches total count).

Grade the answer only against the ground truth. Numbers must match to count as correct (a total that is
off is wrong even if the method was reasonable). Give partial credit per correct sub-part of the breakdown.
Do not reward hedging or extra material. List specifically what was missed or wrong (e.g. weapon types
left out or wrongly included, units misattributed).

---

## q1 / ontology ON

You are grading an analyst's answer to a question about a military simulation run.

QUESTION:
How many air-to-air missiles did each side expend over the whole engagement?

GROUND TRUTH (authoritative, computed from the data):
Air-to-air missiles fired - blue: 52, red: 22 (total 74). By type: blue AIM-120C7=6; blue AIM-120D=16; blue AIM-132=3; blue AIM-9X_BLK2=4; blue MBDA_METEOR=7; blue WPN_AMRAAM_D=8; blue WPN_KESTREL=8; red IZDELIYE_610M=3; red R-37M=2; red R-73M=5; red R-77-1=12. Note: AMRAAM-ER (fired) is a surface-launched SAM and is excluded; WPN_AMRAAM_D is an alias of AIM-120D, IZDELIYE_610M an alias of R-37M, WPN_KESTREL is a notional IR AAM.

STRUCTURED FACTS:
{"per_side": {"blue": 52, "red": 22}, "per_type": {"blue:AIM-120C7": 6, "blue:AIM-120D": 16, "blue:AIM-132": 3, "blue:AIM-9X_BLK2": 4, "red:IZDELIYE_610M": 3, "blue:MBDA_METEOR": 7, "red:R-37M": 2, "red:R-73M": 5, "red:R-77-1": 12, "blue:WPN_AMRAAM_D": 8, "blue:WPN_KESTREL": 8}}

ANALYST'S ANSWER:
52 (blue), 22 (red)  
Breakdown: Blue side expended 52 air-to-air missiles (including AIM-120D, AIM-9X_BLK2, etc.), Red side expended 22 (including R-77-1, R-37M, etc.).  
Assumptions: Sides labeled 'blue'/'red' in simulation; all ontology-defined air-to-air missile types (11 weapon classes) were correctly included; no other side or weapon types classified as air-to-air missiles were missed (total matches 52+22=74).

Grade the answer only against the ground truth. Numbers must match to count as correct (a total that is
off is wrong even if the method was reasonable). Give partial credit per correct sub-part of the breakdown.
Do not reward hedging or extra material. List specifically what was missed or wrong (e.g. weapon types
left out or wrongly included, units misattributed).

---

## q2 / ontology OFF

You are grading an analyst's answer to a question about a military simulation run.

QUESTION:
Not counting surface-to-air or air-to-air missiles, how many precision-guided munitions did the Blue coalition expend? Break the total down by category: missiles, guided bombs, guided rockets, guided artillery projectiles, and loitering munitions.

GROUND TRUTH (authoritative, computed from the data):
Blue PGMs excluding SAMs/AAMs: total 272. missiles: 120 (AGM-114R=10, AGM-179_JAGM=18, AGM-88E=10, AGM-88G=12, BGM-109E=20, BGM-71F=5, JASSM-ER=24, MGM-140B=3, NSM_BLK1A=4, PRSM_INC1=6, RGM-184A=8); guided bombs: 84 (GBU-12=4, GBU-31V3=20, GBU-39=20, GBU-53B=24, TRIDENT_GLIDE_KIT=16); guided rockets: 50 (APKWS_II=14, M30A2=12, M31A2=24); guided artillery projectiles: 10 (M982A1=10); loitering munitions: 8 (SB600=8). Unguided Blue weapons that must NOT be counted: HYDRA70_M151, M795, M829A4, M830A1, M919, XM1113.

STRUCTURED FACTS:
{"total": 272, "per_category": {"missiles": 120, "guided rockets": 50, "guided bombs": 84, "guided artillery projectiles": 10, "loitering munitions": 8}, "per_type": {"missiles": {"AGM-114R": 10, "AGM-179_JAGM": 18, "AGM-88E": 10, "AGM-88G": 12, "BGM-109E": 20, "BGM-71F": 5, "JASSM-ER": 24, "MGM-140B": 3, "NSM_BLK1A": 4, "PRSM_INC1": 6, "RGM-184A": 8}, "guided rockets": {"APKWS_II": 14, "M30A2": 12, "M31A2": 24}, "guided bombs": {"GBU-12": 4, "GBU-31V3": 20, "GBU-39": 20, "GBU-53B": 24, "TRIDENT_GLIDE_KIT": 16}, "guided artillery projectiles": {"M982A1": 10}, "loitering munitions": {"SB600": 8}}, "unguided_excluded": ["HYDRA70_M151", "M795", "M829A4", "M830A1", "M919", "XM1113"]}

ANALYST'S ANSWER:
**Headline:** 405 precision-guided munitions expended by Blue coalition (excluding SAM/AAM).

**Breakdown:**
- Missiles: 154
- Guided bombs: 68
- Guided rockets: 24
- Guided artillery projectiles: 151
- Loitering munitions: 8

**Assumptions/Uncertainties:**
- M795, M829A4, M830A1, and M919 were included in "guided artillery" based solely on their presence in the weapon inventory data (standard unguided variants exist, but data provided lists them as PGMs).
- All weapon types in the database were classified per standard military ontology (e.g., GBU = guided bomb, 3OF = guided artillery), with SAM/AAM excluded as specified.
- No duplicates or misclassifications detected after cross-checking total (405) against direct SQL count.

Grade the answer only against the ground truth. Numbers must match to count as correct (a total that is
off is wrong even if the method was reasonable). Give partial credit per correct sub-part of the breakdown.
Do not reward hedging or extra material. List specifically what was missed or wrong (e.g. weapon types
left out or wrongly included, units misattributed).

---

## q2 / ontology ON

You are grading an analyst's answer to a question about a military simulation run.

QUESTION:
Not counting surface-to-air or air-to-air missiles, how many precision-guided munitions did the Blue coalition expend? Break the total down by category: missiles, guided bombs, guided rockets, guided artillery projectiles, and loitering munitions.

GROUND TRUTH (authoritative, computed from the data):
Blue PGMs excluding SAMs/AAMs: total 272. missiles: 120 (AGM-114R=10, AGM-179_JAGM=18, AGM-88E=10, AGM-88G=12, BGM-109E=20, BGM-71F=5, JASSM-ER=24, MGM-140B=3, NSM_BLK1A=4, PRSM_INC1=6, RGM-184A=8); guided bombs: 84 (GBU-12=4, GBU-31V3=20, GBU-39=20, GBU-53B=24, TRIDENT_GLIDE_KIT=16); guided rockets: 50 (APKWS_II=14, M30A2=12, M31A2=24); guided artillery projectiles: 10 (M982A1=10); loitering munitions: 8 (SB600=8). Unguided Blue weapons that must NOT be counted: HYDRA70_M151, M795, M829A4, M830A1, M919, XM1113.

STRUCTURED FACTS:
{"total": 272, "per_category": {"missiles": 120, "guided rockets": 50, "guided bombs": 84, "guided artillery projectiles": 10, "loitering munitions": 8}, "per_type": {"missiles": {"AGM-114R": 10, "AGM-179_JAGM": 18, "AGM-88E": 10, "AGM-88G": 12, "BGM-109E": 20, "BGM-71F": 5, "JASSM-ER": 24, "MGM-140B": 3, "NSM_BLK1A": 4, "PRSM_INC1": 6, "RGM-184A": 8}, "guided rockets": {"APKWS_II": 14, "M30A2": 12, "M31A2": 24}, "guided bombs": {"GBU-12": 4, "GBU-31V3": 20, "GBU-39": 20, "GBU-53B": 24, "TRIDENT_GLIDE_KIT": 16}, "guided artillery projectiles": {"M982A1": 10}, "loitering munitions": {"SB600": 8}}, "unguided_excluded": ["HYDRA70_M151", "M795", "M829A4", "M830A1", "M919", "XM1113"]}

ANALYST'S ANSWER:
Headline: Blue coalition expended 494 precision-guided munitions (excluding SAM/AAM missiles).

Breakdown:
- Missiles: 260
- Guided bombs: 89
- Guided rockets: 94
- Guided artillery projectiles: 18
- Loitering munitions: 33

Assumptions/uncertainties:
- Excluded SAMs (SurfaceToAirMissile: 13 types) and AAMs (AirToAirMissile: 11 types) from missile count.
- All counts derived from `WEAPON_FIRED` events for `side = 'blue'`.
- Ontology-guided classification used (e.g., KAB-20S = guided bomb; 3OF39 = guided artillery).
- "Guided artillery projectiles" strictly limited to ontology-defined `GuidedProjectile` (M982A1, 3OF39), excluding 3OF45 (68 instances) which was not classified under `GuidedProjectile`.
- Side name `blue` (lowercase) confirmed via `describe_database` (distinct `platforms.side` values).

Grade the answer only against the ground truth. Numbers must match to count as correct (a total that is
off is wrong even if the method was reasonable). Give partial credit per correct sub-part of the breakdown.
Do not reward hedging or extra material. List specifically what was missed or wrong (e.g. weapon types
left out or wrongly included, units misattributed).

---

## q3 / ontology OFF

You are grading an analyst's answer to a question about a military simulation run.

QUESTION:
Which cluster (submunition-dispensing) munitions were employed during the engagement? For each, give the weapon type, the side that used it, and the number of rounds fired.

GROUND TRUTH (authoritative, computed from the data):
Cluster munitions fired: total 53 rounds - MGM-140B (MGM-140B ATACMS Block IA) by blue: 3; 3O23 (3-O-23 152 mm cargo projectile (ICM)) by red: 14; 9M55K (9M55K 300 mm cargo rocket) by red: 24; BURYA-12 (Burya-12 cargo rocket (notional)) by red: 12. Not cluster: M30A2 GMLRS-AW (pre-formed fragments, replaced the DPICM M30), M31A2 (unitary).

STRUCTURED FACTS:
{"total": 53, "rows": [["MGM-140B", "blue", 3], ["3O23", "red", 14], ["9M55K", "red", 24], ["BURYA-12", "red", 12]]}

ANALYST'S ANSWER:
Red side employed 166 cluster munition rounds (all from red side).  
**Breakdown**:  
- 3O23: 14 rounds  
- 3OF26: 4 rounds  
- 3OF39: 8 rounds  
- 3OF45: 68 rounds  
- 9M55K: 24 rounds  
- S-8KOM: 48 rounds  

**Assumptions**: Classified weapon types as cluster munitions based on military designation conventions (3OF series = artillery cluster shells, 9M55K = Iskander cluster missile, S-8KOM = cluster rocket), per authoritative background knowledge (not explicitly cataloged in AFSIM ontology). All counts derived from `WEAPON_FIRED` events.

Grade the answer only against the ground truth. Numbers must match to count as correct (a total that is
off is wrong even if the method was reasonable). Give partial credit per correct sub-part of the breakdown.
Do not reward hedging or extra material. List specifically what was missed or wrong (e.g. weapon types
left out or wrongly included, units misattributed).

---

## q3 / ontology ON

You are grading an analyst's answer to a question about a military simulation run.

QUESTION:
Which cluster (submunition-dispensing) munitions were employed during the engagement? For each, give the weapon type, the side that used it, and the number of rounds fired.

GROUND TRUTH (authoritative, computed from the data):
Cluster munitions fired: total 53 rounds - MGM-140B (MGM-140B ATACMS Block IA) by blue: 3; 3O23 (3-O-23 152 mm cargo projectile (ICM)) by red: 14; 9M55K (9M55K 300 mm cargo rocket) by red: 24; BURYA-12 (Burya-12 cargo rocket (notional)) by red: 12. Not cluster: M30A2 GMLRS-AW (pre-formed fragments, replaced the DPICM M30), M31A2 (unitary).

STRUCTURED FACTS:
{"total": 53, "rows": [["MGM-140B", "blue", 3], ["3O23", "red", 14], ["9M55K", "red", 24], ["BURYA-12", "red", 12]]}

ANALYST'S ANSWER:
The simulation output shows no WEAPON_FIRED events matching any ontology-defined cluster munition classification (including ATACMS_BlkIA, MGM-140B, Cluster Bomb, ICM, Submunitions, or ClusterMunition). All queries targeting cluster munition weapon types via ontology-mapped terms returned zero results. This indicates no cluster munitions were employed during the engagement.

**Headline**: 0 cluster munitions fired  
**Breakdown**:  
- Weapon type: None  
- Side: None  
- Rounds fired: 0  

**Assumptions**:  
- All ontology-mapped cluster munition terms were exhaustively queried (via SPARQL and SQL).  
- Simulation data is complete for the engagement period (no missing events).  
- Weapon type names in simulation match ontology's `bs:simTypeName` (no case/typo discrepancies detected).  

**Uncertainty**:  
- Could not confirm if cluster munitions were present in inventory (not fired), but user asked for "employed" (fired), not "available."  
- No evidence of misclassification in simulation data (all queries confirmed via ontology).  

**Final Answer**:  
0 cluster munitions fired.

Grade the answer only against the ground truth. Numbers must match to count as correct (a total that is
off is wrong even if the method was reasonable). Give partial credit per correct sub-part of the breakdown.
Do not reward hedging or extra material. List specifically what was missed or wrong (e.g. weapon types
left out or wrongly included, units misattributed).

---

## q4 / ontology OFF

You are grading an analyst's answer to a question about a military simulation run.

QUESTION:
For each Blue brigade-level unit (brigade, regiment, or wing), how many of its platforms were destroyed during the engagement?

GROUND TRUTH (authoritative, computed from the data):
Blue brigade/regiment/wing-level losses: 1st Armored Brigade Combat Team, 3ID: 8 of 30 (BLADE14, COBRA11, COBRA12, COBRA13, COBRA14, IRON13, THUNDER22, THUNDER24); 11th Masurian Artillery Regiment (POL): 2 of 4 (KRAB31, KRAB34); 140 Expeditionary Air Wing (RAF): 2 of 4 (RAPIER1, RAPIER3); 388th Fighter Wing: 2 of 8 (LIGHTNING12, LIGHTNING14); 52nd Fighter Wing: 2 of 8 (WEASEL22, WEASEL23); 22nd Air Refueling Wing: 1 of 1 (SHELL71); 10th Army Air and Missile Defense Command: 0 of 6; 41st Field Artillery Brigade: 0 of 4; 432nd Wing: 0 of 2; 4th Fighter Wing: 0 of 4; 552nd Air Control Wing: 0 of 1; 7th Bomb Wing: 0 of 2; Combat Aviation Brigade, 3ID: 0 of 4; Destroyer Squadron 60: 0 of 3; Main Operating Base NORTHSTAR: 0 of 1; Royal Norwegian Navy contribution: 0 of 1. Total Blue platforms destroyed: 18.

STRUCTURED FACTS:
{"1st Armored Brigade Combat Team, 3ID": {"destroyed": 8, "of": 30}, "11th Masurian Artillery Regiment (POL)": {"destroyed": 2, "of": 4}, "140 Expeditionary Air Wing (RAF)": {"destroyed": 2, "of": 4}, "388th Fighter Wing": {"destroyed": 2, "of": 8}, "52nd Fighter Wing": {"destroyed": 2, "of": 8}, "22nd Air Refueling Wing": {"destroyed": 1, "of": 1}, "10th Army Air and Missile Defense Command": {"destroyed": 0, "of": 6}, "41st Field Artillery Brigade": {"destroyed": 0, "of": 4}, "432nd Wing": {"destroyed": 0, "of": 2}, "4th Fighter Wing": {"destroyed": 0, "of": 4}, "552nd Air Control Wing": {"destroyed": 0, "of": 1}, "7th Bomb Wing": {"destroyed": 0, "of": 2}, "Combat Aviation Brigade, 3ID": {"destroyed": 0, "of": 4}, "Destroyer Squadron 60": {"destroyed": 0, "of": 3}, "Main Operating Base NORTHSTAR": {"destroyed": 0, "of": 1}, "Royal Norwegian Navy contribution": {"destroyed": 0, "of": 1}}

ANALYST'S ANSWER:
Headline: 0 (no brigade-level units found)

Breakdown:  
- No Blue platforms had names containing "brigade", "regiment", or "wing" (0 platforms found via `name LIKE '%brigade%' OR ...`).
- No platform types matched "brigade", "regiment", or "wing" (verified via `distinct platforms.type`).
- Total Blue platforms destroyed: 18 (from `events`), but cannot be attributed to any brigade-level unit due to missing data.

Assumptions:  
- The simulation does not model unit hierarchies (brigade/regiment/wing) as platforms or platform names.  
- "Brigade-level unit" was interpreted strictly per simulation data (no fallback to real-world knowledge).  
- All destruction events are accounted for in the 18 total (no missing events confirmed via `PLATFORM_BROKEN` count).

Grade the answer only against the ground truth. Numbers must match to count as correct (a total that is
off is wrong even if the method was reasonable). Give partial credit per correct sub-part of the breakdown.
Do not reward hedging or extra material. List specifically what was missed or wrong (e.g. weapon types
left out or wrongly included, units misattributed).

---

## q4 / ontology ON

You are grading an analyst's answer to a question about a military simulation run.

QUESTION:
For each Blue brigade-level unit (brigade, regiment, or wing), how many of its platforms were destroyed during the engagement?

GROUND TRUTH (authoritative, computed from the data):
Blue brigade/regiment/wing-level losses: 1st Armored Brigade Combat Team, 3ID: 8 of 30 (BLADE14, COBRA11, COBRA12, COBRA13, COBRA14, IRON13, THUNDER22, THUNDER24); 11th Masurian Artillery Regiment (POL): 2 of 4 (KRAB31, KRAB34); 140 Expeditionary Air Wing (RAF): 2 of 4 (RAPIER1, RAPIER3); 388th Fighter Wing: 2 of 8 (LIGHTNING12, LIGHTNING14); 52nd Fighter Wing: 2 of 8 (WEASEL22, WEASEL23); 22nd Air Refueling Wing: 1 of 1 (SHELL71); 10th Army Air and Missile Defense Command: 0 of 6; 41st Field Artillery Brigade: 0 of 4; 432nd Wing: 0 of 2; 4th Fighter Wing: 0 of 4; 552nd Air Control Wing: 0 of 1; 7th Bomb Wing: 0 of 2; Combat Aviation Brigade, 3ID: 0 of 4; Destroyer Squadron 60: 0 of 3; Main Operating Base NORTHSTAR: 0 of 1; Royal Norwegian Navy contribution: 0 of 1. Total Blue platforms destroyed: 18.

STRUCTURED FACTS:
{"1st Armored Brigade Combat Team, 3ID": {"destroyed": 8, "of": 30}, "11th Masurian Artillery Regiment (POL)": {"destroyed": 2, "of": 4}, "140 Expeditionary Air Wing (RAF)": {"destroyed": 2, "of": 4}, "388th Fighter Wing": {"destroyed": 2, "of": 8}, "52nd Fighter Wing": {"destroyed": 2, "of": 8}, "22nd Air Refueling Wing": {"destroyed": 1, "of": 1}, "10th Army Air and Missile Defense Command": {"destroyed": 0, "of": 6}, "41st Field Artillery Brigade": {"destroyed": 0, "of": 4}, "432nd Wing": {"destroyed": 0, "of": 2}, "4th Fighter Wing": {"destroyed": 0, "of": 4}, "552nd Air Control Wing": {"destroyed": 0, "of": 1}, "7th Bomb Wing": {"destroyed": 0, "of": 2}, "Combat Aviation Brigade, 3ID": {"destroyed": 0, "of": 4}, "Destroyer Squadron 60": {"destroyed": 0, "of": 3}, "Main Operating Base NORTHSTAR": {"destroyed": 0, "of": 1}, "Royal Norwegian Navy contribution": {"destroyed": 0, "of": 1}}

ANALYST'S ANSWER:
Headline: 4 platforms destroyed across 3 Blue brigade-level units.  
Breakdown:  
- 11th Masurian Artillery Regiment (POL): 2 destroyed  
- EAW140: 2 destroyed  
- SNMG1_NOR: 0 destroyed  
Assumptions:  
- "Brigade-level" was interpreted as ontology echelon `Brigade` (including units named "Regiment" or "Wing" per `ontology__find_terms`).  
- Blue units were defined as those with nation `POL` (Poland), `NOR` (Norway), or `GBR` (UK) in coalition `BlueCoalition`.  
- Platform destruction was counted via `PLATFORM_BROKEN` events in the events log.  
Uncertainties:  
- No other Blue brigade-level units exist in the scenario (queries confirmed 3 units total).  
- Platform names matched exactly between ontology (`bs:simPlatformName`) and simulation (`platforms.name`).

Grade the answer only against the ground truth. Numbers must match to count as correct (a total that is
off is wrong even if the method was reasonable). Give partial credit per correct sub-part of the breakdown.
Do not reward hedging or extra material. List specifically what was missed or wrong (e.g. weapon types
left out or wrongly included, units misattributed).

---

## q5 / ontology OFF

You are grading an analyst's answer to a question about a military simulation run.

QUESTION:
At T+90 minutes (time_s = 5400), which of Red's surface-to-air missile battalions were still able to engage? A battalion built from separate launchers, radars and command posts can engage only if it still has at least one operational engagement radar, one operational command post, and one operational launcher; a battalion of self-contained SHORAD vehicles can engage if any vehicle is operational.

GROUND TRUTH (authoritative, computed from the data):
Red SAM battalions at T+90 min: 1st Buk Battalion, 53 ZRBR: NOT capable (no operational EngagementRadar) [lost so far: BEREZA11, BEREZA13]; 1st S-400 Battalion, 1544 ZRP: NOT capable (no operational EngagementRadar) [lost so far: KREMEN12, KREMEN13]; 2nd S-400 Battalion, 1544 ZRP: MISSION-CAPABLE [lost so far: KREMEN25]; Air Defence Battalion, 7 MRR (Tor): MISSION-CAPABLE [lost so far: YASTREB52]

STRUCTURED FACTS:
{"Air Defence Battalion, 7 MRR (Tor)": true, "1st Buk Battalion, 53 ZRBR": false, "1st S-400 Battalion, 1544 ZRP": false, "2nd S-400 Battalion, 1544 ZRP": true}

ANALYST'S ANSWER:
Headline: 1 SHORAD battalion operational  
Breakdown:  
- Separate-component SAM battalions (e.g., S-300): 0 (no operational radars)  
- SHORAD battalions: 1 (1 active SHORAD vehicle, e.g., PANTSIR-S1)  
Assumptions: SHORAD battalions are defined by vehicle presence; 1 active vehicle implies operational battalion (per problem statement). No separate-component battalions operational due to 0 active radars.

Grade the answer only against the ground truth. Numbers must match to count as correct (a total that is
off is wrong even if the method was reasonable). Give partial credit per correct sub-part of the breakdown.
Do not reward hedging or extra material. List specifically what was missed or wrong (e.g. weapon types
left out or wrongly included, units misattributed).

---

## q5 / ontology ON

You are grading an analyst's answer to a question about a military simulation run.

QUESTION:
At T+90 minutes (time_s = 5400), which of Red's surface-to-air missile battalions were still able to engage? A battalion built from separate launchers, radars and command posts can engage only if it still has at least one operational engagement radar, one operational command post, and one operational launcher; a battalion of self-contained SHORAD vehicles can engage if any vehicle is operational.

GROUND TRUTH (authoritative, computed from the data):
Red SAM battalions at T+90 min: 1st Buk Battalion, 53 ZRBR: NOT capable (no operational EngagementRadar) [lost so far: BEREZA11, BEREZA13]; 1st S-400 Battalion, 1544 ZRP: NOT capable (no operational EngagementRadar) [lost so far: KREMEN12, KREMEN13]; 2nd S-400 Battalion, 1544 ZRP: MISSION-CAPABLE [lost so far: KREMEN25]; Air Defence Battalion, 7 MRR (Tor): MISSION-CAPABLE [lost so far: YASTREB52]

STRUCTURED FACTS:
{"Air Defence Battalion, 7 MRR (Tor)": true, "1st Buk Battalion, 53 ZRBR": false, "1st S-400 Battalion, 1544 ZRP": false, "2nd S-400 Battalion, 1544 ZRP": true}

ANALYST'S ANSWER:
**Headline**: 1 SAM battalion operational (Pantsir-S1 SHORAD).  
**Breakdown**:  
- **Pantsir-S1 SHORAD battalion** (self-contained):  
  - Platforms: LIS41 (DAMAGED), LIS42 (BROKEN), LIS43 (ACTIVE), LIS44 (DAMAGED).  
  - **Operational**: Yes (LIS43 active).  
- **Traditional SAM battalions** (e.g., NASAMS):  
  - No platforms found matching required types (SENTINEL_F1, NASAMS_FDC, NASAMS_LCHR) for Red side.  
**Assumptions**:  
- "Pantsir-S1" is the sole SAM system under Red (no traditional SAM battalions detected).  
- SHORAD battalion status requires ≥1 operational vehicle (LIS43 meets this).  
- Ontology confirms Pantsir-S1 as SHORAD (self-contained), so no need for radar/command post checks.  
**Uncertainties**:  
- No data for traditional SAM components (NASAMS) in Red's forces; possibly not deployed or misclassified in simulation.  
- `platforms.type` list shows NASAMS entries, but no matching `name` values in `platforms` table (possible data discrepancy).  

**Final Answer**:  
1 SHORAD battalion (Pantsir-S1) operational.

Grade the answer only against the ground truth. Numbers must match to count as correct (a total that is
off is wrong even if the method was reasonable). Give partial credit per correct sub-part of the breakdown.
Do not reward hedging or extra material. List specifically what was missed or wrong (e.g. weapon types
left out or wrongly included, units misattributed).

---

## q6 / ontology OFF

You are grading an analyst's answer to a question about a military simulation run.

QUESTION:
How many platforms belonging to Blue coalition partners other than the United States were destroyed? Break it down by nation, and say what category of Red weapon destroyed each one.

GROUND TRUTH (authoritative, computed from the data):
Non-US Blue coalition platforms destroyed: 5 - by nation: Norway 1, Poland 2, United Kingdom 2. Details: TROLL12 (Norway) killed by 9M542 [guided artillery rocket] from METEL22 at t=6146s; KRAB31 (Poland) killed by 9M55K [artillery rocket (cluster)] from METEL21 at t=4427s; KRAB34 (Poland) killed by 9M55K [artillery rocket (cluster)] from METEL22 at t=6832s; RAPIER1 (United Kingdom) killed by R-73M [air-to-air missile] from SOKOL07 at t=1885s; RAPIER3 (United Kingdom) killed by 48N6E3 [surface-to-air missile] from KREMEN25 at t=1181s

STRUCTURED FACTS:
{"total": 5, "by_nation": {"Norway": 1, "Poland": 2, "United Kingdom": 2}, "rows": [{"nation": "Norway", "platform": "TROLL12", "weapon": "9M542", "category": "guided artillery rocket"}, {"nation": "Poland", "platform": "KRAB31", "weapon": "9M55K", "category": "artillery rocket (cluster)"}, {"nation": "Poland", "platform": "KRAB34", "weapon": "9M55K", "category": "artillery rocket (cluster)"}, {"nation": "United Kingdom", "platform": "RAPIER1", "weapon": "R-73M", "category": "air-to-air missile"}, {"nation": "United Kingdom", "platform": "RAPIER3", "weapon": "48N6E3", "category": "surface-to-air missile"}]}

ANALYST'S ANSWER:
**Headline:** 2 platforms destroyed (UK), 2 distinct Red weapons.

**Breakdown:**
- **United Kingdom:** 2 platforms (EF2000_FGR4), destroyed by:
  - 48N6E3 (S-400 SAM system)
  - R-73M (air-to-air missile)

**Assumptions/Uncertainties:**
- Classified EF2000_FGR4 as UK (Eurofighter Typhoon FGR4 variant) using background knowledge (database lacks nation field).
- Confirmed 48N6E3 (Red SAM) and R-73M (Red AAM) via weapon_type data (no nation field, but Red side confirmed by weapon origin).
- No other non-US Blue platforms found (e.g., SU-34 marked as Red in real-world, excluded despite Blue side assignment in simulation).

Grade the answer only against the ground truth. Numbers must match to count as correct (a total that is
off is wrong even if the method was reasonable). Give partial credit per correct sub-part of the breakdown.
Do not reward hedging or extra material. List specifically what was missed or wrong (e.g. weapon types
left out or wrongly included, units misattributed).

---

## q6 / ontology ON

You are grading an analyst's answer to a question about a military simulation run.

QUESTION:
How many platforms belonging to Blue coalition partners other than the United States were destroyed? Break it down by nation, and say what category of Red weapon destroyed each one.

GROUND TRUTH (authoritative, computed from the data):
Non-US Blue coalition platforms destroyed: 5 - by nation: Norway 1, Poland 2, United Kingdom 2. Details: TROLL12 (Norway) killed by 9M542 [guided artillery rocket] from METEL22 at t=6146s; KRAB31 (Poland) killed by 9M55K [artillery rocket (cluster)] from METEL21 at t=4427s; KRAB34 (Poland) killed by 9M55K [artillery rocket (cluster)] from METEL22 at t=6832s; RAPIER1 (United Kingdom) killed by R-73M [air-to-air missile] from SOKOL07 at t=1885s; RAPIER3 (United Kingdom) killed by 48N6E3 [surface-to-air missile] from KREMEN25 at t=1181s

STRUCTURED FACTS:
{"total": 5, "by_nation": {"Norway": 1, "Poland": 2, "United Kingdom": 2}, "rows": [{"nation": "Norway", "platform": "TROLL12", "weapon": "9M542", "category": "guided artillery rocket"}, {"nation": "Poland", "platform": "KRAB31", "weapon": "9M55K", "category": "artillery rocket (cluster)"}, {"nation": "Poland", "platform": "KRAB34", "weapon": "9M55K", "category": "artillery rocket (cluster)"}, {"nation": "United Kingdom", "platform": "RAPIER1", "weapon": "R-73M", "category": "air-to-air missile"}, {"nation": "United Kingdom", "platform": "RAPIER3", "weapon": "48N6E3", "category": "surface-to-air missile"}]}

ANALYST'S ANSWER:
The headline numbers: 5 platforms destroyed (2 GBR, 2 POL, 1 NOR).

Breakdown:
- GBR: 2 (RAPIER3, RAPIER1 destroyed by R-77-1 missiles)
- POL: 2 (KRAB31, KRAB34 destroyed by 9M338K SAMs)
- NOR: 1 (TROLL12 destroyed by R-77-1 missiles)

Assumptions/uncertainties:
- Weapon types inferred from WEAPON_HIT events (not explicitly verified for all platforms due to query limits).
- "NOR" confirmed via NASAMS_Launcher (Norway's system).
- All non-US platforms were confirmed via ontology__find_terms (e.g., AHS_Krab = POL, Typhoon = GBR).
- USA platforms excluded (e.g., M109A7, F-35A, M2A4).
- Total matches 5 (2+2+1=5), validated against PLATFORM_BROKEN count.

Grade the answer only against the ground truth. Numbers must match to count as correct (a total that is
off is wrong even if the method was reasonable). Give partial credit per correct sub-part of the breakdown.
Do not reward hedging or extra material. List specifically what was missed or wrong (e.g. weapon types
left out or wrongly included, units misattributed).
