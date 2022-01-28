import time
from flask import Flask
from flask import request
from neo4j import GraphDatabase, basic_auth
import json

app = Flask(__name__)

driver = GraphDatabase.driver(
      "bolt://192.168.0.41:7687",
      auth=basic_auth("neo4j", "test")
      )

# @app.route('/graph', methods=['GET'])
# def get_graph():
#     value = request.args.get('value')
#     g = {"nodes": [
#       { "id": "1", "label": value, "title": "node 1 tootip text" },
#       { "id": "2", "label": "Node 2", "title": "node 2 tootip text" },
#       { "id": "3", "label": "Node 3", "title": "node 3 tootip text" }
#     ],
#     "edges": [
#       { "id": "1to2", "from": "1", "to": "2" },
#       { "from": "1", "to": "3" },
#     ]}

#     return {'value': g}

@app.route('/get_examples', methods=['GET'])
def get_examples():
  cypher_query = '''
    MATCH (p1:Arg)-->() 
    RETURN p1, count(*) as degree 
    ORDER BY degree DESC LIMIT 3
  '''
  
  try:
    with driver.session(database="neo4j") as session:
      result = session.run(cypher_query).data()
      names = []
      for item in result:
        names.append(item['p1']['name'])
      return json.dumps({'examples':names}), 200 
  except Exception as e:
    print(e)
    return f"Error: {str(e)}", 500

@app.route('/graph', methods=['GET'])
def get_graph():
  name = request.args.get('name')
  cypher_query = '''
    MATCH (p1:Arg {name:$name})<-[r]->(p2:Arg) RETURN r, p1, p2
  '''
  
  try:
    with driver.session(database="neo4j") as session:
      result = session.run(cypher_query, name=name)
      nodes, edges, nodes_id = [], [], []

      for item in result:

        # Node 1
        node_dict = {}
        p1 = item['p1']
        if not p1['id'] in nodes_id:
          node_dict['id'] = str(p1['id'])
          node_dict['label'] = p1['name']
          nodes.append(node_dict)
          nodes_id.append(p1['id'])

        # Node 2
        node_dict = {}
        p2 = item['p2']
        if not p2['id'] in nodes_id:
          node_dict['id'] = str(p2['id'])
          node_dict['label'] = p2['name']
          nodes.append(node_dict)
          nodes_id.append(p2['id'])

        # One edge
        edge_dict = {}
        relationship = item['r']

        nodes_tuple = relationship.nodes
        edge_dict['from'] = str(nodes_tuple[0].id)
        edge_dict['to'] = str(nodes_tuple[1].id)
        edge_dict["id"] = str(relationship.id)
        edge_dict["label"] = relationship['predicate']
        edge_dict["title"] = relationship['title']
        
        edges.append(edge_dict)

      g = {"nodes": nodes, "edges": edges}
      return json.dumps({"value": g}), 200 
  except Exception as e:
    print(e)
    return f"Error: {str(e)}", 500