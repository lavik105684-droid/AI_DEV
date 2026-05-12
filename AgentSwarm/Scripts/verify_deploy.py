import sqlite3
import json

DB_PATH = r'C:\AI_DEV\AgentSwarm\n8n_data\database.sqlite'

def verify_deployment():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, active, nodes FROM workflow_entity")
    rows = cursor.fetchall()
    
    print(f"{'ID':<20} | {'Name':<40} | {'Active':<7} | {'Exec Version'}")
    print("-" * 85)
    
    for row in rows:
        wf_id, name, active, nodes_json = row
        nodes = json.loads(nodes_json)
        exec_versions = [str(n.get('typeVersion')) for n in nodes if n.get('type') == 'n8n-nodes-base.executeCommand']
        versions_str = ", ".join(exec_versions) if exec_versions else "N/A"
        print(f"{wf_id:<20} | {name[:40]:<40} | {active:<7} | {versions_str}")
    
    conn.close()

if __name__ == "__main__":
    verify_deployment()
