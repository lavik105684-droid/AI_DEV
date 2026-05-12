import json

def find_nodes():
    with open(r'C:\AI_DEV\AgentSwarm\nodes_export.json', encoding='utf-8') as f:
        nodes = json.load(f)
    
    for node in nodes:
        name = node['name'].lower()
        if 'executecommand' in name or 'localfile' in name:
            print(json.dumps(node, indent=2))
            print("-" * 40)

if __name__ == "__main__":
    find_nodes()
