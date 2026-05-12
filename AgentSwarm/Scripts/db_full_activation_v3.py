import sqlite3
import datetime

DB_PATH = r'C:\AI_DEV\AgentSwarm\n8n_data\database.sqlite'

def full_activation():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # 1. Get all workflows that should be active
    cursor.execute("SELECT id, versionId, name, nodes, connections, description FROM workflow_entity WHERE active = 1")
    active_workflows = cursor.fetchall()
    
    now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%f')[:-3]
    
    for wf_id, version_id, name, nodes, connections, description in active_workflows:
        print(f"Full activation for: {name} ({wf_id}) - Version: {version_id}")
        
        # 2. Ensure current version is in workflow_history
        cursor.execute("SELECT versionId FROM workflow_history WHERE versionId = ?", (version_id,))
        if not cursor.fetchone():
            print(f"  Adding version {version_id} to history.")
            cursor.execute('''
                INSERT INTO workflow_history (versionId, workflowId, nodes, connections, name, description, createdAt, updatedAt, authors, autosaved)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (version_id, wf_id, nodes, connections, name, description, now, now, "[]", 0))
        
        # 3. Set activeVersionId
        cursor.execute('''
            UPDATE workflow_entity 
            SET activeVersionId = ?, updatedAt = ?
            WHERE id = ?
        ''', (version_id, now, wf_id))
        
        # 4. Populate workflow_published_version
        cursor.execute("SELECT workflowId FROM workflow_published_version WHERE workflowId = ?", (wf_id,))
        if cursor.fetchone():
            cursor.execute('''
                UPDATE workflow_published_version
                SET publishedVersionId = ?, updatedAt = ?
                WHERE workflowId = ?
            ''', (version_id, now, wf_id))
        else:
            cursor.execute('''
                INSERT INTO workflow_published_version (workflowId, publishedVersionId, createdAt, updatedAt)
                VALUES (?, ?, ?, ?)
            ''', (wf_id, version_id, now, now))
            
    conn.commit()
    conn.close()
    print("Full activation completed.")

if __name__ == "__main__":
    full_activation()
