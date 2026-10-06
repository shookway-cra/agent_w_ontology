# Ontology vs. no-ontology agent comparison

Model: `gpt-oss:20b` - 2026-10-05 21:58

## Run statistics

| Question | Mode | Agent time | Model time | Tool time | Turns | Tool calls | Slowest tool call | Output tokens | Score |
|---|---|---|---|---|---|---|---|---|---|
| q0 | ontology OFF | 0m10s | 0m10s | 0m00s | 5 | 4 | 0.1s | 421 | 100 |
| q0 | ontology ON | 0m18s | 0m16s | 0m00s | 6 | 5 | 0.0s | 788 | 100 |
| q1 | ontology OFF | 0m56s | 0m55s | 0m00s | 7 | 6 | 0.0s | 2,914 | 20 |
| q1 | ontology ON | 0m51s | 0m46s | 0m04s | 8 | 7 | 3.2s | 2,283 | 100 |
| q2 | ontology OFF | 4m06s | 4m06s | 0m00s | 20 | 19 | 0.0s | 12,835 | 10 |
| q2 | ontology ON | 1m38s | 1m32s | 0m05s | 24 | 22 | 3.2s | 4,428 | 0 |
| q3 | ontology OFF | 0m38s | 0m37s | 0m00s | 8 | 7 | 0.0s | 1,912 | 0 |
| q3 | ontology ON | 1m00s | 0m56s | 0m02s | 10 | 9 | 1.4s | 2,684 | 100 |
| q4 | ontology OFF | 2m26s | 2m26s | 0m00s | 16 | 15 | 0.0s | 7,666 | 25 |
| q4 | ontology ON | 3m07s | 2m58s | 0m08s | 12 | 11 | 3.2s | 9,041 | 80 |
| q5 | ontology OFF | 2m10s | 2m10s | 0m00s | 21 | 20 | 0.0s | 6,764 | 0 |
| q5 | ontology ON | 2m38s | 2m29s | 0m08s | 30 | 29 | 1.4s | 7,584 | 75 |
| q6 | ontology OFF | 1m36s | 1m35s | 0m00s | 10 | 9 | 0.0s | 5,063 | 5 |
| q6 | ontology ON | 3m48s | 3m39s | 0m07s | 23 | 22 | 3.2s | 11,189 | 100 |

| Mode | Questions | Total agent time | Mean | Min | Max | Mean per turn | Mean score | Errors |
|---|---|---|---|---|---|---|---|---|
| ontology OFF | 7 | 12m03s | 1m43s | 0m10s | 4m06s | 8s | 23 | 0 |
| ontology ON | 7 | 13m22s | 1m55s | 0m18s | 3m48s | 7s | 79 | 0 |

| Question | Wall time (both modes + judge) | Judge time |
|---|---|---|
| q0 | 0m29s | 0m00s |
| q1 | 1m47s | 0m00s |
| q2 | 5m45s | 0m00s |
| q3 | 1m38s | 0m00s |
| q4 | 5m34s | 0m00s |
| q5 | 4m57s | 0m00s |
| q6 | 5m24s | 0m00s |

**Total run time:** 25m33s

| Question | Ontology OFF | Ontology ON |
|---|---|---|
| q0: Control: total expenditure | 100 (correct) | 100 (correct) |
| q1: Air-to-air missile expenditure | 20 (incorrect) | 100 (correct) |
| q2: Precision-guided munitions (munition hierarchy) | 10 (incorrect) | 0 (incorrect) |
| q3: Cluster munition employment | 0 (incorrect) | 100 (correct) |
| q4: Losses rolled up by force structure | 25 (incorrect) | 80 (partially_correct) |
| q5: Air defense mission capability at a point in time | 0 (incorrect) | 75 (partially_correct) |
| q6: Coalition partner losses | 5 (incorrect) | 100 (correct) |

## q0: Control: total expenditure

**Question.** How many weapons were fired in total by each side, and which single weapon type was fired most often?

**Why the ontology matters.** Control question - answerable from the database alone. Both agents should get it right.

**Ground truth.** Weapons fired: blue 598, red 452 (total 1050). Most-fired weapon type: M795 (116).

### ontology OFF - score 100/100

4 tool calls, 5 turns, 10.5 s, 2,502 input / 421 output tokens

**Total weapons fired**

| Side | Weapons fired |
|------|---------------|
| Blue | **598** |
| Red  | **452** |

**Most‑fired weapon type**

- **M795** – fired **116** times (the highest count among all weapon types).

The totals sum to 1 050 WEAPON_FIRED events in the simulation.

<details><summary>Tool calls</summary>

**simdb__describe_database**
```
{"": ""}
```
**simdb__run_sql**
```
SELECT side, COUNT(*) AS fired_count FROM events WHERE event_type='WEAPON_FIRED' GROUP BY side;
```
**simdb__run_sql**
```
SELECT weapon_type, COUNT(*) AS cnt FROM events WHERE event_type='WEAPON_FIRED' GROUP BY weapon_type ORDER BY cnt DESC LIMIT 5;
```
**simdb__run_sql**
```
SELECT SUM(fired_count) FROM (SELECT side, COUNT(*) AS fired_count FROM events WHERE event_type='WEAPON_FIRED' GROUP BY side);
```
</details>

### ontology ON - score 100/100

5 tool calls, 6 turns, 18.1 s, 1,903 input / 788 output tokens

**Weapons fired by side**

| Side | Weapons fired |
|------|---------------|
| Blue | 598 |
| Red  | 452 |

*Total fired events in the simulation: 1,050 (598 + 452).*

**Most frequently fired weapon type**

- **M795** – 116 shots (the highest count among all weapon types).

These numbers were obtained by counting the `WEAPON_FIRED` events in the AFSIM events table, grouping by the shooter’s side and by weapon type. The side labels “blue” and “red” are the coalition names recorded in `platforms.side`. No other weapon type matched the 116‑shot count.

<details><summary>Tool calls</summary>

**simdb__run_sql**
```
SELECT side, COUNT(*) as fired FROM events WHERE event_type='WEAPON_FIRED' GROUP BY side;
```
**simdb__run_sql**
```
SELECT weapon_type, COUNT(*) as cnt FROM events WHERE event_type='WEAPON_FIRED' GROUP BY weapon_type ORDER BY cnt DESC LIMIT 1;
```
**simdb__run_sql**
```
SELECT weapon_type, COUNT(*) as cnt FROM events WHERE event_type='WEAPON_FIRED' GROUP BY weapon_type ORDER BY cnt DESC LIMIT 5;
```
**simdb__run_sql**
```
SELECT COUNT(*) FROM events WHERE event_type='WEAPON_FIRED';
```
**simdb__run_sql**
```
SELECT DISTINCT side FROM platforms;
```
</details>

## q1: Air-to-air missile expenditure

**Question.** How many air-to-air missiles did each side expend over the whole engagement?

**Why the ontology matters.** Weapon names come from different federates: WPN_AMRAAM_D and IZDELIYE_610M are aliases, WPN_KESTREL is a notional scenario weapon, and AMRAAM-ER looks like an AAM but is a SAM.

**Ground truth.** Air-to-air missiles fired - blue: 52, red: 22 (total 74). By type: blue AIM-120C7=6; blue AIM-120D=16; blue AIM-132=3; blue AIM-9X_BLK2=4; blue MBDA_METEOR=7; blue WPN_AMRAAM_D=8; blue WPN_KESTREL=8; red IZDELIYE_610M=3; red R-37M=2; red R-73M=5; red R-77-1=12. Note: AMRAAM-ER (fired) is a surface-launched SAM and is excluded; WPN_AMRAAM_D is an alias of AIM-120D, IZDELIYE_610M an alias of R-37M, WPN_KESTREL is a notional IR AAM.

### ontology OFF - score 20/100

6 tool calls, 7 turns, 55.8 s, 2,369 input / 2,914 output tokens

**Air‑to‑air missile expenditure (total over the 4‑hour engagement)**  

| Side | Missiles expended | Breakdown (by type) |
|------|-------------------|---------------------|
| **Blue** | **29** | AIM‑120C7: 6  <br> AIM‑120D: 16 <br> AIM‑132: 3 <br> AIM‑9X BLK2: 4 |
| **Red** | **31** | 9M317M (R‑73M‑variant): 12 <br> R‑37M: 2 <br> R‑73M: 5 <br> R‑77‑1: 12 |

**How the numbers were derived**

1. Identified all weapon types that are air‑to‑air missiles by consulting the distinct `weapon_type` values in the `events` table and selecting those that are known AAMs (AIM‑, R‑, and the 9M317M variant).  
2. Queried the `events` table for rows where `event_type = 'WEAPON_FIRED'` and the `weapon_type` is one of the identified AAMs.  
3. Grouped the results by `side` and summed the counts.  
4. Verified the totals by a second aggregation that summed the per‑type counts for each side.  

No assumptions were made about the classification of weapon types beyond the names present in the database; all counts come directly from the event log.

**Judge - missed or wrong:**
- Blue 29, should be 52 (METEOR, KESTREL, WPN_AMRAAM_D missing)
- Red 31, should be 22 (9M317M, a SAM, counted; IZDELIYE_610M missing)

<details><summary>Tool calls</summary>

**simdb__describe_database**
```
{}
```
**simdb__run_sql**
```
SELECT side, weapon_type, COUNT(*) AS expended FROM events WHERE event_type='WEAPON_FIRED' AND weapon_type IN ('AIM-120C7','AIM-120D','AIM-132','AIM-9X_BLK2','R-73M','R-77-1','R-37M','9M317M') GROUP BY side, weapon_type;
```
**simdb__run_sql**
```
SELECT side, SUM(expended) AS total FROM (SELECT side, weapon_type, COUNT(*) AS expended FROM events WHERE event_type='WEAPON_FIRED' AND weapon_type IN ('AIM-120C7','AIM-120D','AIM-132','AIM-9X_BLK2','R-73M','R-77-1','R-37M','9M317M') GROUP BY side, weapon_type) GROUP BY side;
```
**simdb__run_sql**
```
SELECT DISTINCT weapon_type FROM events WHERE event_type='WEAPON_FIRED' AND (weapon_type LIKE 'AIM-%' OR weapon_type LIKE 'R-%' OR weapon_type LIKE '9M3%');
```
**simdb__run_sql**
```
SELECT DISTINCT weapon_type FROM events WHERE event_type='WEAPON_FIRED' AND weapon_type LIKE 'R-%';
```
**simdb__run_sql**
```
SELECT DISTINCT weapon_type FROM events WHERE event_type='WEAPON_FIRED' AND weapon_type LIKE 'AIM-%';
```
</details>

### ontology ON - score 100/100

7 tool calls, 8 turns, 51.1 s, 5,626 input / 2,283 output tokens

**Air‑to‑air missiles expended**

| Side | Total AAM fired |
|------|-----------------|
| Blue | **52** |
| Red  | **22** |

**Breakdown by missile type**

| Missile | Blue | Red |
|---------|------|-----|
| AIM‑120C7 | 6 | – |
| AIM‑120D | 16 | – |
| AIM‑132 | 3 | – |
| AIM‑9X_BLK2 | 4 | – |
| MBDA_METEOR | 7 | – |
| WPN_AMRAAM_D | 8 | – |
| WPN_KESTREL | 8 | – |
| IZDELIYE_610M | – | 3 |
| R‑37M | – | 2 |
| R‑73M | – | 5 |
| R‑77‑1 | – | 12 |

**Methodology & data sources**

1. **Weapon classification** – queried the battlespace ontology for all simulation‑type names that are instances of the class `bs:AirToAirMissile` (11 names).  
2. **Event counting** – executed a SQLite query on the `events` table, selecting rows where `event_type = 'WEAPON_FIRED'` and `weapon_type` is one of those 11 names, grouped by `side`.  
3. **Verification** – summed the counts to confirm the total (74) matched the sum of per‑side totals, and displayed the per‑type breakdown to ensure all 11 weapons were captured.

**Assumptions / uncertainties**

* The ontology mapping of simulation type names to `bs:AirToAirMissile` is complete; no additional AAM types exist in the simulation.  
* The `side` field in the events table reflects the side of the firing platform (consistent with `platforms.side`).  
* No other events (e.g., intercepted or misdirected missiles) were counted; only direct firings were considered.

<details><summary>Tool calls</summary>

**ontology__ontology_overview**
```
{}
```
**ontology__sparql_query**
```
SELECT DISTINCT ?simTypeName WHERE { ?t a bs:AirToAirMissile . ?t bs:simTypeName ?simTypeName . }
```
**simdb__describe_database**
```
{}
```
**simdb__run_sql**
```
SELECT side, COUNT(*) AS cnt FROM events WHERE event_type='WEAPON_FIRED' AND weapon_type IN ('MBDA_METEOR','R-77-1','AIM-9X_BLK2','WPN_KESTREL','WPN_AMRAAM_D','AIM-132','AIM-120D','R-37M','R-73M','AIM-120C7','IZDELIYE_610M') GROUP BY side
```
**ontology__sparql_query**
```
SELECT ?t WHERE { ?t bs:simTypeName 'WPN_KESTREL' . ?t a bs:AirToAirMissile . }
```
**simdb__run_sql**
```
SELECT COUNT(*) FROM events WHERE event_type='WEAPON_FIRED' AND weapon_type IN ('MBDA_METEOR','R-77-1','AIM-9X_BLK2','WPN_KESTREL','WPN_AMRAAM_D','AIM-132','AIM-120D','R-37M','R-73M','AIM-120C7','IZDELIYE_610M')
```
**simdb__run_sql**
```
SELECT weapon_type, side, COUNT(*) AS cnt FROM events WHERE event_type='WEAPON_FIRED' AND weapon_type IN ('MBDA_METEOR','R-77-1','AIM-9X_BLK2','WPN_KESTREL','WPN_AMRAAM_D','AIM-132','AIM-120D','R-37M','R-73M','AIM-120C7','IZDELIYE_610M') GROUP BY weapon_type, side
```
</details>

## q2: Precision-guided munitions (munition hierarchy)

**Question.** Not counting surface-to-air or air-to-air missiles, how many precision-guided munitions did the Blue coalition expend? Break the total down by category: missiles, guided bombs, guided rockets, guided artillery projectiles, and loitering munitions.

**Why the ontology matters.** PGM is a cross-cutting class: Excalibur (M982A1), APKWS_II and GMLRS are guided; XM1113 and Hydra M151 are not; TRIDENT_GLIDE_KIT is a notional GPS bomb kit; MGM-140B/PRSM are missiles.

**Ground truth.** Blue PGMs excluding SAMs/AAMs: total 272. missiles: 120 (AGM-114R=10, AGM-179_JAGM=18, AGM-88E=10, AGM-88G=12, BGM-109E=20, BGM-71F=5, JASSM-ER=24, MGM-140B=3, NSM_BLK1A=4, PRSM_INC1=6, RGM-184A=8); guided bombs: 84 (GBU-12=4, GBU-31V3=20, GBU-39=20, GBU-53B=24, TRIDENT_GLIDE_KIT=16); guided rockets: 50 (APKWS_II=14, M30A2=12, M31A2=24); guided artillery projectiles: 10 (M982A1=10); loitering munitions: 8 (SB600=8). Unguided Blue weapons that must NOT be counted: HYDRA70_M151, M795, M829A4, M830A1, M919, XM1113.

### ontology OFF - score 10/100

19 tool calls, 20 turns, 246.4 s, 10,581 input / 12,835 output tokens

**Blue coalition precision‑guided munitions expended (surface‑to‑air and air‑to‑air missiles excluded)**  

| Category | Count |
|----------|-------|
| Missiles | 152 |
| Guided bombs | 68 |
| Guided rockets | 157 |
| Guided artillery projectiles | 46 |
| Loitering munitions | 8 |
| **Total** | **431** |

**How the numbers were derived**

1. **Identify Blue‑side weapon‑fire events**  
   ```sql
   SELECT weapon_type, COUNT(*) AS cnt
   FROM events
   WHERE event_type='WEAPON_FIRED' AND side='blue'
   GROUP BY weapon_type;
   ```
   The result (41 distinct weapon types) was the basis for all further counting.

2. **Exclude surface‑to‑air (SAM) and air‑to‑air (AAM) missiles**  
   SAM/AAM types were determined by name patterns (`AIM-`, `RIM-`, `SM-`, `PAC-3`, `RGM-184`, `WPN_AMRAAM_D`, `AMRAAM-ER`, `FIM-92K`, `GEM‑T`).  
   ```sql
   SELECT SUM(cnt) AS sam_aam_total
   FROM (SELECT COUNT(*) AS cnt
         FROM events
         WHERE event_type='WEAPON_FIRED'
           AND side='blue'
           AND weapon_type IN (…list of SAM/AAM types…));
   ```
   Total SAM/AAM events = 136 (128 + 8 “GEM‑T” intercepts).

3. **Count each requested category** – all counts verified by individual SQL sub‑queries:

   *Missiles* (non‑SAM/AAM)  
   ```sql
   SELECT SUM(cnt)
   FROM (SELECT COUNT(*) AS cnt
         FROM events
         WHERE event_type='WEAPON_FIRED' AND side='blue'
           AND weapon_type IN ('XM1113','JASSM-ER','TRIDENT_GLIDE_KIT',
                               'NSM_BLK1A','MBDA_METEOR','AGM-114R',
                               'AGM-179_JAGM','AGM-88E','AGM-88G',
                               'BGM-109E','BGM-71F','WPN_KESTREL'));
   ```
   Result: **152**

   *Guided bombs*  
   ```sql
   SELECT SUM(cnt)
   FROM (SELECT COUNT(*) AS cnt
         FROM events
         WHERE event_type='WEAPON_FIRED' AND side='blue'
           AND weapon_type IN ('GBU-12','GBU-31V3','GBU-39','GBU-53B'));
   ```
   Result: **68**

   *Guided rockets*  
   ```sql
   SELECT SUM(cnt)
   FROM (SELECT COUNT(*) AS cnt
         FROM events
         WHERE event_type='WEAPON_FIRED' AND side='blue'
           AND weapon_type IN ('M795','MGM-140B','HYDRA70_M151','APKWS_II'));
   ```
   Result: **157**

   *Guided artillery projectiles*  
   M982A1 (guid‑artillery), M30A2, and M31A2 are 155 mm guided projectiles fired from howitzers.  
   ```sql
   SELECT SUM(cnt)
   FROM (SELECT COUNT(*) AS cnt
         FROM events
         WHERE event_type='WEAPON_FIRED' AND side='blue'
           AND weapon_type IN ('M982A1','M30A2','M31A2'));
   ```
   Result: **46**

   *Loitering munitions* – only SB600 was fired.  
   ```sql
   SELECT SUM(cnt)
   FROM (SELECT COUNT(*) AS cnt
         FROM events
         WHERE event_type='WEAPON_FIRED' AND side='blue'
           AND weapon_type='SB600');
   ```
   Result: **8**

4. **Cross‑check** – total fired = 598.  
   Excluded SAM/AAM = 136.  
   Tank‑projectile events (M829A4, M830A1, M919, PRSM_INC1) = 31.  
   Remaining 598 – 136 – 31 = **431**, matching the sum of the five categories above.

**Assumptions / Uncertainties**

* SAM/AAM classification relied on weapon‑type naming conventions; we excluded all types beginning with `AIM-`, `RIM-`, `SM-`, `PAC-3`, `RGM-184`, `WPN_AMRAAM_D`, `AMRAAM-ER`, `FIM-92K`, and `GEM‑T`.  
* Guided artillery projectiles were defined as 155 mm guided projectiles (M982A1, M30A2, M31A2).  
* Loitering munitions were identified by the single type `SB600`.  
* Any weapon type not falling into the above categories (e.g., tank projectiles) was omitted from the precision‑guided tally as requested.

**Judge - missed or wrong:**
- Total 431, should be 272
- Every other category wrong

<details><summary>Tool calls</summary>

**simdb__describe_database**
```
{"name": "simdb__describe_database", "arguments": {}}
```
**simdb__run_sql**
```
SELECT weapon_type, COUNT(*) as cnt FROM events WHERE event_type='WEAPON_FIRED' AND side='blue' GROUP BY weapon_type ORDER BY cnt DESC
```
**simdb__run_sql**
```
SELECT weapon_type, COUNT(*) as cnt FROM events WHERE event_type='WEAPON_FIRED' AND side='blue' GROUP BY weapon_type ORDER BY weapon_type
```
**simdb__run_sql**
```
SELECT * FROM events WHERE event_type='WEAPON_FIRED' AND side='blue' AND weapon_type='LANCET-3'
```
**simdb__run_sql**
```
SELECT * FROM events WHERE event_type='WEAPON_FIRED' AND side='blue' AND weapon_type='ZALA_LANCET3'
```
**simdb__run_sql**
```
SELECT * FROM events WHERE event_type='WEAPON_FIRED' AND side='blue' AND weapon_type='XM1113'
```
**simdb__run_sql**
```
SELECT * FROM events WHERE event_type='WEAPON_FIRED' AND side='blue' AND weapon_type='TRIDENT_GLIDE_KIT'
```
**simdb__run_sql**
```
SELECT COUNT(*) as total FROM events WHERE event_type='WEAPON_FIRED' AND side='blue'
```
**simdb__run_sql**
```
SELECT * FROM events WHERE event_type='WEAPON_FIRED' AND side='blue' AND weapon_type='GEM-T'
```
**simdb__run_sql**
```
SELECT * FROM events WHERE event_type='WEAPON_FIRED' AND side='blue' AND weapon_type='M31A2'
```
**simdb__run_sql**
```
SELECT * FROM events WHERE event_type='WEAPON_FIRED' AND side='blue' AND weapon_type='M30A2'
```
**simdb__run_sql**
```
SELECT weapon_type, COUNT(*) as cnt FROM events WHERE event_type='WEAPON_FIRED' AND side='blue' AND weapon_type IN ('FIM-92K','RIM-162D','SM-2_BLK3C','SM-6_BLK1A','PAC-3_MSE','RGM-184A','AMRAAM-ER','WPN_AMRAAM_D','AIM-120D','AIM-120C7','AIM-132','AIM-9X_BLK2') GROUP BY weapon_type
```
**simdb__run_sql**
```
SELECT weapon_type, COUNT(*) as cnt FROM events WHERE event_type='WEAPON_FIRED' AND side='blue' ORDER BY cnt DESC
```
**simdb__run_sql**
```
SELECT weapon_type, COUNT(*) as cnt FROM events WHERE event_type='WEAPON_FIRED' AND side='blue' GROUP BY weapon_type ORDER BY cnt DESC
```
**simdb__run_sql**
```
SELECT SUM(cnt) as total FROM (SELECT COUNT(*) as cnt FROM events WHERE event_type='WEAPON_FIRED' AND side='blue' AND weapon_type IN ('XM1113','JASSM-ER','TRIDENT_GLIDE_KIT','NSM_BLK1A','MBDA_METEOR','AGM-114R','AGM-179_JAGM','AGM-88E','AGM-88G','BGM-109E','BGM-71F','WPN_KESTREL'))
```
**simdb__run_sql**
```
SELECT SUM(cnt) as total FROM (SELECT COUNT(*) as cnt FROM events WHERE event_type='WEAPON_FIRED' AND side='blue' AND weapon_type IN ('GBU-12','GBU-31V3','GBU-39','GBU-53B'))
```
**simdb__run_sql**
```
SELECT SUM(cnt) as total FROM (SELECT COUNT(*) as cnt FROM events WHERE event_type='WEAPON_FIRED' AND side='blue' AND weapon_type IN ('M795','MGM-140B','HYDRA70_M151','APKWS_II'))
```
**simdb__run_sql**
```
SELECT SUM(cnt) as total FROM (SELECT COUNT(*) as cnt FROM events WHERE event_type='WEAPON_FIRED' AND side='blue' AND weapon_type IN ('M982A1','M30A2','M31A2'))
```
**simdb__run_sql**
```
SELECT SUM(cnt) as total FROM (SELECT COUNT(*) as cnt FROM events WHERE event_type='WEAPON_FIRED' AND side='blue' AND weapon_type='SB600')
```
</details>

### ontology ON - score 0/100

22 tool calls, 24 turns, 98.3 s, 14,855 input / 4,428 output tokens

_no answer_ (None)

**Judge - missed or wrong:**
- Empty final answer after 22 tool calls (still empty after the nudge)

<details><summary>Tool calls</summary>

**ontology__ontology_overview**
```
{}
```
**simdb__describe_database**
```
{}
```
**ontology__sparql_query**
```
SELECT DISTINCT ?name WHERE { ?t a bs:SimulationType ; bs:simTypeName ?name . ?t a bs:SurfaceToAirMissile . }
```
**ontology__sparql_query**
```
SELECT DISTINCT ?name WHERE { ?t a bs:SimulationType ; bs:simTypeName ?name . ?t a bs:AirToAirMissile . }
```
**ontology__sparql_query**
```
SELECT DISTINCT ?name WHERE { ?t a bs:SimulationType ; bs:simTypeName ?name . ?t a bs:Missile . FILTER NOT EXISTS { ?t a bs:SurfaceToAirMissile . } FILTER NOT EXISTS { ?t a bs:AirToAirMissile . } }
```
**ontology__sparql_query**
```
SELECT DISTINCT ?name WHERE { ?t a bs:SimulationType ; bs:simTypeName ?name . ?t a bs:GuidedBomb . }
```
**ontology__sparql_query**
```
SELECT DISTINCT ?name WHERE { ?t a bs:SimulationType ; bs:simTypeName ?name . ?t a bs:GuidedRocket . }
```
**ontology__sparql_query**
```
SELECT DISTINCT ?name WHERE { ?t a bs:SimulationType ; bs:simTypeName ?name . ?t a bs:GuidedProjectile . }
```
**ontology__sparql_query**
```
SELECT DISTINCT ?name WHERE { ?t a bs:SimulationType ; bs:simTypeName ?name . ?t a bs:LoiteringMunition . }
```
**simdb__run_sql**
```
SELECT weapon_type, COUNT(*) as cnt FROM events WHERE event_type='WEAPON_FIRED' AND side='blue' AND weapon_type IN ('3M55','AGM-88E','9M728','9M117M1','MGM-140B','PRSM_INC1','P-800','9M723','KH-31PD','RGM-184A','9M133M-2','NSM_BLK1A','3M54','3M14','BGM-71F','BGM-109E','AGM-179_JAGM','AGM-88G','9M127-1','JASSM-ER','AGM-114R','KH-59MK2','9M119M','KAB-20S','GBU-31V3','GBU-39','TRIDENT_GLIDE_KIT','KAB-500S','GBU-53B','GBU-12','9M542','M30A2','M31A2','APKWS_II','3OF39','M982A1','ZALA_LANCET3','VORON-K','LANCET-3','SB600','GERAN-2') GROUP BY weapon_type;
```
**simdb__run_sql**
```
SELECT weapon_type, COUNT(*) as cnt FROM events WHERE event_type='WEAPON_FIRED' AND side='blue' AND weapon_type IN ('3M55','AGM-88E','9M728','9M117M1','MGM-140B','PRSM_INC1','P-800','9M723','KH-31PD','RGM-184A','9M133M-2','NSM_BLK1A','3M54','3M14','BGM-71F','BGM-109E','AGM-179_JAGM','AGM-88G','9M127-1','JASSM-ER','AGM-114R','KH-59MK2','9M119M') GROUP BY weapon_type;
```
**simdb__run_sql**
```
SELECT COUNT(*) FROM events WHERE event_type='WEAPON_FIRED' AND side='blue' AND weapon_type='3M55';
```
**simdb__run_sql**
```
SELECT weapon_type, COUNT(*) as cnt FROM events WHERE event_type='WEAPON_FIRED' AND side='blue' AND weapon_type IN ('KAB-20S','GBU-31V3','GBU-39','TRIDENT_GLIDE_KIT','KAB-500S','GBU-53B','GBU-12') GROUP BY weapon_type;
```
**simdb__run_sql**
```
SELECT weapon_type, COUNT(*) as cnt FROM events WHERE event_type='WEAPON_FIRED' AND side='blue' AND weapon_type IN ('3M55','AGM-88E','9M728','9M117M1','MGM-140B','PRSM_INC1','P-800','9M723','KH-31PD','RGM-184A','9M133M-2','NSM_BLK1A','3M54','3M14','BGM-71F','BGM-109E','AGM-179_JAGM','AGM-88G','9M127-1','JASSM-ER','AGM-114R','KH-59MK2','9M119M') GROUP BY weapon_type;
```
**simdb__run_sql**
```
SELECT COUNT(*) FROM events WHERE event_type='WEAPON_FIRED' AND side='blue' AND weapon_type='3M55';
```
**simdb__run_sql**
```
SELECT COUNT(*) FROM events WHERE event_type='WEAPON_FIRED' AND side='blue' AND weapon_type='9M728';
```
**simdb__run_sql**
```
SELECT COUNT(*) FROM events WHERE event_type='WEAPON_FIRED' AND side='blue' AND weapon_type='9M117M1';
```
**simdb__run_sql**
```
SELECT COUNT(*) FROM events WHERE event_type='WEAPON_FIRED' AND side='blue' AND weapon_type='9M723';
```
**simdb__run_sql**
```
SELECT COUNT(*) FROM events WHERE event_type='WEAPON_FIRED' AND side='blue' AND weapon_type='KH-31PD';
```
**simdb__run_sql**
```
SELECT COUNT(*) FROM events WHERE event_type='WEAPON_FIRED' AND side='blue' AND weapon_type='9M133M-2';
```
**simdb__run_sql**
```
SELECT COUNT(*) FROM events WHERE event_type='WEAPON_FIRED' AND side='blue' AND weapon_type='9M127-1';
```
**simdb__run_sql**
```
SELECT COUNT(*) FROM events WHERE event_type='WEAPON_FIRED' AND side='blue' AND weapon_type='9M119M';
```
</details>

## q3: Cluster munition employment

**Question.** Which cluster (submunition-dispensing) munitions were employed during the engagement? For each, give the weapon type, the side that used it, and the number of rounds fired.

**Why the ontology matters.** Requires warhead knowledge: MGM-140B is ATACMS Block IA (APAM submunitions), BURYA-12 is notional, while M30A2 (GMLRS Alternative Warhead) looks like the old DPICM rocket but has no submunitions.

**Ground truth.** Cluster munitions fired: total 53 rounds - MGM-140B (MGM-140B ATACMS Block IA) by blue: 3; 3O23 (3-O-23 152 mm cargo projectile (ICM)) by red: 14; 9M55K (9M55K 300 mm cargo rocket) by red: 24; BURYA-12 (Burya-12 cargo rocket (notional)) by red: 12. Not cluster: M30A2 GMLRS-AW (pre-formed fragments, replaced the DPICM M30), M31A2 (unitary).

### ontology OFF - score 0/100

7 tool calls, 8 turns, 37.8 s, 2,690 input / 1,912 output tokens

**Cluster (submunition‑dispensing) munitions used**

| Weapon type | Side that fired it | Rounds fired |
|-------------|--------------------|--------------|
| **GBU‑39**  | blue | 20 |
| **GBU‑53B** | blue | 24 |

**Notes & assumptions**

* The only weapons in the simulation output that are recognized as submunition‑dispensing (cluster) munitions are the GBU‑39 and GBU‑53B.  
* The `events` table shows 44 instances of `WEAPON_FIRED` for these two types, all attributed to the blue side and none to the red side.  
* No other weapon types in the log (e.g., 9M55K, 9M542, 9M728, 9M117M1, 9M119M, 9M127‑1) are classified as cluster munitions in standard NATO/Russian doctrine, and therefore were not included.  

Thus, during the engagement only the GBU‑39 (20 rounds) and GBU‑53B (24 rounds) cluster bombs were employed, all by the blue side.

**Judge - missed or wrong:**
- GBU-39 and GBU-53B are not cluster munitions
- All four true ones missed

<details><summary>Tool calls</summary>

**simdb__describe_database**
```
{}
```
**simdb__run_sql**
```
SELECT DISTINCT weapon_type FROM events WHERE event_type='WEAPON_FIRED' AND weapon_type IN ('GBU-53B','GBU-39','9M55K','9M542','9M127-1','9M728','9M117M1','9M119M')
```
**simdb__run_sql**
```
SELECT weapon_type, COUNT(*) as rounds_fired FROM events WHERE event_type='WEAPON_FIRED' AND weapon_type IN ('GBU-53B','GBU-39') GROUP BY weapon_type
```
**simdb__run_sql**
```
SELECT side, weapon_type, COUNT(*) as rounds_fired FROM events WHERE event_type='WEAPON_FIRED' AND weapon_type IN ('GBU-53B','GBU-39') GROUP BY side, weapon_type
```
**simdb__run_sql**
```
SELECT DISTINCT weapon_type FROM events WHERE event_type='WEAPON_FIRED' AND weapon_type LIKE '%55K%'
```
**simdb__run_sql**
```
SELECT COUNT(*) FROM events WHERE event_type='WEAPON_FIRED' AND weapon_type IN ('GBU-39','GBU-53B')
```
**simdb__run_sql**
```
SELECT COUNT(*) FROM events WHERE event_type='WEAPON_FIRED' AND side='red' AND weapon_type IN ('GBU-39','GBU-53B')
```
</details>

### ontology ON - score 100/100

9 tool calls, 10 turns, 60.3 s, 3,412 input / 2,684 output tokens

**Cluster munitions that actually fired during the engagement**

| Weapon type | Side that used it | Rounds fired |
|-------------|-------------------|--------------|
| **9M55K**  | red | 24 |
| **BURYA‑12** | red | 12 |
| **3O23**   | red | 14 |
| **MGM‑140B** | blue | 3 |

**Head‑line summary**

- 4 cluster‑munition types were expended (9M55K, BURYA‑12, 3O23, MGM‑140B).  
- Total rounds fired: **53**.

**Notes**

- The ontology lists five cluster‑munition types (`9M55K`, `BURYA‑12`, `3O23`, `MGM‑140B`, `RBK‑500_SPBE`).  
- The simulation events confirm that `RBK‑500_SPBE` was present but **no rounds of it were fired** (0 events).  
- Counts were obtained by querying the `events` table for rows with `event_type='WEAPON_FIRED'` and grouping by `weapon_type` and `side`. The results sum to 53, matching the total number of cluster‑munition firings.

<details><summary>Tool calls</summary>

**ontology__find_terms**
```
cluster
```
**ontology__sparql_query**
```
PREFIX bs: <http://example.org/battlespace#>
SELECT DISTINCT ?typeName WHERE {
  ?type a bs:SimulationType ; bs:simTypeName ?typeName .
  ?type a bs:ClusterMunition .
}
```
**ontology__sparql_query**
```
PREFIX bs: <http://example.org/battlespace#>
SELECT ?typeName ?className WHERE {
  ?type a bs:SimulationType ; bs:simTypeName ?typeName .
  ?type a ?className .
  FILTER(?typeName IN ("9M55K","MGM-140B","BURYA-12","3O23","RBK-500_SPBE"))
}
```
**ontology__sparql_query**
```
PREFIX bs: <http://example.org/battlespace#>
SELECT ?typeName ?className WHERE {
  ?type a bs:SimulationType ; bs:simTypeName ?typeName .
  ?type a ?className .
  FILTER(?typeName IN ("9M55K","MGM-140B","BURYA-12","RBK-500_SPBE"))
}
```
**simdb__run_sql**
```
SELECT events.weapon_type, events.side, COUNT(*) AS cnt FROM events
WHERE events.event_type='WEAPON_FIRED'
AND events.weapon_type IN ('9M55K','MGM-140B','BURYA-12','3O23','RBK-500_SPBE')
GROUP BY events.weapon_type, events.side
ORDER BY events.weapon_type
```
**simdb__run_sql**
```
SELECT COUNT(*) FROM events WHERE event_type='WEAPON_FIRED' AND weapon_type='RBK-500_SPBE'
```
**simdb__run_sql**
```
SELECT DISTINCT events.weapon_type, COUNT(*) AS cnt FROM events
WHERE event_type='WEAPON_FIRED'
GROUP BY events.weapon_type
ORDER BY cnt DESC
```
**ontology__sparql_query**
```
PREFIX bs: <http://example.org/battlespace#>
SELECT ?typeName ?className WHERE {
  ?type a bs:SimulationType ; bs:simTypeName ?typeName .
  FILTER(?typeName="M795")
  ?type a ?className .
}
```
**simdb__run_sql**
```
SELECT SUM(cnt) FROM (
SELECT COUNT(*) AS cnt FROM events WHERE event_type='WEAPON_FIRED' AND weapon_type IN ('9M55K','MGM-140B','BURYA-12','3O23','RBK-500_SPBE')
)
```
</details>

## q4: Losses rolled up by force structure

**Question.** For each Blue brigade-level unit (brigade, regiment, or wing), how many of its platforms were destroyed during the engagement?

**Why the ontology matters.** The database only has callsigns. Which callsign belongs to which squadron/battalion/brigade exists only in the ontology's chain of command (bs:subordinateTo).

**Ground truth.** Blue brigade/regiment/wing-level losses: 1st Armored Brigade Combat Team, 3ID: 8 of 30 (BLADE14, COBRA11, COBRA12, COBRA13, COBRA14, IRON13, THUNDER22, THUNDER24); 11th Masurian Artillery Regiment (POL): 2 of 4 (KRAB31, KRAB34); 140 Expeditionary Air Wing (RAF): 2 of 4 (RAPIER1, RAPIER3); 388th Fighter Wing: 2 of 8 (LIGHTNING12, LIGHTNING14); 52nd Fighter Wing: 2 of 8 (WEASEL22, WEASEL23); 22nd Air Refueling Wing: 1 of 1 (SHELL71); 10th Army Air and Missile Defense Command: 0 of 6; 41st Field Artillery Brigade: 0 of 4; 432nd Wing: 0 of 2; 4th Fighter Wing: 0 of 4; 552nd Air Control Wing: 0 of 1; 7th Bomb Wing: 0 of 2; Combat Aviation Brigade, 3ID: 0 of 4; Destroyer Squadron 60: 0 of 3; Main Operating Base NORTHSTAR: 0 of 1; Royal Norwegian Navy contribution: 0 of 1. Total Blue platforms destroyed: 18.

### ontology OFF - score 25/100

15 tool calls, 16 turns, 146.4 s, 5,525 input / 7,666 output tokens

**Blue brigade‑level units and how many of their platforms were destroyed**

| Unit (prefix) | Platforms destroyed |
|---------------|---------------------|
| BANDIT        | 0 |
| BLADE         | 1 |
| BONE          | 0 |
| COBRA         | 4 |
| DRAGON        | 0 |
| HAMMER        | 0 |
| IRON          | 1 |
| KRAB          | 2 |
| LASSO         | 0 |
| LIGHTNING     | 2 |
| RAZOR         | 0 |
| REAPER        | 0 |
| THUNDER       | 2 |
| TROLL         | 1 |
| WARLORD       | 0 |
| WEASEL        | 2 |
| WOLFPACK      | 0 |

**How the figures were obtained**

1. **Unit identification** – Platform names ending in two digits (e.g., `LIGHTNING12`) were treated as belonging to a unit.  
   The unit name (prefix) was extracted as the portion of the name before the final two digits (`substr(name,1,length(name)-2)`).

2. **Brigade‑level filtering** – Only prefixes that had **≥ 2** platforms on the Blue side were retained, giving 17 units (the rest, e.g., `DARKSTAR`, `SHELL`, had only one platform and were excluded).

3. **Destroyed platforms** – A platform was counted as destroyed if any record in `platform_status` had `state='BROKEN'`.  
   Distinct platform names were used so that a platform destroyed at multiple time steps was counted only once.

4. **Counting** – For each of the 17 units the number of distinct destroyed platforms was tallied.

**Assumptions / uncertainties**

* The naming convention (`PREFIXxx`) was taken as the authoritative link between a platform and its brigade‑level unit.  
* Only platforms whose names ended in two digits were considered; any unit whose platform names did not follow this pattern (e.g., airbases, facilities) were ignored.  
* A unit with only one platform was assumed **not** to be a brigade‑level entity (the simulation may have modeled it as a special detachment).  

These counts reflect the number of distinct Blue platforms that reached a `BROKEN` state during the 4‑hour engagement.

**Judge - missed or wrong:**
- Grouped by callsign prefix, not unit

<details><summary>Tool calls</summary>

**simdb__describe_database**
```
{}
```
**simdb__run_sql**
```
SELECT name, type, side FROM platforms LIMIT 50;
```
**simdb__run_sql**
```
SELECT name, type, side FROM platforms WHERE name LIKE '%12%' OR name LIKE '%13%' OR name LIKE '%14%' LIMIT 50;
```
**simdb__run_sql**
```
SELECT DISTINCT name FROM platforms ORDER BY name;
```
**simdb__run_sql**
```
SELECT name, substr(name, -1) AS last1, substr(name, -2, 1) AS last2 FROM platforms LIMIT 20;
```
**simdb__run_sql**
```
SELECT name, substr(name, 1, length(name)-2) AS prefix FROM platforms WHERE substr(name,-1) BETWEEN '0' AND '9' AND substr(name,-2,1) BETWEEN '0' AND '9' LIMIT 20;
```
**simdb__run_sql**
```
SELECT DISTINCT p.name, substr(p.name, 1, length(p.name)-2) AS prefix FROM platforms p JOIN platform_status s ON p.name=s.platform WHERE s.state='BROKEN' AND p.side='blue' AND substr(p.name,-1) BETWEEN '0' AND '9' AND substr(p.name,-2,1) BETWEEN '0' AND '9';
```
**simdb__run_sql**
```
SELECT prefix, count(*) AS total FROM (SELECT substr(name,1,length(name)-2) AS prefix FROM platforms WHERE side='blue' AND substr(name,-1) BETWEEN '0' AND '9' AND substr(name,-2,1) BETWEEN '0' AND '9') GROUP BY prefix HAVING total >= 2 ORDER BY prefix;
```
**simdb__run_sql**
```
SELECT substr(name,1,length(name)-2) AS prefix, count(*) AS destroyed FROM platforms p JOIN platform_status s ON p.name=s.platform WHERE s.state='BROKEN' AND p.side='blue' AND substr(p.name,-1) BETWEEN '0' AND '9' AND substr(p.name,-2,1) BETWEEN '0' AND '9' GROUP BY prefix ORDER BY prefix;
```
**simdb__run_sql**
```
SELECT prefix, count(*) AS destroyed FROM (SELECT DISTINCT p.name, substr(p.name,1,length(p.name)-2) AS prefix FROM platforms p JOIN platform_status s ON p.name=s.platform WHERE s.state='BROKEN' AND p.side='blue' AND substr(p.name,-1) BETWEEN '0' AND '9' AND substr(p.name,-2,1) BETWEEN '0' AND '9') GROUP BY prefix ORDER BY prefix;
```
**simdb__run_sql**
```
SELECT prefix, count(DISTINCT p.name) AS destroyed FROM platforms p JOIN platform_status s ON p.name=s.platform WHERE s.state='BROKEN' AND p.side='blue' AND substr(p.name,-1) BETWEEN '0' AND '9' AND substr(p.name,-2,1) BETWEEN '0' AND '9' GROUP BY prefix ORDER BY prefix;
```
**simdb__run_sql**
```
SELECT prefix, count(*) AS destroyed FROM (SELECT DISTINCT p.name, substr(p.name,1,length(p.name)-2) AS prefix FROM platforms p JOIN platform_status s ON p.name=s.platform WHERE s.state='BROKEN' AND p.side='blue' AND substr(p.name,-1) BETWEEN '0' AND '9' AND substr(p.name,-2,1) BETWEEN '0' AND '9') GROUP BY prefix ORDER BY prefix;
```
**simdb__run_sql**
```
SELECT prefix, count(*) AS total FROM (SELECT substr(name,1,length(name)-2) AS prefix FROM platforms WHERE side='blue' AND substr(name,-1) BETWEEN '0' AND '9' AND substr(name,-2,1) BETWEEN '0' AND '9') GROUP BY prefix ORDER BY prefix;
```
**simdb__run_sql**
```
SELECT p.name FROM platforms p JOIN platform_status s ON p.name=s.platform WHERE s.state='BROKEN' AND p.side='blue' AND substr(p.name,-1) BETWEEN '0' AND '9' AND substr(p.name,-2,1) BETWEEN '0' AND '9' AND substr(p.name,1,length(p.name)-2)='BONE';
```
**simdb__run_sql**
```
SELECT p.name FROM platforms p JOIN platform_status s ON p.name=s.platform WHERE s.state='BROKEN' AND p.side='blue' AND substr(p.name,-1) BETWEEN '0' AND '9' AND substr(p.name,-2,1) BETWEEN '0' AND '9' AND substr(p.name,1,length(p.name)-2)='DRAGON';
```
</details>

### ontology ON - score 80/100

11 tool calls, 12 turns, 187.3 s, 13,486 input / 9,041 output tokens

**Destroyed platforms per Blue brigade‑level unit**

| Unit (label) | Number of destroyed platforms |
|--------------|------------------------------|
| 22nd Air Refueling Wing | **1** |
| 140 Expeditionary Air Wing (RAF) | **2** |
| 52nd Fighter Wing | **2** |
| 388th Fighter Wing | **2** |
| 11th Masurian Artillery Regiment (POL) | **1** |
| 1st Armored Brigade Combat Team, 3ID | **7** |
| All other Blue brigades/regiments/air‑wings | **0** |

**Break‑down**

| Unit (label) | Destroyed platforms (by name) |
|--------------|--------------------------------|
| 22nd Air Refueling Wing | SHELL71 |
| 140 Expeditionary Air Wing (RAF) | RAPIER3, RAPIER1 |
| 52nd Fighter Wing | WEASEL23, WEASEL22 |
| 388th Fighter Wing | LIGHTNING14, LIGHTNING12 |
| 11th Masurian Artillery Regiment (POL) | KRAB31 |
| 1st Armored Brigade Combat Team, 3ID | THUNDER22, THUNDER24, COBRA14, COBRA12, COBRA11, IRON13, BLADE14 |

**Methodology & Assumptions**

1. **Unit Identification** – Used the ontology to list all Blue‑coalition units whose echelon is *Brigade*, *Regiment*, or *Wing*.
2. **Platform Ownership** – Platforms are linked to their owning unit via the `bs:assignedTo` property.  
   The `bs:hasSubordinate` relationship gives the full set of platforms under a unit at any depth.
3. **Destroyed Platforms** – Queried the AFSIM `events` table for `PLATFORM_BROKEN` entries; each row gives the name of the destroyed platform.
4. **Mapping Destroyed Platforms to Units** – For each destroyed platform name, a SPARQL query followed the chain `bs:assignedTo → bs:subordinateTo*` to find the nearest ancestor unit that is a brigade‑level unit.  
   This ensures we count a platform destroyed under any subordinate unit of a brigade.
5. **Counting** – For each top‑level brigade‑level unit, we counted the distinct destroyed platforms that resolved to that unit.

If the interpretation were “platforms directly assigned to the brigade” rather than “all platforms under it”, many of the counts would drop to 0 for units whose aircraft are assigned to subordinate squadrons. The counts above reflect the broader definition that includes all platforms under a brigade’s command chain.

**Judge - missed or wrong:**
- 11th Masurian 1, should be 2 (KRAB34 missed)
- 1st ABCT 7, should be 8 (COBRA13 missed)

<details><summary>Tool calls</summary>

**ontology__ontology_overview**
```
{}
```
**ontology__sparql_query**
```
SELECT ?unit ?label ?coalition WHERE { ?unit a bs:MilitaryUnit ; bs:echelon ?echelon ; rdfs:label ?label ; bs:coalition ?coalition . ?echelon rdfs:label ?echelonLabel . FILTER(?echelonLabel IN ("Brigade","Regiment","Wing")) . }
```
**ontology__sparql_query**
```
SELECT ?unit ?label ?coalition WHERE { ?unit a bs:MilitaryUnit ; bs:echelon ?echelon ; rdfs:label ?label ; bs:coalition ?coalition . FILTER(?echelon IN (bs:Brigade, bs:Regiment, bs:Wing)) . }
```
**ontology__sparql_query**
```
SELECT ?unit ?label WHERE { ?unit a bs:MilitaryUnit ; bs:echelon ?echelon ; rdfs:label ?label ; bs:coalition bs:BlueCoalition . FILTER(?echelon IN (bs:Brigade, bs:Regiment, bs:Wing)) . }
```
**ontology__sparql_query**
```
SELECT ?platform ?name ?unit WHERE { ?platform a bs:Platform ; bs:simPlatformName ?name ; bs:assignedTo ?unit . }
```
**ontology__sparql_query**
```
SELECT ?platform ?name WHERE { ?platform a bs:Platform ; bs:simPlatformName ?name ; bs:assignedTo ?unit . FILTER(?unit IN (bs:unit_FW4, bs:unit_AAMDC10, bs:unit_FAB41, bs:unit_ABCT1, bs:unit_ART11_POL, bs:unit_MOB_Northstar_Unit, bs:unit_ARW22, bs:unit_CAB3, bs:unit_DESRON60, bs:unit_SNMG1_NOR, bs:unit_BW7, bs:unit_FW52, bs:unit_EAW140, bs:unit_WG432, bs:unit_ACW552, bs:unit_FW388)) . }
```
**ontology__sparql_query**
```
SELECT ?platform WHERE { bs:unit_FW4 bs:hasSubordinate ?platform . ?platform a bs:Platform . }
```
**ontology__sparql_query**
```
SELECT ?unit ?platform WHERE { ?unit a bs:MilitaryUnit ; bs:coalition bs:BlueCoalition ; bs:echelon ?e ; FILTER(?e IN (bs:Brigade, bs:Regiment, bs:Wing)). ?unit bs:hasSubordinate ?platform . ?platform a bs:Platform . }
```
**simdb__run_sql**
```
SELECT platform FROM events WHERE event_type='PLATFORM_BROKEN';
```
**ontology__sparql_query**
```
SELECT ?platform ?unit ?name WHERE { VALUES ?name { "SHELL71" "RAPIER3" "RAPIER1" "WEASEL23" "BERKUT06" "SOKOL05" "BERKUT01" "BERKUT02" "BERKUT03" "BERKUT04" "SOKOL02" "LIGHTNING14" "WEASEL22" "SOKOL06" "MAYAK01" "BERKUT05" "SOKOL04" "KOBRA01" "LIGHTNING12" "SOKOL07" "KOBRA02" "KREMEN12" "KREMEN25" "KREMEN13" "BEREZA13" "KRAB31" "BEREZA11" "KAMEN12" "THUNDER22" "LIS42" "YASTREB52" "OPLOT01" "TAIGA11" "TAIGA14" "BEREZA12" "TUNDRA14" "TUNDRA11" "THUNDER24" "TAIGA12" "KREMEN22" "COBRA14" "METEL21" "TROLL12" "KREMEN11" "KREMEN23" "TAIGA13" "TUNDRA12" "COBRA12" "BEREZA15" "KRAB34" "KREMEN10" "TUNDRA13" "KAMEN11" "AB_CHKALOVSK" "YASTREB51" "BEREZA14" "COBRA11" "OSKOL31" "LIS43" "OSKOL32" "IRON13" "COBRA13" "VULKAN13" "BLADE14" "VULKAN14" "VULKAN11" "STRIZH02" "PTITSA02" "VULKAN12" "LIS44" "SERPUKHOV" "METEL22" "MYTISHCHI" } . ?platform a bs:Platform ; bs:simPlatformName ?name ; bs:assignedTo ?unit . }
```
**ontology__sparql_query**
```
SELECT ?platform ?name ?topUnit ?topLabel WHERE { VALUES ?name { "SHELL71" "RAPIER3" "RAPIER1" "WEASEL23" "LIGHTNING14" "WEASEL22" "LIGHTNING12" "KRAB31" "THUNDER22" "THUNDER24" "COBRA14" "COBRA12" "COBRA11" "IRON13" "BLADE14" } . ?platform a bs:Platform ; bs:simPlatformName ?name ; bs:assignedTo ?unit . ?unit bs:subordinateTo* ?topUnit . ?topUnit a bs:MilitaryUnit ; bs:echelon ?e . FILTER(?e IN (bs:Brigade, bs:Regiment, bs:Wing)) . OPTIONAL { ?topUnit rdfs:label ?topLabel } . }
```
</details>

## q5: Air defense mission capability at a point in time

**Question.** At T+90 minutes (time_s = 5400), which of Red's surface-to-air missile battalions were still able to engage? A battalion built from separate launchers, radars and command posts can engage only if it still has at least one operational engagement radar, one operational command post, and one operational launcher; a battalion of self-contained SHORAD vehicles can engage if any vehicle is operational.

**Why the ontology matters.** Needs system composition (which radar/CP/launchers form which battalion) and component roles (engagement vs surveillance radar), both from the ontology, joined to time-sliced status data.

**Ground truth.** Red SAM battalions at T+90 min: 1st Buk Battalion, 53 ZRBR: NOT capable (no operational EngagementRadar) [lost so far: BEREZA11, BEREZA13]; 1st S-400 Battalion, 1544 ZRP: NOT capable (no operational EngagementRadar) [lost so far: KREMEN12, KREMEN13]; 2nd S-400 Battalion, 1544 ZRP: MISSION-CAPABLE [lost so far: KREMEN25]; Air Defence Battalion, 7 MRR (Tor): MISSION-CAPABLE [lost so far: YASTREB52]

### ontology OFF - score 0/100

20 tool calls, 21 turns, 130.4 s, 4,638 input / 6,764 output tokens

**Headline:** At T + 90 min (time_s = 5 400) Red fielded **two surface‑to‑air missile battalions that were still able to engage** – the **BEREZA** and **KAMEN** battalions.  

| Battalion | Operational launchers | Operational radars | Operational command posts | Other components |
|-----------|-----------------------|--------------------|---------------------------|------------------|
| **BEREZA** | 1 (BEREZA14) | 1 (BEREZA10) | 1 (KREMEN20) | 1 launcher damaged (BEREZA13), 1 radar broken (BEREZA11), 1 launcher damaged (BEREZA15) |
| **KAMEN** | 1 (KAMEN11) | 1 (SHTORM02) | 1 (KREMEN20) | 1 launcher broken (KAMEN12) |
| **METEL** | 0 (both launchers damaged) | – | – | – |
| **YASTREB** | 0 (one launcher damaged, one broken) | – | – | – |
| **SHTORM** | – | 1 active (SHTORM02) | – | – |

**Evidence (SQL queries)**  

*BEREZA components*  
- Launchers active:  
  `SELECT COUNT(*) FROM platform_status WHERE time_s=5400 AND platform IN ('BEREZA13','BEREZA14','BEREZA15') AND state='ACTIVE';` → 1  
- Radars active:  
  `SELECT COUNT(*) FROM platform_status WHERE time_s=5400 AND platform IN ('BEREZA10','BEREZA11','BEREZA12') AND state='ACTIVE';` → 1  
- Command posts active:  
  `SELECT COUNT(*) FROM platform_status WHERE time_s=5400 AND platform IN ('KREMEN10','KREMEN20') AND state='ACTIVE';` → 1  

*KAMEN components*  
- Launchers active:  
  `SELECT COUNT(*) FROM platform_status WHERE time_s=5400 AND platform IN ('KAMEN11','KAMEN12') AND state='ACTIVE';` → 1  
- Radars active:  
  `SELECT COUNT(*) FROM platform_status WHERE time_s=5400 AND platform IN ('SHTORM01','SHTORM02') AND state='ACTIVE';` → 1  
- Command posts active:  
  `SELECT COUNT(*) FROM platform_status WHERE time_s=5400 AND platform IN ('KREMEN10','KREMEN20') AND state='ACTIVE';` → 1  

All other Red SAM groups lacked at least one operational component (launcher or radar), so they could not engage at that time.

**Assumptions & Uncertainties**  
- *Command‑post assignment*: The database does not explicitly link a command post to a specific battalion. We assumed any operational command post can serve any battalion, which is why KREMEN20 (ACTIVE) satisfies the requirement for both BEREZA and KAMEN. If command posts are actually battalion‑specific, the result for KAMEN would change.  
- *Radar identification*: We inferred radars from platform types that are not launchers or command posts (e.g., 9S18M1, 9S36M, 9S510M, 5P85TE2_TEL). If any of those types were actually non‑radar, the counts would adjust.  
- *SHORAD vehicles*: No Red M‑SHORAD_INC1 platforms were present, so the SHORAD vehicle condition is moot.  

Under the above interpretations, BEREZA and KAMEN were the only Red SAM battalions capable of engaging at T + 90 min.

**Judge - missed or wrong:**
- BEREZA (Buk) and KAMEN (ATGM) judged capable
- 2nd S-400 and Tor not identified

<details><summary>Tool calls</summary>

**simdb__describe_database**
```
{}
```
**simdb__run_sql**
```
SELECT name,type,side FROM platforms WHERE side='red' AND type LIKE '9%' ORDER BY type, name;
```
**simdb__run_sql**
```
SELECT name,type,side FROM platforms WHERE side='red' AND type LIKE '%SAM%' OR type LIKE '%TELAR%' OR type LIKE '%RADAR%' OR type LIKE '%CP%' ORDER BY type, name;
```
**simdb__run_sql**
```
SELECT name,type FROM platforms WHERE side='red' ORDER BY name;
```
**simdb__run_sql**
```
SELECT type, COUNT(*) FROM platforms WHERE type='5P85TE2_TEL' GROUP BY type;
```
**simdb__run_sql**
```
SELECT type, COUNT(*) FROM platforms WHERE type='55ZH6M_NEBO-M' GROUP BY type;
```
**simdb__run_sql**
```
SELECT platform, state FROM platform_status WHERE time_s=5400 AND platform IN ('BEREZA10','BEREZA11','BEREZA12','BEREZA13','BEREZA14','BEREZA15') ORDER BY platform;
```
**simdb__run_sql**
```
SELECT platform, state FROM platform_status WHERE time_s=5400 AND platform IN ('KREMEN10','KREMEN20') ORDER BY platform;
```
**simdb__run_sql**
```
SELECT platform, state FROM platform_status WHERE time_s=5400 AND platform IN ('METEL21','METEL22') ORDER BY platform;
```
**simdb__run_sql**
```
SELECT platform, state FROM platform_status WHERE time_s=5400 AND platform IN ('YASTREB51','YASTREB52') ORDER BY platform;
```
**simdb__run_sql**
```
SELECT platform, state FROM platform_status WHERE time_s=5400 AND platform IN ('KAMEN11','KAMEN12') ORDER BY platform;
```
**simdb__run_sql**
```
SELECT platform, state FROM platform_status WHERE time_s=5400 AND platform IN ('SHTORM01','SHTORM02') ORDER BY platform;
```
**simdb__run_sql**
```
SELECT name,type FROM platforms WHERE side='red' AND type='M-SHORAD_INC1' ORDER BY name;
```
**simdb__run_sql**
```
SELECT platform, state FROM platform_status WHERE time_s=5400 AND platform LIKE 'KREMEN%' ORDER BY platform;
```
**simdb__run_sql**
```
SELECT COUNT(*) AS cnt FROM platform_status WHERE time_s=5400 AND platform IN ('BEREZA13','BEREZA14','BEREZA15') AND state='ACTIVE';
```
**simdb__run_sql**
```
SELECT COUNT(*) AS cnt FROM platform_status WHERE time_s=5400 AND platform IN ('BEREZA10','BEREZA11','BEREZA12') AND state='ACTIVE';
```
**simdb__run_sql**
```
SELECT COUNT(*) AS cnt FROM platform_status WHERE time_s=5400 AND platform IN ('KREMEN10','KREMEN20') AND state='ACTIVE';
```
**simdb__run_sql**
```
SELECT COUNT(*) AS cnt FROM platform_status WHERE time_s=5400 AND platform IN ('KAMEN11','KAMEN12') AND state='ACTIVE';
```
**simdb__run_sql**
```
SELECT COUNT(*) AS cnt FROM platform_status WHERE time_s=5400 AND platform IN ('SHTORM01','SHTORM02') AND state='ACTIVE';
```
**simdb__run_sql**
```
SELECT COUNT(*) AS cnt FROM platform_status WHERE time_s=5400 AND platform IN ('KREMEN10','KREMEN20') AND state='ACTIVE';
```
</details>

### ontology ON - score 75/100

29 tool calls, 30 turns, 158.5 s, 9,303 input / 7,584 output tokens

**Headline**  
At T + 90 min (time = 5400 s) only **one** of Red’s SAM battalions remains mission‑capable – **unit_ZRP1544_2**.  

**Breakdown**

| Battalion | Type | Operational components at 5400 s | Engagement‑capable? |
|-----------|------|----------------------------------|----------------------|
| **unit_ZRP1544_2** | Integrated SAM | • **KREMEN14** (5P85TE2_TEL – launcher, ACTIVE)  <br>• **KREMEN15** (5P85TE2_TEL – launcher, ACTIVE) <br>• **KREMEN20** (55K6E_CP – command post, ACTIVE) <br>• **KREMEN24** (92N6E_GRAVE_STONE – engagement radar, ACTIVE) <br>• **KREMEN26** (5P85TE2_TEL – launcher, ACTIVE) | **Yes** – has at least one ACTIVE launcher, one ACTIVE command post, and one ACTIVE radar. |
| unit_ZRP1544_1 | Integrated SAM | • KREMEN14 (ACTIVE launcher) <br>• KREMEN15 (ACTIVE launcher) | **No** – lacks an ACTIVE command post (KREMEN10 was DAMAGED) and an ACTIVE radar (KREMEN12 BROKEN, KREMEN13 BROKEN). |
| unit_ZRBR53_1 | Integrated SAM | • BEREZA14 (ACTIVE launcher) | **No** – no ACTIVE radar (BEREZA11 BROKEN, BEREZA13 BROKEN) and no ACTIVE command post (BEREZA12 DAMAGED). |
| unit_MRR7_AD | SHORAD | • YASTREB51 (DAMAGED) <br>• YASTREB52 (BROKEN) | **No** – no operational SHORADSystem. |

**Assumptions & Uncertainties**

* “Operational” is interpreted strictly as **ACTIVE** state in `platform_status`. DAMAGED platforms are considered degraded and not mission‑capable.  
* The mapping between AFSIM `platforms.type` strings and ontology classes was obtained via the `bs:simulationType/bs:simTypeName` path. No other types were present for these battalions.  
* The battalion‑to‑platform assignment comes from the ontology property `bs:assignedTo`. All queried platforms were verified to belong to the corresponding battalion.  

Thus, at the requested time, only Red’s **unit_ZRP1544_2** can still engage.

**Judge - missed or wrong:**
- Tor judged not capable: counted only ACTIVE as operational despite the DAMAGED note

<details><summary>Tool calls</summary>

**simdb__describe_database**
```
{"max_rows": 20}
```
**ontology__find_terms**
```
SAM battalion
```
**ontology__sparql_query**
```
PREFIX bs: <http://example.org/bs#>
SELECT ?unit ?coalition WHERE {
  ?unit a bs:SAMBattalion .
  ?unit bs:hasCoalition ?coalition .
}
```
**ontology__sparql_query**
```
PREFIX bs: <http://example.org/bs#>
SELECT ?unit ?side WHERE {
  ?unit a bs:SAMBattalion .
  ?unit bs:side ?side .
}
```
**ontology__sparql_query**
```
PREFIX bs: <http://example.org/battlespace#>
SELECT ?c WHERE { ?c a bs:Coalition . }
```
**ontology__sparql_query**
```
PREFIX bs: <http://example.org/battlespace#>
SELECT ?unit ?coalition WHERE {
  ?unit a bs:SAMBattalion .
  ?unit bs:coalition ?coalition .
}
```
**ontology__sparql_query**
```
PREFIX bs: <http://example.org/battlespace#>
SELECT ?unit ?type WHERE {
  ?unit a bs:IntegratedSAMBattalion .
  BIND("Integrated" AS ?type)
}
UNION
{ SELECT ?unit "SHORAD" AS ?type WHERE { ?unit a bs:SHORADBattalion . }
```
**ontology__sparql_query**
```
PREFIX bs: <http://example.org/battlespace#>
SELECT ?unit "Integrated" AS ?type WHERE { ?unit a bs:IntegratedSAMBattalion . }
```
**ontology__sparql_query**
```
PREFIX bs: <http://example.org/battlespace#>
SELECT ?unit WHERE { ?unit a bs:IntegratedSAMBattalion . }
```
**ontology__sparql_query**
```
PREFIX bs: <http://example.org/battlespace#>
SELECT ?unit WHERE { ?unit a bs:SHORADBattalion . }
```
**ontology__sparql_query**
```
PREFIX bs: <http://example.org/battlespace#>
SELECT ?typeName ?class WHERE {
  ?t a bs:SimulationType ; bs:simTypeName ?typeName .
  ?t a ?class .
  FILTER(?class IN (bs:EngagementRadar, bs:AirDefenseCommandPost, bs:SAMLauncher, bs:SHORADSystem))
}
```
**ontology__sparql_query**
```
PREFIX bs: <http://example.org/battlespace#>
SELECT ?platName ?unit WHERE {
  ?p a bs:SimulationPlatform .
  ?p bs:simPlatformName ?platName .
  ?p bs:assignedTo ?unit .
}
```
**ontology__sparql_query**
```
PREFIX bs: <http://example.org/battlespace#>
SELECT ?platform ?unit WHERE {
  ?platform bs:assignedTo ?unit .
}
```
**ontology__sparql_query**
```
PREFIX bs: <http://example.org/battlespace#>
SELECT ?unit ?platName ?typeName WHERE {
  ?p bs:assignedTo ?unit ;
     bs:simPlatformName ?platName ;
     bs:simTypeName ?typeName .
  FILTER(?unit IN (bs:unit_ZRP1544_2, bs:unit_ZRP1544_1, bs:unit_ZRBR53_1, bs:unit_MRR7_AD))
}
```
**ontology__sparql_query**
```
PREFIX bs: <http://example.org/battlespace#>
SELECT ?p ?simType ?typeName WHERE {
  ?p bs:simPlatformName "bs:plat_BEREZA10" .
  ?p bs:simulationType ?simType .
  ?simType bs:simTypeName ?typeName .
}
```
**ontology__find_terms**
```
simType
```
**ontology__sparql_query**
```
PREFIX bs: <http://example.org/battlespace#>
SELECT ?p ?typeName WHERE {
  ?p bs:simPlatformName "bs:plat_BEREZA10" .
  ?p bs:simulationType ?sim .
  ?sim bs:simTypeName ?typeName .
}
```
**ontology__sparql_query**
```
PREFIX bs: <http://example.org/battlespace#>
SELECT ?p ?typeName WHERE {
  ?p bs:simPlatformName "plat_BEREZA10" .
  ?p bs:simulationType ?sim .
  ?sim bs:simTypeName ?typeName .
}
```
**ontology__find_terms**
```
simPlatformName
```
**ontology__sparql_query**
```
PREFIX bs: <http://example.org/battlespace#>
SELECT ?p ?o WHERE {
  bs:plat_BEREZA10 ?p ?o .
}
```
**ontology__sparql_query**
```
PREFIX bs: <http://example.org/battlespace#>
SELECT ?typeName WHERE {
  bs:simtype_9S18M1 bs:simTypeName ?typeName .
}
```
**ontology__sparql_query**
```
PREFIX bs: <http://example.org/battlespace#>
SELECT ?simType ?typeName ?class WHERE {
  ?simType bs:simTypeName ?typeName .
  ?simType a ?class .
  FILTER(?class IN (bs:EngagementRadar, bs:AirDefenseCommandPost, bs:SAMLauncher, bs:SHORADSystem))
}
```
**ontology__sparql_query**
```
PREFIX bs: <http://example.org/battlespace#>
SELECT ?unit ?plat ?typeName ?class WHERE {
  ?p bs:assignedTo ?unit ;
     bs:simulationType ?sim .
  ?sim bs:simTypeName ?typeName .
  ?sim a ?class .
  FILTER(?class IN (bs:EngagementRadar, bs:AirDefenseCommandPost, bs:SAMLauncher, bs:SHORADSystem))
  FILTER(?unit IN (bs:unit_ZRP1544_2, bs:unit_ZRP1544_1, bs:unit_ZRBR53_1, bs:unit_MRR7_AD))
  BIND(REPLACE(STR(?p),".*#","") AS ?plat)
} ORDER BY ?unit
```
**simdb__run_sql**
```
SELECT platform, state FROM platform_status WHERE time_s = 5400 AND platform IN ('plat_YASTREB51','plat_YASTREB52','plat_BEREZA11','plat_BEREZA12','plat_BEREZA13','plat_BEREZA14','plat_BEREZA15','plat_KREMEN10','plat_KREMEN12','plat_KREMEN13','plat_KREMEN14','plat_KREMEN15','plat_KREMEN16','plat_KREMEN20','plat_KREMEN22','plat_KREMEN23','plat_KREMEN24','plat_KREMEN25','plat_KREMEN26');
```
**simdb__describe_database**
```
{"max_rows": 20}
```
**simdb__run_sql**
```
SELECT name FROM platforms LIMIT 10;
```
**simdb__run_sql**
```
SELECT name FROM platforms WHERE name LIKE '%YASTREB%';
```
**simdb__run_sql**
```
SELECT name, state FROM platform_status WHERE time_s = 5400 AND name IN ('YASTREB51','YASTREB52','BEREZA11','BEREZA12','BEREZA13','BEREZA14','BEREZA15','KREMEN10','KREMEN12','KREMEN13','KREMEN14','KREMEN15','KREMEN16','KREMEN20','KREMEN22','KREMEN23','KREMEN24','KREMEN25','KREMEN26');
```
**simdb__run_sql**
```
SELECT platform, state FROM platform_status WHERE time_s = 5400 AND platform IN ('YASTREB51','YASTREB52','BEREZA11','BEREZA12','BEREZA13','BEREZA14','BEREZA15','KREMEN10','KREMEN12','KREMEN13','KREMEN14','KREMEN15','KREMEN16','KREMEN20','KREMEN22','KREMEN23','KREMEN24','KREMEN25','KREMEN26');
```
</details>

## q6: Coalition partner losses

**Question.** How many platforms belonging to Blue coalition partners other than the United States were destroyed? Break it down by nation, and say what category of Red weapon destroyed each one.

**Why the ontology matters.** Side 'blue' in the sim lumps all coalition members together. Nationality comes from the unit hierarchy in the ontology, and the weapon category from the munition hierarchy.

**Ground truth.** Non-US Blue coalition platforms destroyed: 5 - by nation: Norway 1, Poland 2, United Kingdom 2. Details: TROLL12 (Norway) killed by 9M542 [guided artillery rocket] from METEL22 at t=6146s; KRAB31 (Poland) killed by 9M55K [artillery rocket (cluster)] from METEL21 at t=4427s; KRAB34 (Poland) killed by 9M55K [artillery rocket (cluster)] from METEL22 at t=6832s; RAPIER1 (United Kingdom) killed by R-73M [air-to-air missile] from SOKOL07 at t=1885s; RAPIER3 (United Kingdom) killed by 48N6E3 [surface-to-air missile] from KREMEN25 at t=1181s

### ontology OFF - score 5/100

9 tool calls, 10 turns, 96.1 s, 3,224 input / 5,063 output tokens

**Headline**  
*4 Blue‑coalition platforms outside the United States were destroyed.*

---

### Breakdown by nation (and the Red weapon that killed each)

| Platform (callsign) | Nation (Blue partner) | Red weapon type | Weapon category (background‑knowledge inference) |
|---------------------|------------------------|-----------------|----------------------------------------------|
| **RAPIER3** | Germany | 48N6E3 | **Anti‑ship missile** (surface‑to‑surface) |
| **RAPIER1** | Germany | R‑73M | **Air‑to‑air missile** |
| **KRAB31** | Ukraine | 9M55K | **Air‑to‑surface missile** |
| **KRAB34** | Ukraine | 9M55K | **Air‑to‑surface missile** |

*Totals:*  
- Germany: 2 destroyed (RAPIER1, RAPIER3)  
- Ukraine: 2 destroyed (KRAB31, KRAB34)

---

### Notes & Assumptions

1. **Platform nation** – The simulation does not include an explicit nation field.  
   *   “EF2000_FGR4” (RAPIER1/3) is identified as German by the platform name “RAPIER”.  
   *   “AHS_KRAB” (KRAB31/34) is classified as Ukrainian because the Krab self‑propelled howitzer is operated by Ukraine in this scenario.  
   *   No other Blue‑coalition partner types were destroyed in the run.  
2. **Weapon category** – Weapon types in the event log have no categorical label; the categories listed above are derived from standard military knowledge (e.g., 48N6E3 is an anti‑ship missile, R‑73M is an air‑to‑air missile, 9M55K is an air‑to‑surface missile).  
3. **Data source** – All counts and associations come from the `events` table (`event_type='PLATFORM_BROKEN'`, `side='blue'`) joined with the `platforms` table to filter by platform type. No other platform types in the dataset were destroyed aside from the US‑equipped ones.

**Judge - missed or wrong:**
- UK guessed as Germany, Poland as Ukraine
- Norway missed
- Categories wrong (48N6E3 called anti-ship, 9M55K air-to-surface)

<details><summary>Tool calls</summary>

**simdb__describe_database**
```
{"input": ""}
```
**simdb__run_sql**
```
SELECT DISTINCT type FROM platforms WHERE side='blue';
```
**simdb__run_sql**
```
SELECT name, type FROM platforms WHERE side='blue' AND type='EF2000_FGR4' LIMIT 10;
```
**simdb__run_sql**
```
SELECT name, type FROM platforms WHERE side='blue' AND type='AHS_KRAB' LIMIT 10;
```
**simdb__run_sql**
```
SELECT name, type FROM platforms WHERE side='blue' AND type='NANSEN_CLASS_FFG' LIMIT 10;
```
**simdb__run_sql**
```
SELECT name, type FROM platforms WHERE side='blue' AND type='M-SHORAD_INC1' LIMIT 10;
```
**simdb__run_sql**
```
SELECT e.platform, p.type FROM events e JOIN platforms p ON e.platform=p.name WHERE e.event_type='PLATFORM_BROKEN' AND e.side='blue' AND p.type IN ('EF2000_FGR4','AHS_KRAB','NANSEN_CLASS_FFG','M-SHORAD_INC1');
```
**simdb__run_sql**
```
SELECT e.platform, e.weapon_type, e.result, e.details FROM events e WHERE e.event_type='PLATFORM_BROKEN' AND e.side='blue' AND e.platform IN ('RAPIER3','RAPIER1','KRAB31','KRAB34');
```
**simdb__run_sql**
```
SELECT e.platform, p.type FROM events e JOIN platforms p ON e.platform=p.name WHERE e.event_type='PLATFORM_BROKEN' AND e.side='blue' LIMIT 100;
```
</details>

### ontology ON - score 100/100

22 tool calls, 23 turns, 228.0 s, 10,865 input / 11,189 output tokens

**Headline number**  
- **5 Blue‑coalition platforms (excluding the United States) were destroyed.**

**Breakdown by nation & weapon category**

| Nation | Destroyed platform | Red‑weapon category that killed it |
|--------|--------------------|-----------------------------------|
| **Poland** | KRAB31 | Cluster munition (9 M55K) |
|  | KRAB34 | Cluster munition (9 M55K) |
| **United Kingdom** | RAPIER1 | Air‑to‑air missile (R‑73M) |
|  | RAPIER3 | Surface‑to‑air missile (48 N6E3) |
| **Norway** | TROLL12 | Guided rocket (9 M542) |

**Methodology & sources**

1. **Destroyed events** – Queried the AFSIM SQLite `events` table for rows where `event_type='PLATFORM_BROKEN'` and `side='blue'`.  
2. **Platform‑nation mapping** – Queried the battlespace ontology for each platform’s `bs:simPlatformName` and the `bs:nation` label of the unit to which it is assigned.  
3. **Filtering** – Excluded platforms belonging to the United States and Redland (the Red coalition). The remaining 5 platforms were the ones listed above.  
4. **Weapon category** – For each `weapon_type` in the broken‑platform events, the ontology was queried for the class labels of the corresponding `bs:SimulationType` individual. The most specific subclass of `bs:Weapon` was used as the weapon category (e.g., “Cluster munition”, “Air‑to‑air missile”, “Surface‑to‑air missile”, “Guided rocket”).  
5. **Cross‑check** – Confirmed that the sum of individual counts (2 + 2 + 1) equals the total number of destroyed platforms (5).

**Assumptions & uncertainties**

- Classification of weapons was based strictly on ontology class labels; no additional background knowledge was applied.  
- The mapping assumes that the ontology’s class hierarchy correctly reflects weapon categories for the simulation’s munition types.  
- No other Blue‑coalition platforms outside the 5 listed were destroyed in the simulation.

<details><summary>Tool calls</summary>

**simdb__run_sql**
```
SELECT e.platform AS destroyed_platform, e.weapon_type AS killer_weapon, e.details, e.side AS destroyed_side FROM events e WHERE e.event_type = 'PLATFORM_BROKEN' AND e.side = 'Blue';
```
**simdb__describe_database**
```
{}
```
**simdb__run_sql**
```
SELECT event_id, platform, side, weapon_type FROM events WHERE event_type='PLATFORM_BROKEN' AND side='blue';
```
**ontology__sparql_query**
```
PREFIX bs: <http://example.com/bs#> 
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
SELECT ?platformName ?nationLabel WHERE {
  ?platform a bs:SimulationPlatform .
  ?platform bs:simPlatformName ?platformName .
  ?platform bs:assignedTo ?unit .
  ?unit bs:nation ?nation .
  ?nation rdfs:label ?nationLabel .
}
```
**ontology__ontology_overview**
```
{}
```
**ontology__sparql_query**
```
SELECT ?p ?type WHERE {
  ?p bs:simPlatformName ?name .
  ?p a ?type .
  FILTER(?type != bs:Platform) .
  FILTER(?type != bs:SimulationPlatform) .
} LIMIT 10
```
**ontology__sparql_query**
```
SELECT ?platformName ?nationLabel WHERE {
  ?platform bs:simPlatformName ?platformName .
  ?platform bs:assignedTo ?unit .
  ?unit bs:nation ?nation .
  ?nation rdfs:label ?nationLabel .
}
```
**ontology__sparql_query**
```
SELECT DISTINCT ?nationLabel WHERE {
  ?platform bs:simPlatformName ?name .
  ?platform bs:assignedTo ?unit .
  ?unit bs:nation ?nation .
  ?nation rdfs:label ?nationLabel .
}
```
**ontology__sparql_query**
```
SELECT ?platformName ?nationLabel WHERE {
  ?platform bs:simPlatformName ?platformName .
  ?platform bs:assignedTo ?unit .
  ?unit bs:nation ?nation .
  ?nation rdfs:label ?nationLabel .
  FILTER(?platformName IN ("SHELL71","RAPIER3","RAPIER1","WEASEL23","LIGHTNING14","WEASEL22","LIGHTNING12","KRAB31","THUNDER22","THUNDER24","COBRA14","TROLL12","COBRA12","KRAB34","COBRA11","IRON13","COBRA13","BLADE14"))
}
```
**ontology__sparql_query**
```
SELECT ?simName ?clsLabel WHERE {
  ?type a bs:SimulationType .
  ?type bs:simTypeName ?simName .
  FILTER(?simName IN ("IZDELIYE_610M","48N6E3","R-73M","R-77-1","9M317M","9M542","9M55K","VORON-K","9M127-1","S-8KOM")) .
  ?type a ?cls .
  ?cls rdfs:subClassOf+ bs:Weapon .
  ?cls rdfs:label ?clsLabel .
}
```
**ontology__sparql_query**
```
SELECT ?type ?label ?cls ?clsLabel WHERE {
  ?type a bs:SimulationType .
  ?type bs:simTypeName "R-73M" .
  ?type a ?cls .
  ?cls rdfs:label ?clsLabel .
}
```
**ontology__sparql_query**
```
SELECT ?type ?clsLabel WHERE {
  ?type a bs:SimulationType .
  ?type bs:simTypeName "R-73M" .
  ?type a ?cls .
  ?cls rdfs:subClassOf+ bs:Weapon .
  ?cls rdfs:label ?clsLabel .
  FILTER NOT EXISTS {
    ?cls2 a ?cls .
    ?cls2 rdfs:subClassOf+ bs:Weapon .
    FILTER(?cls2 != ?cls)
  }
}
```
**ontology__sparql_query**
```
SELECT ?type ?clsLabel WHERE {
  ?type a bs:SimulationType .
  ?type bs:simTypeName "R-73M" .
  ?type a ?cls .
  ?cls rdfs:subClassOf+ bs:Weapon .
  ?cls rdfs:label ?clsLabel .
  FILTER NOT EXISTS {
    ?cls rdfs:subClassOf ?other .
    ?other rdfs:subClassOf+ bs:Weapon .
  }
}
```
**ontology__sparql_query**
```
SELECT ?type ?clsLabel WHERE {
  ?type a bs:SimulationType .
  ?type bs:simTypeName "IZDELIYE_610M" .
  ?type a ?cls .
  ?cls rdfs:label ?clsLabel .
}
```
**ontology__sparql_query**
```
SELECT ?type ?clsLabel WHERE {
  ?type a bs:SimulationType .
  ?type bs:simTypeName "48N6E3" .
  ?type a ?cls .
  ?cls rdfs:label ?clsLabel .
}
```
**ontology__sparql_query**
```
SELECT ?type ?clsLabel WHERE {
  ?type a bs:SimulationType .
  ?type bs:simTypeName "R-77-1" .
  ?type a ?cls .
  ?cls rdfs:label ?clsLabel .
}
```
**ontology__sparql_query**
```
SELECT ?type ?clsLabel WHERE {
  ?type a bs:SimulationType .
  ?type bs:simTypeName "9M317M" .
  ?type a ?cls .
  ?cls rdfs:label ?clsLabel .
}
```
**ontology__sparql_query**
```
SELECT ?type ?clsLabel WHERE {
  ?type a bs:SimulationType .
  ?type bs:simTypeName "9M542" .
  ?type a ?cls .
  ?cls rdfs:label ?clsLabel .
}
```
**ontology__sparql_query**
```
SELECT ?type ?clsLabel WHERE {
  ?type a bs:SimulationType .
  ?type bs:simTypeName "9M55K" .
  ?type a ?cls .
  ?cls rdfs:label ?clsLabel .
}
```
**ontology__sparql_query**
```
SELECT ?type ?clsLabel WHERE {
  ?type a bs:SimulationType .
  ?type bs:simTypeName "VORON-K" .
  ?type a ?cls .
  ?cls rdfs:label ?clsLabel .
}
```
**ontology__sparql_query**
```
SELECT ?type ?clsLabel WHERE {
  ?type a bs:SimulationType .
  ?type bs:simTypeName "9M127-1" .
  ?type a ?cls .
  ?cls rdfs:label ?clsLabel .
}
```
**ontology__sparql_query**
```
SELECT ?type ?clsLabel WHERE {
  ?type a bs:SimulationType .
  ?type bs:simTypeName "S-8KOM" .
  ?type a ?cls .
  ?cls rdfs:label ?clsLabel .
}
```
</details>
