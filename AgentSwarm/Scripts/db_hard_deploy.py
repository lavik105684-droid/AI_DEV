import sqlite3
import json
import datetime
import uuid

DB_PATH = r'C:\AI_DEV\AgentSwarm\n8n_data\database.sqlite'
JSON_PATH = r'C:\AI_DEV\AgentSwarm\Workflows\fixed_workflows.json'

def db_hard_deploy():
    with open(JSON_PATH, 'r', encoding='utf-8') as f:
        workflows = json.load(f)

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    for wf in workflows:
        wf_id = wf.get('id')
        name = wf.get('name')
        nodes = json.dumps(wf.get('nodes', []))
        connections = json.dumps(wf.get('connections', {}))
        active = 1 if wf.get('active') else 0
        now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%f')[:-3]
        new_version_id = str(uuid.uuid4())

        print(f"Deploying workflow: {name} ({wf_id})")
        
        # Check if exists
        cursor.execute('SELECT id FROM workflow_entity WHERE id = ?', (wf_id,))
        if cursor.fetchone():
            cursor.execute('''
                UPDATE workflow_entity 
                SET nodes = ?, connections = ?, active = ?, updatedAt = ?, versionId = ?, versionCounter = versionCounter + 1
                WHERE id = ?
            ''', (nodes, connections, active, now, new_version_id, wf_id))
            print(f"  Updated existing workflow.")
        else:
            print(f"  Workflow {wf_id} not found in database. Skipping insert for safety.")

    conn.commit()
    conn.close()
    print("Hard deploy completed.")

if __name__ == "__main__":
    db_hard_deploy()
