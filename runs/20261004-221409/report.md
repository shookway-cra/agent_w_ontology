# Ontology vs. no-ontology agent comparison

Model: `qwen3:30b` - 2026-10-05 07:56

## Run statistics

| Question | Mode | Agent time | Model time | Tool time | Turns | Tool calls | Slowest tool call | Output tokens | Score |
|---|---|---|---|---|---|---|---|---|---|
| q0 | ontology OFF | 2m05s | 2m04s | 0m00s | 3 | 2 | 0.1s | 3,791 | 65 |
| q0 | ontology ON | 2m41s | 2m39s | 0m00s | 4 | 3 | 0.0s | 4,750 | 100 |
| q1 | ontology OFF | 2m08s | 2m07s | 0m00s | 3 | 2 | 0.0s | 3,907 | 15 |
| q1 | ontology ON | 2m30s | 2m28s | 0m01s | 5 | 4 | 0.5s | 4,517 | 0 |
| q2 | ontology OFF | 8m03s | 8m02s | 0m00s | 3 | 2 | 0.0s | 15,418 | 15 |
| q2 | ontology ON | 8m10s | 8m07s | 0m01s | 5 | 4 | 1.3s | 15,481 | 25 |
| q3 | ontology OFF | 2m08s | 2m07s | 0m00s | 3 | 2 | 0.0s | 3,887 | 0 |
| q3 | ontology ON | 3m00s | 2m57s | 0m01s | 4 | 3 | 0.4s | 5,489 | 45 |
| q4 | ontology OFF | 2m30s | 2m29s | 0m00s | 3 | 2 | 0.0s | 4,567 | 10 |
| q4 | ontology ON | 2m37s | 2m34s | 0m01s | 3 | 2 | 1.2s | 4,629 | 0 |
| q5 | ontology OFF | 2m20s | 2m19s | 0m00s | 3 | 2 | 0.0s | 4,262 | 5 |
| q5 | ontology ON | 4m16s | 4m14s | 0m00s | 3 | 2 | 0.0s | 7,799 | 10 |
| q6 | ontology OFF | 4m18s | 4m18s | 0m00s | 3 | 2 | 0.0s | 7,904 | 45 |
| q6 | ontology ON | 5m45s | 5m42s | 0m01s | 5 | 4 | 1.3s | 10,725 | 25 |

| Mode | Questions | Total agent time | Mean | Min | Max | Mean per turn | Mean score | Errors |
|---|---|---|---|---|---|---|---|---|
| ontology OFF | 7 | 23m32s | 3m22s | 2m05s | 8m03s | 67s | 22 | 0 |
| ontology ON | 7 | 28m58s | 4m08s | 2m30s | 8m10s | 59s | 29 | 0 |

| Question | Wall time (both modes + judge) | Judge time |
|---|---|---|
| q0 | 8m13s | 3m27s |
| q1 | 14m07s | 9m29s |
| q2 | 22m07s | 5m54s |
| q3 | 7m52s | 2m45s |
| q4 | 12m37s | 7m30s |
| q5 | 11m46s | 5m04s |
| q6 | 18m06s | 8m03s |

**Total run time:** 1h34m48s

| Question | Ontology OFF | Ontology ON |
|---|---|---|
| q0: Control: total expenditure | 65 (partially_correct) | 100 (correct) |
| q1: Air-to-air missile expenditure | 15 (incorrect) | 0 (incorrect) |
| q2: Precision-guided munitions (munition hierarchy) | 15 (incorrect) | 25 (incorrect) |
| q3: Cluster munition employment | 0 (incorrect) | 45 (partially_correct) |
| q4: Losses rolled up by force structure | 10 (incorrect) | 0 (incorrect) |
| q5: Air defense mission capability at a point in time | 5 (incorrect) | 10 (incorrect) |
| q6: Coalition partner losses | 45 (partially_correct) | 25 (incorrect) |

## q0: Control: total expenditure

**Question.** How many weapons were fired in total by each side, and which single weapon type was fired most often?

**Why the ontology matters.** Control question - answerable from the database alone. Both agents should get it right.

**Ground truth.** Weapons fired: blue 598, red 452 (total 1050). Most-fired weapon type: M795 (116).

### ontology OFF - score 65/100

2 tool calls, 3 turns, 125.3 s, 5,532 input / 3,791 output tokens

Headline numbers: Blue fired 598 weapons, Red fired 452 weapons. S-8KOM was the most frequently fired weapon type (48 firings).

Breakdown:
- Total weapons fired: 1,050 (598 blue + 452 red)
- Most fired weapon type: S-8KOM (48 occurrences)
- Other top weapon types: 9M338K (32), 9M96E2 (23), SB600 (8)

Assumptions:
- Events.weapon_type accurately reflects weapon types for WEAPON_FIRED events (confirmed by describe_database listing S-8KOM as 48 occurrences)
- Platform-side mapping via events.platform = platforms.name is valid (supported by platform count matching sides)
- No duplicate or misclassified WEAPON_FIRED events (1050 total matches event_type count from describe_database)

**Judge - missed or wrong:**
- Most-fired weapon is M795 (116), not S-8KOM (48)

<details><summary>Tool calls</summary>

**simdb__describe_database**
```
{}
```
**simdb__run_sql**
```
SELECT e.side, COUNT(*) AS total_weapons FROM events e JOIN platforms p ON e.platform = p.name WHERE e.event_type = 'WEAPON_FIRED' GROUP BY e.side
```
</details>

### ontology ON - score 100/100

3 tool calls, 4 turns, 160.9 s, 6,750 input / 4,750 output tokens

Headline: Blue fired 598 weapons, Red fired 452 weapons. Most common weapon: M795 (116 shots).

Breakdown:
- Blue: 598 weapons (598 total WEAPON_FIRED events linked to blue-side platforms)
- Red: 452 weapons (452 total WEAPON_FIRED events linked to red-side platforms)
- Top weapon type: M795 (116 occurrences, confirmed by SQL count)

Assumptions/Uncertainties:
- Weapon type "M795" is a 155mm artillery shell (validated via ontology__find_terms: "M795" matches artillery ammunition in ontology).
- No intercepts or non-firing events counted (only WEAPON_FIRED events included).
- Side determination via platform join (not events.side column) as events.side was not confirmed as reliable in database description.

<details><summary>Tool calls</summary>

**simdb__describe_database**
```
{}
```
**simdb__run_sql**
```
SELECT platforms.side, COUNT(*) AS total FROM events JOIN platforms ON events.platform = platforms.name WHERE events.event_type = 'WEAPON_FIRED' GROUP BY platforms.side
```
**simdb__run_sql**
```
SELECT events.weapon_type, COUNT(*) AS count FROM events WHERE events.event_type = 'WEAPON_FIRED' GROUP BY events.weapon_type ORDER BY count DESC LIMIT 1
```
</details>

## q1: Air-to-air missile expenditure

**Question.** How many air-to-air missiles did each side expend over the whole engagement?

**Why the ontology matters.** Weapon names come from different federates: WPN_AMRAAM_D and IZDELIYE_610M are aliases, WPN_KESTREL is a notional scenario weapon, and AMRAAM-ER looks like an AAM but is a SAM.

**Ground truth.** Air-to-air missiles fired - blue: 52, red: 22 (total 74). By type: blue AIM-120C7=6; blue AIM-120D=16; blue AIM-132=3; blue AIM-9X_BLK2=4; blue MBDA_METEOR=7; blue WPN_AMRAAM_D=8; blue WPN_KESTREL=8; red IZDELIYE_610M=3; red R-37M=2; red R-73M=5; red R-77-1=12. Note: AMRAAM-ER (fired) is a surface-launched SAM and is excluded; WPN_AMRAAM_D is an alias of AIM-120D, IZDELIYE_610M an alias of R-37M, WPN_KESTREL is a notional IR AAM.

### ontology OFF - score 15/100

2 tool calls, 3 turns, 127.7 s, 5,142 input / 3,907 output tokens

Headline: Blue expended 67, Red expended 19 air-to-air missiles.  
Breakdown:  
- Blue: 67 (AIM-120 variants: 32, R-77-1:12, R-73M:5, MBDA_METEOR:7, AIM-132:3, WPN_KESTREL:8, others: 10)  
- Red: 19 (R-37M:2, R-77-1:12, AIM-9X_BLK2:4, others: 1)  
Assumptions: Weapon types were classified as air-to-air based on authoritative database entries (no external knowledge used), and all WEAPON_FIRED events with these types were counted. Total matches sum of weapon-type counts from describe_database (86 total).

**Judge - missed or wrong:**
- Blue total 67, should be 52
- Red total 19, should be 22
- Red R-77-1 (12) and R-73M (5) counted under Blue
- Blue AIM-9X_BLK2 (4) counted under Red
- Red IZDELIYE_610M (3) missing
- AIM-120 variants lumped together as 32 (truth: C7 6 + D 16 + WPN_AMRAAM_D 8 = 30)

<details><summary>Tool calls</summary>

**simdb__describe_database**
```
{}
```
**simdb__run_sql**
```
SELECT side, COUNT(*) AS total_air_to_air_missiles FROM events WHERE event_type = 'WEAPON_FIRED' AND weapon_type IN ('AIM-120C7', 'AIM-120D', 'AIM-132', 'AIM-9X_BLK2', 'MBDA_METEOR', 'R-77-1', 'R-73M', 'R-37M', 'AMRAAM-ER', 'WPN_AMRAAM_D', 'WPN_KESTREL') GROUP BY side
```
</details>

### ontology ON - score 0/100

4 tool calls, 5 turns, 149.8 s, 4,358 input / 4,517 output tokens

Headline: Blue side expended 59 air-to-air missiles, Red side expended 19.

Breakdown:
- Blue: 59 (AMRAAM-ER, AIM-120D, AIM-120C7, R-77-1, R-37M, MBDA_METEOR, R-73M, AIM-9X_BLK2, AIM-132, WPN_AMRAAM_D)
- Red: 19 (same weapon types as Blue)

Assumptions: 
- AMRAAM-ER was included despite ontology misclassifying it as a SAM (real-world AAM); confirmed via weapon type list and standard military knowledge.
- All listed weapon types in the SQL IN clause are confirmed AAMs (e.g., R-77-1, AIM-120 series, METEOR).
- Side names "blue" and "red" align with simulation's force designations (no evidence of alternative side labels in data).

**Judge - missed or wrong:**
- Blue total 59, should be 52
- Red total 19, should be 22
- AMRAAM-ER included after overriding the ontology's (correct) SAM classification
- Red types (R-77-1, R-37M, R-73M) listed under Blue
- No per-type counts; Red breakdown says 'same weapon types as Blue'
- WPN_KESTREL and IZDELIYE_610M missing

<details><summary>Tool calls</summary>

**ontology__find_terms**
```
air-to-air missile
```
**ontology__sparql_query**
```
SELECT ?simTypeName WHERE { bs:AirToAirMissile bs:simTypeName ?simTypeName }
```
**simdb__run_sql**
```
SELECT DISTINCT weapon_type FROM events WHERE event_type = 'WEAPON_FIRED'
```
**simdb__run_sql**
```
SELECT platforms.side, COUNT(*) AS count FROM events JOIN platforms ON events.platform = platforms.name WHERE events.event_type = 'WEAPON_FIRED' AND events.weapon_type IN ('AMRAAM-ER', 'AIM-120D', 'AIM-120C7', 'R-77-1', 'R-37M', 'MBDA_METEOR', 'R-73M', 'AIM-9X_BLK2', 'AIM-132', 'WPN_AMRAAM_D') GROUP BY platforms.side
```
</details>

## q2: Precision-guided munitions (munition hierarchy)

**Question.** Not counting surface-to-air or air-to-air missiles, how many precision-guided munitions did the Blue coalition expend? Break the total down by category: missiles, guided bombs, guided rockets, guided artillery projectiles, and loitering munitions.

**Why the ontology matters.** PGM is a cross-cutting class: Excalibur (M982A1), APKWS_II and GMLRS are guided; XM1113 and Hydra M151 are not; TRIDENT_GLIDE_KIT is a notional GPS bomb kit; MGM-140B/PRSM are missiles.

**Ground truth.** Blue PGMs excluding SAMs/AAMs: total 272. missiles: 120 (AGM-114R=10, AGM-179_JAGM=18, AGM-88E=10, AGM-88G=12, BGM-109E=20, BGM-71F=5, JASSM-ER=24, MGM-140B=3, NSM_BLK1A=4, PRSM_INC1=6, RGM-184A=8); guided bombs: 84 (GBU-12=4, GBU-31V3=20, GBU-39=20, GBU-53B=24, TRIDENT_GLIDE_KIT=16); guided rockets: 50 (APKWS_II=14, M30A2=12, M31A2=24); guided artillery projectiles: 10 (M982A1=10); loitering munitions: 8 (SB600=8). Unguided Blue weapons that must NOT be counted: HYDRA70_M151, M795, M829A4, M830A1, M919, XM1113.

### ontology OFF - score 15/100

2 tool calls, 3 turns, 483.2 s, 12,668 input / 15,418 output tokens

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

**Judge - missed or wrong:**
- Total 255, should be 272
- Missiles 105, should be 120: RGM-184A (8) wrongly excluded as a SAM, TRIDENT_GLIDE_KIT wrongly included
- Guided bombs 94, should be 84: XM1113 and GEM-T wrongly included, TRIDENT_GLIDE_KIT missing
- Guided rockets 46, should be 50: unguided HYDRA70_M151 included, SB600 misfiled here, M30A2/M31A2 wrongly excluded as unguided
- Loitering munitions 0, should be 8 (SB600)

<details><summary>Tool calls</summary>

**simdb__describe_database**
```
{}
```
**simdb__run_sql**
```
SELECT weapon_type, COUNT(*) AS count
FROM events
WHERE event_type = 'WEAPON_FIRED' AND side = 'blue'
  AND weapon_type NOT IN (
    '40N6E', '48N6E3', '9M317M', '9M338K', '9M542', '9M55K', 'PAC-3_MSE',
    'AIM-120C7', 'AIM-120D', 'AIM-132', 'AIM-9X_BLK2', 'R-73M', 'R-77-1', 'MBDA_METEOR', 'R-37M',
    'RIM-162D', 'SM-2_BLK3C', 'SM-6_BLK1A', 'WPN_AMRAAM_D', 'WPN_KESTREL', 'FIM-92K'
  )
GROUP BY weapon_type
ORDER BY count DESC;
```
</details>

### ontology ON - score 25/100

4 tool calls, 5 turns, 489.7 s, 14,092 input / 15,481 output tokens

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

**Judge - missed or wrong:**
- Total 286, should be 272
- Missiles 162, should be 120: GEM-T (a SAM), TRIDENT_GLIDE_KIT (a bomb) and XM1113 (unguided) wrongly included
- Guided bombs 68, should be 84: TRIDENT_GLIDE_KIT missing
- Guided rockets 46, should be 50: unguided HYDRA70_M151 included, M30A2/M31A2 excluded, SB600 misfiled
- Loitering munitions 0, should be 8 (SB600)

<details><summary>Tool calls</summary>

**ontology__ontology_overview**
```
{}
```
**simdb__run_sql**
```
SELECT weapon_type, COUNT(*) AS count
FROM events
JOIN platforms ON events.platform = platforms.name
WHERE events.event_type = 'WEAPON_FIRED'
  AND platforms.side = 'Blue'
GROUP BY weapon_type
```
**simdb__describe_database**
```
{}
```
**simdb__run_sql**
```
SELECT weapon_type, COUNT(*) AS count
FROM events
JOIN platforms ON events.platform = platforms.name
WHERE events.event_type = 'WEAPON_FIRED'
  AND platforms.side = 'blue'
  AND weapon_type NOT IN ('AIM-120C7', 'AIM-120D', 'AIM-132', 'AIM-9X_BLK2', 'PAC-3_MSE')
GROUP BY weapon_type
```
</details>

## q3: Cluster munition employment

**Question.** Which cluster (submunition-dispensing) munitions were employed during the engagement? For each, give the weapon type, the side that used it, and the number of rounds fired.

**Why the ontology matters.** Requires warhead knowledge: MGM-140B is ATACMS Block IA (APAM submunitions), BURYA-12 is notional, while M30A2 (GMLRS Alternative Warhead) looks like the old DPICM rocket but has no submunitions.

**Ground truth.** Cluster munitions fired: total 53 rounds - MGM-140B (MGM-140B ATACMS Block IA) by blue: 3; 3O23 (3-O-23 152 mm cargo projectile (ICM)) by red: 14; 9M55K (9M55K 300 mm cargo rocket) by red: 24; BURYA-12 (Burya-12 cargo rocket (notional)) by red: 12. Not cluster: M30A2 GMLRS-AW (pre-formed fragments, replaced the DPICM M30), M31A2 (unitary).

### ontology OFF - score 0/100

2 tool calls, 3 turns, 127.9 s, 5,190 input / 3,887 output tokens

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

**Judge - missed or wrong:**
- None of the four true cluster munitions identified (MGM-140B, 3O23, 9M55K, BURYA-12)
- 3OF26, 3OF39, 3OF45 (HE rounds) and S-8KOM wrongly classed as cluster munitions
- Total 128, should be 53

<details><summary>Tool calls</summary>

**simdb__describe_database**
```
{}
```
**simdb__run_sql**
```
SELECT weapon_type, side, COUNT(*) AS rounds FROM events WHERE event_type = 'WEAPON_FIRED' AND weapon_type IN ('3OF26', '3OF39', '3OF45', 'S-8KOM') GROUP BY weapon_type, side
```
</details>

### ontology ON - score 45/100

3 tool calls, 4 turns, 179.5 s, 5,332 input / 5,489 output tokens

Headline: 2 cluster munition types employed, 38 rounds total.  
Breakdown:  
- 3O23 (3-O-23 152 mm cargo projectile): red side, 14 rounds  
- 9M55K (9M55K 300 mm cargo rocket): red side, 24 rounds  
Assumptions: Only weapon types explicitly matching ontology labels were counted; other cluster types (e.g., ATACMS_BlkIA) had zero firings. Side "red" is the coalition name per simulation metadata.

**Judge - missed or wrong:**
- MGM-140B (Blue, 3) missing; it looked for 'ATACMS_BlkIA' and found no firings
- BURYA-12 (Red, 12) missing
- Total 38, should be 53

<details><summary>Tool calls</summary>

**ontology__find_terms**
```
cluster
```
**ontology__sparql_query**
```
SELECT ?weapon ?name WHERE { ?weapon rdfs:subClassOf* bs:ClusterMunition . ?weapon rdfs:label ?name . }
```
**simdb__run_sql**
```
SELECT e.weapon_type, p.side, COUNT(*) AS count FROM events e JOIN platforms p ON e.platform = p.name WHERE e.event_type = 'WEAPON_FIRED' AND e.weapon_type IN ('ATACMS_BlkIA', 'Cluster bomb (dispenser)', 'RBK-500 SPBE-D', '9M55K', 'Burya12', '3O23') GROUP BY e.weapon_type, p.side
```
</details>

## q4: Losses rolled up by force structure

**Question.** For each Blue brigade-level unit (brigade, regiment, or wing), how many of its platforms were destroyed during the engagement?

**Why the ontology matters.** The database only has callsigns. Which callsign belongs to which squadron/battalion/brigade exists only in the ontology's chain of command (bs:subordinateTo).

**Ground truth.** Blue brigade/regiment/wing-level losses: 1st Armored Brigade Combat Team, 3ID: 8 of 30 (BLADE14, COBRA11, COBRA12, COBRA13, COBRA14, IRON13, THUNDER22, THUNDER24); 11th Masurian Artillery Regiment (POL): 2 of 4 (KRAB31, KRAB34); 140 Expeditionary Air Wing (RAF): 2 of 4 (RAPIER1, RAPIER3); 388th Fighter Wing: 2 of 8 (LIGHTNING12, LIGHTNING14); 52nd Fighter Wing: 2 of 8 (WEASEL22, WEASEL23); 22nd Air Refueling Wing: 1 of 1 (SHELL71); 10th Army Air and Missile Defense Command: 0 of 6; 41st Field Artillery Brigade: 0 of 4; 432nd Wing: 0 of 2; 4th Fighter Wing: 0 of 4; 552nd Air Control Wing: 0 of 1; 7th Bomb Wing: 0 of 2; Combat Aviation Brigade, 3ID: 0 of 4; Destroyer Squadron 60: 0 of 3; Main Operating Base NORTHSTAR: 0 of 1; Royal Norwegian Navy contribution: 0 of 1. Total Blue platforms destroyed: 18.

### ontology OFF - score 10/100

2 tool calls, 3 turns, 150.1 s, 5,689 input / 4,567 output tokens

Headline: 18 Blue platforms destroyed (1 each, no brigade grouping possible).

Breakdown: 
- 18 distinct Blue platforms destroyed, each with exactly 1 destruction event (BLADE14, COBRA11, COBRA12, COBRA13, COBRA14, IRON13, KRAB31, KRAB34, LIGHTNING12, LIGHTNING14, RAPIER1, RAPIER3, SHELL71, THUNDER22, THUNDER24, TROLL12, WEASEL22, WEASEL23).

Assumptions/uncertainties: 
- Simulation data contains no identifiable "brigade-level unit" names in platform names (e.g., no entries like "1st_Brigade" or "Regiment_3"). All destroyed platforms are individually identified by alphanumeric callsigns, not grouped by organizational unit. 
- AFSIM's platform table does not include organizational hierarchy fields (e.g., parent unit), so brigade-level aggregation is impossible with available data. 
- Platform names like "COBRA" and "KRAB" refer to specific vehicle types (e.g., M109A7 howitzers or M1A2 tanks), not command units.

**Judge - missed or wrong:**
- No per-unit breakdown; wrongly concluded unit hierarchy is unavailable
- All six units with losses missing (1st ABCT 8, 11th Masurian 2, 140 EAW 2, 388th FW 2, 52nd FW 2, 22nd ARW 1)

<details><summary>Tool calls</summary>

**simdb__describe_database**
```
{}
```
**simdb__run_sql**
```
SELECT p.name, COUNT(e.event_id) AS destroyed_count FROM platforms p JOIN events e ON p.name = e.platform WHERE p.side = 'blue' AND e.event_type = 'PLATFORM_BROKEN' GROUP BY p.name
```
</details>

### ontology ON - score 0/100

2 tool calls, 3 turns, 156.7 s, 7,147 input / 4,629 output tokens

The query for Blue coalition units with echelon "Brigade" returned **0 rows** in the ontology. The ontology's echelon facet explicitly lists "Brigade" as a valid echelon (e.g., `bs:Brigade`), but no matching units were found in the simulation's force structure. 

**Assumption**: The user's query assumes brigade-level units exist in the Blue coalition, but the simulation data contains none at the "Brigade" echelon. The ontology does not list "Regiment" or "Wing" as valid echelons (only "Battalion," "Company," etc.), so those terms do not match the simulation's structure. 

**Conclusion**: No Blue brigade-level units (as defined by the ontology) exist in the simulation, so **0 platforms were destroyed**.

---

**Headline**: 0 destroyed platforms across all Blue brigade-level units  
**Breakdown**: No Blue brigade-level units detected in simulation  
**Assumptions**:  
- "Brigade" is the only valid echelon term matching the ontology's `bs:Brigade` (not "Regiment" or "Wing").  
- Simulation lacks units at the "Brigade" echelon in the Blue coalition.

**Judge - missed or wrong:**
- Claimed no Blue brigade-level units exist; there are 16
- Wrongly said the ontology has no Regiment or Wing echelons
- Total 0 destroyed, should be 18

<details><summary>Tool calls</summary>

**ontology__ontology_overview**
```
{}
```
**ontology__sparql_query**
```
SELECT DISTINCT ?unitLabel WHERE { ?unit a bs:MilitaryUnit ; bs:echelon bs:Brigade ; bs:coalition bs:BlueCoalition ; rdfs:label ?unitLabel . }
```
</details>

## q5: Air defense mission capability at a point in time

**Question.** At T+90 minutes (time_s = 5400), which of Red's surface-to-air missile battalions were still able to engage? A battalion built from separate launchers, radars and command posts can engage only if it still has at least one operational engagement radar, one operational command post, and one operational launcher; a battalion of self-contained SHORAD vehicles can engage if any vehicle is operational.

**Why the ontology matters.** Needs system composition (which radar/CP/launchers form which battalion) and component roles (engagement vs surveillance radar), both from the ontology, joined to time-sliced status data.

**Ground truth.** Red SAM battalions at T+90 min: 1st Buk Battalion, 53 ZRBR: NOT capable (no operational EngagementRadar) [lost so far: BEREZA11, BEREZA13]; 1st S-400 Battalion, 1544 ZRP: NOT capable (no operational EngagementRadar) [lost so far: KREMEN12, KREMEN13]; 2nd S-400 Battalion, 1544 ZRP: MISSION-CAPABLE [lost so far: KREMEN25]; Air Defence Battalion, 7 MRR (Tor): MISSION-CAPABLE [lost so far: YASTREB52]

### ontology OFF - score 5/100

2 tool calls, 3 turns, 139.7 s, 5,099 input / 4,262 output tokens

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

**Judge - missed or wrong:**
- No Red battalion identified by name
- Reasoned over Blue equipment (M-SHORAD_INC1, NASAMS, MPQ-65) instead of Red
- 2nd S-400 Battalion is capable, not counted
- Tor battalion is capable, not identified

<details><summary>Tool calls</summary>

**simdb__describe_database**
```
{}
```
**simdb__run_sql**
```
SELECT platform, state FROM platform_status WHERE time_s = 5400 AND platform IN (SELECT name FROM platforms WHERE side = 'red' AND type IN ('M-SHORAD_INC1', '9S36M', '9S510M', 'MPQ-65A_RADAR', 'NASAMS_FDC', '9P85TE2_TEL', '9A317M_TELAR', '9A53-S', 'NASAMS_LCHR'))
```
</details>

### ontology ON - score 10/100

2 tool calls, 3 turns, 256.0 s, 8,438 input / 7,799 output tokens

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

**Judge - missed or wrong:**
- No battalion identified by name
- 2nd S-400 Battalion is capable, judged not capable
- Tor battalion is capable but its Tor-M2 was judged non-operational
- Pantsir named as the capable unit; it is not one of the four SAM battalions

<details><summary>Tool calls</summary>

**simdb__describe_database**
```
{}
```
**simdb__run_sql**
```
SELECT type, COUNT(*) AS active_count FROM platform_status ps JOIN platforms p ON ps.platform = p.name WHERE ps.time_s = 5400 AND p.side = 'red' AND ps.state = 'ACTIVE' GROUP BY type;
```
</details>

## q6: Coalition partner losses

**Question.** How many platforms belonging to Blue coalition partners other than the United States were destroyed? Break it down by nation, and say what category of Red weapon destroyed each one.

**Why the ontology matters.** Side 'blue' in the sim lumps all coalition members together. Nationality comes from the unit hierarchy in the ontology, and the weapon category from the munition hierarchy.

**Ground truth.** Non-US Blue coalition platforms destroyed: 5 - by nation: Norway 1, Poland 2, United Kingdom 2. Details: TROLL12 (Norway) killed by 9M542 [guided artillery rocket] from METEL22 at t=6146s; KRAB31 (Poland) killed by 9M55K [artillery rocket (cluster)] from METEL21 at t=4427s; KRAB34 (Poland) killed by 9M55K [artillery rocket (cluster)] from METEL22 at t=6832s; RAPIER1 (United Kingdom) killed by R-73M [air-to-air missile] from SOKOL07 at t=1885s; RAPIER3 (United Kingdom) killed by 48N6E3 [surface-to-air missile] from KREMEN25 at t=1181s

### ontology OFF - score 45/100

2 tool calls, 3 turns, 258.3 s, 8,789 input / 7,904 output tokens

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

**Judge - missed or wrong:**
- Total 7, should be 5
- Netherlands 2 wrongly included (nation guessed from the aircraft type)
- Weapon names given but not weapon categories, which the question asked for

<details><summary>Tool calls</summary>

**simdb__describe_database**
```
{}
```
**simdb__run_sql**
```
SELECT p.name, p.type, e.weapon_type FROM events e JOIN platforms p ON e.platform = p.name WHERE e.event_type = 'PLATFORM_BROKEN' AND p.side = 'blue' AND p.type NOT IN ('DDG-51_FLT_IIA', 'F-15EX', 'F-35A', 'M109A7', 'M1A2_SEPV3', 'M2A4', 'B-1B', 'E-3G', 'KC-46A', 'M142_HIMARS', 'M903_LS', 'M795', 'M829A4', 'M830A1', 'M919', 'M982A1')
```
</details>

### ontology ON - score 25/100

4 tool calls, 5 turns, 345.1 s, 12,854 input / 10,725 output tokens

Headline: 3 Blue coalition platforms (non-US) destroyed.

Breakdown:
- GBR (UK): 2 platforms destroyed by Air-to-Air Missiles (e.g., AIM-120D)
- NOR (Norway): 1 platform destroyed by Surface-to-Air Missiles (e.g., RIM-162D)

Assumptions/uncertainties:
- Platform types "EF2000_FGR4" (UK) and "NASAMS_LCHR" (Norway) were classified as non-US Blue via ontology mapping (GBR/NOR nations).
- Weapon categories inferred from ontology: "AIM-120D" → Air-to-Air Missile (subClassOf bs:AirToAirMissile), "RIM-162D" → Surface-to-Air Missile (subClassOf bs:SurfaceToAirMissile).
- No platforms from POL/RDL were found in destroyed events (0 rows for these nations).
- SQL queries now correctly use `side = 'blue'` (lowercase) after initial case sensitivity error.

**Judge - missed or wrong:**
- Total 3, should be 5
- Poland (2, 9M55K cluster artillery rocket) missed
- UK categories wrong: one was a SAM (48N6E3), one an AAM (R-73M); it cited AIM-120D, a Blue weapon
- Norway category wrong: guided artillery rocket (9M542), not SAM; it cited RIM-162D, a Blue weapon

<details><summary>Tool calls</summary>

**ontology__ontology_overview**
```
{}
```
**simdb__run_sql**
```
SELECT 
    CASE 
        WHEN p.name LIKE '%GBR%' THEN 'GBR' 
        WHEN p.name LIKE '%POL%' THEN 'POL' 
        WHEN p.name LIKE '%NOR%' THEN 'NOR' 
        WHEN p.name LIKE '%RDL%' THEN 'RDL' 
        ELSE 'Unknown' 
    END AS nation,
    COUNT(*) AS destroyed
FROM events e
JOIN platforms p ON e.platform = p.name
WHERE e.event_type = 'PLATFORM_BROKEN'
  AND p.side = 'Blue'
  AND e.platform NOT LIKE '%USA%'
  AND (p.name LIKE '%GBR%' OR p.name LIKE '%POL%' OR p.name LIKE '%NOR%' OR p.name LIKE '%RDL%')
GROUP BY nation;
```
**simdb__run_sql**
```
SELECT name FROM platforms WHERE side = 'Blue' AND name NOT LIKE '%USA%';
```
**simdb__describe_database**
```
{}
```
</details>
