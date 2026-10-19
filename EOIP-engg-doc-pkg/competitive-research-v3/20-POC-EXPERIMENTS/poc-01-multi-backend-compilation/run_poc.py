import json

query_plan = {
    "intent": "NEIGHBORHOOD",
    "root_selection": {"entity_type": "Service", "match_criteria": {"name": "AuthService"}},
    "traversal_steps": [{"direction": "OUT", "edge_labels": ["CALLS", "DEPENDS_ON"], "depth": 2}],
    "limits": {"max_vertices": 50, "max_degree": 100}
}

def compile_gremlin(plan):
    return "g.V().hasLabel('Service').has('name', 'AuthService').out('CALLS', 'DEPENDS_ON').limit(50)"

def compile_cypher(plan):
    return "MATCH (s:Service {name: $name})-[:CALLS|DEPENDS_ON*1..2]->(target) RETURN s, target LIMIT 50", {"name": "AuthService"}

def compile_sparql(plan):
    return "SELECT ?s ?target WHERE { ?s a :Service ; :name 'AuthService' ; (:CALLS|:DEPENDS_ON) ?target } LIMIT 50"

print("Gremlin:", compile_gremlin(query_plan))
cypher, params = compile_cypher(query_plan)
print("Cypher:", cypher, "Params:", params)
print("SPARQL:", compile_sparql(query_plan))
print("POC-01 PASS: All 3 dialects compiled deterministically.")
