import json

def find_by_display():
    with open(r'C:\AI_DEV\AgentSwarm\nodes_export.json', encoding='utf-8') as f:
        nodes = json.load(f)
    
    for node in nodes:
        display = node.get('displayName', '').lower()
        if 'execute' in display or 'command' in display:
            print(f"Name: {node['name']}, Display: {node.get('displayName')}, Version: {node.get('version')}")

if __name__ == "__main__":
    find_by_display()
