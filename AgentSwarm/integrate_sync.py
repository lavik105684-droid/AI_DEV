import json
import uuid
import os

SYNC_NODE = {
    "parameters": {
        "command": "bash /data/sync_swarm.sh"
    },
    "id": "sync-swarm-node-id",
    "name": "Sync Swarm",
    "type": "n8n-nodes-base.executeCommand",
    "typeVersion": 1,
    "position": [0, 0]
}

def integrate_sync(workflow_json):
    nodes = workflow_json.get("nodes", [])
    if not nodes:
        return workflow_json

    # Check if sync node already exists
    if any(n.get("name") == "Sync Swarm" for n in nodes):
        return workflow_json

    # Add the node
    sync_node = SYNC_NODE.copy()
    sync_node["id"] = str(uuid.uuid4())
    
    # Position it at the far right
    max_x = max(n.get("position", [0, 0])[0] for n in nodes)
    avg_y = sum(n.get("position", [0, 0])[1] for n in nodes) / len(nodes)
    sync_node["position"] = [max_x + 300, avg_y]
    
    nodes.append(sync_node)
    
    # Connect terminal nodes
    connections = workflow_json.get("connections", {})
    connected_to = set()
    for source_node, targets in connections.items():
        for target_type, target_list in targets.items():
            for target in target_list:
                # This doesn't account for all edge cases but works for simple pipelines
                pass
    
    # Find nodes that have NO outgoing connections in 'main'
    has_outgoing = set()
    for node_name, node_conn in connections.items():
        if node_conn.get("main"):
            has_outgoing.add(node_name)
    
    terminal_nodes = []
    for node in nodes:
        if node["name"] != "Sync Swarm" and node["name"] not in has_outgoing:
            terminal_nodes.append(node["name"])
    
    for term_node in terminal_nodes:
        if term_node not in connections:
            connections[term_node] = {"main": []}
        if "main" not in connections[term_node]:
            connections[term_node]["main"] = []
        
        connections[term_node]["main"].append([
            {
                "node": sync_node["name"],
                "type": "main",
                "index": 0
            }
        ])
    
    workflow_json["nodes"] = nodes
    workflow_json["connections"] = connections
    return workflow_json

def main():
    input_path = "Workflows/all_workflows.json"
    output_path = "Workflows/all_workflows_synced.json"
    
    if not os.path.exists(input_path):
        print(f"File {input_path} not found.")
        return

    with open(input_path, "r", encoding="utf-8") as f:
        workflows = json.load(f)

    processed_workflows = []
    for wf in workflows:
        print(f"Processing {wf['name']}...")
        # If it's 04 or 06 and we have better versions, we could replace them here
        # but the user said "integrate into EACH", so I'll just integrate into what's there.
        # However, 04 and 06 were empty in the export.
        
        processed_wf = integrate_sync(wf)
        processed_workflows.append(processed_wf)

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(processed_workflows, f, indent=2)
    
    print(f"Done. Saved to {output_path}")

if __name__ == "__main__":
    main()
