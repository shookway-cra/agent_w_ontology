"""Minimal read-only SPARQL 1.1 Protocol endpoint over the battlespace ontology.

Serves  http://localhost:3030/battlespace/sparql   (Fuseki-style path)
  GET  ?query=...                       (URL-encoded)
  POST application/x-www-form-urlencoded  query=...
  POST application/sparql-query          (raw query body)

SELECT/ASK -> application/sparql-results+json
CONSTRUCT/DESCRIBE -> text/turtle
SPARQL Update is rejected.

Any SPARQL 1.1 server (Apache Jena Fuseki, GraphDB, Oxigraph...) loaded with
ontology/*.ttl can be used instead - just point SPARQL_ENDPOINT at it.

Reasoning: at load time the OWL-RL closure (owlrl) is materialised into the graph, so queries
see inferred types, transitive subclass / command chains, inherited facets and coalitions.
Pass --no-reasoning to serve only the asserted triples.

Usage:  python ontology/sparql_server.py [--port 3030] [--no-reasoning]
"""
import argparse
import json
import threading
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse

import owlrl
from rdflib import BNode, Graph
from rdflib.namespace import OWL, RDF, RDFS

HERE = Path(__file__).parent
DATASET_PATHS = ("/battlespace/sparql", "/battlespace/query", "/sparql")
# Reflexive triples OWL-RL adds for every resource; true but useless to a querying agent.
REFLEXIVE = (OWL.sameAs, RDFS.subClassOf, OWL.equivalentClass, RDFS.subPropertyOf, OWL.equivalentProperty)


def load_graph(reasoning=True):
    g = Graph()
    for ttl in sorted(HERE.glob("*.ttl")):
        g.parse(ttl)
    if reasoning:
        asserted, t0 = len(g), time.time()
        owlrl.DeductiveClosure(owlrl.OWLRL_Semantics, axiomatic_triples=False, datatype_axioms=False).expand(g)
        noise = [t for p in REFLEXIVE for t in g.triples((None, p, None)) if t[0] == t[2]]
        noise += [t for t in g.triples((None, RDF.type, None)) if isinstance(t[2], BNode)]  # restriction memberships
        for t in noise:
            g.remove(t)
        print(f"[sparql] OWL-RL closure: {asserted} asserted -> {len(g)} triples in {time.time() - t0:.1f}s",
              flush=True)
    return g


class Handler(BaseHTTPRequestHandler):
    graph: Graph = None
    lock = threading.Lock()  # rdflib in-memory graphs are not guaranteed thread-safe

    def log_message(self, fmt, *args):  # quieter logs
        print(f"[sparql] {self.address_string()} {fmt % args}")

    def _send(self, code, body: bytes, ctype):
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(body)

    def _error(self, code, msg):
        self._send(code, msg.encode("utf-8"), "text/plain; charset=utf-8")

    def _run(self, query):
        if not query:
            triples = len(self.graph)
            return self._send(200, json.dumps({"status": "ok", "triples": triples}).encode(), "application/json")
        head = query.lstrip().upper()
        if any(kw in head for kw in ("INSERT ", "DELETE ", "LOAD ", "CLEAR ", "DROP ", "CREATE ")) and \
                "SELECT" not in head and "CONSTRUCT" not in head and "ASK" not in head:
            return self._error(403, "SPARQL Update is not permitted on this endpoint")
        try:
            with self.lock:
                result = self.graph.query(query)
                if result.type in ("SELECT", "ASK"):
                    body, ctype = result.serialize(format="json"), "application/sparql-results+json"
                else:
                    body, ctype = result.serialize(format="turtle"), "text/turtle; charset=utf-8"
        except Exception as e:  # parse or evaluation error
            return self._error(400, f"SPARQL error: {e}")
        return self._send(200, body, ctype)

    def do_GET(self):
        url = urlparse(self.path)
        if url.path not in DATASET_PATHS:
            return self._error(404, f"not found; use {DATASET_PATHS[0]}")
        q = parse_qs(url.query).get("query", [""])[0]
        self._run(q)

    def do_POST(self):
        url = urlparse(self.path)
        if url.path not in DATASET_PATHS:
            return self._error(404, f"not found; use {DATASET_PATHS[0]}")
        length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(length).decode("utf-8")
        ctype = self.headers.get("Content-Type", "")
        if ctype.startswith("application/sparql-query"):
            q = body
        elif ctype.startswith("application/sparql-update"):
            return self._error(403, "SPARQL Update is not permitted on this endpoint")
        else:
            q = parse_qs(body).get("query", [""])[0]
        self._run(q)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--host", default="127.0.0.1")
    ap.add_argument("--port", type=int, default=3030)
    ap.add_argument("--no-reasoning", action="store_true", help="serve asserted triples only")
    args = ap.parse_args()
    Handler.graph = load_graph(reasoning=not args.no_reasoning)
    srv = ThreadingHTTPServer((args.host, args.port), Handler)
    print(f"[sparql] {len(Handler.graph)} triples loaded; endpoint http://{args.host}:{args.port}{DATASET_PATHS[0]}",
          flush=True)
    srv.serve_forever()


if __name__ == "__main__":
    main()
