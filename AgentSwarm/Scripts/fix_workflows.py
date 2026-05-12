import json
import os

INPUT_FILE = r'C:\AI_DEV\AgentSwarm\Workflows\all_workflows_v2.json'
OUTPUT_FILE = r'C:\AI_DEV\AgentSwarm\Workflows\fixed_workflows.json'

def fix_workflows():
    with open(INPUT_FILE, 'r', encoding='utf-8') as f:
        workflows = json.load(f)

    for wf in workflows:
        print(f"Processing workflow: {wf.get('name')} ({wf.get('id')})")
        
        # 1. Force Activation
        wf['active'] = True
        
        nodes = wf.get('nodes', [])
        connections = wf.get('connections', {})
        
        # 2. Upgrade executeCommand version
        for node in nodes:
            if node.get('type') == 'n8n-nodes-base.executeCommand':
                print(f"  Upgrading {node.get('name')} to typeVersion 2")
                node['typeVersion'] = 2
                
        # 3. Add JULES_CONSULT logic to Master Workflow (ZBWr6WCp0vRzrTpZ)
        if wf.get('id') == 'ZBWr6WCp0vRzrTpZ':
            print("  Injecting JULES_CONSULT logic into Master workflow...")
            
            # Check if already exists
            if not any(n.get('id') == 'jules-consult-master' for n in nodes):
                new_node = {
                    "id": "jules-consult-master",
                    "name": "Generate JULES_CONSULT",
                    "type": "n8n-nodes-base.executeCommand",
                    "typeVersion": 2,
                    "position": [4000, 272],
                    "parameters": {
                        "command": "cat <<EOF > /data/JULES_CONSULT.md\n# JULES CONSULT REPORT\n## Source Text\n{{ $node[\"Read Memoir\"].json.memoir_text }}\n\n## Failed JSON\n{{ $node[\"Clean and Prepare QA\"].json.clean_storyboard_text }}\n\n## Archivist Critique\n{{ $node[\"Archivarius (QA)\"].json.response }}\n\n## Rejection Reason\n{{ $node[\"Format Rejection\"].json.rejection_reason }}\nEOF"
                    }
                }
                nodes.append(new_node)
                
                # Re-route: Dashboard: Critical Error -> Generate JULES_CONSULT -> Sync Swarm
                # Current connections:
                # "Dashboard: Critical Error": {"main": [[{"node": "Sync Swarm", "type": "main", "index": 0}]]}
                
                critical_error_node_name = "Dashboard: Critical Error"
                sync_swarm_node_name = "Sync Swarm"
                
                if critical_error_node_name in connections:
                    connections[critical_error_node_name]['main'] = [[{"node": "Generate JULES_CONSULT", "type": "main", "index": 0}]]
                
                connections["Generate JULES_CONSULT"] = {
                    "main": [[{"node": sync_swarm_node_name, "type": "main", "index": 0}]]
                }

    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(workflows, f, indent=2, ensure_ascii=False)
    
    print(f"Saved {len(workflows)} fixed workflows to {OUTPUT_FILE}")

if __name__ == "__main__":
    fix_workflows()
