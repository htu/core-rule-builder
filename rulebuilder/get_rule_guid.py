# Purpose: Get or generate a GUID 
# -----------------------------------------------------------------------------
# History: MM/DD/YYYY (developer) - description
#   03/14/2023 (htu) - ported from proc_rules_sdtm as get_rule_guid module
#    

import uuid

def get_rule_guid(json_data):
    rule_guid = json_data.get('id')
    if rule_guid is None:
        rule_guid = str(uuid.uuid4())
    return rule_guid

