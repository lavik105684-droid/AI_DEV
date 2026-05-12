import sqlite3
import json
import uuid
from datetime import datetime

DB_PATH = r'C:\AI_DEV\AgentSwarm\n8n_data\database.sqlite'
JSON_PATH = r'C:\AI_DEV\AgentSwarm\Workflows\final_workflows_v1.json'

def activate():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    with open(JSON_PATH, 'r', encoding='utf-8') as f:
        workflows = json.load(f)
    
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%f')[:-3]
    
    for wf in workflows:
        wf_id = wf['id']
        name = wf['name']
        version_id = str(uuid.uuid4())
        
        # Ensure correct versions in JSON for DB
        for node in wf['nodes']:
            if node['type'] == 'n8n-nodes-base.executeCommand':
                node['typeVersion'] = 1
            elif node['type'] == 'n8n-nodes-base.localFileTrigger':
                node['typeVersion'] = 1
            elif node['type'] == 'n8n-nodes-base.httpRequest':
                node['typeVersion'] = 4.4
        
        nodes_json = json.dumps(wf['nodes'])
        conn_json = json.dumps(wf['connections'])
        
        # 1. Update/Insert workflow_entity
        cursor.execute("""
            INSERT INTO workflow_entity (id, name, nodes, connections, active, createdAt, updatedAt, isArchived, versionId)
            VALUES (?, ?, ?, ?, 1, ?, ?, 0, ?)
            ON CONFLICT(id) DO UPDATE SET
                name=excluded.name,
                nodes=excluded.nodes,
                connections=excluded.connections,
                active=1,
                updatedAt=excluded.updatedAt,
                versionId=excluded.versionId
        """, (wf_id, name, nodes_json, conn_json, now, now, version_id))
        
        # 2. Create history entry
        cursor.execute("""
            INSERT INTO workflow_history (versionId, workflowId, nodes, connections, name, createdAt, updatedAt, authors)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (version_id, wf_id, nodes_json, conn_json, name, now, now, '[]'))
        
        # 3. Mark as published
        cursor.execute("""
            INSERT INTO workflow_published_version (workflowId, publishedVersionId, createdAt, updatedAt)
            VALUES (?, ?, ?, ?)
            ON CONFLICT(workflowId) DO UPDATE SET
                publishedVersionId=excluded.publishedVersionId,
                updatedAt=excluded.updatedAt
        """, (wf_id, version_id, now, now))
        
        # 4. Set activeVersionId in main entity
        cursor.execute("""
            UPDATE workflow_entity SET activeVersionId = ? WHERE id = ?
        """, (version_id, wf_id))
        
        print(f"Successfully activated: {name} ({wf_id})")
    
    conn.commit()
    conn.close()

if __name__ == "__main__":
    activate()
