# Graph visualization

A collaborative effort to extract entities & visualize relationships between them from unstructured text data 

Simple Flask server with endpoints to interface with Neo4j. See website at http://35.183.206.138:8080, or access the default neo4j view at http://35.183.206.138:7474/browser/

authentication: No authentication

Try the following!

MATCH (p1:Arg)<-[r]->(p2:Arg) RETURN r, p1, p2
