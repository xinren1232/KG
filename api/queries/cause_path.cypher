// Query cause-effect paths from symptom to root causes and countermeasures
// Input: $symptom (symptom name to trace)
// Output: graph paths with nodes and relationships

MATCH (s:Entity:Symptom)
WHERE s.name = $symptom OR s.name CONTAINS $symptom

// Find anomalies with this symptom
OPTIONAL MATCH (s)<-[:HAS_SYMPTOM]-(a:Entity:Anomaly)

// Find root causes (direct or through intermediate anomalies)
OPTIONAL MATCH path1 = (a)-[:CAUSED_BY|DUPLICATE_OF*1..3]->(rc:Entity:RootCause)

// Find countermeasures/solutions
OPTIONAL MATCH path2 = (a)-[:RESOLVED_BY*1..2]->(cm:Entity:Countermeasure)

// Find affected components
OPTIONAL MATCH (a)-[:AFFECTS]->(comp:Entity:Component)

// Collect all paths and nodes
WITH s, a, 
     collect(DISTINCT path1) + collect(DISTINCT path2) as all_paths,
     collect(DISTINCT comp) as components

// Extract nodes and relationships from paths
UNWIND CASE WHEN size(all_paths) > 0 THEN all_paths ELSE [null] END as path
WITH s, a, components,
     CASE WHEN path IS NOT NULL THEN nodes(path) ELSE [] END as path_nodes,
     CASE WHEN path IS NOT NULL THEN relationships(path) ELSE [] END as path_rels

// Combine all unique nodes
WITH collect(DISTINCT s) + collect(DISTINCT a) + collect(DISTINCT components) + collect(DISTINCT path_nodes) as all_node_lists,
     collect(DISTINCT path_rels) as all_rel_lists

UNWIND all_node_lists as node_list
UNWIND CASE WHEN size(node_list) > 0 THEN node_list ELSE [null] END as node
WITH collect(DISTINCT node) as unique_nodes, all_rel_lists
WHERE unique_nodes[0] IS NOT NULL

UNWIND all_rel_lists as rel_list  
UNWIND CASE WHEN size(rel_list) > 0 THEN rel_list ELSE [null] END as rel

RETURN 
    [n IN unique_nodes WHERE n IS NOT NULL | {
        id: toString(id(n)),
        labels: labels(n),
        properties: properties(n)
    }] as nodes,
    [r IN collect(DISTINCT rel) WHERE r IS NOT NULL | {
        id: toString(id(r)),
        type: type(r),
        source: toString(id(startNode(r))),
        target: toString(id(endNode(r)))
    }] as relations
