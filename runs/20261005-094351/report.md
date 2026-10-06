# Ontology vs. no-ontology agent comparison

Model: `qwen3:30b` - 2026-10-05 09:48

## Run statistics

| Question | Mode | Agent time | Model time | Tool time | Turns | Tool calls | Slowest tool call | Output tokens | Score |
|---|---|---|---|---|---|---|---|---|---|
| q3 | ontology OFF | 2m17s | 2m16s | 0m00s | 3 | 2 | 0.2s | 3,752 | 0 |
| q3 | ontology ON | 1m56s | 1m51s | 0m04s | 4 | 3 | 3.3s | 3,242 | 100 |

| Mode | Questions | Total agent time | Mean | Min | Max | Mean per turn | Mean score | Errors |
|---|---|---|---|---|---|---|---|---|
| ontology OFF | 1 | 2m17s | 2m17s | 2m17s | 2m17s | 45s | 0 | 0 |
| ontology ON | 1 | 1m56s | 1m56s | 1m56s | 1m56s | 28s | 100 | 0 |

| Question | Wall time (both modes + judge) | Judge time |
|---|---|---|
| q3 | 4m14s | 0m00s |

**Total run time:** 4m14s

| Question | Ontology OFF | Ontology ON |
|---|---|---|
| q3: Cluster munition employment | 0 (incorrect) | 100 (correct) |

## q3: Cluster munition employment

**Question.** Which cluster (submunition-dispensing) munitions were employed during the engagement? For each, give the weapon type, the side that used it, and the number of rounds fired.

**Why the ontology matters.** Requires warhead knowledge: MGM-140B is ATACMS Block IA (APAM submunitions), BURYA-12 is notional, while M30A2 (GMLRS Alternative Warhead) looks like the old DPICM rocket but has no submunitions.

**Ground truth.** Cluster munitions fired: total 53 rounds - MGM-140B (MGM-140B ATACMS Block IA) by blue: 3; 3O23 (3-O-23 152 mm cargo projectile (ICM)) by red: 14; 9M55K (9M55K 300 mm cargo rocket) by red: 24; BURYA-12 (Burya-12 cargo rocket (notional)) by red: 12. Not cluster: M30A2 GMLRS-AW (pre-formed fragments, replaced the DPICM M30), M31A2 (unitary).

### ontology OFF - score 0/100

2 tool calls, 3 turns, 137.0 s, 5,647 input / 3,752 output tokens

Headline: 1 cluster munition type employed by red side (48 rounds fired).  
Breakdown:  
- Weapon type: S-8KOM (S-8 cluster rocket)  
- Side: red  
- Rounds fired: 48  

Assumptions:  
- S-8KOM is classified as a cluster munition based on the "KOM" suffix (Russian for "cluster" / kasseta), consistent with S-8 rocket family variants.  
- No other weapon types in the dataset (e.g., GERAN-2, GBU series) match the criteria for submunition-dispensing cluster munitions.  
- All 48 instances of S-8KOM were fired by the red side (verified via SQL count).

**Judge - missed or wrong:**
- S-8KOM wrongly classed as a cluster munition from its 'KOM' suffix
- All four true cluster munitions missed (MGM-140B, 3O23, 9M55K, BURYA-12)
- Total 48, should be 53

<details><summary>Tool calls</summary>

**simdb__describe_database**
```
{}
```
**simdb__run_sql**
```
SELECT side, COUNT(*) AS count FROM events WHERE event_type = 'WEAPON_FIRED' AND weapon_type = 'S-8KOM' GROUP BY side
```
</details>

### ontology ON - score 100/100

3 tool calls, 4 turns, 116.4 s, 6,896 input / 3,242 output tokens

Headline: 53 cluster munitions employed (14 red, 24 red, 12 red, 3 blue).  
Breakdown:  
- 3O23 (Red): 14 rounds  
- 9M55K (Red): 24 rounds  
- BURYA-12 (Red): 12 rounds  
- MGM-140B (Blue): 3 rounds  
Assumptions: RBK-500_SPBE was classified as a cluster munition by ontology but had zero WEAPON_FIRED events (confirmed via SQL count). All weapon types matched exactly to ontology-specified `simTypeName` values.

<details><summary>Tool calls</summary>

**ontology__ontology_overview**
```
{}
```
**ontology__sparql_query**
```
SELECT ?name WHERE { ?t a bs:SimulationType ; bs:warheadType bs:Submunitions ; bs:simTypeName ?name }
```
**simdb__run_sql**
```
SELECT e.weapon_type, p.side, COUNT(*) AS count FROM events e JOIN platforms p ON e.platform = p.name WHERE e.event_type = 'WEAPON_FIRED' AND e.weapon_type IN ('MGM-140B', '3O23', 'RBK-500_SPBE', 'BURYA-12', '9M55K') GROUP BY e.weapon_type, p.side
```
</details>
