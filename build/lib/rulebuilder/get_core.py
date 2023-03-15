# Purpose: Get json.Core for a rule 
# -----------------------------------------------------------------------------
# History: MM/DD/YYYY (developer) - description
#   03/14/2023 (htu) - ported from proc_rules_sdtm as get_core module
#    

def get_core(rule_id: str, org: str = "CDISC", std: str = "SDTMIG"):
    core_id = org + '.' + std + '.' + rule_id 
    json_core = {
            "Id": core_id,
            "Version": "1",
            "Status": "Draft"
    }
    return json_core


