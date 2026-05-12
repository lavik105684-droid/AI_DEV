import json

wf_ids = {
    "04_Memoirs_Full_Production": "I1GZvDOhd2v9ERe3",
    "06_Voiceover_Generator": "LYTjW458N9UY2Vnp"
}

def fix_id(filename, wf_name):
    with open(filename, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    # If it's a single workflow object
    if isinstance(data, dict):
        data["id"] = wf_ids[wf_name]
        # n8n also expects 'nodes' and 'connections' at top level for single import
    
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

fix_id("n8n_master_production_v3.json", "04_Memoirs_Full_Production")
fix_id("n8n_voiceover_generator.json", "06_Voiceover_Generator")
print("IDs fixed.")
