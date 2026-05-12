import json

def check_node_versions():
    with open(r'C:\AI_DEV\AgentSwarm\nodes_export.json', encoding='utf-8') as f:
        nodes = json.load(f)
    
    targets = ['n8n-nodes-base.executeCommand', 'n8n-nodes-base.localFileTrigger']
    
    print(f"{'Node Name':<40} | {'Versions'}")
    print("-" * 60)
    
    for node in nodes:
        if node['name'] in targets:
            print(f"{node['name']:<40} | {node.get('defaultSpec', {}).get('version', 'N/A')} (Current: {node.get('currentVersion', 'N/A')})")
            # Also print all versions if available
            # Note: The export format might vary. Let's see.

if __name__ == "__main__":
    check_node_versions()
