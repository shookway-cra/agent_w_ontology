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
Headline numbers: Blue fired 598 weapons, Red fired 452 weapons. S-8KOM was the most frequently fired weapon type (48 firings).

Breakdown:
- Total weapons fired: 1,050 (598 blue + 452 red)
- Most fired weapon type: S-8KOM (48 occurrences)
- Other top weapon types: 9M338K (32), 9M96E2 (23), SB600 (8)

Assumptions:
- Events.weapon_type accurately reflects weapon types for WEAPON_FIRED events (confirmed by describe_database listing S-8KOM as 48 occurrences)
- Platform-side mapping via events.platform = platforms.name is valid (supported by platform count matching sides)
- No duplicate or misclassified WEAPON_FIRED events (1050 total matches event_type count from describe_database)

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
Headline: Blue fired 598 weapons, Red fired 452 weapons. Most common weapon: M795 (116 shots).

Breakdown:
- Blue: 598 weapons (598 total WEAPON_FIRED events linked to blue-side platforms)
- Red: 452 weapons (452 total WEAPON_FIRED events linked to red-side platforms)
- Top weapon type: M795 (116 occurrences, confirmed by SQL count)

Assumptions/Uncertainties:
- Weapon type "M795" is a 155mm artillery shell (validated via ontology__find_terms: "M795" matches artillery ammunition in ontology).
- No intercepts or non-firing events counted (only WEAPON_FIRED events included).
- Side determination via platform join (not events.side column) as events.side was not confirmed as reliable in database description.

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
Headline: Blue expended 67, Red expended 19 air-to-air missiles.  
Breakdown:  
- Blue: 67 (AIM-120 variants: 32, R-77-1:12, R-73M:5, MBDA_METEOR:7, AIM-132:3, WPN_KESTREL:8, others: 10)  
- Red: 19 (R-37M:2, R-77-1:12, AIM-9X_BLK2:4, others: 1)  
Assumptions: Weapon types were classified as air-to-air based on authoritative database entries (no external knowledge used), and all WEAPON_FIRED events with these types were counted. Total matches sum of weapon-type counts from describe_database (86 total).

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
Headline: Blue side expended 59 air-to-air missiles, Red side expended 19.

Breakdown:
- Blue: 59 (AMRAAM-ER, AIM-120D, AIM-120C7, R-77-1, R-37M, MBDA_METEOR, R-73M, AIM-9X_BLK2, AIM-132, WPN_AMRAAM_D)
- Red: 19 (same weapon types as Blue)

Assumptions: 
- AMRAAM-ER was included despite ontology misclassifying it as a SAM (real-world AAM); confirmed via weapon type list and standard military knowledge.
- All listed weapon types in the SQL IN clause are confirmed AAMs (e.g., R-77-1, AIM-120 series, METEOR).
- Side names "blue" and "red" align with simulation's force designations (no evidence of alternative side labels in data).

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
Headline: 255 precision-guided munitions expended by Blue coalition (excluding SAM/AAM).

Breakdown:
- Missiles: 105 (JASSM-ER, BGM-109E, AGM-179_JAGM, TRIDENT_GLIDE_KIT, AGM-88G/E, AGM-114R, PRSM_INC1, BGM-71F, NSM_BLK1A, MGM-140B)
- Guided bombs: 94 (GBU-53B, GBU-39, GBU-31V3, XM1113, GEM-T, GBU-12)
- Guided rockets: 46 (HYDRA70_M151, APKWS_II, SB600)
- Guided artillery projectiles: 10 (M982A1)
- Loitering munitions: 0

Assumptions/uncertainties:
- Excluded RGM-184A (8) and AMRAAM-ER (15) from missiles as SAM/AAM (not included in initial SQL NOT IN clause but excluded per query requirements).
- M795/M31A2/M919/M30A2/M829A4/M830A1 excluded as unguided artillery.
- LANCET-3/ZALA_LANCET3 absent in Blue-side counts; classified as 0 for Blue coalition.

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
Headline: Blue coalition expended 286 precision-guided munitions (excluding SAM/AAM), broken down as follows:

- Missiles: 162  
- Guided bombs: 68  
- Guided rockets: 46  
- Guided artillery: 10  
- Loitering munitions: 0  

**Breakdown by category** (with counts):  
- **Missiles**: AGM-114R (10), AGM-179_JAGM (18), AGM-88E (10), AGM-88G (12), BGM-109E (20), BGM-71F (5), GEM-T (8), JASSM-ER (24), MGM-140B (3), NSM_BLK1A (4), PRSM_INC1 (6), RGM-184A (8), TRIDENT_GLIDE_KIT (16), XM1113 (18).  
- **Guided bombs**: GBU-12 (4), GBU-31V3 (20), GBU-39 (20), GBU-53B (24).  
- **Guided rockets**: APKWS_II (14), HYDRA70_M151 (24), SB600 (8).  
- **Guided artillery**: M982A1 (10).  
- **Loitering munitions**: None recorded.  

**Assumptions/uncertainties**:  
1. **Excluded SAM/AAM**: All SAMs (e.g., PAC-3_MSE, FIM-92K, RIM-162D, SM-2/6) and AAMs (e.g., AMRAAM-ER, MBDA_METEOR) were excluded per query.  
2. **PGM classification**: Only guided weapons (ontology: `PrecisionGuidedMunition` subclass) were counted. Unguided weapons (e.g., M795, M30A2) were excluded.  
3. **Loitering munitions**: No loitering munition events (e.g., LANCET-3) were fired by Blue coalition in the simulation.  
4. **Weapon categorization**: Based on ontology (e.g., `GuidedRocket` for APKWS/HYDRA, `GuidedBomb` for GBU series).  
5. **Data completeness**: SQL results included all Blue-fired events (562 total), with 99 SAM/AAM events excluded (99 total SAM/AAM).

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
Headline: 4 cluster munition types employed by red side, totaling 128 rounds.

Breakdown:
- 3OF26 (red): 4 rounds
- 3OF39 (red): 8 rounds
- 3OF45 (red): 68 rounds
- S-8KOM (red): 48 rounds

Assumptions: 
- Classification of 3OF-series and S-8KOM as cluster munitions based on authoritative military data (noted as background knowledge due to lack of explicit "cluster" flag in database).
- All 4 weapon types identified as cluster munitions via standard military designations (3OF = Russian cluster warhead series; S-8KOM = cluster rocket).
- No blue-side cluster munition use observed in query results (all 128 rounds fired by red side).

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
Headline: 2 cluster munition types employed, 38 rounds total.  
Breakdown:  
- 3O23 (3-O-23 152 mm cargo projectile): red side, 14 rounds  
- 9M55K (9M55K 300 mm cargo rocket): red side, 24 rounds  
Assumptions: Only weapon types explicitly matching ontology labels were counted; other cluster types (e.g., ATACMS_BlkIA) had zero firings. Side "red" is the coalition name per simulation metadata.

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
Headline: 18 Blue platforms destroyed (1 each, no brigade grouping possible).

Breakdown: 
- 18 distinct Blue platforms destroyed, each with exactly 1 destruction event (BLADE14, COBRA11, COBRA12, COBRA13, COBRA14, IRON13, KRAB31, KRAB34, LIGHTNING12, LIGHTNING14, RAPIER1, RAPIER3, SHELL71, THUNDER22, THUNDER24, TROLL12, WEASEL22, WEASEL23).

Assumptions/uncertainties: 
- Simulation data contains no identifiable "brigade-level unit" names in platform names (e.g., no entries like "1st_Brigade" or "Regiment_3"). All destroyed platforms are individually identified by alphanumeric callsigns, not grouped by organizational unit. 
- AFSIM's platform table does not include organizational hierarchy fields (e.g., parent unit), so brigade-level aggregation is impossible with available data. 
- Platform names like "COBRA" and "KRAB" refer to specific vehicle types (e.g., M109A7 howitzers or M1A2 tanks), not command units.

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
The query for Blue coalition units with echelon "Brigade" returned **0 rows** in the ontology. The ontology's echelon facet explicitly lists "Brigade" as a valid echelon (e.g., `bs:Brigade`), but no matching units were found in the simulation's force structure. 

**Assumption**: The user's query assumes brigade-level units exist in the Blue coalition, but the simulation data contains none at the "Brigade" echelon. The ontology does not list "Regiment" or "Wing" as valid echelons (only "Battalion," "Company," etc.), so those terms do not match the simulation's structure. 

**Conclusion**: No Blue brigade-level units (as defined by the ontology) exist in the simulation, so **0 platforms were destroyed**.

---

**Headline**: 0 destroyed platforms across all Blue brigade-level units  
**Breakdown**: No Blue brigade-level units detected in simulation  
**Assumptions**:  
- "Brigade" is the only valid echelon term matching the ontology's `bs:Brigade` (not "Regiment" or "Wing").  
- Simulation lacks units at the "Brigade" echelon in the Blue coalition.

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
Headline: 1 SHORAD battalion operational, 0 separate-component battalions operational.

Breakdown:
- **SHORAD battalion** (`M-SHORAD_INC1`): 
  - Active platform: `BEREZA14` (state: ACTIVE)
- **Separate-component battalions**:
  - No active radars (all `9S36M`, `9S510M`, `MPQ-65A_RADAR` platforms: `BROKEN`/`DAMAGED`)
  - No active command posts (`NASAMS_FDC` platform `METEL21`: `DAMAGED`)
  - No active launchers (all `9P85TE2_TEL`, `9A317M_TELAR`, `9A53-S`, `NASAMS_LCHR` platforms: `BROKEN`/`DAMAGED`)

Assumptions: 
- Platform names (`BEREZA*`) are correctly mapped to their types (`M-SHORAD_INC1` for SHORAD, others as separate components).
- All `M-SHORAD_INC1` platforms form a single battalion (self-contained).
- No hidden battalion groupings exist (e.g., no "battalion ID" in data, so SHORAD is treated as one unit).

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
Headline: 1 Red SAM battalion operational at T+90 minutes (96K6_PANTSIR-S1).

Breakdown:
- **Separate-component SAM battalions (e.g., S-300 systems)**: None operational. No active engagement radars (91N6E_BIG_BIRD, 92N6E_GRAVE_STONE, etc. not listed in active platforms), though 5P85TE2_TEL launchers (4 active) and 55K6E_CP command posts (1 active) exist.
- **Self-contained SHORAD battalions**:
  - 96K6_PANTSIR-S1: 1 operational vehicle (active_count=1), meeting the SHORAD engagement criterion.
  - M-SHORAD_INC1: 0 operational vehicles (not listed in active platforms).

Assumptions/uncertainties:
- Confirmed 96K6_PANTSIR-S1 is a self-contained SHORAD system (not a separate-component SAM).
- Radar types (e.g., 91N6E_BIG_BIRD) not appearing in active_count implies 0 operational radars (critical for separate-component battalions).
- 9K332_TOR-M2 (SAM launcher) not listed in active_count → assumed non-operational.
- No command posts (MSQ-132_ECS, NASAMS_FDC) listed in active_count → only 55K6E_CP active, but irrelevant without radars.

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
Headline: 7 Blue coalition platforms (non-US) destroyed.

Breakdown:
- UK (2): EF2000_FGR4 destroyed by 48N6E3, R-73M
- Netherlands (2): F-16CM_BLK50 destroyed by R-77-1, R-73M
- Poland (2): AHS_KRAB destroyed by 9M55K
- Norway (1): NASAMS_LCHR destroyed by 9M542

Assumptions: 
- EF2000_FGR4 = UK (Eurofighter Typhoon primary user)
- F-16CM_BLK50 = Netherlands (common NATO F-16 operator)
- AHS_KRAB = Poland (KrAB is Polish system)
- NASAMS_LCHR = Norway (NASAMS is Norwegian-developed)
- All weapon types are Red (Russian) as per event data.

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
Headline: 3 Blue coalition platforms (non-US) destroyed.

Breakdown:
- GBR (UK): 2 platforms destroyed by Air-to-Air Missiles (e.g., AIM-120D)
- NOR (Norway): 1 platform destroyed by Surface-to-Air Missiles (e.g., RIM-162D)

Assumptions/uncertainties:
- Platform types "EF2000_FGR4" (UK) and "NASAMS_LCHR" (Norway) were classified as non-US Blue via ontology mapping (GBR/NOR nations).
- Weapon categories inferred from ontology: "AIM-120D" → Air-to-Air Missile (subClassOf bs:AirToAirMissile), "RIM-162D" → Surface-to-Air Missile (subClassOf bs:SurfaceToAirMissile).
- No platforms from POL/RDL were found in destroyed events (0 rows for these nations).
- SQL queries now correctly use `side = 'blue'` (lowercase) after initial case sensitivity error.

Grade the answer only against the ground truth. Numbers must match to count as correct (a total that is
off is wrong even if the method was reasonable). Give partial credit per correct sub-part of the breakdown.
Do not reward hedging or extra material. List specifically what was missed or wrong (e.g. weapon types
left out or wrongly included, units misattributed).
