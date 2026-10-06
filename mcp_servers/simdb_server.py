"""MCP server: read-only SQL access to the AFSIM simulation output (SQLite).

Tools:
  describe_database()      tables, columns, row counts and sample values
  run_sql(query, max_rows) read-only SELECT / WITH / PRAGMA query

Usage (stdio):  python mcp_servers/simdb_server.py [--db data/afsim_run.sqlite]
"""
import argparse
import os
import re
import sqlite3
from pathlib import Path

from mcp.server.mcpserver import MCPServer

ROOT = Path(__file__).resolve().parent.parent
DB_PATH = Path(os.environ.get("SIM_DB", ROOT / "data" / "afsim_run.sqlite"))

INSTRUCTIONS = """\
Read-only access to the output of an AFSIM (Advanced Framework for Simulation, Integration
and Modeling) run, stored in SQLite. Tables:
  platforms         one row per simulated platform: name (callsign), type (AFSIM platform type), side
  platform_status   state snapshots every 60 s: position, speed, fuel, damage_factor, state (ACTIVE|DAMAGED|BROKEN)
                    A DAMAGED platform is degraded but still functioning (operational); only BROKEN
                    (destroyed, matching its PLATFORM_BROKEN event) is out of action.
  weapon_inventory  weapon quantities per platform every 600 s
  events            event log: PLATFORM_ADDED, SENSOR_TRACK_INITIATED, WEAPON_FIRED, WEAPON_HIT,
                    WEAPON_MISSED, PLATFORM_BROKEN (platform destroyed)
  sim_info          run metadata
What the events columns mean depends on event_type:
  WEAPON_FIRED     platform = shooter, side = shooter's side, weapon_type = weapon expended,
                   target = intended target (for intercepts: the weapon_id of the incoming weapon).
                   One row = one weapon expended.
  WEAPON_HIT / WEAPON_MISSED
                   platform = shooter, side = shooter's side, target = platform that was hit / missed
                   (for intercepts: the weapon_id of the incoming weapon).
  PLATFORM_BROKEN  platform = the DESTROYED platform, side = the destroyed platform's side,
                   weapon_type = the weapon that killed it, target is empty,
                   details holds JSON {"killer": <shooter platform name>}.
Start with describe_database to see columns and the distinct values of key fields."""

server = MCPServer("simdb", instructions=INSTRUCTIONS, log_level="WARNING")

_READONLY = re.compile(r"^\s*(--[^\n]*\n\s*)*(select|with|pragma|explain)\b", re.IGNORECASE)
_FORBIDDEN = re.compile(r"\b(insert|update|delete|drop|alter|create|replace|attach|detach|vacuum)\b", re.IGNORECASE)


def _connect():
    return sqlite3.connect(f"file:{DB_PATH.as_posix()}?mode=ro", uri=True)


def _format(cols, rows, max_rows):
    out = ["\t".join(cols)]
    for r in rows[:max_rows]:
        out.append("\t".join("" if v is None else str(v) for v in r))
    if len(rows) > max_rows:
        out.append(f"... truncated: showing {max_rows} of {len(rows)} rows. Aggregate or add LIMIT/WHERE.")
    else:
        out.append(f"({len(rows)} rows)")
    return "\n".join(out)


@server.tool()
def describe_database() -> str:
    """Describe the simulation database: every table with its columns and row count, plus the
    distinct values of low-cardinality columns (event types, sides, states, platform types,
    weapon types)."""
    con = _connect()
    try:
        parts = []
        tables = [r[0] for r in con.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")]
        for t in tables:
            cols = con.execute(f"PRAGMA table_info({t})").fetchall()
            n = con.execute(f"SELECT COUNT(*) FROM {t}").fetchone()[0]
            parts.append(f"TABLE {t} ({n} rows)\n  " + "\n  ".join(f"{c[1]} {c[2]}" for c in cols))
        parts.append("sim_info:\n  " + "\n  ".join(f"{k} = {v}" for k, v in con.execute("SELECT * FROM sim_info")))
        for label, sql in [
            ("events.event_type", "SELECT event_type, COUNT(*) FROM events GROUP BY 1 ORDER BY 2 DESC"),
            ("events.result", "SELECT result, COUNT(*) FROM events WHERE result IS NOT NULL GROUP BY 1 ORDER BY 2 DESC"),
            ("platforms.side", "SELECT side, COUNT(*) FROM platforms GROUP BY 1"),
            ("platform_status.state", "SELECT state, COUNT(*) FROM platform_status GROUP BY 1"),
            ("platforms.type", "SELECT type, COUNT(*) FROM platforms GROUP BY 1 ORDER BY 1"),
            ("events.weapon_type (WEAPON_FIRED)",
             "SELECT weapon_type, COUNT(*) FROM events WHERE event_type='WEAPON_FIRED' GROUP BY 1 ORDER BY 1"),
        ]:
            vals = ", ".join(f"{v} ({n})" for v, n in con.execute(sql))
            parts.append(f"distinct {label}: {vals}")
        return "\n\n".join(parts)
    finally:
        con.close()


@server.tool()
def run_sql(query: str, max_rows: int = 200) -> str:
    """Run a read-only SQLite query (SELECT / WITH / PRAGMA) against the simulation output and
    return tab-separated rows. Results longer than max_rows are truncated - aggregate in SQL
    where possible."""
    if not _READONLY.match(query) or _FORBIDDEN.search(query):
        return "ERROR: only read-only SELECT / WITH / PRAGMA queries are allowed."
    con = _connect()
    try:
        cur = con.execute(query)
        cols = [d[0] for d in cur.description] if cur.description else []
        rows = cur.fetchall()
        return _format(cols, rows, max(1, min(max_rows, 2000)))
    except sqlite3.Error as e:
        return f"SQL ERROR: {e}"
    finally:
        con.close()


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--db", default=str(DB_PATH))
    args = ap.parse_args()
    DB_PATH = Path(args.db)
    server.run("stdio")
