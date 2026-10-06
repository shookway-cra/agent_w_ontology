# Ontology-augmented agent demo: AFSIM output analysis

This demo gives the same Claude agent the same question about a simulation run twice:

* **ontology OFF**: the agent can query only the simulation output (SQLite, via the `simdb` MCP server).
* **ontology ON**: the agent can also query a battlespace ontology through a SPARQL endpoint (via the `ontology` MCP server).

Everything else is held constant: model, system prompt, tools, loop and data. Each answer is scored against ground truth computed directly from the data, so the comparison is apples to apples. The only variable is whether the semantic layer is attached.

**Results:** with a local `gpt-oss:20b`, the agent averaged **84/100 with the ontology and 23/100 without it** over three runs of all seven questions. See [RESULTS.md](RESULTS.md) for the experiment setup, per-question results, timing, what the ontology contributes, and caveats.

```
                 ┌─────────────────────────────┐
  question ───▶  │  Claude agent (demo/agent)  │ ───▶ answer ──▶ LLM judge vs ground truth
                 └──────┬───────────────┬──────┘
                        │ MCP (always)  │ MCP (toggle: --ontology on|off|both)
              ┌─────────▼──────┐   ┌────▼─────────────────┐
              │ simdb server   │   │ ontology server      │
              │ read-only SQL  │   │ SPARQL client        │
              └─────────┬──────┘   └────┬─────────────────┘
                        │               │ HTTP, SPARQL 1.1 protocol
          data/afsim_run.sqlite    ontology/sparql_server.py  (or Fuseki / GraphDB / ...)
          AFSIM-style output       ontology/battlespace.ttl     TBox: munition + platform hierarchies
          (callsigns, sim type     ontology/scenario_orbat.ttl  ABox: force structure (ORBAT)
           names, side, events)
```

## What lives where

| | Simulation output (SQLite) | Ontology (RDF/OWL via SPARQL) |
|---|---|---|
| Platforms | `name` (callsign), `type` (AFSIM type string), `side` | platform-type class hierarchy (fighter, SAM launcher, engagement radar, AD command post...) |
| Weapons | `weapon_type` strings in events and inventories | munition hierarchy, guidance, warhead type, intended target, aliases across federates |
| Units | nothing | chain of command (`bs:subordinateTo`, transitive), echelon, nation, service, coalition |
| Time | status snapshots every 60 s, inventory every 600 s, event log | n/a |

The join keys are literal strings: `bs:simTypeName` matches `platforms.type` and `events.weapon_type`, and `bs:simPlatformName` matches `platforms.name`. A class can carry several `simTypeName` aliases, because different federates name the same missile differently. For example, `AIM-120D` and `WPN_AMRAAM_D` are the same weapon.

### The simulation output (`data/afsim_run.sqlite`)

This is a synthetic 4-hour joint scenario, **BALTIC SHIELD**. A Blue coalition (US, UK, Norway, Poland) faces Redland across air, IADS, land and maritime phases. The run has 168 platforms, about 1,050 weapons fired and 73 platforms destroyed. The tables follow AFSIM output conventions:

* `platforms(name, type, side, added_time_s)`
* `platform_status(time_s, platform, lat, lon, alt_m, heading_deg, speed_mps, fuel_kg, damage_factor, state)`, where `state` is `ACTIVE`, `DAMAGED` or `BROKEN`
* `weapon_inventory(time_s, platform, weapon_type, quantity)`
* `events(event_id, time_s, event_type, platform, side, target, weapon_type, weapon_id, result, lat, lon, alt_m, details)`, with event types `PLATFORM_ADDED`, `SENSOR_TRACK_INITIATED`, `WEAPON_FIRED`, `WEAPON_HIT`, `WEAPON_MISSED` and `PLATFORM_BROKEN`. Intercepts put the incoming weapon's `weapon_id` in `target`.

### The ontology (`ontology/`)

* `battlespace.ttl` (hand-written TBox, about 1,100 triples) contains:
  * **Munitions:** `Missile` (AAM IR/radar, SAM by range and BMD, ARM, cruise/LACM, anti-ship, ballistic, ATGM incl. gun-launched), `Bomb` (LGB, GPS, multi-mode, unguided, cluster), `Rocket` (guided/unguided), `ArtilleryProjectile` (guided/unguided), direct-fire rounds, and loitering munitions.
  * **Cross-cutting classes:** `PrecisionGuidedMunition`, `ClusterMunition` and `UnguidedMunition`. Multiple inheritance is used where it's real; for example, SM-6 is a SAM, a BMD interceptor and an anti-ship missile.
  * **Facets as OWL axioms:** `bs:guidance`, `bs:warheadType` and `bs:intendedTarget`, stated on classes as `owl:hasValue` restrictions, so a reasoner gives them to every individual of the class.
  * **Property chains** for each unit's and platform's `bs:coalition` and each platform's `bs:nation`.
  * **Its own usage guide:** `skos:scopeNote` (how to query it and how it aligns with AFSIM) and `skos:example` queries on the ontology header. The ontology MCP server serves these to the agent, and holds no domain knowledge itself.
  * **Platform types:** aircraft roles, ground systems, and air-defense elements (`SAMLauncher`, `EngagementRadar`, `SurveillanceRadar`, `AirDefenseCommandPost`, `SHORADSystem`), plus ships and facilities.
  * **Notional systems** that no model could know from training: `WPN_KESTREL`, `TRIDENT_GLIDE_KIT`, `BURYA-12`, `VORON-K`.
* `scenario_orbat.ttl` (generated ABox, about 1,530 triples) holds about 100 units from joint force down to platoon, with nation, echelon and service, and 168 platform individuals. Each platform has its AFSIM name (`bs:simPlatformName`), its AFSIM type (`bs:simulationType`, linking to the type's individual in `afsim_alignment.ttl`) and its owning unit (`bs:assignedTo`). It also holds platform-type loadouts (`bs:canCarry`).
* `afsim_alignment.ttl` (hand-maintained) aligns AFSIM with the ontology. Every type string AFSIM can emit is a `bs:SimulationType` individual, asserted to be an instance of the class it denotes, with the exact string in `bs:simTypeName`. This is the only place AFSIM type strings appear; everything else about them follows by reasoning. To align a new AFSIM type, add one entry. `data/build_orbat_ttl.py` checks that every string the simulation emits is aligned to exactly one class.

The SPARQL endpoint materialises the OWL-RL closure (`owlrl`) at load time, which takes about 3 seconds. Queries therefore see inferred types, transitive subclass and command chains, inherited facets on AFSIM type individuals, each unit's and platform's `bs:coalition`, and each platform's `bs:nation` (property chains). The ORBAT asserts only one-step links (`bs:assignedTo` for platform to owning unit, `bs:directlySubordinateTo` for unit to parent); the transitive `bs:subordinateTo` is inferred from them. So `?t a bs:ClusterMunition ; bs:simTypeName ?n` returns every AFSIM cluster munition string. Start the endpoint with `--no-reasoning` to serve only the asserted triples.

## Quick start

```bash
python -m venv .venv
```
```bash
.venv\Scripts\activate
```
```bash
pip install -r requirements.txt
```
```bash
python demo/run_demo.py --list
```
```bash
python demo/run_demo.py q1
```

On macOS or Linux, activate with `source .venv/bin/activate`. The agent needs Anthropic API credentials: either `ANTHROPIC_API_KEY` or an `ant auth login` profile. To use a free local model instead, see [Running on a local model with Ollama](#running-on-a-local-model-with-ollama).

`run_demo.py` starts the bundled SPARQL endpoint on `http://127.0.0.1:3030/battlespace/sparql` if nothing is listening there. It runs both configurations of the agent concurrently, streams each tool call live (yellow = ontology OFF, green = ontology ON), prints both answers, the judge's scores and the ground truth, and writes `runs/<timestamp>/report.md` and `results.json`.

```bash
python demo/run_demo.py --all
```
```bash
python demo/run_demo.py q4 --ontology off
```
```bash
python demo/run_demo.py --ask "Which Red units employed loitering munitions, and against what?"
```

Options: `--model` (default `claude-opus-5-5`), `--effort` (default `high`), `--no-judge`. Set the environment variable `DEMO_FALLBACKS=0` to disable the server-side refusal fallback parameter.

### Running on a local model with Ollama

No API key needed. Install [Ollama](https://ollama.com), pull a tool-capable model and give the server a context window big enough for the tool loop (Ollama defaults to 4K on GPUs under 24 GB), then restart Ollama:

```powershell
ollama pull qwen3:30b
```
```powershell
[Environment]::SetEnvironmentVariable('OLLAMA_CONTEXT_LENGTH','32768','User')
```

Then select the provider and run as usual:

```powershell
$env:DEMO_PROVIDER = 'ollama'
```
```bash
python demo/run_demo.py q1
```

With `DEMO_PROVIDER=ollama`, both the agent and the judge default to `qwen3:30b` (override with `--model`, `DEMO_MODEL` or `JUDGE_MODEL`), requests go to `OLLAMA_URL` (default `http://localhost:11434`), tool results are truncated at 12,000 characters (`MAX_TOOL_RESULT_CHARS`), and the Anthropic-only options (`--effort`, adaptive thinking, refusal fallbacks, structured judge output) are skipped. Expect lower scores and slower runs than with Claude; a small local judge is also less reliable.

To grade without the local judge (for example, by Claude Code in chat), run with `--no-judge`, then export a grading packet, write `grades.json` beside it and rebuild the report:

```bash
python demo/grade_run.py export runs/<timestamp>
```
```bash
python demo/grade_run.py apply runs/<timestamp>
```

To print the ground truth without calling any model:

```bash
python demo/questions.py
```

### Using a different triple store

The `ontology` MCP server is just a SPARQL client. To use Apache Jena Fuseki or GraphDB instead, load `ontology/*.ttl` into the store and set `SPARQL_ENDPOINT`, for example `http://localhost:3030/battlespace/sparql`.

### Running it interactively in Claude Code instead

`mcp_configs/baseline.json` and `mcp_configs/with_ontology.json` attach the same MCP servers to Claude Code. Start the endpoint (`python ontology/sparql_server.py`) and use `--strict-mcp-config` so only that config's servers load. Also restrict Claude Code's built-in tools: otherwise the baseline agent could just read the `.ttl` files or the generator source, which defeats the comparison. See `claude --help` for the exact flags your version supports.

## The demo questions

| id | Question | Why the no-ontology agent struggles |
|---|---|---|
| q0 | Total weapons fired per side; most-fired type | Control question. Both should get it right. |
| q1 | Air-to-air missiles expended per side | `WPN_AMRAAM_D` (an AIM-120D alias), `IZDELIYE_610M` (an R-37M alias) and notional `WPN_KESTREL` are easy to miss. `AMRAAM-ER` looks like an AAM but is the NASAMS SAM. |
| q2 | Blue PGMs (excluding SAM/AAM) by category | "PGM" cuts across bombs, rockets, shells, missiles and loitering munitions. Excalibur `M982A1`, `APKWS_II` and GMLRS are guided; `XM1113` and `HYDRA70_M151` aren't. `TRIDENT_GLIDE_KIT` is notional. |
| q3 | Cluster munitions employed | `MGM-140B` is ATACMS Block IA (APAM submunitions). `BURYA-12` is notional. `M30A2` looks like the old DPICM rocket but is the Alternative Warhead (no submunitions). |
| q4 | Losses rolled up to each Blue brigade/wing | The database only has callsigns (`COBRA12`, `RAPIER3`...). Unit membership exists only in the ORBAT. |
| q5 | Which Red SAM battalions could still engage at T+90 min | This needs system composition (which radar, CP and TELs form a battalion) and component roles (engagement vs surveillance radar), joined to time-sliced status. Trap: the Buk battalion still has launchers but lost its engagement radar. |
| q6 | Non-US coalition losses by nation and weapon category | The sim's `side` is just "blue". Nationality comes from the unit hierarchy, and weapon category from the munition hierarchy. |

Ground truth for this run (from `python demo/questions.py`):

* **q1:** Blue 52, Red 22 air-to-air missiles.
* **q2:** 272 Blue PGMs: 120 missiles, 84 guided bombs, 50 guided rockets, 10 guided projectiles and 8 loitering munitions.
* **q3:** 53 cluster rounds: MGM-140B ×3 (blue), 3O23 ×14, 9M55K ×24 and BURYA-12 ×12 (red).
* **q5:** the 2nd S-400 Battalion and the Tor battalion can engage. The 1st S-400 Battalion and the Buk battalion can't, because each lost its engagement radar.
* **q6:** 5 non-US platforms destroyed: UK 2, Poland 2, Norway 1.

There are two sources of ontology advantage, and the demo exercises both:
1. **Knowledge no model can have:** scenario-specific force structure, notional systems, and federate-specific type-name aliases.
2. **Precise, authoritative definitions** where general knowledge is fuzzy or unreliable to apply across 80 weapon types: what counts as a PGM, as a cluster munition, or as an engagement radar.

### More query ideas

* **Kill chain by unit:** which Red platforms were destroyed by weapons launched from 4th Fighter Wing aircraft?
* **Interceptor economics:** interceptors expended per threat defeated, by threat class (ballistic, cruise, one-way attack UAV, anti-ship). This needs the weapon hierarchy on both sides of the intercept.
* **Anti-armor effectiveness:** Pk of ATGMs (incl. gun-launched 9M119M / 9M117M1) vs kinetic-energy rounds vs loitering munitions against main battle tanks.
* **SEAD:** which emitters (ontology: `AirDefenseRadar`) were targeted by anti-radiation missiles, and how many were destroyed?
* **Residual capability:** which Blue platforms could still engage air targets at T+3h? This joins `bs:canCarry` + `bs:intendedTarget bs:AirTargets` + `weapon_inventory`.
* **Remaining precision-strike capacity per brigade** at end of run (inventory × PGM class × ORBAT).
* **HVAA threat:** which high-value airborne assets were engaged, by which weapon classes, and from which Red regiments?

## Regenerating the data

`data/scenario.py` is the single source of truth for the ORBAT, loadouts and engagement script.

```bash
python data/build_orbat_ttl.py
```
```bash
python data/generate_sim_data.py
```

`build_orbat_ttl.py` also checks that every platform and weapon type string the simulation can emit maps to exactly one ontology class. Change `SEED` in `scenario.py` for a different stochastic outcome. The engagement plan stays the same; hits, kills and intercepts change.

## Layout

```
data/scenario.py            ORBAT, kinematics, loadouts, engagement plan
data/generate_sim_data.py   event-driven engagement simulator -> afsim_run.sqlite
data/build_orbat_ttl.py     ORBAT -> ontology/scenario_orbat.ttl (+ validation)
ontology/battlespace.ttl    hand-written TBox
ontology/sparql_server.py   minimal SPARQL 1.1 protocol endpoint (rdflib)
mcp_servers/simdb_server.py     MCP: describe_database, run_sql
mcp_servers/ontology_server.py  MCP: ontology_overview, find_terms, sparql_query
demo/agent.py               Claude tool loop over MCP clients (ontology attachable)
demo/questions.py           demo questions + ground truth
demo/judge.py               LLM judge (structured output)
demo/run_demo.py            CLI: side-by-side runs, scoring, reports
```

All system names are open-source or notional, and the data is synthetic. It is not real AFSIM output and is not derived from any real scenario.
