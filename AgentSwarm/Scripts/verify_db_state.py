import sqlite3
import json

def verify():
    conn = sqlite3.connect(r'C:\AI_DEV\AgentSwarm\n8n_data\database.sqlite')
    cursor = conn.cursor()
    cursor.execute('SELECT name, nodes FROM workflow_entity')
    for name, nodes_json in cursor.fetchall():
        nodes = json.loads(nodes_json)
        v1_nodes = [n['name'] for n in nodes if n.get('typeVersion') == 1]
        print(f"WF: {name}, V1 Nodes: {v1_nodes}")
    conn.close()

if __name__ == "__main__":
    verify()
