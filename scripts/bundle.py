import os
import json
import yaml

input_dir = './bulletins'
output_file = './bulletins.json'

MOD_REFERENCE_KEYS = {"id","notBefore","notAfter"}
def validate_mod_reference(mod):
    """Validate ModReference format."""
    if isinstance(mod, str):
        return True
    if isinstance(mod, dict):
        if 'id' not in mod or not isinstance(mod['id'], str):
            raise ValueError("Missing or invalid id")
        if 'notBefore' in mod and not isinstance(mod['notBefore'], str):
            if not isinstance(mod['notBefore'], float) and not isinstance(mod['notBefore'], int):
                raise ValueError("Invalid notBefore")
            mod['notBefore'] = str(mod['notBefore'])
        if 'notAfter' in mod:
            if not isinstance(mod['notAfter'], str) and not isinstance(mod['notAfter'], float) and not isinstance(mod['notAfter'], int):
                raise ValueError("Invalid notAfter")
            mod['notAfter'] = str(mod['notAfter'])
        if unknown_keys := set(mod.keys()) - MOD_REFERENCE_KEYS:
            raise ValueError(f"Unknown mod reference keys {unknown_keys} for {mod}")
        return True
    raise ValueError('Invalid mod reference')

BULLETIN_ENTRY_KEYS = {"mods","requires","conflictsWith","message","forceFail","url"}
def validate_bulletin_entry(entry):
    """Validate a single BulletinEntry."""
    if not isinstance(entry, dict):
        raise ValueError(f"Entry {entry} is not an object")
    if 'mods' not in entry or not isinstance(entry['mods'], list):
        raise ValueError(f"Missing mods entry in {entry}")
    if not all(validate_mod_reference(mod) for mod in entry['mods']):
        raise ValueError(f"One or more mod references failed to be parsed in {entry}")
    if 'requires' in entry and (not isinstance(entry['requires'], list) or 
                                not all(validate_mod_reference(mod) for mod in entry['requires'])):
        raise ValueError(f"One or more requires failed in {entry}")
    if 'conflictsWith' in entry and (not isinstance(entry['conflictsWith'], list) or 
                                     not all(validate_mod_reference(mod) for mod in entry['conflictsWith'])):
        raise ValueError(f"One or more conflictsWith failed in {entry}")
    if 'message' not in entry or not isinstance(entry['message'], str) or not bool(entry['message'].strip()):
        raise ValueError(f"Message is missing or invalid in {entry}")
    if 'forceFail' in entry and not isinstance(entry['forceFail'], bool):
        raise ValueError(f"forceFail is not a bool in {entry}")
    if 'url' in entry and not isinstance(entry['url'], str):
        raise ValueError(f"Url is invalid in {entry}")
    if unknown_keys := set(entry.keys()) - BULLETIN_ENTRY_KEYS:
        raise ValueError(f"Unknown mod bulletin entry keys {unknown_keys} for {entry}")        
    return True

def validate_yaml(data):
    """Ensure YAML file is a valid list of BulletinEntry."""
    if not isinstance(data, list):
        raise ValueError(f"Expected bulletin list; got {data}")
    return all(validate_bulletin_entry(entry) for entry in data)


data = []
for filename in os.listdir(input_dir):
    if filename.endswith('.yml'):
        with open(os.path.join(input_dir, filename)) as f:
            yaml_data = yaml.safe_load(f)
            if not validate_yaml(yaml_data):
                raise ValueError(f"Could not parse {filename}")
                
            data.extend(yaml_data)
            
with open(output_file, 'w') as f:
    json.dump(dict(entries = data), f)