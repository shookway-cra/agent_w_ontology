"""Generate synthetic AFSIM-style output for the BALTIC SHIELD scenario.

Writes data/afsim_run.sqlite with tables modelled on AFSIM event/state output:

  sim_info          key/value run metadata
  platforms         one row per platform (PLATFORM_ADDED): name, type, side
  platform_status   periodic state snapshots (position, kinematics, fuel, damage, state)
  weapon_inventory  periodic weapon-quantity snapshots per platform
  events            discrete event log (PLATFORM_ADDED, SENSOR_TRACK_INITIATED,
                    WEAPON_FIRED, WEAPON_HIT, WEAPON_MISSED, PLATFORM_BROKEN)

Only raw simulation identifiers are written: callsigns, sim type strings and
side names.  Chain of command, nationality and type semantics are NOT in here -
they live in the ontology.

Usage:  python data/generate_sim_data.py [--out data/afsim_run.sqlite]
"""
import argparse
import heapq
import json
import math
import random
import sqlite3
import sys
from dataclasses import dataclass, field
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import scenario as S  # noqa: E402

# Theater regions (lat_min, lat_max, lon_min, lon_max) by (side, role)
REGIONS = {
    ("blue", "air"): (57.3, 58.6, 23.6, 24.6), ("red", "air"): (57.4, 58.7, 26.0, 26.9),
    ("blue", "hvaa"): (57.6, 58.2, 22.6, 23.2), ("red", "hvaa"): (57.8, 58.3, 27.4, 27.9),
    ("blue", "rotary"): (57.5, 58.1, 24.5, 24.8), ("red", "rotary"): (57.5, 58.1, 25.3, 25.6),
    ("blue", "uav"): (57.5, 58.2, 24.6, 25.0), ("red", "uav"): (57.5, 58.2, 25.1, 25.5),
    ("blue", "maneuver"): (57.5, 58.1, 24.70, 24.80), ("red", "maneuver"): (57.5, 58.1, 25.20, 25.30),
    ("blue", "fires"): (57.5, 58.2, 24.2, 24.5), ("red", "fires"): (57.5, 58.2, 25.5, 25.9),
    ("blue", "ad"): (57.4, 58.4, 23.4, 23.9), ("red", "ad"): (57.4, 58.4, 26.1, 26.8),
    ("blue", "rear"): (57.3, 58.5, 22.6, 23.2), ("red", "rear"): (57.3, 58.5, 27.0, 27.8),
    ("blue", "sea"): (57.6, 58.6, 20.6, 21.6), ("red", "sea"): (59.0, 59.4, 21.8, 22.8),
    ("red", "coast"): (58.9, 59.2, 23.4, 24.0),
}
MANEUVER_TYPES = {"M1A2_SEPV3", "M2A4", "T-90M", "BMP-3", "9P163_KORNET", "SB600_TEAM", "ZALA_LANCET_TEAM"}
FIRES_TYPES = {"M109A7", "AHS_KRAB", "M142_HIMARS", "2S19M2", "9A53-S", "M-SHORAD_INC1"}
AD_TYPES = {"MPQ-65A_RADAR", "MSQ-132_ECS", "M903_LS", "NASAMS_FDC", "SENTINEL_F1", "NASAMS_LCHR",
            "55K6E_CP", "91N6E_BIG_BIRD", "92N6E_GRAVE_STONE", "5P85TE2_TEL", "96K6_PANTSIR-S1",
            "55ZH6M_NEBO-M", "BAIKAL-1ME", "9S18M1", "9S36M", "9S510M", "9A317M_TELAR", "9K332_TOR-M2"}
HVAA_TYPES = {"E-3G", "KC-46A", "A-50U"}
FACILITY_TYPES = {"AIRBASE_FACILITY", "PORT_FACILITY", "FUEL_DEPOT"}
REAR_TYPES = FACILITY_TYPES | {"9P78-1", "GERAN_LAUNCH_RAIL"}


def haversine_m(lat1, lon1, lat2, lon2):
    r = 6371000.0
    p1, p2 = math.radians(lat1), math.radians(lat2)
    dp, dl = p2 - p1, math.radians(lon2 - lon1)
    a = math.sin(dp / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(dl / 2) ** 2
    return 2 * r * math.asin(math.sqrt(a))


@dataclass
class Plat:
    name: str
    ptype: str
    side: str
    motion: str
    speed: float
    cruise_alt: float
    fuel_max: float
    inv: dict
    lat: float
    lon: float
    center: tuple
    phase: float
    alt: float = 0.0
    heading: float = 0.0
    cur_speed: float = 0.0
    fuel: float = 0.0
    damage: float = 0.0
    goal_lon: float | None = None

    @property
    def alive(self):
        return self.damage < 1.0

    @property
    def state(self):
        if self.damage >= 1.0:
            return "BROKEN"
        return "DAMAGED" if self.damage > 0 else "ACTIVE"


def region_for(side, ptype, motion, callsign):
    if callsign.startswith("SKALA"):
        return REGIONS[("red", "coast")]
    if ptype in HVAA_TYPES:
        return REGIONS[(side, "hvaa")]
    if motion in ("air",):
        return REGIONS[(side, "air")]
    if motion == "rotary":
        return REGIONS[(side, "rotary")]
    if motion == "uav":
        return REGIONS[(side, "uav")]
    if motion == "sea":
        return REGIONS[(side, "sea")]
    if ptype in MANEUVER_TYPES:
        return REGIONS[(side, "maneuver")]
    if ptype in FIRES_TYPES:
        return REGIONS[(side, "fires")]
    if ptype in AD_TYPES:
        return REGIONS[(side, "ad")]
    return REGIONS[(side, "rear")]


def build_platforms(rng):
    plats = {}
    unit_centers = {}
    for root in (S.BLUE, S.RED):
        for callsign, ptype, unit, side in S.iter_platforms(root):
            motion, speed, alt, fuel, loadout = S.PTYPE[ptype]
            loadout = dict(S.LOADOUT_OVERRIDE.get(callsign, loadout))
            reg = region_for(side, ptype, motion, callsign)
            key = (unit.id, ptype)
            if key not in unit_centers:
                unit_centers[key] = (rng.uniform(reg[0], reg[1]), rng.uniform(reg[2], reg[3]))
            clat, clon = unit_centers[key]
            jitter = 0.01 if motion in ("ground", "fixed") else 0.05
            lat, lon = clat + rng.uniform(-jitter, jitter), clon + rng.uniform(-jitter, jitter)
            p = Plat(callsign, ptype, side, motion, speed, alt, fuel, loadout, lat, lon, (lat, lon),
                     rng.uniform(0, 2 * math.pi))
            p.fuel = fuel * rng.uniform(0.85, 1.0)
            p.alt = alt
            p.cur_speed = speed if motion in ("air", "rotary", "uav", "sea") else 0.0
            if ptype in MANEUVER_TYPES and not ptype.endswith("TEAM") and ptype != "9P163_KORNET":
                p.goal_lon = 24.95 if side == "blue" else 25.03
            plats[callsign] = p
    return plats


def move(p: Plat, t: float, dt: float, rng):
    """Advance kinematics by dt seconds."""
    if not p.alive:
        p.cur_speed = 0.0
        if p.motion in ("air", "rotary", "uav"):
            p.alt = 0.0
        return
    if p.motion in ("air", "rotary", "uav"):
        radius_m = {"air": 25000, "rotary": 6000, "uav": 12000}[p.motion]
        omega = p.speed / radius_m
        p.phase += omega * dt
        dlat = (radius_m / 111000.0) * math.sin(p.phase)
        dlon = (radius_m / (111000.0 * math.cos(math.radians(p.center[0])))) * math.cos(p.phase)
        p.lat, p.lon = p.center[0] + dlat, p.center[1] + dlon
        p.heading = (math.degrees(-p.phase) + 360.0) % 360.0
        p.alt = p.cruise_alt + rng.uniform(-150, 150) if p.motion == "air" else p.cruise_alt + rng.uniform(-20, 20)
        p.cur_speed = p.speed * rng.uniform(0.95, 1.05)
        burn = p.fuel_max / (3.2 * 3600) * dt
        p.fuel = max(p.fuel - burn, 0.04 * p.fuel_max)
        if p.motion == "air" and p.fuel < 0.25 * p.fuel_max and p.ptype not in HVAA_TYPES:
            p.fuel = 0.9 * p.fuel_max  # air refueling (abstracted)
    elif p.motion == "sea":
        p.phase += dt / 1800.0
        p.lat = p.center[0] + 0.05 * math.sin(p.phase)
        p.lon = p.center[1] + 0.08 * math.cos(p.phase)
        p.heading = (math.degrees(-p.phase) + 360.0) % 360.0
        p.cur_speed = p.speed
        p.fuel = max(p.fuel - p.fuel_max * 0.00002 * dt / 60.0, 0)
    elif p.motion == "ground":
        if p.goal_lon is not None and 45 * 60 <= t <= 95 * 60 and abs(p.lon - p.goal_lon) > 0.002:
            step_deg = p.speed * dt / (111000.0 * math.cos(math.radians(p.lat)))
            direction = 1 if p.goal_lon > p.lon else -1
            p.lon += direction * min(step_deg, abs(p.goal_lon - p.lon))
            p.heading = 90.0 if direction > 0 else 270.0
            p.cur_speed = p.speed
            p.fuel = max(p.fuel - p.fuel_max * 0.0004 * dt / 60.0, 0)
        else:
            p.cur_speed = 0.0
    # fixed: nothing moves


PK_SCALE = 0.6          # global realism knob applied to every weapon's base Pk


def vulnerability(p: Plat):
    if p.ptype in FACILITY_TYPES:
        return 0.15
    if p.motion in ("air", "rotary", "uav"):
        return 1.25
    if p.ptype in {"M1A2_SEPV3", "T-90M"}:
        return 0.6
    if p.ptype in AD_TYPES:
        return 0.8
    if p.motion == "sea":
        return 0.7
    return 0.9


def select_targets(plats, selector, enemy_side):
    kind, values = selector
    assert kind == "cs"
    return [p for p in plats.values()
            if p.alive and p.side == enemy_side and any(p.name.startswith(v) for v in values)]


class Sim:
    def __init__(self, seed):
        self.rng = random.Random(seed)
        self.plats = build_platforms(self.rng)
        self.events = []          # rows for events table
        self.queue = []           # (time, seq, kind, payload)
        self.seq = 0
        self.weapon_counter = {}
        self.killed_weapons = set()
        self.tracks = set()

    # -- helpers ---------------------------------------------------------------
    def push(self, t, kind, payload):
        self.seq += 1
        heapq.heappush(self.queue, (t, self.seq, kind, payload))

    def log(self, t, etype, platform, target=None, weapon_type=None, weapon_id=None, result=None, details=None):
        p = self.plats.get(platform)
        self.events.append(dict(
            time_s=round(t, 2), event_type=etype, platform=platform, side=p.side if p else None,
            target=target, weapon_type=weapon_type, weapon_id=weapon_id, result=result,
            lat=round(p.lat, 5) if p else None, lon=round(p.lon, 5) if p else None,
            alt_m=round(p.alt, 1) if p else None,
            details=json.dumps(details) if details else None))

    def new_weapon_id(self, shooter, weapon):
        k = (shooter, weapon)
        self.weapon_counter[k] = self.weapon_counter.get(k, 0) + 1
        return f"{shooter}_{weapon}_{self.weapon_counter[k]}"

    # -- scheduling ------------------------------------------------------------
    def schedule_waves(self):
        for (t0, t1, shooters, weapon, selector, n, salvo) in S.WAVES:
            for _ in range(n):
                t = self.rng.uniform(t0 * 60, t1 * 60)
                self.push(t, "engage", dict(shooters=shooters, weapon=weapon, selector=selector, salvo=salvo))

    # -- event handlers --------------------------------------------------------
    def handle_engage(self, t, ev):
        weapon = ev["weapon"]
        cands = [p for p in self.plats.values()
                 if p.alive and p.inv.get(weapon, 0) > 0 and any(p.name.startswith(s) for s in ev["shooters"])]
        if not cands:
            return
        shooter = self.rng.choice(cands)
        enemy = "red" if shooter.side == "blue" else "blue"
        targets = select_targets(self.plats, ev["selector"], enemy)
        if not targets:
            return
        target = self.rng.choice(targets)
        if (shooter.side, target.name) not in self.tracks:
            self.tracks.add((shooter.side, target.name))
            self.log(t - self.rng.uniform(15, 90), "SENSOR_TRACK_INITIATED", shooter.name, target=target.name,
                     details={"sensor": "onboard" if shooter.motion != "fixed" else "site"})
        speed, pk, lethality, threat = S.WEAPON[weapon]
        n = min(ev["salvo"], shooter.inv[weapon])
        for k in range(n):
            tf = t + k * self.rng.uniform(1.0, 4.0)
            shooter.inv[weapon] -= 1
            wid = self.new_weapon_id(shooter.name, weapon)
            self.log(tf, "WEAPON_FIRED", shooter.name, target=target.name, weapon_type=weapon, weapon_id=wid)
            dist = haversine_m(shooter.lat, shooter.lon, target.lat, target.lon)
            tof = max(dist / speed, 4.0) + self.rng.uniform(1, 6)
            impact_t = tf + tof
            self.push(impact_t, "impact", dict(shooter=shooter.name, target=target.name, weapon=weapon, wid=wid))
            if threat:
                self.schedule_intercepts(tf, impact_t, wid, weapon, threat, target)

    def schedule_intercepts(self, t_launch, t_impact, wid, weapon, threat, target):
        defenders_side = target.side
        attempts = 0
        for dtype, interceptor, p_engage in S.INTERCEPTORS[defenders_side].get(threat, []):
            if attempts >= 2:
                break
            cands = [p for p in self.plats.values()
                     if p.alive and p.ptype == dtype and p.inv.get(interceptor, 0) > 0]
            if not cands or self.rng.random() > p_engage:
                continue
            d = self.rng.choice(cands)
            window = t_impact - t_launch
            t_fire = t_launch + window * self.rng.uniform(0.3, 0.6)
            t_res = t_fire + (t_impact - t_fire) * self.rng.uniform(0.5, 0.9)
            self.push(t_fire, "intercept_fire", dict(defender=d.name, interceptor=interceptor, wid=wid,
                                                     weapon=weapon, t_res=t_res))
            attempts += 1

    def handle_intercept_fire(self, t, ev):
        d = self.plats[ev["defender"]]
        if not d.alive or d.inv.get(ev["interceptor"], 0) <= 0 or ev["wid"] in self.killed_weapons:
            return
        d.inv[ev["interceptor"]] -= 1
        iid = self.new_weapon_id(d.name, ev["interceptor"])
        self.log(t, "WEAPON_FIRED", d.name, target=ev["wid"], weapon_type=ev["interceptor"], weapon_id=iid,
                 details={"engagement": "intercept", "threat_weapon_type": ev["weapon"]})
        self.push(ev["t_res"], "intercept_resolve", dict(defender=d.name, interceptor=ev["interceptor"],
                                                         iid=iid, wid=ev["wid"]))

    def handle_intercept_resolve(self, t, ev):
        pk = S.WEAPON[ev["interceptor"]][1]
        if ev["wid"] in self.killed_weapons:
            self.log(t, "WEAPON_MISSED", ev["defender"], target=ev["wid"], weapon_type=ev["interceptor"],
                     weapon_id=ev["iid"], result="TARGET_ALREADY_DESTROYED")
        elif self.rng.random() < pk:
            self.killed_weapons.add(ev["wid"])
            self.log(t, "WEAPON_HIT", ev["defender"], target=ev["wid"], weapon_type=ev["interceptor"],
                     weapon_id=ev["iid"], result="INTERCEPT")
        else:
            self.log(t, "WEAPON_MISSED", ev["defender"], target=ev["wid"], weapon_type=ev["interceptor"],
                     weapon_id=ev["iid"], result="MISS")

    def handle_impact(self, t, ev):
        tgt = self.plats[ev["target"]]
        weapon, wid, shooter = ev["weapon"], ev["wid"], ev["shooter"]
        if wid in self.killed_weapons:
            self.log(t, "WEAPON_MISSED", shooter, target=tgt.name, weapon_type=weapon, weapon_id=wid,
                     result="INTERCEPTED")
            return
        if not tgt.alive:
            self.log(t, "WEAPON_MISSED", shooter, target=tgt.name, weapon_type=weapon, weapon_id=wid,
                     result="TARGET_ALREADY_DESTROYED")
            return
        _, pk, lethality, _ = S.WEAPON[weapon]
        pk *= PK_SCALE
        if tgt.ptype in FACILITY_TYPES:
            pk = min(0.97, pk + 0.3)
        if self.rng.random() < pk:
            dmg = lethality * vulnerability(tgt) * self.rng.uniform(0.45, 1.15)
            before = tgt.damage
            tgt.damage = min(1.0, tgt.damage + dmg)
            self.log(t, "WEAPON_HIT", shooter, target=tgt.name, weapon_type=weapon, weapon_id=wid, result="HIT",
                     details={"damage_before": round(before, 3), "damage_after": round(tgt.damage, 3)})
            if tgt.damage >= 1.0:
                self.log(t, "PLATFORM_BROKEN", tgt.name, target=None, weapon_type=weapon, weapon_id=wid,
                         result="KILLED", details={"killer": shooter})
        else:
            self.log(t, "WEAPON_MISSED", shooter, target=tgt.name, weapon_type=weapon, weapon_id=wid, result="MISS")

    # -- main loop -------------------------------------------------------------
    def run(self):
        status_rows, inv_rows = [], []
        for p in self.plats.values():
            self.log(0.0, "PLATFORM_ADDED", p.name)
        self.schedule_waves()
        handlers = {"engage": self.handle_engage, "impact": self.handle_impact,
                    "intercept_fire": self.handle_intercept_fire, "intercept_resolve": self.handle_intercept_resolve}
        t_prev = 0.0
        for t_snap in range(0, S.DURATION_S + 1, S.STATUS_INTERVAL_S):
            while self.queue and self.queue[0][0] <= t_snap:
                t, _, kind, payload = heapq.heappop(self.queue)
                handlers[kind](t, payload)
            dt = t_snap - t_prev
            for p in self.plats.values():
                if dt > 0:
                    move(p, t_snap, dt, self.rng)
                status_rows.append((t_snap, p.name, round(p.lat, 5), round(p.lon, 5), round(p.alt, 1),
                                    round(p.heading, 1), round(p.cur_speed, 1), round(p.fuel, 1),
                                    round(p.damage, 3), p.state))
                if t_snap % S.INVENTORY_INTERVAL_S == 0:
                    for w, q in sorted(p.inv.items()):
                        inv_rows.append((t_snap, p.name, w, q))
            t_prev = t_snap
        return status_rows, inv_rows


SCHEMA = """
CREATE TABLE sim_info (key TEXT PRIMARY KEY, value TEXT);
CREATE TABLE platforms (
    name TEXT PRIMARY KEY,          -- platform name (callsign) as in the scenario file
    type TEXT NOT NULL,             -- AFSIM platform_type name
    side TEXT NOT NULL,             -- AFSIM side
    added_time_s REAL NOT NULL
);
CREATE TABLE platform_status (
    time_s REAL NOT NULL, platform TEXT NOT NULL,
    lat REAL, lon REAL, alt_m REAL, heading_deg REAL, speed_mps REAL,
    fuel_kg REAL, damage_factor REAL, state TEXT,   -- state: ACTIVE | DAMAGED | BROKEN
    PRIMARY KEY (time_s, platform)
);
CREATE TABLE weapon_inventory (
    time_s REAL NOT NULL, platform TEXT NOT NULL, weapon_type TEXT NOT NULL, quantity INTEGER NOT NULL,
    PRIMARY KEY (time_s, platform, weapon_type)
);
CREATE TABLE events (
    event_id INTEGER PRIMARY KEY,
    time_s REAL NOT NULL,
    event_type TEXT NOT NULL,       -- PLATFORM_ADDED | SENSOR_TRACK_INITIATED | WEAPON_FIRED | WEAPON_HIT | WEAPON_MISSED | PLATFORM_BROKEN
    platform TEXT,                  -- acting platform (shooter / sensor owner / broken platform)
    side TEXT,
    target TEXT,                    -- target platform name, or a weapon_id for intercepts
    weapon_type TEXT,               -- AFSIM weapon type name
    weapon_id TEXT,                 -- unique weapon instance name
    result TEXT,
    lat REAL, lon REAL, alt_m REAL,
    details TEXT                    -- JSON
);
CREATE INDEX ix_events_type ON events(event_type);
CREATE INDEX ix_events_weapon ON events(weapon_type);
CREATE INDEX ix_status_platform ON platform_status(platform, time_s);
"""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=str(Path(__file__).parent / "afsim_run.sqlite"))
    args = ap.parse_args()

    sim = Sim(S.SEED)
    status_rows, inv_rows = sim.run()
    events = sorted(sim.events, key=lambda e: e["time_s"])

    out = Path(args.out)
    if out.exists():
        out.unlink()
    con = sqlite3.connect(out)
    con.executescript(SCHEMA)
    con.executemany("INSERT INTO sim_info VALUES (?,?)", [
        ("scenario", "BALTIC SHIELD (synthetic)"),
        ("generator", "AFSIM-style synthetic output, generate_sim_data.py"),
        ("sim_start_utc", S.SIM_START_UTC),
        ("duration_s", str(S.DURATION_S)),
        ("status_interval_s", str(S.STATUS_INTERVAL_S)),
        ("inventory_interval_s", str(S.INVENTORY_INTERVAL_S)),
        ("random_seed", str(S.SEED)),
    ])
    con.executemany("INSERT INTO platforms VALUES (?,?,?,?)",
                    [(p.name, p.ptype, p.side, 0.0) for p in sim.plats.values()])
    con.executemany("INSERT INTO platform_status VALUES (?,?,?,?,?,?,?,?,?,?)", status_rows)
    con.executemany("INSERT INTO weapon_inventory VALUES (?,?,?,?)", inv_rows)
    con.executemany(
        "INSERT INTO events (time_s,event_type,platform,side,target,weapon_type,weapon_id,result,lat,lon,alt_m,details) "
        "VALUES (:time_s,:event_type,:platform,:side,:target,:weapon_type,:weapon_id,:result,:lat,:lon,:alt_m,:details)",
        events)
    con.commit()

    fired = sum(1 for e in events if e["event_type"] == "WEAPON_FIRED")
    broken = sum(1 for e in events if e["event_type"] == "PLATFORM_BROKEN")
    print(f"wrote {out}: {len(sim.plats)} platforms, {len(events)} events "
          f"({fired} weapons fired, {broken} platforms destroyed), {len(status_rows)} status rows")
    con.close()


if __name__ == "__main__":
    main()
