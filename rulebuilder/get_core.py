# Purpose: Get json.Core for a rule 
# -----------------------------------------------------------------------------
# History: MM/DD/YYYY (developer) - description
#   03/14/2023 (htu) - ported from proc_rules_sdtm as get_core module
#   03/17/2023 (htu) - added docstring and test cases
#    


import os
import json
from rulebuilder.echo_msg import echo_msg

def get_core(rule_id: str = None, org: str = "CDISC", std: str = "SDTMIG"):
    """
    ===============
    get_core
    ===============
    This method builds the json.Core element in the core rule.

    Parameters:
    -----------
    rule_id: str
        Core rule id from rule definition
    org: str
        Organization name or abbreviation
    std: str
        Standard name or abbreviation

    returns
    -------
        r_json: json content for json.Check

    Raises
    ------
    ValueError
        None

    """
    v_prg = __name__
    v_stp = 1.0
    v_msg = "Setting parameters..."
    echo_msg(v_prg, v_stp, v_msg, 2)
    v_stp = 1.1
    v_msg = "Input parameter rule_id is empty."
    if rule_id is None:
        echo_msg(v_prg, v_stp, v_msg, 0)
        return {}

    core_id = org + '.' + std + '.' + rule_id 
    r_json= {
            "Id": core_id,
            "Version": "1",
            "Status": "Draft"
    }
    return r_json


# Test cases
if __name__ == "__main__":
    # set input parameters
    v_prg = __name__ + "::get_core"
    os.environ["g_lvl"] = "3"

    # 1. Test with basic parameters
    v_stp = 1.0
    echo_msg(v_prg, v_stp, "Test Case 01: Basic Parameter", 1)
    r_json = get_core()
    # print out the result
    print(json.dumps(r_json, indent=4))

    # Expected output:

   # 2. Test with parameters
    v_stp = 2.0
    echo_msg(v_prg, v_stp, "Test Case 02: With one rule id", 1)
    rule_id = "CG0001"
    r_json = get_core(rule_id, "FDA","Conformance Rule v1")
    # print out the result
    print(json.dumps(r_json, indent=4))

    # Expected output:

# End of File
