"""MCP server: a generic front end to an OWL ontology behind a SPARQL 1.1 endpoint.

Tools:
  ontology_overview()   the ontology's usage guide, vocabulary, class skeleton and example queries
  find_terms(text)      keyword search over every text value (labels, comments, AFSIM names...)
  sparql_query(query)   run a SELECT / ASK / CONSTRUCT query (common PREFIXes added automatically)

The server is a thin client of the endpoint at SPARQL_ENDPOINT (default
http://127.0.0.1:3030/battlespace/sparql), so any triple store holding
ontology/*.ttl can sit behind it.

Usage (stdio):  python mcp_servers/ontology_server.py [--endpoint URL]
"""
import argparse
import logging
import os
import re

import httpx
from mcp.server.mcpserver import MCPServer

ENDPOINT = os.environ.get("SPARQL_ENDPOINT", "http://127.0.0.1:3030/battlespace/sparql")

PREFIXES = {
    "bs": "http://example.org/battlespace#",
    "rdf": "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
    "rdfs": "http://www.w3.org/2000/01/rdf-schema#",
    "owl": "http://www.w3.org/2002/07/owl#",
    "skos": "http://www.w3.org/2004/02/skos/core#",
    "xsd": "http://www.w3.org/2001/XMLSchema#",
}
PREFIX_BLOCK = "".join(f"PREFIX {p}: <{u}>\n" for p, u in PREFIXES.items())

# Everything domain-specific - what the ontology covers, how it aligns with the simulation,
# example queries - is read from the ontology's own annotations (rdfs:comment, skos:scopeNote,
# skos:example on the owl:Ontology resource), so this server stays a generic SPARQL front end.
GENERIC_INSTRUCTIONS = "OWL ontology queried with SPARQL. Start with ontology_overview."
logging.getLogger("httpx").setLevel(logging.WARNING)


def _compact(term: str) -> str:
    for p, u in PREFIXES.items():
        if term.startswith(u):
            return f"{p}:{term[len(u):]}"
    return term


def _fix_prefixes(query: str):
    """Correct declarations of our standard prefixes that point at a different IRI. A wrong namespace
    otherwise matches nothing and silently returns 0 rows. Returns (query, notes)."""
    notes = []

    def repl(m):
        p, iri = m.group(1), m.group(2)
        if p in PREFIXES and iri != PREFIXES[p]:
            notes.append(f"NOTE: corrected 'PREFIX {p}: <{iri}>' to <{PREFIXES[p]}> (the namespace this endpoint uses). "
                         f"You can omit PREFIX declarations; the standard ones are added automatically.")
            return f"PREFIX {p}: <{PREFIXES[p]}>"
        return m.group(0)
    return re.sub(r"PREFIX\s+(\w*)\s*:\s*<([^>]*)>", repl, query, flags=re.IGNORECASE), notes


def _sparql(query: str, timeout: float = 30.0):
    # declare any of our standard prefixes the caller did not declare
    missing = [p for p in PREFIXES if not re.search(rf"PREFIX\s+{p}\s*:", query, re.IGNORECASE)]
    query = "".join(f"PREFIX {p}: <{PREFIXES[p]}>\n" for p in missing) + query
    r = httpx.post(ENDPOINT, data={"query": query},
                   headers={"Accept": "application/sparql-results+json, text/turtle"}, timeout=timeout)
    if r.status_code != 200:
        raise RuntimeError(r.text.strip()[:2000])
    if r.headers.get("content-type", "").startswith("application/sparql-results+json"):
        return r.json()
    return r.text


def _table(res, max_rows=500):
    if isinstance(res, str):
        return res if len(res) < 40000 else res[:40000] + "\n... truncated"
    if "boolean" in res:
        return str(res["boolean"]).lower()
    cols = res["head"]["vars"]
    rows = res["results"]["bindings"]
    out = ["\t".join(cols)]
    for b in rows[:max_rows]:
        out.append("\t".join(_compact(b[c]["value"]) if c in b else "" for c in cols))
    out.append(f"... truncated: {max_rows} of {len(rows)} rows" if len(rows) > max_rows else f"({len(rows)} rows)")
    return "\n".join(out)


def _ontology_doc():
    """The ontology's self-description: (comment, scope note, [example queries])."""
    res = _sparql("""SELECT ?comment ?note ?example WHERE { ?o a owl:Ontology .
        OPTIONAL { ?o rdfs:comment ?comment } OPTIONAL { ?o skos:scopeNote ?note }
        OPTIONAL { ?o skos:example ?example } }""")["results"]["bindings"]
    val = lambda k: next((b[k]["value"] for b in res if k in b), "")
    return val("comment"), val("note"), sorted({b["example"]["value"] for b in res if "example" in b})


def _instructions():
    try:
        comment, note, _ = _ontology_doc()
        return "\n\n".join(x for x in (comment, note) if x) or GENERIC_INSTRUCTIONS
    except Exception:  # endpoint not up yet: fall back to the generic text
        return GENERIC_INSTRUCTIONS


server = MCPServer("ontology", instructions=_instructions(), log_level="WARNING")


@server.tool()
def ontology_overview() -> str:
    """Summarise the ontology: its usage guide, prefixes, properties (with comments), the allowed
    values of enumerated properties, the class hierarchy skeleton (every class that has
    subclasses, with its direct parents and number of individuals), and example queries.
    Specific individuals (weapons, platforms, units) are best found with SPARQL or find_terms."""
    comment, note, examples = _ontology_doc()
    parts = [x for x in (comment, note) if x]
    parts.append("PREFIXES (added automatically to sparql_query):\n" + PREFIX_BLOCK)

    props = _sparql("""SELECT ?p ?type ?comment WHERE {
        VALUES ?type { owl:ObjectProperty owl:DatatypeProperty owl:AnnotationProperty }
        ?p a ?type . FILTER(STRSTARTS(STR(?p), STR(bs:)))
        OPTIONAL { ?p rdfs:comment ?comment } } ORDER BY ?p""")
    lines = []
    for b in props["results"]["bindings"]:
        lines.append(f"  {_compact(b['p']['value'])} ({_compact(b['type']['value'])})"
                     + (f": {b['comment']['value']}" if 'comment' in b else ""))
    parts.append("PROPERTIES:\n" + "\n".join(lines))

    # Enumerated properties: object properties whose range class has a small set of named individuals.
    facets = _sparql("""SELECT ?p ?range (COUNT(DISTINCT ?i) AS ?n) (GROUP_CONCAT(DISTINCT STR(?i); separator=" ") AS ?values)
        WHERE { ?p a owl:ObjectProperty ; rdfs:range ?range . FILTER(isIRI(?range) && ?range != owl:Thing)
                ?i a ?range . FILTER(isIRI(?i)) }
        GROUP BY ?p ?range ORDER BY ?p""")
    parts.append("PROPERTY VALUES (object properties with an enumerated range):\n" + "\n".join(
        f"  {_compact(b['p']['value'])} -> {_compact(b['range']['value'])}: "
        + (", ".join(sorted(_compact(v) for v in b["values"]["value"].split())) if int(b["n"]["value"]) <= 30
           else f"{b['n']['value']} individuals - query them")
        for b in facets["results"]["bindings"]))

    # Named classes only, and direct parents only: with reasoning on, rdfs:subClassOf also
    # holds every inferred ancestor, so drop a parent that is implied via another parent.
    edges = _sparql("""SELECT ?c ?parent WHERE { ?c a owl:Class ; rdfs:subClassOf ?parent .
        FILTER(isIRI(?c) && isIRI(?parent) && ?c != ?parent && ?parent != owl:Thing && ?c != owl:Nothing)
        FILTER NOT EXISTS { ?c rdfs:subClassOf ?mid . ?mid rdfs:subClassOf ?parent .
                            FILTER(isIRI(?mid) && ?mid != ?c && ?mid != ?parent) } }""")
    labels = _sparql("SELECT ?c ?label WHERE { ?c a owl:Class ; rdfs:label ?label }")
    # with reasoning, instances of subclasses are instances of the class too
    members = _sparql("""SELECT ?c (COUNT(DISTINCT ?i) AS ?n) WHERE { ?i a ?c . ?c a owl:Class .
        FILTER(isIRI(?i) && isIRI(?c)) } GROUP BY ?c""")
    parents, children = {}, {}
    for b in edges["results"]["bindings"]:
        c, p = _compact(b["c"]["value"]), _compact(b["parent"]["value"])
        parents.setdefault(c, []).append(p)
        children.setdefault(p, []).append(c)
    label = {_compact(b["c"]["value"]): b["label"]["value"] for b in labels["results"]["bindings"]}
    count = {_compact(b["c"]["value"]): b["n"]["value"] for b in members["results"]["bindings"]}
    lines = [f"  {c} - {label.get(c, '')}  [subClassOf {' '.join(parents.get(c, [])) or '(root)'};"
             f" {count.get(c, 0)} individuals]" for c in sorted(children)]
    parts.append("CLASS HIERARCHY SKELETON (non-leaf classes; multiple inheritance is used):\n" + "\n".join(lines))
    if examples:
        parts.append("EXAMPLE QUERIES:\n" + "\n".join("  " + ex.replace("\n", "\n  ") for ex in examples))
    return "\n\n".join(parts)


@server.tool()
def find_terms(text: str, limit: int = 40) -> str:
    """Case-insensitive keyword search over every text value in the ontology (labels, alternative
    labels, comments, AFSIM names...). Returns matching resources with their most specific
    type/parent class and label. Use it to map words from a question (e.g. 'cluster',
    'Patriot', 'S-400', 'Norway') or AFSIM strings to ontology terms."""
    safe = text.replace("\\", "\\\\").replace('"', '\\"')
    q = f"""SELECT DISTINCT ?s ?matched WHERE {{
        ?s ?prop ?matched . FILTER(isLiteral(?matched) && isIRI(?s) && ?prop NOT IN (skos:example, skos:scopeNote))
        FILTER(CONTAINS(LCASE(STR(?matched)), LCASE("{safe}"))) }} LIMIT {int(limit)}"""
    try:
        hits = [(b["s"]["value"], b["matched"]["value"]) for b in _sparql(q)["results"]["bindings"]]
        if not hits:
            return "s\tlabel\tkind\tmatched\n(0 rows)"
        values = " ".join(f"<{s}>" for s in {s for s, _ in hits})
        info = _sparql(f"""SELECT ?s ?label ?k WHERE {{ VALUES ?s {{ {values} }}
            OPTIONAL {{ ?s rdfs:label ?label }}
            OPTIONAL {{ {{ ?s rdfs:subClassOf ?k }} UNION {{ ?s a ?k }} FILTER(isIRI(?k) && ?k != ?s) }} }}""")
        label, kinds = {}, {}
        for b in info["results"]["bindings"]:
            s = b["s"]["value"]
            label.setdefault(s, b.get("label", {}).get("value", ""))
            if "k" in b:
                kinds.setdefault(s, set()).add(b["k"]["value"])
        # The closure lists every ancestor as a kind; keep only the most specific ones.
        ancestors = {}
        for b in _sparql("SELECT ?c ?a WHERE { ?c rdfs:subClassOf ?a . FILTER(isIRI(?c) && isIRI(?a) && ?c != ?a) }"
                         )["results"]["bindings"]:
            ancestors.setdefault(b["c"]["value"], set()).add(b["a"]["value"])
        skip = {PREFIXES["owl"] + n for n in ("Class", "Thing", "NamedIndividual", "Ontology")}
        out = ["s\tlabel\tkind\tmatched"]
        for s, matched in hits:
            ks = kinds.get(s, set()) - skip
            implied = set().union(*(ancestors.get(k, set()) for k in ks)) if ks else set()
            kind = " ".join(sorted(_compact(k) for k in ks - implied))
            out.append("\t".join([_compact(s), label.get(s, ""), kind, matched]))
        out.append(f"({len(out) - 1} rows)")
        return "\n".join(out)
    except Exception as e:
        return f"ERROR: {e}"


@server.tool()
def sparql_query(query: str, max_rows: int = 500) -> str:
    """Run a SPARQL 1.1 SELECT, ASK or CONSTRUCT query against the battlespace ontology and
    return tab-separated results (IRIs compacted to prefix:name). The bs, rdf, rdfs, owl, skos
    and xsd prefixes are declared automatically."""
    query, notes = _fix_prefixes(query)
    try:
        return "\n".join(notes + [_table(_sparql(query), max_rows=max(1, min(max_rows, 5000)))])
    except Exception as e:
        return "\n".join(notes + [f"SPARQL ERROR: {e}"])


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--endpoint", default=ENDPOINT)
    args = ap.parse_args()
    ENDPOINT = args.endpoint
    server.run("stdio")
