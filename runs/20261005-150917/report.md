# Ontology vs. no-ontology agent comparison

Model: `gpt-oss:20b` - 2026-10-05 15:41

## Run statistics

| Question | Mode | Agent time | Model time | Tool time | Turns | Tool calls | Slowest tool call | Output tokens | Score |
|---|---|---|---|---|---|---|---|---|---|
| q0 | ontology OFF | 0m17s | 0m16s | 0m00s | 5 | 4 | 0.2s | 706 | 100 |
| q0 | ontology ON | 0m14s | 0m12s | 0m00s | 4 | 3 | 0.0s | 447 | 100 |
| q1 | ontology OFF | 1m24s | 1m23s | 0m00s | 10 | 9 | 0.1s | 3,974 | 30 |
| q1 | ontology ON | 1m38s | 1m32s | 0m04s | 16 | 15 | 3.2s | 4,404 | 95 |
| q2 | ontology OFF | 3m31s | 3m30s | 0m00s | 17 | 16 | 0.0s | 10,775 | 10 |
| q2 | ontology ON | 2m49s | 2m42s | 0m05s | 25 | 24 | 3.3s | 7,677 | 100 |
| q3 | ontology OFF | 1m24s | 1m23s | 0m00s | 14 | 13 | 0.0s | 3,766 | 0 |
| q3 | ontology ON | 1m07s | 1m00s | 0m05s | 13 | 12 | 3.7s | 2,862 | 100 |
| q4 | ontology OFF | 2m43s | 2m42s | 0m00s | 13 | 12 | 0.0s | 7,849 | 25 |
| q4 | ontology ON | 2m40s | 2m25s | 0m13s | 15 | 14 | 4.0s | 7,186 | 100 |
| q5 | ontology OFF | 2m42s | 2m41s | 0m00s | 11 | 10 | 0.0s | 7,205 | 5 |
| q5 | ontology ON | 2m58s | 2m45s | 0m11s | 34 | 33 | 3.4s | 6,891 | 0 |
| q6 | ontology OFF | 1m52s | 1m51s | 0m00s | 8 | 7 | 0.0s | 4,986 | 20 |
| q6 | ontology ON | 5m32s | 5m26s | 0m04s | 6 | 5 | 3.4s | 14,691 | 75 |

| Mode | Questions | Total agent time | Mean | Min | Max | Mean per turn | Mean score | Errors |
|---|---|---|---|---|---|---|---|---|
| ontology OFF | 7 | 13m52s | 1m59s | 0m17s | 3m31s | 11s | 27 | 0 |
| ontology ON | 7 | 16m58s | 2m25s | 0m14s | 5m32s | 9s | 81 | 0 |

| Question | Wall time (both modes + judge) | Judge time |
|---|---|---|
| q0 | 0m30s | 0m00s |
| q1 | 3m02s | 0m00s |
| q2 | 6m20s | 0m00s |
| q3 | 2m31s | 0m00s |
| q4 | 5m23s | 0m00s |
| q5 | 5m48s | 0m00s |
| q6 | 7m24s | 0m00s |

**Total run time:** 30m58s

| Question | Ontology OFF | Ontology ON |
|---|---|---|
| q0: Control: total expenditure | 100 (correct) | 100 (correct) |
| q1: Air-to-air missile expenditure | 30 (incorrect) | 95 (correct) |
| q2: Precision-guided munitions (munition hierarchy) | 10 (incorrect) | 100 (correct) |
| q3: Cluster munition employment | 0 (incorrect) | 100 (correct) |
| q4: Losses rolled up by force structure | 25 (incorrect) | 100 (correct) |
| q5: Air defense mission capability at a point in time | 5 (incorrect) | 0 (incorrect) |
| q6: Coalition partner losses | 20 (incorrect) | 75 (partially_correct) |

## q0: Control: total expenditure

**Question.** How many weapons were fired in total by each side, and which single weapon type was fired most often?

**Why the ontology matters.** Control question - answerable from the database alone. Both agents should get it right.

**Ground truth.** Weapons fired: blue 598, red 452 (total 1050). Most-fired weapon type: M795 (116).

### ontology OFF - score 100/100

4 tool calls, 5 turns, 16.8 s, 1,024 input / 706 output tokens

**Headline figures**  
- **Total weapons fired:** 1 050  
- **Blue side:** 598 weapons fired  
- **Red side:** 452 weapons fired  
- **Most‑fired weapon type:** **M795** (116 rounds)

**Breakdown**  

| Side | Weapons fired |
|------|---------------|
| Blue | 598 |
| Red  | 452 |

**Most common weapon type**  
- **M795** – 116 shots, 11 % of all fires. The next most frequent types are 3OF45 (68), S‑8KOM (48), 57E6E (48), and 9M338K (32).

**Verification**  
- The sum of the per‑side counts equals the total number of `WEAPON_FIRED` events: 598 + 452 = 1 050, matching the overall count query.  
- The top weapon type is confirmed by ordering the `weapon_type` counts and selecting the highest value.

**Assumptions / Uncertainties**  
- The classification of sides is taken directly from the `side` column in the `events` table; no re‑classification was needed.  
- Weapon names are used as‑is; if alternate naming conventions existed in the simulation, they would appear as distinct `weapon_type` values. No alias mapping was applied.  
- All `WEAPON_FIRED` events are assumed to represent discrete expended weapons; no filtering for type (e.g., missiles vs. bullets) was necessary for the requested totals.

<details><summary>Tool calls</summary>

**simdb__run_sql**
```
SELECT side, COUNT(*) AS fired_count FROM events WHERE event_type='WEAPON_FIRED' GROUP BY side;
```
**simdb__run_sql**
```
SELECT weapon_type, COUNT(*) AS fired_count FROM events WHERE event_type='WEAPON_FIRED' GROUP BY weapon_type ORDER BY fired_count DESC LIMIT 1;
```
**simdb__run_sql**
```
SELECT weapon_type, COUNT(*) AS fired_count FROM events WHERE event_type='WEAPON_FIRED' GROUP BY weapon_type ORDER BY fired_count DESC LIMIT 5;
```
**simdb__run_sql**
```
SELECT COUNT(*) FROM events WHERE event_type='WEAPON_FIRED';
```
</details>

### ontology ON - score 100/100

3 tool calls, 4 turns, 13.7 s, 1,823 input / 447 output tokens

**Total weapons fired**

| Side | Weapons fired |
|------|---------------|
| Blue | 598 |
| Red  | 452 |

**Weapon type fired most often**

| Weapon type | Fires |
|-------------|-------|
| **M795**    | 116 |

*The totals come directly from the `events` table (rows with `event_type = 'WEAPON_FIRED'`), grouped by `side`. The most‑fired weapon is the one with the highest count of such events, which is the M795 missile.*

<details><summary>Tool calls</summary>

**simdb__run_sql**
```
SELECT side, COUNT(*) as total_fired FROM events WHERE event_type='WEAPON_FIRED' GROUP BY side;
```
**simdb__run_sql**
```
SELECT weapon_type, COUNT(*) as cnt FROM events WHERE event_type='WEAPON_FIRED' GROUP BY weapon_type ORDER BY cnt DESC LIMIT 1;
```
**simdb__run_sql**
```
SELECT weapon_type, COUNT(*) as cnt FROM events WHERE event_type='WEAPON_FIRED' GROUP BY weapon_type ORDER BY cnt DESC;
```
</details>

## q1: Air-to-air missile expenditure

**Question.** How many air-to-air missiles did each side expend over the whole engagement?

**Why the ontology matters.** Weapon names come from different federates: WPN_AMRAAM_D and IZDELIYE_610M are aliases, WPN_KESTREL is a notional scenario weapon, and AMRAAM-ER looks like an AAM but is a SAM.

**Ground truth.** Air-to-air missiles fired - blue: 52, red: 22 (total 74). By type: blue AIM-120C7=6; blue AIM-120D=16; blue AIM-132=3; blue AIM-9X_BLK2=4; blue MBDA_METEOR=7; blue WPN_AMRAAM_D=8; blue WPN_KESTREL=8; red IZDELIYE_610M=3; red R-37M=2; red R-73M=5; red R-77-1=12. Note: AMRAAM-ER (fired) is a surface-launched SAM and is excluded; WPN_AMRAAM_D is an alias of AIM-120D, IZDELIYE_610M an alias of R-37M, WPN_KESTREL is a notional IR AAM.

### ontology OFF - score 30/100

9 tool calls, 10 turns, 83.7 s, 2,960 input / 3,974 output tokens

**Air‑to‑air missiles expended**

| Side | Total A/A missiles expended |
|------|-----------------------------|
| Blue | **68** |
| Red  | **31** |

*The totals are based on the `events` table for all `WEAPON_FIRED` records whose `weapon_type` matches the known air‑to‑air missile catalog (AIM‑120C7, AIM‑120D, AIM‑9X_BLK2, R‑73M, R‑77‑1, R‑37M, 9M317M, WPN_AMRAAM_D, WPN_KESTREL, FIM‑92K).  The sum of all such events is 99, which splits as shown above.*

**Breakdown by missile type**

| Weapon type      | Blue | Red | Total |
|------------------|------|-----|-------|
| 9M317M           | 0    | 12  | 12 |
| AIM‑120C7        | 6    | 0   | 6  |
| AIM‑120D         | 16   | 0   | 16 |
| AIM‑9X_BLK2      | 4    | 0   | 4  |
| FIM‑92K          | 26   | 0   | 26 |
| R‑37M            | 0    | 2   | 2  |
| R‑73M            | 0    | 5   | 5  |
| R‑77‑1           | 0    | 12  | 12 |
| WPN_AMRAAM_D     | 8    | 0   | 8  |
| WPN_KESTREL      | 8    | 0   | 8  |
| **Total**        | **68** | **31** | **99** |

**Verification**  
- Query 1: `SELECT COUNT(*) FROM events WHERE event_type='WEAPON_FIRED' AND weapon_type IN (…)` → 99 total A/A missile firings.  
- Query 2: `SELECT side, COUNT(*) FROM events WHERE event_type='WEAPON_FIRED' AND weapon_type IN (…) GROUP BY side;` → 68 for blue, 31 for red.  
- The summed counts match the total of 99.

**Assumptions / Uncertainties**  
- Only weapon types listed above are treated as air‑to‑air; other types present in the database (e.g., AIM‑132, R‑73M duplicates) were omitted unless clearly a known A/A missile.  
- The database does not indicate sub‑type distinctions beyond the weapon_type string, so each string is counted as a separate missile type.  

Thus, over the entire engagement, Blue forces expended 68 air‑to‑air missiles, while Red forces expended 31.

**Judge - missed or wrong:**
- Blue 68, should be 52
- Red 31, should be 22
- SAMs FIM-92K (26) and 9M317M (12) counted as AAMs
- AIM-132, MBDA_METEOR, IZDELIYE_610M missing

<details><summary>Tool calls</summary>

**simdb__describe_database**
```
{}
```
**simdb__run_sql**
```
SELECT weapon_type, COUNT(*) FROM events WHERE event_type='WEAPON_FIRED' AND weapon_type IN ('AIM-120C7','AIM-120D','AIM-9X_BLK2','R-73M','R-77-1','R-37M','9M317M','WPN_AMRAAM_D','WPN_KESTREL','FIM-92K') GROUP BY weapon_type;
```
**simdb__run_sql**
```
SELECT weapon_type, COUNT(*) FROM events WHERE event_type='WEAPON_FIRED' AND weapon_type='AIM-132' GROUP BY weapon_type;
```
**simdb__run_sql**
```
SELECT side, COUNT(*) FROM events WHERE event_type='WEAPON_FIRED' AND weapon_type IN ('9M317M','AIM-120C7','AIM-120D','AIM-9X_BLK2','FIM-92K','R-37M','R-73M','R-77-1','WPN_AMRAAM_D','WPN_KESTREL') GROUP BY side;
```
**simdb__run_sql**
```
SELECT weapon_type, side, COUNT(*) FROM events WHERE event_type='WEAPON_FIRED' AND weapon_type IN ('9M317M','AIM-120C7','AIM-120D','AIM-9X_BLK2','FIM-92K','R-37M','R-73M','R-77-1','WPN_AMRAAM_D','WPN_KESTREL') GROUP BY weapon_type, side ORDER BY weapon_type, side;
```
**simdb__run_sql**
```
SELECT DISTINCT side FROM events WHERE event_type='WEAPON_FIRED' AND weapon_type IN ('9M317M','AIM-120C7','AIM-120D','AIM-9X_BLK2','FIM-92K','R-37M','R-73M','R-77-1','WPN_AMRAAM_D','WPN_KESTREL');
```
**simdb__run_sql**
```
SELECT weapon_type, COUNT(*) FROM events WHERE event_type='WEAPON_FIRED' AND weapon_type IN ('9M317M','AIM-120C7','AIM-120D','AIM-9X_BLK2','FIM-92K','R-37M','R-73M','R-77-1','WPN_AMRAAM_D','WPN_KESTREL') GROUP BY weapon_type ORDER BY weapon_type;
```
**simdb__run_sql**
```
SELECT side, weapon_type, COUNT(*) FROM events WHERE event_type='WEAPON_FIRED' AND weapon_type IN ('9M317M','AIM-120C7','AIM-120D','AIM-9X_BLK2','FIM-92K','R-37M','R-73M','R-77-1','WPN_AMRAAM_D','WPN_KESTREL') GROUP BY side, weapon_type ORDER BY side, weapon_type;
```
**simdb__run_sql**
```
SELECT SUM(cnt) as total FROM (SELECT COUNT(*) as cnt FROM events WHERE event_type='WEAPON_FIRED' AND weapon_type IN ('9M317M','AIM-120C7','AIM-120D','AIM-9X_BLK2','FIM-92K','R-37M','R-73M','R-77-1','WPN_AMRAAM_D','WPN_KESTREL'));
```
</details>

### ontology ON - score 95/100

15 tool calls, 16 turns, 97.7 s, 5,007 input / 4,404 output tokens

**Air‑to‑air missiles expended**

| Side | AAM expended |  Source |
|------|---------------|----------|
| Blue | **52** | Count of WEAPON_FIRED events whose `weapon_type` is one of the 11 AAMs listed below. |
| Red  | **22** | Same count method. |

**AAM types included (per the ontology)**  

- AIM‑132  
- MBDA_METEOR  
- WPN_KESTREL  
- AIM‑120C7  
- IZDELIYE_610M  
- AIM‑120D  
- R‑73M  
- WPN_AMRAAM_D  
- R‑77‑1  
- AIM‑9X_BLK2  
- R‑37M  

(AMRAAM‑ER is *not* counted because the ontology classifies it as a Medium‑Range SAM, not an Air‑to‑Air Missile.)

**Breakdown for the Blue side (counts per weapon)**  

| Weapon | Count |
|--------|-------|
| AIM‑120C7 | 6 |
| AIM‑120D  | 16 |
| AIM‑132   | 3 |
| AIM‑9X_BLK2 | 4 |
| MBDA_METEOR | 7 |
| WPN_AMRAAM_D | 8 |
| WPN_KESTREL | 8 |

**Assumptions / Uncertainties**  

- Classification strictly follows the ontology; any discrepancy with common‑sense naming (e.g., AMRAAM‑ER) is resolved by the ontology’s hierarchy.  
- Only events of type `WEAPON_FIRED` are counted; no other event types (e.g., `WEAPON_HIT`) are considered for expended counts.  
- The side is taken from the `side` field in the events table, which is inferred from the platform’s coalition.  

Thus, the Blue coalition expended 52 AAMs and the Red coalition expended 22 over the entire engagement.

**Judge - missed or wrong:**
- Red per-type breakdown not given

<details><summary>Tool calls</summary>

**ontology__ontology_overview**
```
{}
```
**ontology__sparql_query**
```
SELECT DISTINCT ?simTypeName WHERE { ?t a bs:SimulationType ; a bs:AirToAirMissile ; bs:simTypeName ?simTypeName }
```
**simdb__run_sql**
```
SELECT side, COUNT(*) as cnt FROM events WHERE event_type='WEAPON_FIRED' AND weapon_type IN ('AIM-132','MBDA_METEOR','WPN_KESTREL','AIM-120C7','IZDELIYE_610M','AIM-120D','R-73M','WPN_AMRAAM_D','R-77-1','AIM-9X_BLK2','R-37M') GROUP BY side
```
**simdb__run_sql**
```
SELECT DISTINCT weapon_type FROM events WHERE event_type='WEAPON_FIRED' AND weapon_type LIKE '%AIM-9%'
```
**simdb__run_sql**
```
SELECT DISTINCT weapon_type FROM events WHERE event_type='WEAPON_FIRED' AND weapon_type LIKE '%R-73%'
```
**simdb__run_sql**
```
SELECT DISTINCT weapon_type FROM events WHERE event_type='WEAPON_FIRED' AND weapon_type LIKE '%AMRAAM%'
```
**simdb__run_sql**
```
SELECT DISTINCT weapon_type FROM events WHERE event_type='WEAPON_FIRED' AND weapon_type LIKE '%AIM-120%'
```
**simdb__run_sql**
```
SELECT side, COUNT(*) as cnt FROM events WHERE event_type='WEAPON_FIRED' AND weapon_type IN ('AIM-132','MBDA_METEOR','WPN_KESTREL','AIM-120C7','IZDELIYE_610M','AIM-120D','R-73M','WPN_AMRAAM_D','R-77-1','AIM-9X_BLK2','R-37M','AMRAAM-ER') GROUP BY side
```
**simdb__run_sql**
```
SELECT DISTINCT weapon_type FROM events WHERE event_type='WEAPON_FIRED'
```
**ontology__sparql_query**
```
SELECT ?super WHERE { ?t a bs:SimulationType ; a bs:AirToAirMissile ; bs:simTypeName "AMRAAM-ER" . ?t a ?super . FILTER(?super != bs:SimulationType) }
```
**ontology__sparql_query**
```
SELECT ?super WHERE { ?t a bs:SimulationType ; bs:simTypeName "AMRAAM-ER" . ?t a ?super . FILTER(?super != bs:SimulationType) }
```
**simdb__run_sql**
```
SELECT side, COUNT(*) as cnt FROM events WHERE event_type='WEAPON_FIRED' AND weapon_type IN ('AIM-132','MBDA_METEOR','WPN_KESTREL','AIM-120C7','IZDELIYE_610M','AIM-120D','R-73M','WPN_AMRAAM_D','R-77-1','AIM-9X_BLK2','R-37M') GROUP BY side
```
**simdb__run_sql**
```
SELECT weapon_type, COUNT(*) as cnt FROM events WHERE event_type='WEAPON_FIRED' AND side='blue' AND weapon_type IN ('AIM-132','MBDA_METEOR','WPN_KESTREL','AIM-120C7','IZDELIYE_610M','AIM-120D','R-73M','WPN_AMRAAM_D','R-77-1','AIM-9X_BLK2','R-37M','AMRAAM-ER') GROUP BY weapon_type
```
**simdb__run_sql**
```
SELECT weapon_type, COUNT(*) as cnt FROM events WHERE event_type='WEAPON_FIRED' AND side='red' AND weapon_type IN ('AIM-132','MBDA_METEOR','WPN_KESTREL','AIM-120C7','IZDELIYE_610M','AIM-120D','R-73M','WPN_AMRAAM_D','R-77-1','AIM-9X_BLK2','R-37M','AMRAAM-ER') GROUP BY weapon_type
```
**simdb__run_sql**
```
SELECT DISTINCT side FROM platforms
```
</details>

## q2: Precision-guided munitions (munition hierarchy)

**Question.** Not counting surface-to-air or air-to-air missiles, how many precision-guided munitions did the Blue coalition expend? Break the total down by category: missiles, guided bombs, guided rockets, guided artillery projectiles, and loitering munitions.

**Why the ontology matters.** PGM is a cross-cutting class: Excalibur (M982A1), APKWS_II and GMLRS are guided; XM1113 and Hydra M151 are not; TRIDENT_GLIDE_KIT is a notional GPS bomb kit; MGM-140B/PRSM are missiles.

**Ground truth.** Blue PGMs excluding SAMs/AAMs: total 272. missiles: 120 (AGM-114R=10, AGM-179_JAGM=18, AGM-88E=10, AGM-88G=12, BGM-109E=20, BGM-71F=5, JASSM-ER=24, MGM-140B=3, NSM_BLK1A=4, PRSM_INC1=6, RGM-184A=8); guided bombs: 84 (GBU-12=4, GBU-31V3=20, GBU-39=20, GBU-53B=24, TRIDENT_GLIDE_KIT=16); guided rockets: 50 (APKWS_II=14, M30A2=12, M31A2=24); guided artillery projectiles: 10 (M982A1=10); loitering munitions: 8 (SB600=8). Unguided Blue weapons that must NOT be counted: HYDRA70_M151, M795, M829A4, M830A1, M919, XM1113.

### ontology OFF - score 10/100

16 tool calls, 17 turns, 210.8 s, 3,885 input / 10,775 output tokens

**Precision‑guided munitions expended by the Blue coalition (excluding surface‑to‑air and air‑to‑air missiles)**  
**Total:** **433**  

| Category | Count |
|----------|-------|
| Missiles | 133 |
| Guided bombs | 102 |
| Guided rockets | 38 |
| Guided artillery projectiles | 152 |
| Loitering munitions | 8 |

### How the numbers were derived

1. **Identified Blue‑coalition fire events**  
   ```sql
   SELECT COUNT(*) FROM events
   WHERE event_type='WEAPON_FIRED' AND side='blue';
   ```
   – 598 total Blue‑coalition weapon firings.

2. **Excluded surface‑to‑air and air‑to‑air missiles**  
   Weapon types identified from the event log as SAM or air‑to‑air (e.g., SM‑2, SM‑6, PAC‑3, RIM‑162, RGM‑184, AIM‑120, AIM‑9, WPN_AMRAAM_D, BGM‑71F, MBDA_METEOR, AMRAAM‑ER, etc.) were removed.  
   Excluded count = 140.

3. **Grouped remaining weapons into categories**  
   Using the distinct `weapon_type` values, we mapped each type to one of the five requested categories.  
   *Missiles* (air‑to‑surface guided missiles): JASSM‑ER, BGM‑109E, AGM‑179_JAGM, M982A1, AGM‑88E, AGM‑88G, AGM‑114R, WPN_KESTREL, PRSM_INC1, NSM_BLK1A, MGM‑140B, **GEM‑T** (included as a missile; see assumptions).  
   *Guided bombs*: GBU‑12, GBU‑31V3, GBU‑39, GBU‑53B, XM1113, TRIDENT_GLIDE_KIT.  
   *Guided rockets*: HYDRA70_M151, APKWS_II.  
   *Guided artillery projectiles*: M795, M30A2, M31A2.  
   *Loitering munitions*: SB600.

4. **Counted each category**  
   Counts obtained via separate `SELECT COUNT(*)` queries for each set of weapon types (listed above).  
   *Missiles*: 133  
   *Guided bombs*: 102  
   *Guided rockets*: 38  
   *Guided artillery projectiles*: 152  
   *Loitering munitions*: 8

5. **Verification**  
   The sum of category counts (433) + excluded missiles (140) + other non‑guided weapons (M919, M829A4, M830A1 – 25) = 598, matching the total Blue‑coalition firings.

### Assumptions & Uncertainties

* **GEM‑T**: The database lists `GEM-T` as a weapon type fired by Blue platforms. It is not explicitly labeled as a SAM or air‑to‑air missile in the event log. Based on background knowledge, GEM‑T is a ground‑attack guided missile, so it was counted in the *missiles* category. If GEM‑T is a different weapon (e.g., a sensor or missile of another type), the missile count would be 125 instead of 133.  
* **Unclassified weapons**: M919 (15), M829A4 (7), and M830A1 (3) were not included in any category because they are unguided artillery rounds or tank penetrators.  
* **Other potential loitering munitions**: No additional loitering munitions (e.g., LANCET-3) appeared in the event log for Blue, so the loitering count is solely from SB600.

These numbers are based directly on the AFSIM event log and reflect all weapon firings by the Blue coalition that are precision‑guided but not surface‑to‑air or air‑to‑air missiles.

**Judge - missed or wrong:**
- Total 433, should be 272
- Missiles 133, should be 120 (GEM-T, M982A1, WPN_KESTREL, MGM-140B wrongly in; RGM-184A, BGM-71F wrongly out)
- Guided bombs 102, should be 84 (XM1113 included)
- Guided rockets 38, should be 50 (unguided HYDRA70 in; M30A2, M31A2 out)
- Guided artillery 152, should be 10 (unguided M795 counted)

<details><summary>Tool calls</summary>

**simdb__describe_database**
```
{}
```
**simdb__run_sql**
```
SELECT DISTINCT weapon_type FROM events WHERE event_type='WEAPON_FIRED' AND (weapon_type LIKE 'SM-%' OR weapon_type LIKE 'PAC-%' OR weapon_type LIKE 'RIM-%' OR weapon_type LIKE 'RGM-%' OR weapon_type LIKE 'AIM-%' OR weapon_type LIKE 'FIM-%' OR weapon_type LIKE 'R-%')
```
**simdb__run_sql**
```
SELECT DISTINCT weapon_type, COUNT(*) AS cnt FROM events WHERE event_type='WEAPON_FIRED' AND side='blue' GROUP BY weapon_type ORDER BY cnt DESC
```
**simdb__run_sql**
```
SELECT weapon_type, COUNT(*) AS cnt FROM events WHERE event_type='WEAPON_FIRED' AND side='blue' GROUP BY weapon_type ORDER BY cnt DESC
```
**simdb__run_sql**
```
SELECT weapon_type, COUNT(*) AS cnt FROM events WHERE event_type='WEAPON_FIRED' AND side='blue' AND weapon_type IN ('JASSM-ER','BGM-109E','AGM-179_JAGM','M982A1','AGM-88E','AGM-88G','AGM-114R','WPN_KESTREL','PRSM_INC1','NSM_BLK1A','MGM-140B') GROUP BY weapon_type
```
**simdb__run_sql**
```
SELECT weapon_type, COUNT(*) AS cnt FROM events WHERE event_type='WEAPON_FIRED' AND side='blue' AND weapon_type IN ('GBU-12','GBU-31V3','GBU-39','GBU-53B','XM1113','TRIDENT_GLIDE_KIT') GROUP BY weapon_type
```
**simdb__run_sql**
```
SELECT weapon_type, COUNT(*) AS cnt FROM events WHERE event_type='WEAPON_FIRED' AND side='blue' AND weapon_type IN ('HYDRA70_M151','APKWS_II') GROUP BY weapon_type
```
**simdb__run_sql**
```
SELECT weapon_type, COUNT(*) AS cnt FROM events WHERE event_type='WEAPON_FIRED' AND side='blue' AND weapon_type IN ('M795','M30A2','M31A2') GROUP BY weapon_type
```
**simdb__run_sql**
```
SELECT COUNT(*) AS cnt FROM events WHERE event_type='WEAPON_FIRED' AND side='blue' AND weapon_type='SB600'
```
**simdb__run_sql**
```
SELECT COUNT(*) AS total FROM events WHERE event_type='WEAPON_FIRED' AND side='blue'
```
**simdb__run_sql**
```
SELECT COUNT(*) FROM events WHERE event_type='WEAPON_FIRED' AND side='blue' AND weapon_type='GEM-T'
```
**simdb__run_sql**
```
SELECT weapon_type, COUNT(*) AS cnt FROM events WHERE event_type='WEAPON_FIRED' AND side='blue' AND weapon_type IN ('JASSM-ER','BGM-109E','AGM-179_JAGM','M982A1','AGM-88E','AGM-88G','AGM-114R','WPN_KESTREL','PRSM_INC1','NSM_BLK1A','MGM-140B','GEM-T') GROUP BY weapon_type
```
**simdb__run_sql**
```
SELECT COUNT(*) FROM events WHERE event_type='WEAPON_FIRED' AND side='blue' AND weapon_type IN ('GBU-12','GBU-31V3','GBU-39','GBU-53B','XM1113','TRIDENT_GLIDE_KIT')
```
**simdb__run_sql**
```
SELECT COUNT(*) FROM events WHERE event_type='WEAPON_FIRED' AND side='blue' AND weapon_type IN ('HYDRA70_M151','APKWS_II')
```
**simdb__run_sql**
```
SELECT COUNT(*) FROM events WHERE event_type='WEAPON_FIRED' AND side='blue' AND weapon_type IN ('M795','M30A2','M31A2')
```
**simdb__run_sql**
```
SELECT COUNT(*) FROM events WHERE event_type='WEAPON_FIRED' AND side='blue' AND weapon_type='SB600'
```
</details>

### ontology ON - score 100/100

24 tool calls, 25 turns, 168.9 s, 8,640 input / 7,677 output tokens

**Headline** – Blue coalition expended **272** precision‑guided munitions (excluding surface‑to‑air and air‑to‑air missiles) during the run.

| Category | Count |
|----------|-------|
| Missiles (including all precision‑guided surface‑to‑surface, cruise, anti‑ship, anti‑tank, anti‑radar, anti‑ship, etc.) | **120** |
| Guided bombs | **84** |
| Guided rockets | **50** |
| Guided artillery projectiles | **10** |
| Loitering munitions | **8** |

**How we derived the numbers**

1. **Ontology‑based classification** – Using the battlespace ontology we queried for all AFSIM `SimulationType` instances that are subclasses of `bs:PrecisionGuidedMunition` **and** not subclasses of `bs:SurfaceToAirMissile` or `bs:AirToAirMissile`.  
   * 41 distinct weapon‑type strings were returned (e.g., GBU‑39, KAB‑500S, JASSM‑ER, etc.).  
2. **Weapon‑type to category mapping** – The ontology further provides class membership for each type. We grouped the 41 types into the five requested categories (missiles, guided bombs, guided rockets, guided artillery projectiles, loitering munitions).  
3. **Event counting** – We ran a single SQLite query against the `events` table, filtering on:  
   * `event_type = 'WEAPON_FIRED'`  
   * `side = 'blue'` (the side name in the dataset is all lower‑case)  
   * `weapon_type` in the 41 precision‑guided types list.  
   The query returned `272`.  
4. **Category totals** – We then ran separate counts for each category‑list (as shown above) to obtain the breakdown. The sum of the category totals (272) matches the overall count, confirming no double‑counting.

**Assumptions & Uncertainties**

* The side designation in the AFSIM output is `'blue'` (lower‑case).  
* All weapon‑type strings in the `events` table exactly match the `bs:simTypeName` values in the ontology.  
* The ontology is authoritative for classifying weapons; no manual classification was used.  
* Surface‑to‑air and air‑to‑air missiles were excluded by explicitly filtering out all `SimulationType` instances that are subclasses of `bs:SurfaceToAirMissile` or `bs:AirToAirMissile`.  
* Some weapon types (e.g., KAB‑20S, VORON‑K, 9M542) had no expended events, which is why they did not appear in the final counts.

<details><summary>Tool calls</summary>

**ontology__ontology_overview**
```
{"": ""}
```
**simdb__describe_database**
```
{}
```
**ontology__sparql_query**
```
PREFIX bs: <http://example.org/battlespace#>
SELECT DISTINCT ?name WHERE {
  ?t a bs:SimulationType ; bs:simTypeName ?name .
  ?t rdfs:subClassOf* bs:PrecisionGuidedMunition .
  FILTER NOT EXISTS { ?t rdfs:subClassOf* bs:SurfaceToAirMissile } .
  FILTER NOT EXISTS { ?t rdfs:subClassOf* bs:AirToAirMissile } .
}
```
**ontology__sparql_query**
```
PREFIX bs: <http://example.org/battlespace#>
SELECT DISTINCT ?name WHERE {
  ?t a bs:SimulationType ; bs:simTypeName ?name .
  ?t a bs:PrecisionGuidedMunition .
  FILTER NOT EXISTS { ?t a bs:SurfaceToAirMissile } .
  FILTER NOT EXISTS { ?t a bs:AirToAirMissile } .
}
```
**ontology__sparql_query**
```
PREFIX bs: <http://example.org/battlespace#>
SELECT DISTINCT ?name ?cat WHERE {
  ?t a bs:SimulationType ; bs:simTypeName ?name .
  ?t a bs:PrecisionGuidedMunition .
  FILTER NOT EXISTS { ?t a bs:SurfaceToAirMissile } .
  FILTER NOT EXISTS { ?t a bs:AirToAirMissile } .
  BIND(IF(?t a bs:GuidedBomb, "guided_bomb", "") AS ?gBomb)
  BIND(IF(?t a bs:GuidedRocket, "guided_rocket", "") AS ?gRocket)
  BIND(IF(?t a bs:GuidedProjectile, "guided_artillery", "") AS ?gArt)
  BIND(IF(?t a bs:LoiteringMunition, "loitering", "") AS ?loiter)
  BIND(IF(?t a bs:Missile, "missile", "") AS ?miss)
  BIND(CONCAT(?gBomb,?gRocket,?gArt,?loiter,?miss) AS ?cat)
}
```
**ontology__sparql_query**
```
PREFIX bs: <http://example.org/battlespace#>
SELECT DISTINCT ?name WHERE {
  ?t a bs:SimulationType ; bs:simTypeName ?name .
  ?t a bs:GuidedBomb .
  FILTER NOT EXISTS { ?t a bs:SurfaceToAirMissile } .
  FILTER NOT EXISTS { ?t a bs:AirToAirMissile } .
}
```
**ontology__sparql_query**
```
PREFIX bs: <http://example.org/battlespace#>
SELECT DISTINCT ?name WHERE {
  ?t a bs:SimulationType ; bs:simTypeName ?name .
  ?t a bs:GuidedRocket .
  FILTER NOT EXISTS { ?t a bs:SurfaceToAirMissile } .
  FILTER NOT EXISTS { ?t a bs:AirToAirMissile } .
}
```
**ontology__sparql_query**
```
PREFIX bs: <http://example.org/battlespace#>
SELECT DISTINCT ?name WHERE {
  ?t a bs:SimulationType ; bs:simTypeName ?name .
  ?t a bs:GuidedProjectile .
  FILTER NOT EXISTS { ?t a bs:SurfaceToAirMissile } .
  FILTER NOT EXISTS { ?t a bs:AirToAirMissile } .
}
```
**ontology__sparql_query**
```
PREFIX bs: <http://example.org/battlespace#>
SELECT DISTINCT ?name WHERE {
  ?t a bs:SimulationType ; bs:simTypeName ?name .
  ?t a bs:LoiteringMunition .
  FILTER NOT EXISTS { ?t a bs:SurfaceToAirMissile } .
  FILTER NOT EXISTS { ?t a bs:AirToAirMissile } .
}
```
**ontology__sparql_query**
```
PREFIX bs: <http://example.org/battlespace#>
SELECT DISTINCT ?name WHERE {
  ?t a bs:SimulationType ; bs:simTypeName ?name .
  ?t a bs:Missile .
  FILTER NOT EXISTS { ?t a bs:SurfaceToAirMissile } .
  FILTER NOT EXISTS { ?t a bs:AirToAirMissile } .
}
```
**ontology__sparql_query**
```
PREFIX bs: <http://example.org/battlespace#>
SELECT DISTINCT ?name WHERE {
  ?t a bs:SimulationType ; bs:simTypeName ?name .
  { ?t a bs:SurfaceToAirMissile } UNION { ?t a bs:AirToAirMissile } .
}
```
**simdb__run_sql**
```
SELECT COUNT(*) as count FROM events WHERE event_type='WEAPON_FIRED' AND side='blue' AND weapon_type IN ('GBU-39','KAB-20S','GBU-53B','KAB-500S','GBU-12','TRIDENT_GLIDE_KIT','GBU-31V3')
```
**simdb__run_sql**
```
SELECT COUNT(*) as count FROM events WHERE event_type='WEAPON_FIRED' AND side='blue' AND weapon_type IN ('M30A2','9M542','M31A2','APKWS_II')
```
**simdb__run_sql**
```
SELECT COUNT(*) as count FROM events WHERE event_type='WEAPON_FIRED' AND side='blue' AND weapon_type IN ('M982A1','3OF39')
```
**simdb__run_sql**
```
SELECT COUNT(*) as count FROM events WHERE event_type='WEAPON_FIRED' AND side='blue' AND weapon_type IN ('VORON-K','LANCET-3','SB600','ZALA_LANCET3','GERAN-2')
```
**simdb__run_sql**
```
SELECT COUNT(*) as count FROM events WHERE event_type='WEAPON_FIRED' AND side='blue' AND weapon_type IN ('AGM-179_JAGM','BGM-71F','9M133M-2','3M54','3M55','AGM-88G','9M117M1','P-800','PRSM_INC1','NSM_BLK1A','KH-31PD','9M728','KH-59MK2','AGM-114R','9M127-1','MGM-140B','3M14','AGM-88E','RGM-184A','9M119M','JASSM-ER','BGM-109E','9M723')
```
**simdb__run_sql**
```
SELECT COUNT(*) as total FROM events WHERE event_type='WEAPON_FIRED' AND side='blue' AND weapon_type NOT IN ('40N6E','48N6E3','57E6E','9M317M','9M338K','9M96E2','AIM-120C7','AIM-120D','AIM-132','AIM-9X_BLK2','AMRAAM-ER','FIM-92K','GEM-T','IZDELIYE_610M','MBDA_METEOR','PAC-3_MSE','R-37M','R-73M','R-77-1','RIM-162D','SM-2_BLK3C','SM-6_BLK1A','WPN_AMRAAM_D','WPN_KESTREL')
```
**simdb__run_sql**
```
SELECT weapon_type, COUNT(*) as cnt FROM events WHERE event_type='WEAPON_FIRED' AND side='blue' AND weapon_type IN ('GBU-39','KAB-20S','GBU-53B','KAB-500S','GBU-12','TRIDENT_GLIDE_KIT','GBU-31V3') GROUP BY weapon_type
```
**simdb__run_sql**
```
SELECT weapon_type, COUNT(*) as cnt FROM events WHERE event_type='WEAPON_FIRED' AND side='blue' AND weapon_type IN ('M30A2','9M542','M31A2','APKWS_II') GROUP BY weapon_type
```
**simdb__run_sql**
```
SELECT weapon_type, COUNT(*) as cnt FROM events WHERE event_type='WEAPON_FIRED' AND side='blue' AND weapon_type IN ('M982A1','3OF39') GROUP BY weapon_type
```
**simdb__run_sql**
```
SELECT weapon_type, COUNT(*) as cnt FROM events WHERE event_type='WEAPON_FIRED' AND side='blue' AND weapon_type IN ('VORON-K','LANCET-3','SB600','ZALA_LANCET3','GERAN-2') GROUP BY weapon_type
```
**simdb__run_sql**
```
SELECT weapon_type, COUNT(*) as cnt FROM events WHERE event_type='WEAPON_FIRED' AND side='blue' AND weapon_type IN ('AGM-179_JAGM','BGM-71F','9M133M-2','3M54','3M55','AGM-88G','9M117M1','P-800','PRSM_INC1','NSM_BLK1A','KH-31PD','9M728','KH-59MK2','AGM-114R','9M127-1','MGM-140B','3M14','AGM-88E','RGM-184A','9M119M','JASSM-ER','BGM-109E','9M723') GROUP BY weapon_type
```
**simdb__run_sql**
```
SELECT weapon_type, COUNT(*) as cnt FROM events WHERE event_type='WEAPON_FIRED' AND side='blue' AND weapon_type IN ('9M133M-2','3M54','3M55','9M117M1','9M728','KH-31PD','KH-59MK2','9M127-1','3M14','9M119M','9M723') GROUP BY weapon_type
```
**simdb__run_sql**
```
SELECT COUNT(*) as total_pg FROM events WHERE event_type='WEAPON_FIRED' AND side='blue' AND weapon_type IN ('GBU-39','KAB-20S','GBU-53B','KAB-500S','GBU-12','TRIDENT_GLIDE_KIT','GBU-31V3','M30A2','9M542','M31A2','APKWS_II','M982A1','3OF39','VORON-K','LANCET-3','SB600','ZALA_LANCET3','GERAN-2','AGM-179_JAGM','BGM-71F','9M133M-2','3M54','3M55','AGM-88G','9M117M1','P-800','PRSM_INC1','NSM_BLK1A','KH-31PD','9M728','KH-59MK2','AGM-114R','9M127-1','MGM-140B','3M14','AGM-88E','RGM-184A','9M119M','JASSM-ER','BGM-109E','9M723')
```
</details>

## q3: Cluster munition employment

**Question.** Which cluster (submunition-dispensing) munitions were employed during the engagement? For each, give the weapon type, the side that used it, and the number of rounds fired.

**Why the ontology matters.** Requires warhead knowledge: MGM-140B is ATACMS Block IA (APAM submunitions), BURYA-12 is notional, while M30A2 (GMLRS Alternative Warhead) looks like the old DPICM rocket but has no submunitions.

**Ground truth.** Cluster munitions fired: total 53 rounds - MGM-140B (MGM-140B ATACMS Block IA) by blue: 3; 3O23 (3-O-23 152 mm cargo projectile (ICM)) by red: 14; 9M55K (9M55K 300 mm cargo rocket) by red: 24; BURYA-12 (Burya-12 cargo rocket (notional)) by red: 12. Not cluster: M30A2 GMLRS-AW (pre-formed fragments, replaced the DPICM M30), M31A2 (unitary).

### ontology OFF - score 0/100

13 tool calls, 14 turns, 83.6 s, 3,449 input / 3,766 output tokens

**Cluster (submunition‑dispensing) munitions fired**

| Weapon type | Side that used it | Rounds fired |
|-------------|-------------------|--------------|
| **GBU‑53B** (U.S. 2000‑lb cluster bomb) | blue | 24 |
| **9M127‑1** (Russian 9M127‑1 cluster bomb) | red | 14 |
| **9M133M‑2** (Russian 9M133M‑2 cluster bomb) | red | 4 |

*Total cluster‑munition firings:* 42.

**Notes & assumptions**

* The counts are taken from the `events` table (`WEAPON_FIRED` rows).  
* Cluster munitions are identified by their weapon‑type names; in this run the only ones that dispensed submunitions were the GBU‑53B, 9M127‑1 and 9M133M‑2.  
* Submunitions themselves (e.g., 9M317M) are recorded as separate `WEAPON_FIRED` events, but they are not considered “cluster munitions” in this context.

**Judge - missed or wrong:**
- GBU-53B, 9M127-1 and 9M133M-2 are not cluster munitions
- All four true cluster munitions missed
- Total 42, should be 53

<details><summary>Tool calls</summary>

**simdb__describe_database**
```
{}
```
**simdb__run_sql**
```
SELECT DISTINCT weapon_type FROM events WHERE event_type='WEAPON_FIRED' AND weapon_type LIKE '%CLUSTER%'
```
**simdb__run_sql**
```
SELECT DISTINCT weapon_type FROM events WHERE event_type='WEAPON_FIRED' AND weapon_type LIKE '%SUBMUNITION%'
```
**simdb__run_sql**
```
SELECT COUNT(*) FROM events WHERE event_type='WEAPON_FIRED' AND weapon_type='GBU-53B'
```
**simdb__run_sql**
```
SELECT side, COUNT(*) FROM events WHERE event_type='WEAPON_FIRED' AND weapon_type='GBU-53B' GROUP BY side
```
**simdb__run_sql**
```
SELECT COUNT(*) FROM events WHERE event_type='WEAPON_FIRED' AND weapon_type='9M133M-2'
```
**simdb__run_sql**
```
SELECT side, COUNT(*) FROM events WHERE event_type='WEAPON_FIRED' AND weapon_type='9M133M-2' GROUP BY side
```
**simdb__run_sql**
```
SELECT COUNT(*) FROM events WHERE event_type='WEAPON_FIRED' AND weapon_type='9M127-1'
```
**simdb__run_sql**
```
SELECT side, COUNT(*) FROM events WHERE event_type='WEAPON_FIRED' AND weapon_type='9M127-1' GROUP BY side
```
**simdb__run_sql**
```
SELECT COUNT(*) FROM events WHERE event_type='WEAPON_FIRED' AND weapon_type='9M317M'
```
**simdb__run_sql**
```
SELECT side, COUNT(*) FROM events WHERE event_type='WEAPON_FIRED' AND weapon_type='9M317M' GROUP BY side
```
**simdb__run_sql**
```
SELECT DISTINCT weapon_type FROM events WHERE event_type='WEAPON_FIRED' AND weapon_type LIKE '%KAB%'
```
**simdb__run_sql**
```
SELECT SUM(CASE WHEN weapon_type IN ('GBU-53B','9M127-1','9M133M-2') THEN 1 ELSE 0 END) FROM events WHERE event_type='WEAPON_FIRED'
```
</details>

### ontology ON - score 100/100

12 tool calls, 13 turns, 67.3 s, 7,016 input / 2,862 output tokens

**Cluster munition usage**

| Weapon type | Side that fired it | Rounds fired |
|-------------|--------------------|--------------|
| 9M55K       | **red** (Red Force) | **24** |
| 3O23        | **red** | **14** |
| BURYA‑12    | **red** | **12** |
| MGM‑140B    | **blue** (Blue Coalition) | **3** |

**Summary**

- A total of **4 different cluster‑type munitions** were actually expended during the engagement.  
- The **Red Force** fired **50** cluster‑munitions in all (24 × 9M55K + 14 × 3O23 + 12 × BURYA‑12).  
- The **Blue Coalition** fired **3** rounds of the MGM‑140B cluster munition.

**Notes & assumptions**

1. **Cluster munitions** were identified by querying the ontology for individuals that are instances of `bs:ClusterMunition` or `bs:ClusterBomb`. The AFSIM type strings that match these ontology classes are the four listed above.  
2. **Rounds fired** were counted from `events` rows where `event_type = 'WEAPON_FIRED'`. Each row represents one munition expended.  
3. The `side` column in the events table directly reflects the coalition that deployed the weapon.  
4. The weapon type `RBK-500_SPBE` appears as a cluster munition in the ontology but **no WEAPON_FIRED events** were recorded for it, so it was omitted from the breakdown.  
5. No other cluster munitions appear in the simulation data; all counts sum to the total cluster‑munition expended.

<details><summary>Tool calls</summary>

**ontology__ontology_overview**
```
{}
```
**ontology__sparql_query**
```
PREFIX bs: <http://example.org/battlespace#> 
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> 
SELECT DISTINCT ?name WHERE { 
  ?t a bs:ClusterMunition ; bs:simTypeName ?name .
} UNION {
  ?t a bs:ClusterBomb ; bs:simTypeName ?name .
}
```
**ontology__sparql_query**
```
PREFIX bs: <http://example.org/battlespace#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
SELECT DISTINCT ?name WHERE {
  { ?t a bs:ClusterMunition ; bs:simTypeName ?name }
  UNION
  { ?t a bs:ClusterBomb ; bs:simTypeName ?name }
}
```
**simdb__run_sql**
```
SELECT weapon_type, side, COUNT(*) AS fired FROM events WHERE event_type='WEAPON_FIRED' AND weapon_type IN ('9M55K','MGM-140B','3O23','BURYA-12','RBK-500_SPBE') GROUP BY weapon_type, side
```
**simdb__run_sql**
```
SELECT * FROM events WHERE event_type='WEAPON_FIRED' AND weapon_type='RBK-500_SPBE' LIMIT 5
```
**simdb__run_sql**
```
SELECT * FROM events WHERE event_type='WEAPON_FIRED' AND weapon_type='MGM-140B' LIMIT 5
```
**simdb__run_sql**
```
SELECT * FROM events WHERE event_type='WEAPON_FIRED' AND weapon_type='3O23' LIMIT 10
```
**simdb__run_sql**
```
SELECT * FROM events WHERE event_type='WEAPON_FIRED' AND weapon_type='9M55K' LIMIT 10
```
**simdb__run_sql**
```
SELECT COUNT(*) FROM events WHERE event_type='WEAPON_FIRED' AND weapon_type='9M55K'
```
**simdb__run_sql**
```
SELECT COUNT(*) FROM events WHERE event_type='WEAPON_FIRED' AND weapon_type='BURYA-12'
```
**ontology__sparql_query**
```
PREFIX bs: <http://example.org/battlespace#>
SELECT ?type ?name WHERE {
  ?type a bs:SimulationType ; bs:simTypeName ?name .
  FILTER(?name = 'MGM-140B')
  ?type a ?cls .
  FILTER(?cls IN (bs:ClusterMunition, bs:ClusterBomb))
}
```
**ontology__sparql_query**
```
PREFIX bs: <http://example.org/battlespace#>
SELECT ?type ?cls WHERE {
  ?type a bs:SimulationType ; bs:simTypeName 'MGM-140B' .
  ?type a ?cls .
}
```
</details>

## q4: Losses rolled up by force structure

**Question.** For each Blue brigade-level unit (brigade, regiment, or wing), how many of its platforms were destroyed during the engagement?

**Why the ontology matters.** The database only has callsigns. Which callsign belongs to which squadron/battalion/brigade exists only in the ontology's chain of command (bs:subordinateTo).

**Ground truth.** Blue brigade/regiment/wing-level losses: 1st Armored Brigade Combat Team, 3ID: 8 of 30 (BLADE14, COBRA11, COBRA12, COBRA13, COBRA14, IRON13, THUNDER22, THUNDER24); 11th Masurian Artillery Regiment (POL): 2 of 4 (KRAB31, KRAB34); 140 Expeditionary Air Wing (RAF): 2 of 4 (RAPIER1, RAPIER3); 388th Fighter Wing: 2 of 8 (LIGHTNING12, LIGHTNING14); 52nd Fighter Wing: 2 of 8 (WEASEL22, WEASEL23); 22nd Air Refueling Wing: 1 of 1 (SHELL71); 10th Army Air and Missile Defense Command: 0 of 6; 41st Field Artillery Brigade: 0 of 4; 432nd Wing: 0 of 2; 4th Fighter Wing: 0 of 4; 552nd Air Control Wing: 0 of 1; 7th Bomb Wing: 0 of 2; Combat Aviation Brigade, 3ID: 0 of 4; Destroyer Squadron 60: 0 of 3; Main Operating Base NORTHSTAR: 0 of 1; Royal Norwegian Navy contribution: 0 of 1. Total Blue platforms destroyed: 18.

### ontology OFF - score 25/100

12 tool calls, 13 turns, 162.7 s, 7,238 input / 7,849 output tokens

**Blue brigade‑level units (brigade, regiment or wing) – platforms destroyed**

| Blue unit (prefix) | Platforms destroyed |
|-------------------|---------------------|
| BANDIT | 0 |
| BLADE | 1 |
| BONE | 0 |
| COBRA | 4 |
| DARKSTAR | 0 |
| DRAGON | 0 |
| HAMMER | 0 |
| IRON | 1 |
| KRAB | 2 |
| LASSO | 0 |
| LIGHTNING | 2 |
| RAPIER | 2 |
| RAZOR | 0 |
| REAPER | 0 |
| SHELL | 1 |
| THUNDER | 2 |
| TROLL | 1 |
| WARLORD | 0 |
| WEASEL | 2 |
| WOLFPACK | 0 |

**Key points & assumptions**

1. **Unit identification** – The “prefix” before the first numeric digit in each platform callsign (e.g., *LIGHTNING* from *LIGHTNING11*) was used as the brigade‑level unit identifier.  
2. **Brigade‑level filter** – Prefixes that represented naval vessels (e.g., *CONSTELLATION*, *NANSEN*), airbases, or port facilities were excluded, leaving 20 units that correspond to land brigades, artillery regiments, or air wings.  
3. **Destroyed platforms** – Counts are taken from the `PLATFORM_BROKEN` events in the `events` table for side *blue*. Each event corresponds to a single platform that was destroyed.  
4. **Data check** – The sum of destroyed platforms (18) matches the total number of `PLATFORM_BROKEN` events for Blue, confirming consistency.  

These numbers reflect the loss of Blue platforms attributable to each brigade‑level unit during the engagement.

**Judge - missed or wrong:**
- Grouped by callsign prefix, not by unit
- 1st ABCT's 8 losses split across COBRA/BLADE/IRON/THUNDER
- TROLL treated as a brigade-level unit

<details><summary>Tool calls</summary>

**simdb__describe_database**
```
{"input": ""}
```
**simdb__run_sql**
```
SELECT name, type, side FROM platforms LIMIT 50;
```
**simdb__run_sql**
```
SELECT name, type, side FROM platforms WHERE side='blue' ORDER BY name LIMIT 200;
```
**simdb__run_sql**
```
SELECT DISTINCT substr(name,1,instr(name||'0','0')-1) AS unit_prefix FROM platforms WHERE side='blue';
```
**simdb__run_sql**
```
SELECT DISTINCT name, substr(name,1,case when instr(name,'0')>0 then instr(name,'0')-1 when instr(name,'1')>0 then instr(name,'1')-1 when instr(name,'2')>0 then instr(name,'2')-1 when instr(name,'3')>0 then instr(name,'3')-1 when instr(name,'4')>0 then instr(name,'4')-1 when instr(name,'5')>0 then instr(name,'5')-1 when instr(name,'6')>0 then instr(name,'6')-1 when instr(name,'7')>0 then instr(name,'7')-1 when instr(name,'8')>0 then instr(name,'8')-1 when instr(name,'9')>0 then instr(name,'9')-1 else length(name) end) as prefix FROM platforms WHERE side='blue';
```
**simdb__run_sql**
```
SELECT name, substr(name,1, (SELECT MIN(pos) FROM (SELECT instr(name,'0') pos UNION ALL SELECT instr(name,'1') pos UNION ALL SELECT instr(name,'2') pos UNION ALL SELECT instr(name,'3') pos UNION ALL SELECT instr(name,'4') pos UNION ALL SELECT instr(name,'5') pos UNION ALL SELECT instr(name,'6') pos UNION ALL SELECT instr(name,'7') pos UNION ALL SELECT instr(name,'8') pos UNION ALL SELECT instr(name,'9') pos)) -1) AS prefix FROM platforms WHERE side='blue' ORDER BY name;
```
**simdb__run_sql**
```
SELECT name, substr(name,1, (SELECT MIN(pos) FROM (SELECT CASE WHEN instr(name,'0')=0 THEN 1000 ELSE instr(name,'0') END pos UNION ALL SELECT CASE WHEN instr(name,'1')=0 THEN 1000 ELSE instr(name,'1') END pos UNION ALL SELECT CASE WHEN instr(name,'2')=0 THEN 1000 ELSE instr(name,'2') END pos UNION ALL SELECT CASE WHEN instr(name,'3')=0 THEN 1000 ELSE instr(name,'3') END pos UNION ALL SELECT CASE WHEN instr(name,'4')=0 THEN 1000 ELSE instr(name,'4') END pos UNION ALL SELECT CASE WHEN instr(name,'5')=0 THEN 1000 ELSE instr(name,'5') END pos UNION ALL SELECT CASE WHEN instr(name,'6')=0 THEN 1000 ELSE instr(name,'6') END pos UNION ALL SELECT CASE WHEN instr(name,'7')=0 THEN 1000 ELSE instr(name,'7') END pos UNION ALL SELECT CASE WHEN instr(name,'8')=0 THEN 1000 ELSE instr(name,'8') END pos UNION ALL SELECT CASE WHEN instr(name,'9')=0 THEN 1000 ELSE instr(name,'9') END pos)) -1) AS prefix FROM platforms WHERE side='blue' ORDER BY name;
```
**simdb__run_sql**
```
SELECT platform FROM events WHERE event_type='PLATFORM_BROKEN' AND side='blue';
```
**simdb__run_sql**
```
WITH prefix_map AS (
  SELECT name, substr(name,1, (SELECT MIN(pos) FROM (SELECT CASE WHEN instr(name,'0')=0 THEN 1000 ELSE instr(name,'0') END pos UNION ALL SELECT CASE WHEN instr(name,'1')=0 THEN 1000 ELSE instr(name,'1') END pos UNION ALL SELECT CASE WHEN instr(name,'2')=0 THEN 1000 ELSE instr(name,'2') END pos UNION ALL SELECT CASE WHEN instr(name,'3')=0 THEN 1000 ELSE instr(name,'3') END pos UNION ALL SELECT CASE WHEN instr(name,'4')=0 THEN 1000 ELSE instr(name,'4') END pos UNION ALL SELECT CASE WHEN instr(name,'5')=0 THEN 1000 ELSE instr(name,'5') END pos UNION ALL SELECT CASE WHEN instr(name,'6')=0 THEN 1000 ELSE instr(name,'6') END pos UNION ALL SELECT CASE WHEN instr(name,'7')=0 THEN 1000 ELSE instr(name,'7') END pos UNION ALL SELECT CASE WHEN instr(name,'8')=0 THEN 1000 ELSE instr(name,'8') END pos UNION ALL SELECT CASE WHEN instr(name,'9')=0 THEN 1000 ELSE instr(name,'9') END pos)) -1) AS prefix
  FROM platforms WHERE side='blue'
)
SELECT e.platform, pm.prefix
FROM events e
JOIN prefix_map pm ON e.platform = pm.name
WHERE e.event_type='PLATFORM_BROKEN' AND e.side='blue';
```
**simdb__run_sql**
```
WITH prefix_map AS (
  SELECT name, substr(name,1, (SELECT MIN(pos) FROM (SELECT CASE WHEN instr(name,'0')=0 THEN 1000 ELSE instr(name,'0') END pos UNION ALL SELECT CASE WHEN instr(name,'1')=0 THEN 1000 ELSE instr(name,'1') END pos UNION ALL SELECT CASE WHEN instr(name,'2')=0 THEN 1000 ELSE instr(name,'2') END pos UNION ALL SELECT CASE WHEN instr(name,'3')=0 THEN 1000 ELSE instr(name,'3') END pos UNION ALL SELECT CASE WHEN instr(name,'4')=0 THEN 1000 ELSE instr(name,'4') END pos UNION ALL SELECT CASE WHEN instr(name,'5')=0 THEN 1000 ELSE instr(name,'5') END pos UNION ALL SELECT CASE WHEN instr(name,'6')=0 THEN 1000 ELSE instr(name,'6') END pos UNION ALL SELECT CASE WHEN instr(name,'7')=0 THEN 1000 ELSE instr(name,'7') END pos UNION ALL SELECT CASE WHEN instr(name,'8')=0 THEN 1000 ELSE instr(name,'8') END pos UNION ALL SELECT CASE WHEN instr(name,'9')=0 THEN 1000 ELSE instr(name,'9') END pos)) -1) AS prefix
  FROM platforms WHERE side='blue'
)
SELECT pm.prefix, COUNT(*) as destroyed
FROM events e
JOIN prefix_map pm ON e.platform = pm.name
WHERE e.event_type='PLATFORM_BROKEN' AND e.side='blue'
GROUP BY pm.prefix
ORDER BY destroyed DESC, pm.prefix;
```
**simdb__run_sql**
```
SELECT pm.prefix, p.type, COUNT(*) as count
FROM platforms p
JOIN (SELECT name, substr(name,1, (SELECT MIN(pos) FROM (SELECT CASE WHEN instr(name,'0')=0 THEN 1000 ELSE instr(name,'0') END pos UNION ALL SELECT CASE WHEN instr(name,'1')=0 THEN 1000 ELSE instr(name,'1') END pos UNION ALL SELECT CASE WHEN instr(name,'2')=0 THEN 1000 ELSE instr(name,'2') END pos UNION ALL SELECT CASE WHEN instr(name,'3')=0 THEN 1000 ELSE instr(name,'3') END pos UNION ALL SELECT CASE WHEN instr(name,'4')=0 THEN 1000 ELSE instr(name,'4') END pos UNION ALL SELECT CASE WHEN instr(name,'5')=0 THEN 1000 ELSE instr(name,'5') END pos UNION ALL SELECT CASE WHEN instr(name,'6')=0 THEN 1000 ELSE instr(name,'6') END pos UNION ALL SELECT CASE WHEN instr(name,'7')=0 THEN 1000 ELSE instr(name,'7') END pos UNION ALL SELECT CASE WHEN instr(name,'8')=0 THEN 1000 ELSE instr(name,'8') END pos UNION ALL SELECT CASE WHEN instr(name,'9')=0 THEN 1000 ELSE instr(name,'9') END pos)) -1) AS prefix
  FROM platforms) pm ON p.name = pm.name
WHERE p.side='blue'
GROUP BY pm.prefix, p.type
ORDER BY pm.prefix, p.type;
```
**simdb__run_sql**
```
WITH prefix_map AS (
  SELECT name, substr(name,1, (SELECT MIN(pos) FROM (SELECT CASE WHEN instr(name,'0')=0 THEN 1000 ELSE instr(name,'0') END pos UNION ALL SELECT CASE WHEN instr(name,'1')=0 THEN 1000 ELSE instr(name,'1') END pos UNION ALL SELECT CASE WHEN instr(name,'2')=0 THEN 1000 ELSE instr(name,'2') END pos UNION ALL SELECT CASE WHEN instr(name,'3')=0 THEN 1000 ELSE instr(name,'3') END pos UNION ALL SELECT CASE WHEN instr(name,'4')=0 THEN 1000 ELSE instr(name,'4') END pos UNION ALL SELECT CASE WHEN instr(name,'5')=0 THEN 1000 ELSE instr(name,'5') END pos UNION ALL SELECT CASE WHEN instr(name,'6')=0 THEN 1000 ELSE instr(name,'6') END pos UNION ALL SELECT CASE WHEN instr(name,'7')=0 THEN 1000 ELSE instr(name,'7') END pos UNION ALL SELECT CASE WHEN instr(name,'8')=0 THEN 1000 ELSE instr(name,'8') END pos UNION ALL SELECT CASE WHEN instr(name,'9')=0 THEN 1000 ELSE instr(name,'9') END pos)) -1) AS prefix
  FROM platforms WHERE side='blue'
), destroyed_counts AS (
  SELECT pm.prefix, COUNT(*) AS destroyed
  FROM events e
  JOIN prefix_map pm ON e.platform = pm.name
  WHERE e.event_type='PLATFORM_BROKEN' AND e.side='blue'
  GROUP BY pm.prefix
)
SELECT pm.prefix,
       COALESCE(dc.destroyed,0) AS destroyed
FROM prefix_map pm
LEFT JOIN destroyed_counts dc ON pm.prefix = dc.prefix
WHERE pm.prefix NOT IN ('CONSTELLATION','LSA_HARBOR','MOB_NORTHSTAR','NANSEN','PORTER','ROSS')
GROUP BY pm.prefix, destroyed
ORDER BY pm.prefix;
```
</details>

### ontology ON - score 100/100

14 tool calls, 15 turns, 160.2 s, 11,060 input / 7,186 output tokens

**Destroyed platforms per Blue brigade‑level unit**

| Blue brigade‑level unit (echelon = brigade, regiment or wing) | Platforms destroyed |
|----------------------------------------------------------------|----------------------|
| Main Operating Base NORTHSTAR                                 | 0 |
| 41st Field Artillery Brigade                                 | 0 |
| **1st Armored Brigade Combat Team, 3ID**                      | **8** |
| 7th Bomb Wing                                                | 0 |
| Destroyer Squadron 60                                         | 0 |
| Royal Norwegian Navy contribution                            | 0 |
| 432nd Wing                                                   | 0 |
| **52nd Fighter Wing**                                        | **2** |
| 10th Army Air and Missile Defense Command                    | 0 |
| Combat Aviation Brigade, 3ID                                 | 0 |
| **11th Masurian Artillery Regiment (POL)**                   | **2** |
| 4th Fighter Wing                                             | 0 |
| **22nd Air Refueling Wing**                                 | **1** |
| 552nd Air Control Wing                                       | 0 |
| **140 Expeditionary Air Wing (RAF)**                          | **2** |
| **388th Fighter Wing**                                       | **2** |

**How the numbers were obtained**

1. **Destroyed platforms** – queried the SQLite `events` table for rows where `event_type='PLATFORM_BROKEN'` and `side='blue'` (side values are lowercase).  
   ```
   SELECT DISTINCT platform
   FROM events
   WHERE event_type='PLATFORM_BROKEN' AND side='blue';
   ```
   Result: 18 distinct platform names.

2. **Platform‑to‑unit mapping** – used the ontology to find the unit that owns each destroyed platform:
   ```
   SELECT ?platformName ?unit ?unitLabel
   WHERE {
     ?platform a bs:Platform ;
               bs:simPlatformName ?platformName ;
               bs:assignedTo ?unit .
     ?unit rdfs:label ?unitLabel .
   }
   ```
   The mapping showed that 17 of the 18 destroyed platforms belong to units that are subordinate (directly or transitively) to a Blue brigade‑level unit, while the remaining platform (`TROLL12`) belongs to a company that is not under any brigade‑level command.

3. **Brigade‑level units** – selected all Blue units whose `bs:echelon` is `bs:Brigade`, `bs:Regiment` or `bs:Wing`:
   ```
   SELECT ?unit ?unitLabel
   WHERE {
     ?unit a bs:MilitaryUnit ;
           bs:coalition bs:BlueCoalition ;
           bs:echelon ?echelon ;
           rdfs:label ?unitLabel .
     FILTER(?echelon IN (bs:Brigade, bs:Regiment, bs:Wing))
   }
   ```
   16 units were returned.

4. **Counting destroyed platforms per brigade** – joined the above data in SPARQL, using the transitive property `bs:subordinateTo*` to include all units beneath a brigade, and counted distinct platform names that were in the destroyed‑platform list:
   ```
   SELECT ?brigadeLabel (COUNT(DISTINCT ?platformName) AS ?destroyedCount)
   WHERE {
     ?brigade a bs:MilitaryUnit ;
              bs:coalition bs:BlueCoalition ;
              bs:echelon ?echelon ;
              rdfs:label ?brigadeLabel .
     FILTER(?echelon IN (bs:Brigade, bs:Regiment, bs:Wing))
     ?unit (bs:subordinateTo*) ?brigade .
     ?platform a bs:Platform ;
               bs:simPlatformName ?platformName ;
               bs:assignedTo ?unit .
     VALUES ?platformName { ... }   # the 18 platform names
   }
   GROUP BY ?brigadeLabel
   ```

   The query returned non‑zero counts for six brigades; the other ten brigades had no destroyed platforms, which is why they appear with zero in the table above.

**Key points**

- 18 platforms were destroyed in total; 17 were within the command structure of a Blue brigade‑level unit, 1 (`TROLL12`) was not.
- The largest loss occurred in the **1st Armored Brigade Combat Team, 3ID** (8 platforms destroyed).
- Wings also suffered losses (e.g., 52nd Fighter Wing, 140 Expeditionary Air Wing, 388th Fighter Wing, 22nd Air Refueling Wing).  
- The remaining Blue brigades (regiments, wings, etc.) experienced no platform losses.

<details><summary>Tool calls</summary>

**ontology__ontology_overview**
```
{}
```
**ontology__ontology_overview**
```
{}
```
**ontology__sparql_query**
```
SELECT ?unitLabel ?echelonLabel WHERE { ?unit a bs:MilitaryUnit ; bs:coalition bs:BlueCoalition ; bs:echelon ?echelon . ?echelon rdfs:label ?echelonLabel . ?unit rdfs:label ?unitLabel . FILTER(?echelon IN (bs:Brigade, bs:Regiment, bs:Wing)) . }
```
**ontology__sparql_query**
```
SELECT ?unit ?echelon WHERE { ?unit a bs:MilitaryUnit ; bs:coalition bs:BlueCoalition ; bs:echelon ?echelon . FILTER(?echelon IN (bs:Brigade, bs:Regiment, bs:Wing)) . }
```
**simdb__run_sql**
```
SELECT DISTINCT platform FROM events WHERE event_type='PLATFORM_BROKEN' AND side='Blue';
```
**simdb__run_sql**
```
SELECT DISTINCT event_type FROM events LIMIT 100;
```
**simdb__run_sql**
```
SELECT DISTINCT side FROM events LIMIT 100;
```
**simdb__run_sql**
```
SELECT DISTINCT platform FROM events WHERE event_type='PLATFORM_BROKEN' AND side='blue';
```
**ontology__sparql_query**
```
SELECT ?platformName ?unit ?unitLabel WHERE { ?platform a bs:Platform ; bs:simPlatformName ?platformName ; bs:assignedTo ?unit . ?unit rdfs:label ?unitLabel . FILTER(?platformName IN ('SHELL71','RAPIER3','RAPIER1','WEASEL23','LIGHTNING14','WEASEL22','LIGHTNING12','KRAB31','THUNDER22','THUNDER24','COBRA14','TROLL12','COBRA12','KRAB34','COBRA11','IRON13','COBRA13','BLADE14')) }
```
**ontology__sparql_query**
```
PREFIX bs: <http://example.org/battlespace#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
SELECT ?brigadeLabel (COUNT(DISTINCT ?platformName) AS ?destroyedCount)
WHERE {
  ?brigade a bs:MilitaryUnit ;
           bs:coalition bs:BlueCoalition ;
           bs:echelon ?echelon ;
           rdfs:label ?brigadeLabel .
  FILTER(?echelon IN (bs:Brigade, bs:Regiment, bs:Wing))
  ?unit (bs:subordinateTo*) ?brigade .
  ?platform a bs:Platform ;
            bs:simPlatformName ?platformName ;
            bs:assignedTo ?unit .
  VALUES ?platformName {
    'SHELL71' 'RAPIER3' 'RAPIER1' 'WEASEL23' 'LIGHTNING14' 'WEASEL22' 'LIGHTNING12' 'KRAB31' 'THUNDER22' 'THUNDER24' 'COBRA14' 'TROLL12' 'COBRA12' 'KRAB34' 'COBRA11' 'IRON13' 'COBRA13' 'BLADE14'
  }
}
GROUP BY ?brigadeLabel
```
**ontology__sparql_query**
```
PREFIX bs: <http://example.org/battlespace#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
SELECT ?unit ?unitLabel
WHERE {
  ?unit a bs:MilitaryUnit ;
        bs:coalition bs:BlueCoalition ;
        bs:echelon ?echelon ;
        rdfs:label ?unitLabel .
  FILTER(?echelon IN (bs:Brigade, bs:Regiment, bs:Wing))
}

```
**ontology__sparql_query**
```
PREFIX bs: <http://example.org/battlespace#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
SELECT ?platformName ?unitLabel ?brigadeLabel WHERE {
  VALUES ?platformName { 'SHELL71' 'RAPIER3' 'RAPIER1' 'WEASEL23' 'LIGHTNING14' 'WEASEL22' 'LIGHTNING12' 'KRAB31' 'THUNDER22' 'THUNDER24' 'COBRA14' 'TROLL12' 'COBRA12' 'KRAB34' 'COBRA11' 'IRON13' 'COBRA13' 'BLADE14' }
  ?platform a bs:Platform ; bs:simPlatformName ?platformName ; bs:assignedTo ?unit .
  ?unit rdfs:label ?unitLabel .
  ?unit (bs:subordinateTo*) ?brigade .
  ?brigade rdfs:label ?brigadeLabel .
  FILTER(?brigadeLabel IN ('1st Armored Brigade Combat Team, 3ID','52nd Fighter Wing','11th Masurian Artillery Regiment (POL)','22nd Air Refueling Wing','140 Expeditionary Air Wing (RAF)','388th Fighter Wing'))
} ORDER BY ?platformName
```
**ontology__sparql_query**
```
PREFIX bs: <http://example.org/battlespace#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
SELECT ?unitLabel ?brigadeLabel WHERE {
  ?unit a bs:MilitaryUnit ; bs:simPlatformName ?plat .
  ?unit rdfs:label ?unitLabel .
  ?unit (bs:subordinateTo*) ?brigade .
  ?brigade rdfs:label ?brigadeLabel .
  FILTER(?unitLabel='1st NASAMS Fire Unit (NOR)')
}
```
**ontology__sparql_query**
```
PREFIX bs: <http://example.org/battlespace#>
SELECT ?unit ?coalition ?echelon WHERE { ?unit a bs:MilitaryUnit ; bs:coalition ?coalition ; bs:echelon ?echelon . FILTER(?unit = bs:unit_ADBN_NOR_1)}
```
</details>

## q5: Air defense mission capability at a point in time

**Question.** At T+90 minutes (time_s = 5400), which of Red's surface-to-air missile battalions were still able to engage? A battalion built from separate launchers, radars and command posts can engage only if it still has at least one operational engagement radar, one operational command post, and one operational launcher; a battalion of self-contained SHORAD vehicles can engage if any vehicle is operational.

**Why the ontology matters.** Needs system composition (which radar/CP/launchers form which battalion) and component roles (engagement vs surveillance radar), both from the ontology, joined to time-sliced status data.

**Ground truth.** Red SAM battalions at T+90 min: 1st Buk Battalion, 53 ZRBR: NOT capable (no operational EngagementRadar) [lost so far: BEREZA11, BEREZA13]; 1st S-400 Battalion, 1544 ZRP: NOT capable (no operational EngagementRadar) [lost so far: KREMEN12, KREMEN13]; 2nd S-400 Battalion, 1544 ZRP: MISSION-CAPABLE [lost so far: KREMEN25]; Air Defence Battalion, 7 MRR (Tor): MISSION-CAPABLE [lost so far: YASTREB52]

### ontology OFF - score 5/100

10 tool calls, 11 turns, 161.9 s, 3,839 input / 7,205 output tokens

**Headline**

At T + 90 min (time = 5400 s) **no Red surface‑to‑air missile battalion was still able to engage**.

---

### Breakdown by battalion

| Battalion (Red) | Launcher(s) (type) | Radar(s) (type) | Command post(s) (type) | Operational status at 5400 s | Engagement‑ready? |
|-----------------|--------------------|-----------------|------------------------|-----------------------------|-------------------|
| **BEREZA** | BEREZA13–15 – 9A317M_TELAR (launcher) | BEREZA10–12 – 9S18M1 / 9S36M / 9S510M (radar) | *none* | 1 active radar (BEREZA10), 1 active launcher (BEREZA14) | **No** – missing a command post |
| **KREMEN** | *none* | KREMEN13–26 – 5P85TE2_TEL (radar) plus KREMEN11–12 – 91N6E_BIG_BIRD / 92N6E_GRAVE_STONE (radar) | KREMEN10 / KREMEN20 – 55K6E_CP (command post) | 1 active command post (KREMEN20), no launchers | **No** – missing a launcher |
| **YASTREB** | YASTREB51–52 – 9K332_TOR‑M2 (launcher) | *none* | *none* | YASTREB51 damaged, YASTREB52 broken | **No** – missing radar and command post |
| **SHTORM** | SHTORM01–02 – 9P78‑1 (launcher) | *none* | *none* | SHTORM01 damaged, SHTORM02 active | **No** – missing radar and command post |
| **KAMEN** | KAMEN11–12 – 9P163_KORNET (launcher) | *none* | *none* | KAMEN11 active, KAMEN12 broken | **No** – missing radar and command post |
| **Other** | *none* | *none* | *none* | – | **No** – no self‑contained SHORAD vehicles present (type *M‑SHORAD_INC1* not in the database) |

**Key queries used**

1. **Launcher, radar, CP status at 5400 s**

   ```sql
   SELECT platform, type, state
   FROM platforms
   JOIN platform_status USING (platform)
   WHERE time_s = 5400
     AND side = 'red'
   ORDER BY platform;
   ```

2. **Individual battalion component checks**

   Example for BEREZA launchers:

   ```sql
   SELECT platform, state
   FROM platform_status
   WHERE time_s = 5400
     AND platform IN ('BEREZA13','BEREZA14','BEREZA15');
   ```

   Similar queries were run for all other battalion components.

---

### Assumptions / Uncertainties

* The analysis assumes that a battalion’s command post must belong to the same battalion; i.e., a battalion cannot use a command post that is not named as part of it.  
* No self‑contained SHORAD vehicles of type `M‑SHORAD_INC1` are present in the database, so that category is empty.  
* Operational status is taken as `ACTIVE`; `DAMAGED` or `BROKEN` is considered non‑operational.  

Under these definitions, no Red SAM battalion met all three required conditions (radar + command post + launcher) at 90 min.

**Judge - missed or wrong:**
- Said no battalion could engage; 2nd S-400 and Tor battalions could
- Grouped by callsign; included non-SAM units (Kornet, Shtorm)

<details><summary>Tool calls</summary>

**simdb__describe_database**
```
{}
```
**simdb__run_sql**
```
SELECT name, type, side FROM platforms WHERE side='red' ORDER BY name;
```
**simdb__run_sql**
```
SELECT name FROM platforms WHERE type='M-SHORAD_INC1' AND side='red';
```
**simdb__run_sql**
```
SELECT name FROM platforms WHERE name LIKE '%BEREZA%';
```
**simdb__run_sql**
```
SELECT platform, state FROM platform_status WHERE time_s=5400 AND platform IN ('KREMEN10','KREMEN20');
```
**simdb__run_sql**
```
SELECT platform, state FROM platform_status WHERE time_s=5400 AND platform IN ('BEREZA10','BEREZA11','BEREZA12');
```
**simdb__run_sql**
```
SELECT platform, state FROM platform_status WHERE time_s=5400 AND platform IN ('BEREZA13','BEREZA14','BEREZA15');
```
**simdb__run_sql**
```
SELECT platform, state FROM platform_status WHERE time_s=5400 AND platform IN ('YASTREB51','YASTREB52');
```
**simdb__run_sql**
```
SELECT platform, state FROM platform_status WHERE time_s=5400 AND platform IN ('SHTORM01','SHTORM02');
```
**simdb__run_sql**
```
SELECT platform, state FROM platform_status WHERE time_s=5400 AND platform IN ('KAMEN11','KAMEN12');
```
</details>

### ontology ON - score 0/100

33 tool calls, 34 turns, 178.4 s, 11,388 input / 6,891 output tokens

_no answer_ (None)

**Judge - missed or wrong:**
- Empty final answer after 33 tool calls
- Could not get from a platform to its AFSIM type string: platforms have no bs:simTypeName and no link to their bs:SimulationType individual

<details><summary>Tool calls</summary>

**ontology__find_terms**
```
surface-to-air missile battalion
```
**ontology__find_terms**
```
SAM battalion
```
**ontology__ontology_overview**
```
{}
```
**ontology__sparql_query**
```
SELECT ?b ?label WHERE { ?b a bs:MilitaryUnit ; bs:echelon bs:Battalion ; rdfs:label ?label . FILTER regex(?label, "SAM", "i") }
```
**ontology__sparql_query**
```
SELECT ?u ?c WHERE { ?u a bs:MilitaryUnit ; a ?c . FILTER(contains(str(?c), "SAM")) }
```
**ontology__sparql_query**
```
SELECT ?u ?label WHERE { ?u a bs:MilitaryUnit ; rdfs:label ?label . }
```
**ontology__sparql_query**
```
SELECT ?c WHERE { ?c a owl:Class ; rdfs:label ?label . FILTER regex(?label, "SAM", "i") }
```
**ontology__sparql_query**
```
SELECT ?u ?label WHERE { ?u a bs:MilitaryUnit ; rdfs:label ?label ; bs:memberOf bs:RedForce . FILTER (regex(?label, "S-400", "i") || regex(?label, "NASAMS", "i") || regex(?label, "Patriot", "i") || regex(?label, "S-400", "i") || regex(?label, "Buk", "i")) }
```
**ontology__sparql_query**
```
SELECT ?u ?m WHERE { bs:unit_ZRBR53 bs:memberOf ?m . }
```
**ontology__sparql_query**
```
SELECT ?u ?c WHERE { ?u a bs:MilitaryUnit ; bs:coalition ?c . }
```
**ontology__sparql_query**
```
SELECT ?u ?label WHERE { ?u a bs:MilitaryUnit ; bs:coalition bs:RedForce ; rdfs:label ?label . }
```
**simdb__run_sql**
```
SELECT p.name, p.type, s.state FROM platforms p JOIN platform_status s ON p.name = s.platform WHERE s.time_s = 5400 AND p.assignedTo = 'bs:unit_ZRBR53'
```
**ontology__sparql_query**
```
SELECT ?p ?name ?type WHERE { ?p a bs:Platform ; bs:assignedTo bs:unit_ZRBR53 ; bs:simPlatformName ?name ; bs:simTypeName ?type . }
```
**ontology__sparql_query**
```
SELECT ?p ?name ?type WHERE { ?p a bs:Platform ; bs:simPlatformName ?name ; bs:simTypeName ?type . FILTER regex(?name, "AEW") }
```
**ontology__sparql_query**
```
SELECT ?p WHERE { ?p a bs:Platform . }
```
**ontology__sparql_query**
```
SELECT ?p ?assignedTo WHERE { ?p a bs:Platform ; bs:assignedTo ?assignedTo . }
```
**ontology__sparql_query**
```
SELECT ?p ?type WHERE { ?p a bs:Platform ; bs:simTypeName ?type . }
```
**ontology__sparql_query**
```
SELECT ?p ?name WHERE { ?p a bs:SAMLauncher ; bs:simTypeName ?name . }
```
**ontology__sparql_query**
```
SELECT ?p ?name WHERE { ?p a bs:EngagementRadar ; bs:simTypeName ?name . }
```
**ontology__sparql_query**
```
SELECT ?p ?name WHERE { ?p a bs:AirDefenseCommandPost ; bs:simTypeName ?name . }
```
**ontology__sparql_query**
```
SELECT ?p ?name WHERE { ?p a bs:SHORADSystem ; bs:simTypeName ?name . }
```
**ontology__sparql_query**
```
SELECT ?p ?name ?type WHERE { ?p a bs:Platform ; bs:assignedTo bs:unit_ZRP1544_1 ; bs:simPlatformName ?name ; bs:simTypeName ?type . }
```
**ontology__sparql_query**
```
SELECT ?p ?name ?type WHERE { ?p a bs:Platform ; bs:assignedTo bs:unit_ZRP1544_2 ; bs:simPlatformName ?name ; bs:simTypeName ?type . }
```
**ontology__sparql_query**
```
SELECT ?p ?assignedUnit WHERE { ?p a bs:Platform ; bs:assignedTo ?assignedUnit ; bs:subordinateTo bs:unit_ZRP1544_1 . }
```
**ontology__sparql_query**
```
SELECT ?p ?name ?type WHERE { ?p a bs:Platform ; bs:assignedTo ?assignedUnit ; bs:subordinateTo bs:unit_ZRP1544_1 ; bs:simPlatformName ?name ; bs:simTypeName ?type . }
```
**ontology__sparql_query**
```
SELECT ?p ?name ?type WHERE { ?p a bs:Platform ; bs:assignedTo ?assignedUnit ; bs:subordinateTo bs:unit_ZRP1544_1 ; bs:simPlatformName ?name ; bs:simTypeName ?type . }
```
**ontology__sparql_query**
```
SELECT ?p ?name ?type WHERE { bs:plat_KREMEN13 a bs:Platform ; bs:simPlatformName ?name ; bs:simTypeName ?type . }
```
**ontology__sparql_query**
```
SELECT ?p ?o WHERE { bs:plat_KREMEN13 ?o ?v . }
```
**ontology__sparql_query**
```
SELECT ?p ?o ?v WHERE { bs:plat_KREMEN13 ?o ?v . FILTER(?o = bs:simPlatformName) }
```
**ontology__sparql_query**
```
SELECT ?p ?name ?type WHERE { ?p a bs:Platform ; bs:assignedTo ?assignedUnit ; bs:subordinateTo bs:unit_ZRP1544_1 ; bs:simPlatformName ?name ; bs:simTypeName ?type . }
```
**ontology__sparql_query**
```
SELECT ?p ?o ?v WHERE { bs:plat_KREMEN13 ?o ?v . FILTER(?o = bs:subordinateTo) }
```
**ontology__sparql_query**
```
SELECT ?p ?type WHERE { ?p a bs:Platform ; bs:subordinateTo bs:unit_ZRP1544_1 ; bs:simTypeName ?type . }
```
**ontology__sparql_query**
```
SELECT ?p WHERE { bs:plat_KREMEN13 a bs:Platform ; bs:subordinateTo bs:unit_ZRP1544_1 . }
```
</details>

## q6: Coalition partner losses

**Question.** How many platforms belonging to Blue coalition partners other than the United States were destroyed? Break it down by nation, and say what category of Red weapon destroyed each one.

**Why the ontology matters.** Side 'blue' in the sim lumps all coalition members together. Nationality comes from the unit hierarchy in the ontology, and the weapon category from the munition hierarchy.

**Ground truth.** Non-US Blue coalition platforms destroyed: 5 - by nation: Norway 1, Poland 2, United Kingdom 2. Details: TROLL12 (Norway) killed by 9M542 [guided artillery rocket] from METEL22 at t=6146s; KRAB31 (Poland) killed by 9M55K [artillery rocket (cluster)] from METEL21 at t=4427s; KRAB34 (Poland) killed by 9M55K [artillery rocket (cluster)] from METEL22 at t=6832s; RAPIER1 (United Kingdom) killed by R-73M [air-to-air missile] from SOKOL07 at t=1885s; RAPIER3 (United Kingdom) killed by 48N6E3 [surface-to-air missile] from KREMEN25 at t=1181s

### ontology OFF - score 20/100

7 tool calls, 8 turns, 112.2 s, 3,851 input / 4,986 output tokens

**Blue coalition partners (non‑U.S.) destroyed:** 4 platforms  

| Nation (Blue partner) | Platforms destroyed | Red weapon that killed each | Weapon category |
|-----------------------|---------------------|-----------------------------|-----------------|
| **France** | 2 | • **RAPIER3** – *48N6E3* <br>• **RAPIER1** – *R‑73M* | • 48N6E3 – surface‑to‑air missile (long‑range) <br>• R‑73M – air‑to‑air missile (short‑range) |
| **South Korea** | 2 | • **KRAB31** – *9M55K* <br>• **KRAB34** – *9M55K* | • 9M55K – surface‑to‑air missile (short‑range) |

**Headline:** 4 Blue coalition platforms that were not U.S. were destroyed – 2 French, 2 South‑Korean – with the Red weapons that destroyed them being one long‑range SAM, one short‑range AAM, and two short‑range SAMs.

---

### Assumptions & Uncertainties

* **Nation inference:** The database has no explicit nation field.  Nations were inferred from the platform *type* name:
  * `EF2000_FGR4` → France  
  * `AHS_KRAB` → South Korea  
  * All other Blue types (e.g., `F‑35A`, `M2A4`, `M109A7`, `NASAMS_LCHR`) are U.S.  
* **Weapon‑category mapping:** Derived from standard missile designations:
  * `48N6E3` – Russian S‑400/4D‑300 missile → surface‑to‑air (SAM), long‑range  
  * `R‑73M` – Russian R‑73 (AA‑11 Archer) → air‑to‑air (AAM), short‑range  
  * `9M55K` – Russian 9M55 (R‑60) → surface‑to‑air (SAM), short‑range  

No other Blue platforms belonging to non‑U.S. partners were destroyed in the simulation.

**Judge - missed or wrong:**
- Nations guessed wrong: France and South Korea instead of UK and Poland
- Norway (TROLL12) missed
- 9M55K is a cluster artillery rocket, not a SAM
- Total 4, should be 5

<details><summary>Tool calls</summary>

**simdb__describe_database**
```
{}
```
**simdb__run_sql**
```
SELECT name, type, side FROM platforms LIMIT 20;
```
**simdb__run_sql**
```
SELECT name, type, side FROM platforms WHERE side='blue' ORDER BY name LIMIT 50;
```
**simdb__run_sql**
```
SELECT DISTINCT type FROM platforms WHERE side='blue';
```
**simdb__run_sql**
```
SELECT name, type FROM platforms WHERE type='NANSEN_CLASS_FFG';
```
**simdb__run_sql**
```
SELECT e.platform, p.type, e.weapon_type, e.details FROM events e JOIN platforms p ON e.platform=p.name WHERE e.event_type='PLATFORM_BROKEN' AND e.side='blue';
```
**simdb__run_sql**
```
SELECT p.type, COUNT(*) as cnt FROM events e JOIN platforms p ON e.platform=p.name WHERE e.event_type='PLATFORM_BROKEN' AND e.side='blue' GROUP BY p.type ORDER BY cnt DESC;
```
</details>

### ontology ON - score 75/100

5 tool calls, 6 turns, 331.9 s, 10,554 input / 14,691 output tokens

**Total Blue‑coalition partner platforms destroyed (excluding U.S.)**  
**6**

| Nation (Blue coalition partner) | # destroyed |
|---------------------------------|-------------|
| United Kingdom                  | 2 |
| Poland                          | 2 |
| Norway                          | 1 |
| Redland (notional nation)      | 1 |

---

**Red weapons that destroyed each platform**

| Platform | Nation | Red weapon expended | Weapon category (from ontology) |
|----------|--------|---------------------|--------------------------------|
| RAPIER3  | UK     | 48N6E3              | Surface‑to‑air missile (SAM) |
| RAPIER1  | UK     | R‑73M               | Air‑to‑air missile (AAM) |
| KRAB31   | Poland | 9M55K               | Unguided rocket |
| KRAB34   | Poland | 9M55K               | Unguided rocket |
| TROLL12  | Norway | 9M542               | Guided rocket |
| LIS42    | Redland | 9M542              | Guided rocket |

**Weapon‑category totals**

| Weapon category | # of destroyed platforms |
|-----------------|--------------------------|
| Surface‑to‑air missile (SAM) | 1 |
| Air‑to‑air missile (AAM) | 1 |
| Unguided rocket | 2 |
| Guided rocket | 2 |

---

**Notes & assumptions**

* Platform–nation links were taken from the ontology (`bs:assignedTo → bs:nation`).  
* Weapon‑type categories were inferred from the ontology’s class hierarchy (`bs:SimType`).  
* The only non‑U.S. Blue‑coalition platforms in the destroyed set were RAPIER3, RAPIER1, KRAB31, KRAB34, TROLL12, and LIS42 (Redland).  
* LIS42 is a Redland‑nation platform but its side is listed as “blue”, so it is treated as a Blue‑coalition partner in the analysis.  
* If any platform’s nation is missing in the ontology, it would be counted as “unknown”, but all destroyed platforms above have defined nations.

**Judge - missed or wrong:**
- LIS42 (a Red platform) wrongly added as a Blue partner loss, so total 6 not 5
- 9M55K called an unguided rocket; it is a cluster artillery rocket

<details><summary>Tool calls</summary>

**simdb__run_sql**
```
SELECT platform, side, weapon_type, details FROM events WHERE event_type='PLATFORM_BROKEN';
```
**ontology__ontology_overview**
```
{}
```
**ontology__sparql_query**
```
PREFIX bs: <http://example.org/battlespace#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
SELECT ?platformName ?nationName WHERE {
  VALUES ?platformName {
    "SHELL71" "RAPIER3" "RAPIER1" "WEASEL23" "LIGHTNING14" "WEASEL22" "LIGHTNING12" "KRAB31" "THUNDER22" "LIS42" "COBRA14" "TROLL12" "COBRA12" "COBRA11" "IRON13" "COBRA13" "BLADE14" "KRAB34"
  }
  ?platform a bs:Platform ; bs:simPlatformName ?platformName ; bs:nation ?nation .
  ?nation rdfs:label ?nationName .
}
```
**ontology__sparql_query**
```
PREFIX bs: <http://example.org/battlespace#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
SELECT ?weaponTypeStr ?categoryLabel WHERE {
  VALUES ?weaponTypeStr { "R-73M" "R-77-1" "48N6E3" "9M55K" "9M542" "9M317M" }
  ?weapon bs:simTypeName ?weaponTypeStr .
  ?weapon a ?cat .
  ?cat rdfs:label ?categoryLabel .
  # Filter categories that are subclasses of bs:Missile
  FILTER EXISTS { ?cat rdfs:subClassOf* bs:Missile } .
  # Prefer most specific: filter that cat has no subclass that is also subclass of bs:Missile
  FILTER NOT EXISTS { ?cat rdfs:subClassOf ?sub . FILTER EXISTS { ?sub rdfs:subClassOf* bs:Missile } } .
}
```
**ontology__sparql_query**
```
PREFIX bs: <http://example.org/battlespace#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
SELECT ?weaponTypeStr ?catLabel WHERE {
  VALUES ?weaponTypeStr { "R-73M" "R-77-1" "48N6E3" "9M55K" "9M542" "9M317M" }
  ?weapon bs:simTypeName ?weaponTypeStr .
  ?weapon a ?cat .
  ?cat rdfs:label ?catLabel .
}
```
</details>
