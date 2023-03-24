# Purpose: Read an existing rule into a json data format 
# -----------------------------------------------------------------------------
# History: MM/DD/YYYY (developer) - description
#   03/14/2023 (htu) - ported from proc_rules_sdtm as get_existing_rule module
#   03/23/2023 (htu) - added "status" 
#    

import os
from datetime import datetime, timezone
import uuid
import json 

def get_existing_rule(rule_id, in_rule_folder):
    rule_guid = None
    for filename in os.listdir(in_rule_folder):
        if rule_id in filename:
            filepath = os.path.join(in_rule_folder, filename)
            with open(filepath, 'r') as f:
                json_data = json.load(f)
                rule_guid = json_data.get('id')
    now_utc = datetime.now(timezone.utc)
    if rule_guid is None:
        r_json = {
            "id": str(uuid.uuid4()),
            "created": now_utc.strftime("%Y-%m-%dT%H:%M:%SZ"),
            "changed": now_utc.strftime("%Y-%m-%dT%H:%M:%SZ"),
            "status": "new"
        }
    else:
        r_json = json_data
        r_json["changed"] = now_utc.strftime("%Y-%m-%dT%H:%M:%SZ")
        r_json["status"] = "exist"
    return r_json 