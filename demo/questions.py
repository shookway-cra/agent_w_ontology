"""Demo questions and their ground truth.

Ground truth is computed deterministically from the ontology files (rdflib, in
process) joined with the simulation database (sqlite).  The agents never see it;
it is used to score their answers.
"""
import sqlite3
from collections import Counter, defaultdict
from dataclasses import dataclass
from functools import cached_property
from pathlib import Path
from typing import Callable

from rdflib import Graph

ROOT = Path(__file__).resolve().parent.parent
PFX = """PREFIX bs: <http://example.org/battlespace#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX owl: <http://www.w3.org/2002/07/owl#>
"""


class KB:
    def __init__(self, db=ROOT / "data" / "afsim_run.sqlite"):
        self.con = sqlite3.connect(f"file:{Path(db).as_posix()}?mode=ro", uri=True)

    @cached_property
    def g(self):
        g = Graph()
        for ttl in sorted((ROOT / "ontology").glob("*.ttl")):
            g.parse(ttl)
        return g

    def sparql(self, q):
        return [tuple(str(v) if v is not None else None for v in row) for row in self.g.query(PFX + q)]

    def sql(self, q, args=()):
        return self.con.execute(q, args).fetchall()

    def sim_names_under(self, cls):
        return {r[0] for r in self.sparql(
            f"SELECT ?n WHERE {{ ?t bs:simTypeName ?n ; a ?c . ?c rdfs:subClassOf* bs:{cls} }}")}

    def fired(self, side=None):
        q = "SELECT weapon_type, side, COUNT(*) FROM events WHERE event_type='WEAPON_FIRED'"
        q += " AND side=?" if side else ""
        q += " GROUP BY 1, 2"
        return self.sql(q, (side,) if side else ())

    def label_of_sim_type(self, name):
        rows = self.sparql(f'SELECT ?l WHERE {{ ?t bs:simTypeName "{name}" ; a ?c . ?c rdfs:label ?l '
                           f'FILTER(?c != bs:SimulationType) }}')
        return rows[0][0] if rows else name


@dataclass
class Question:
    id: str
    title: str
    prompt: str
    why_ontology_helps: str
    ground_truth: Callable[[KB], tuple[str, dict]]   # -> (human readable answer, structured facts)


# ---------------------------------------------------------------------------

def gt_control(kb: KB):
    by_side = dict(kb.sql("SELECT side, COUNT(*) FROM events WHERE event_type='WEAPON_FIRED' GROUP BY 1"))
    top = kb.sql("SELECT weapon_type, COUNT(*) FROM events WHERE event_type='WEAPON_FIRED' "
                 "GROUP BY 1 ORDER BY 2 DESC LIMIT 1")[0]
    text = (f"Weapons fired: blue {by_side['blue']}, red {by_side['red']} (total {sum(by_side.values())}). "
            f"Most-fired weapon type: {top[0]} ({top[1]}).")
    return text, {"by_side": by_side, "top_weapon": top}


def gt_aam(kb: KB):
    aam = kb.sim_names_under("AirToAirMissile")
    per_side, per_type = Counter(), Counter()
    for w, side, n in kb.fired():
        if w in aam:
            per_side[side] += n
            per_type[(side, w)] += n
    lines = [f"{side}: {per_side[side]}" for side in sorted(per_side)]
    detail = "; ".join(f"{s} {w}={n}" for (s, w), n in sorted(per_type.items()))
    sam_like = [w for w, s, n in kb.fired() if w == "AMRAAM-ER"]
    text = (f"Air-to-air missiles fired - {', '.join(lines)} (total {sum(per_side.values())}). "
            f"By type: {detail}. Note: AMRAAM-ER{' (fired)' if sam_like else ''} is a surface-launched SAM and is "
            f"excluded; WPN_AMRAAM_D is an alias of AIM-120D, IZDELIYE_610M an alias of R-37M, "
            f"WPN_KESTREL is a notional IR AAM.")
    return text, {"per_side": dict(per_side), "per_type": {f"{s}:{w}": n for (s, w), n in per_type.items()}}


PGM_CATEGORIES = [("Missile", "missiles"), ("GuidedBomb", "guided bombs"), ("GuidedRocket", "guided rockets"),
                  ("GuidedProjectile", "guided artillery projectiles"), ("LoiteringMunition", "loitering munitions")]


def gt_pgm(kb: KB):
    excluded = kb.sim_names_under("SurfaceToAirMissile") | kb.sim_names_under("AirToAirMissile")
    cats = {cls: kb.sim_names_under(cls) for cls, _ in PGM_CATEGORIES}
    pgm = kb.sim_names_under("PrecisionGuidedMunition")
    per_cat, per_type = Counter(), defaultdict(Counter)
    for w, _side, n in kb.fired("blue"):
        if w in pgm and w not in excluded:
            cat = next(label for cls, label in PGM_CATEGORIES if w in cats[cls])
            per_cat[cat] += n
            per_type[cat][w] += n
    unguided = sorted({w for w, _s, _n in kb.fired("blue")} - pgm)
    parts = [f"{label}: {per_cat[label]} ({', '.join(f'{w}={n}' for w, n in sorted(per_type[label].items()))})"
             for _, label in PGM_CATEGORIES]
    text = (f"Blue PGMs excluding SAMs/AAMs: total {sum(per_cat.values())}. " + "; ".join(parts) +
            f". Unguided Blue weapons that must NOT be counted: {', '.join(unguided)}.")
    return text, {"total": sum(per_cat.values()), "per_category": dict(per_cat),
                  "per_type": {k: dict(v) for k, v in per_type.items()}, "unguided_excluded": unguided}


def gt_cluster(kb: KB):
    cluster = kb.sim_names_under("ClusterMunition")
    rows = [(w, s, n) for w, s, n in kb.fired() if w in cluster]
    rows.sort(key=lambda r: (r[1], r[0]))
    total = sum(n for _, _, n in rows)
    text = (f"Cluster munitions fired: total {total} rounds - " +
            "; ".join(f"{w} ({kb.label_of_sim_type(w)}) by {s}: {n}" for w, s, n in rows) +
            ". Not cluster: M30A2 GMLRS-AW (pre-formed fragments, replaced the DPICM M30), "
            "M31A2 (unitary).")
    return text, {"total": total, "rows": rows}


def _destroyed(kb: KB, before=None):
    q = "SELECT platform, MIN(time_s) FROM events WHERE event_type='PLATFORM_BROKEN'"
    q += f" AND time_s <= {before}" if before is not None else ""
    return dict(kb.sql(q + " GROUP BY 1"))


def gt_orbat_losses(kb: KB):
    dead = _destroyed(kb)
    rows = kb.sparql("""SELECT ?u ?label ?name WHERE {
        ?u a bs:MilitaryUnit ; bs:echelon bs:Brigade ; rdfs:label ?label ; bs:nation/bs:memberOf bs:BlueCoalition .
        OPTIONAL { ?p bs:assignedTo/bs:directlySubordinateTo* ?u ; bs:simPlatformName ?name } }""")
    units = defaultdict(lambda: {"label": None, "total": 0, "destroyed": []})
    for u, label, name in rows:
        units[u]["label"] = label
        if name:
            units[u]["total"] += 1
            if name in dead:
                units[u]["destroyed"].append(name)
    ordered = sorted(units.values(), key=lambda d: (-len(d["destroyed"]), d["label"]))
    text = "Blue brigade/regiment/wing-level losses: " + "; ".join(
        f"{d['label']}: {len(d['destroyed'])} of {d['total']}"
        + (f" ({', '.join(sorted(d['destroyed']))})" if d["destroyed"] else "") for d in ordered)
    text += f". Total Blue platforms destroyed: {sum(1 for p in dead if kb.sql('SELECT side FROM platforms WHERE name=?', (p,))[0][0] == 'blue')}."
    return text, {d["label"]: {"destroyed": len(d["destroyed"]), "of": d["total"]} for d in ordered}


def gt_sam_capability(kb: KB, t=5400):
    dead = _destroyed(kb, before=t)
    rows = kb.sparql("""SELECT ?u ?label ?name ?role WHERE {
        ?u a bs:MilitaryUnit ; bs:echelon bs:Battalion ; rdfs:label ?label ; bs:nation/bs:memberOf bs:RedForce .
        ?p bs:assignedTo/bs:directlySubordinateTo* ?u ; bs:simPlatformName ?name ; a ?t .
        VALUES ?role { bs:SAMLauncher bs:EngagementRadar bs:AirDefenseCommandPost bs:SHORADSystem }
        ?t rdfs:subClassOf* ?role }""")
    units = defaultdict(lambda: defaultdict(list))
    labels = {}
    for u, label, name, role in rows:
        labels[u] = label
        units[u][role.split("#")[1]].append(name)
    results = {}
    for u, roles in units.items():
        if not roles.get("SAMLauncher") and not roles.get("SHORADSystem"):
            continue  # radar or C2-only battalions are not SAM battalions
        alive = {r: [n for n in names if n not in dead] for r, names in roles.items()}
        if roles.get("SAMLauncher"):
            capable = all(alive.get(r) for r in ("EngagementRadar", "AirDefenseCommandPost", "SAMLauncher"))
            missing = [r for r in ("EngagementRadar", "AirDefenseCommandPost", "SAMLauncher") if not alive.get(r)]
        else:
            capable = bool(alive.get("SHORADSystem"))
            missing = [] if capable else ["SHORADSystem"]
        results[labels[u]] = {"capable": capable, "missing": missing,
                              "alive": {r: v for r, v in alive.items()},
                              "lost": {r: [n for n in names if n in dead] for r, names in roles.items()}}
    text = f"Red SAM battalions at T+{t // 60} min: " + "; ".join(
        f"{lbl}: {'MISSION-CAPABLE' if d['capable'] else 'NOT capable (no operational ' + ', '.join(d['missing']) + ')'}"
        f" [lost so far: {', '.join(n for v in d['lost'].values() for n in v) or 'none'}]"
        for lbl, d in sorted(results.items()))
    return text, {k: v["capable"] for k, v in results.items()}


def gt_coalition(kb: KB):
    dead = kb.sql("SELECT platform, weapon_type, json_extract(details,'$.killer'), time_s FROM events "
                  "WHERE event_type='PLATFORM_BROKEN' AND side='blue'")
    nation = dict(kb.sparql("""SELECT ?name ?nl WHERE { ?p bs:simPlatformName ?name ; bs:assignedTo ?u .
                                ?u bs:nation ?n . ?n rdfs:label ?nl }"""))
    broad = [("LoiteringMunition", "loitering munition"), ("BallisticMissile", "ballistic missile"),
             ("CruiseMissile", "cruise missile"), ("AntiRadiationMissile", "anti-radiation missile"),
             ("AntiTankGuidedMissile", "ATGM"), ("AirToAirMissile", "air-to-air missile"), ("GuidedRocket", "guided artillery rocket"),
             ("SurfaceToAirMissile", "surface-to-air missile"), ("GuidedProjectile", "guided artillery"),
             ("ArtilleryProjectile", "artillery projectile"), ("Rocket", "artillery rocket"),
             ("Bomb", "aerial bomb"), ("DirectFireAmmunition", "tank/IFV gun round"), ("Missile", "missile")]
    sets = {cls: kb.sim_names_under(cls) for cls, _ in broad}
    rows = []
    for plat, w, killer, t in dead:
        n = nation.get(plat)
        if n and n != "United States":
            cat = next(label for cls, label in broad if w in sets[cls])
            cluster = " (cluster)" if w in kb.sim_names_under("ClusterMunition") else ""
            rows.append((n, plat, w, cat + cluster, killer, t))
    rows.sort()
    by_nation = Counter(r[0] for r in rows)
    text = (f"Non-US Blue coalition platforms destroyed: {len(rows)} - by nation: "
            + ", ".join(f"{n} {c}" for n, c in sorted(by_nation.items())) + ". Details: "
            + "; ".join(f"{p} ({n}) killed by {w} [{cat}] from {k} at t={t:.0f}s" for n, p, w, cat, k, t in rows))
    return text, {"total": len(rows), "by_nation": dict(by_nation),
                  "rows": [{"nation": n, "platform": p, "weapon": w, "category": c} for n, p, w, c, _, _ in rows]}


QUESTIONS = [
    Question("q0", "Control: total expenditure",
             "How many weapons were fired in total by each side, and which single weapon type was fired most often?",
             "Control question - answerable from the database alone. Both agents should get it right.",
             gt_control),
    Question("q1", "Air-to-air missile expenditure",
             "How many air-to-air missiles did each side expend over the whole engagement?",
             "Weapon names come from different federates: WPN_AMRAAM_D and IZDELIYE_610M are aliases, "
             "WPN_KESTREL is a notional scenario weapon, and AMRAAM-ER looks like an AAM but is a SAM.",
             gt_aam),
    Question("q2", "Precision-guided munitions (munition hierarchy)",
             "Not counting surface-to-air or air-to-air missiles, how many precision-guided munitions did the "
             "Blue coalition expend? Break the total down by category: missiles, guided bombs, guided rockets, "
             "guided artillery projectiles, and loitering munitions.",
             "PGM is a cross-cutting class: Excalibur (M982A1), APKWS_II and GMLRS are guided; XM1113 and Hydra "
             "M151 are not; TRIDENT_GLIDE_KIT is a notional GPS bomb kit; MGM-140B/PRSM are missiles.",
             gt_pgm),
    Question("q3", "Cluster munition employment",
             "Which cluster (submunition-dispensing) munitions were employed during the engagement? For each, give "
             "the weapon type, the side that used it, and the number of rounds fired.",
             "Requires warhead knowledge: MGM-140B is ATACMS Block IA (APAM submunitions), BURYA-12 is notional, "
             "while M30A2 (GMLRS Alternative Warhead) looks like the old DPICM rocket but has no submunitions.",
             gt_cluster),
    Question("q4", "Losses rolled up by force structure",
             "For each Blue brigade-level unit (brigade, regiment, or wing), how many of its platforms were "
             "destroyed during the engagement?",
             "The database only has callsigns. Which callsign belongs to which squadron/battalion/brigade "
             "exists only in the ontology's chain of command (bs:subordinateTo).",
             gt_orbat_losses),
    Question("q5", "Air defense mission capability at a point in time",
             "At T+90 minutes (time_s = 5400), which of Red's surface-to-air missile battalions were still able "
             "to engage? A battalion built from separate launchers, radars and command posts can engage only if "
             "it still has at least one operational engagement radar, one operational command post, and one "
             "operational launcher; a battalion of self-contained SHORAD vehicles can engage if any vehicle is "
             "operational.",
             "Needs system composition (which radar/CP/launchers form which battalion) and component roles "
             "(engagement vs surveillance radar), both from the ontology, joined to time-sliced status data.",
             gt_sam_capability),
    Question("q6", "Coalition partner losses",
             "How many platforms belonging to Blue coalition partners other than the United States were destroyed? "
             "Break it down by nation, and say what category of Red weapon destroyed each one.",
             "Side 'blue' in the sim lumps all coalition members together. Nationality comes from the unit "
             "hierarchy in the ontology, and the weapon category from the munition hierarchy.",
             gt_coalition),
]

BY_ID = {q.id: q for q in QUESTIONS}


if __name__ == "__main__":
    kb = KB()
    for q in QUESTIONS:
        text, _ = q.ground_truth(kb)
        print(f"[{q.id}] {q.title}\n  Q: {q.prompt}\n  A: {text}\n")
