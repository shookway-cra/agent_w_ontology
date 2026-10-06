# Results: does an ontology layer help an AI agent analyse simulation output?

**Short answer: yes, by a wide margin.** Over three runs of seven questions on an AFSIM-style simulation run, a local open-weight model (`gpt-oss:20b`) averaged **84/100 with the ontology attached and 23/100 without it**. The gap held in every run (92, 79 and 81 against 24, 23 and 22).

The ontology wins on exactly the questions it was designed for: classifying weapons, rolling losses up a chain of command, identifying nationality, and determining unit function. On those questions the agent without it can only guess from names, and it guesses wrong.

| | Ontology OFF | Ontology ON |
|---|---|---|
| Mean score, 3 runs × 7 questions | **23** | **84** |
| Answers fully correct (100) | 3 of 21 (all the control question) | 12 of 21 |
| Answers scoring 0 | 6 of 21 | 1 of 21 |

## 1. The experiment

### The question being tested

Simulation output such as AFSIM's records *what happened*: platform callsigns, type strings, sides, and events like "fired", "hit" and "destroyed". It doesn't record *what things are*:
- that `WPN_KESTREL` is an air-to-air missile;
- that `KRAB31` belongs to a Polish artillery regiment;
- that a 9S18M1 is a surveillance radar rather than an engagement radar.

Analysts carry that knowledge in their heads. The experiment asks whether putting it into an ontology, and letting an AI agent query it, produces better answers than letting the agent rely on its own background knowledge.

### Setup

The same agent answers each question twice. The only difference between the two runs is whether the ontology is attached.

| | Ontology OFF | Ontology ON |
|---|---|---|
| Model, system prompt, agent loop | identical | identical |
| Simulation database tool (`simdb`: read-only SQL) | ✅ | ✅ |
| Ontology tool (`ontology`: SPARQL, term search, overview) | ❌ | ✅ |

**Simulation data:** `data/afsim_run.sqlite` is a synthetic, AFSIM-style output of a 4-hour scenario ("BALTIC SHIELD", Blue coalition against Red).

| Table | Rows | Contents |
|---|---|---|
| `platforms` | 168 | Callsign, AFSIM type string and side for each platform |
| `events` | 2,489 | Weapon fired, hit, missed, platform destroyed, ... |
| `platform_status` | 40,488 | State snapshots every 60 s: ACTIVE, DAMAGED or BROKEN |
| `weapon_inventory` | 9,000 | Weapon quantities per platform every 600 s |

**Ontology:** `ontology/*.ttl`, OWL, about 3,400 asserted triples.
- `battlespace.ttl` holds 225 classes:
  - **Munition and platform hierarchies,** with multiple inheritance; for example, SM-6 is a SAM, a ballistic-missile interceptor and an anti-ship missile.
  - **Weapon facets** (guidance, warhead, intended target), written as OWL `hasValue` restrictions.
  - **Property chains** for coalition and nation.
  - **Defined classes** for unit function, such as `SAMBattalion`.
  - **A usage guide and example queries** written into the ontology itself.
- `afsim_alignment.ttl` is the AFSIM alignment: each of the 138 type strings AFSIM can emit is an individual of the ontology class it denotes.
- `scenario_orbat.ttl` is the order of battle (ORBAT), which is generated from the scenario definition. It holds about 100 units with echelon, nation and service. Each of the 168 platforms has its AFSIM name, its AFSIM type and its owning unit.
- **Reasoning:** the SPARQL endpoint applies OWL-RL reasoning (`owlrl`) when it loads. That takes about 8 seconds and brings the graph to about 11,500 triples, so inferred facts can be queried with plain triple patterns.

**Model:** `gpt-oss:20b`, running locally in Ollama with a 32K context window, on an RTX 4070 Super (12 GB) with 31 GB of RAM. About 68% of the model fits on the GPU. Local models get the same short "working method" section added to the system prompt in both modes, e.g. "classify before counting" and "an empty result is not evidence".

**Ground truth:** computed deterministically by `demo/questions.py` from the database and the ontology files, with no model involved. Running `python demo/questions.py` prints it.

**Grading:** Claude graded each answer against the ground truth with a fixed rubric:
- numbers must match exactly to count;
- partial credit is given for each correct part of the breakdown;
- hedging is not rewarded.

The grades and the reasoning behind each one are in `runs/<timestamp>/grades.json`, and alongside each answer in `report.md`. Grading was done offline (`demo/grade_run.py`), so no model calls were needed at run time.

**Repetition:** three full runs of all 7 questions × 2 modes, 42 answers in total, at the model's default sampling temperature.

### The questions

| | Question | What makes it hard without the ontology |
|---|---|---|
| q0 | Weapons fired per side, and the most-fired weapon type | **Control question:** answerable from the database alone |
| q1 | Air-to-air missiles expended per side | `WPN_AMRAAM_D` and `IZDELIYE_610M` are aliases, `WPN_KESTREL` is notional, and `AMRAAM-ER` looks like an AAM but is a surface-launched SAM |
| q2 | Blue precision-guided munitions by category, excluding SAMs and AAMs | "Precision-guided" cuts across the weapon hierarchy: Excalibur, APKWS and GMLRS are guided, while XM1113 and Hydra M151 aren't. `TRIDENT_GLIDE_KIT` is notional |
| q3 | Cluster munitions employed, with side and rounds | Needs warhead knowledge: `MGM-140B` (ATACMS Block IA) is a cluster munition, `BURYA-12` is notional, and `M30A2` looks like the old cluster rocket but isn't one |
| q4 | Destroyed platforms per Blue brigade, regiment or wing | The database has only callsigns; which unit owns which platform exists only in the ontology |
| q5 | Red SAM battalions still able to engage at T+90 min | Needs to know which launchers, radars and command posts form each battalion, and which radars are engagement rather than surveillance radars |
| q6 | Non-US coalition losses by nation, and the category of weapon that killed each one | `side='blue'` lumps all coalition members together; nationality comes from the unit hierarchy |

## 2. Results

### Final configuration (`gpt-oss:20b`, 3 runs)

| Question | OFF (runs 1, 2, 3) | OFF mean | ON (runs 1, 2, 3) | ON mean |
|---|---|---|---|---|
| q0 Total expenditure (control) | 100, 100, 100 | 100 | 100, 100, 100 | **100** |
| q1 Air-to-air missiles | 30, 20, 10 | 20 | 100, 100, 95 | **98** |
| q2 Precision-guided munitions | 15, 10, 15 | 13 | 100, 0, 75 | **58** |
| q3 Cluster munitions | 10, 0, 0 | 3 | 100, 100, 100 | **100** |
| q4 Losses by unit | 0, 25, 25 | 17 | 95, 80, 50 | **75** |
| q5 Air defense capability | 0, 0, 0 | 0 | 50, 75, 50 | **58** |
| q6 Coalition partner losses | 10, 5, 5 | 7 | 100, 100, 100 | **100** |
| **Mean** | 24, 23, 22 | **23** | 92, 79, 81 | **84** |

Reports for these runs: `runs/20261005-204312`, `runs/20261005-210733` and `runs/20261005-213319`.

### Timing

Each full run of 7 questions in both modes took about 25 minutes. Almost all of that is waiting on the model; the SQL and SPARQL queries themselves take well under 2 seconds.

| | Mean time per answer | Notes |
|---|---|---|
| q1 Air-to-air missiles | ON 48s, OFF 93s | Faster with the ontology: one lookup replaces trial and error |
| q2 Precision-guided munitions | ON 139s, OFF 213s | Same |
| q3 Cluster munitions | ON 51s, OFF 47s | Similar |
| q4 / q5 / q6 (force structure) | ON 159–214s, OFF 84–140s | Slower with the ontology, because the agent does the real join work instead of guessing |

### How we got here

The ontology layer went through several iterations, each tested against the same seven questions. The first runs used `qwen3:30b`; all scores are graded by Claude.

| Step | Model | Change | OFF | ON |
|---|---|---|---|---|
| 1 | qwen3:30b | Baseline: ontology as hand-written Turtle with no reasoning | 22 | 29 |
| 2 | qwen3:30b | Added "working method" guidance for local models | 29 | 38 |
| 3 | qwen3:30b | **OWL-RL reasoning**, plus AFSIM types as individuals of their classes | 20 | 45 |
| 4 | qwen3:30b | Moved all alignment logic into the ontology (OWL axioms, SKOS usage notes); generic tools | 31 | 41 |
| 5 | gpt-oss:20b | Model switch (1 run) | 27 | 81 |
| 6 | gpt-oss:20b | Explicit platform → AFSIM type link (3 runs) | 26 | 77 |
| 7 | gpt-oss:20b | **Defined SAM battalion classes**, SPARQL prefix check, database note on damaged platforms (3 runs) | 23 | **84** |

The OFF score barely moves across these steps (20–31), because none of these changes give it any knowledge. The ON score went from 29 to 84 through two kinds of change: making the ontology usable (reasoning, AFSIM alignment, defined classes), and using a model capable enough to use it.

## 3. What the ontology contributes

### It supplies knowledge the model can't have

Some facts in this scenario are notional, so no model could know them from training: `WPN_KESTREL`, `TRIDENT_GLIDE_KIT` and `BURYA-12`. Others are about this scenario specifically: which callsign belongs to which unit, and which unit belongs to which nation. Without the ontology the agent fills these gaps with confident guesses, and they're wrong:

| Question | Without the ontology (actual answers) | With the ontology |
|---|---|---|
| q6 nations | Polish howitzers called "Russian" or "Ukrainian"; British Typhoons called "German", "French" or "Czech" | UK 2, Poland 2, Norway 1, read from inferred `bs:nation`: correct in all 3 runs |
| q3 cluster munitions | GBU-53B, M795 and 3OF45 listed as cluster munitions; the real four all missed | All four found from the inherited warhead facet: correct in all 3 runs |
| q1 air-to-air missiles | AMRAAM-ER counted as an AAM (it's a SAM); SAMs, ATGMs and artillery counted (Red total 338 against a true 22) | All 11 AAM strings, AMRAAM-ER correctly excluded "because the ontology classifies it as a SAM" |
| q4 losses by unit | Grouped by callsign prefix ("COBRA", "THUNDER"), or declared unanswerable | All 16 brigades, wings and regiments, via the inferred chain of command |
| q5 SAM battalions | Invented battalions from callsigns ("KORNET", "SHTORM", "VULKAN") | Exactly the 4 Red SAM battalions, classified by the reasoner |

### It turns classification into a lookup

With the ontology, a classification question becomes one query that returns the exact AFSIM strings, followed by one SQL count. For example:

```sparql
SELECT ?name WHERE { ?t a bs:SimulationType ; bs:warheadType bs:Submunitions ; bs:simTypeName ?name }
```

This returns exactly the five cluster munitions in the scenario. The agent then counts them in SQL. This is why the classification questions are both more accurate and roughly twice as fast with the ontology.

### The analytical logic lives in one place

How AFSIM output maps to these concepts is stated once, in OWL, and not in agent prompts or tool code:
- **Alignment:** every AFSIM type string is an individual of its class (`afsim_alignment.ttl`).
- **Inheritance:** weapon facets pass down the hierarchy as `owl:hasValue` restrictions.
- **Derived facts:** nation and coalition come from `owl:propertyChainAxiom`, e.g. platform → owning unit → nation.
- **Unit functions are defined, not labelled:** a `SAMBattalion` is defined as a battalion with SAM launchers or SHORAD vehicles under it, and the reasoner classifies units from their equipment.
- **Self-description:** the ontology carries its own usage guide (`skos:scopeNote`) and example queries (`skos:example`), which the generic MCP server serves to the agent.

Adding a new AFSIM weapon means adding one alignment entry; its category, facets and so on then follow automatically. The ontology MCP server contains no domain knowledge at all.

## 4. What made the difference (lessons)

1. **Reasoning has to be on.** With the ontology served as plain triples, a query for "cluster munitions" found nothing, because no weapon is *directly* a cluster munition, only through subclasses and inherited facets. A capable model writes the property paths itself; a small one doesn't. Applying OWL-RL reasoning in the endpoint made the natural query work.
2. **Make the alignment explicit and first-class.** Making AFSIM type strings individuals of their ontology classes, and linking each platform to its AFSIM type, removed a whole class of failed joins. Before that, the agent repeatedly used the ontology's internal names (`ATACMS_BlkIA`) in SQL instead of AFSIM's (`MGM-140B`).
3. **Model the concepts the questions use.** q5 scored 0 across four runs until "SAM battalion" existed as a class. The agent kept looking for exactly that class (`bs:SurfaceToAirMissileBattalion`) because the question implied it should exist. Once defined (and inferred from equipment), the agent found the right four battalions every time.
4. **Tool details matter for small models.**
   - A model-invented `PREFIX bs:` namespace silently returned 0 rows for 22 queries in a row. The tool now corrects it and tells the model.
   - An unknown tool name used to crash the agent loop. It now returns an error to the model.
   - Saying what each database column means for each event type fixed a recurring wrong join.
5. **Model capability decides how much of the ontology's value you get.** With the same ontology, `qwen3:30b` peaked at 45 and `gpt-oss:20b` reached 84. The bigger gain came from a model that queries persistently (up to 29 tool calls per answer instead of 2–4).

## 5. Remaining failures

All seven remaining failures with the ontology came from mistakes in using information the ontology already had. None were caused by a missing fact or rule:
- **q5 (×3):** the agent judged readiness from the wrong components. Twice it counted surveillance radars or launchers as engagement radars, although the ontology separates them. Twice it treated `DAMAGED` platforms as out of action, despite a note in the database description. In both cases it still identified the battalions correctly.
- **q4 (×2):** one run left out the coalition filter, so Red regiments got into the table. Another missed two platforms in its join.
- **q2 (×2):** one empty final answer (the model returned nothing, even when asked again), and one run that left an air-to-air missile in a category count.

## 6. Caveats

- **Synthetic, single scenario.** The data is AFSIM-style synthetic output, not a real AFSIM run, and there are seven questions. The questions were chosen to need ontology knowledge, apart from the control.
- **The ground truth relies on the ontology.** It is computed from the ontology, so the experiment measures whether an agent can *use* curated knowledge, assuming that knowledge is correct. An agent without the ontology that disagrees with it, for example about a notional system, is marked wrong by design.
- **Grader.** Claude graded the answers, and also designed the ontology changes during the experiment. The rubric compares numbers against a computed answer, which leaves little room for judgment. Every grade and its rationale is in `runs/*/grades.json` for review.
- **Variance.** Single answers vary between runs at the default temperature; q2 scored 100, 0 and 75 across three runs. Read the per-question numbers as a range rather than a point estimate. The overall OFF/ON gap was stable in every run.
- **Local model only.** All results are from local open-weight models (no API costs). A frontier model would likely score higher in both modes; the size of the gap with such a model is untested here.

## 7. Reproducing

```bash
ollama pull gpt-oss:20b
```
```bash
python demo/run_demo.py --all --no-judge --model gpt-oss:20b
```
```bash
python demo/grade_run.py export runs/<timestamp>
```

Set `DEMO_PROVIDER=ollama` and give Ollama a 32K context window first (see the README section [Running on a local model with Ollama](README.md#running-on-a-local-model-with-ollama)). After exporting, grade `grading_packet.md` into `grades.json` and run `python demo/grade_run.py apply runs/<timestamp>` to rebuild the report with scores and timing statistics.
