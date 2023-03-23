# Purpose: Get json.Scope for a rule 
# -----------------------------------------------------------------------------
# History: MM/DD/YYYY (developer) - description
#   03/14/2023 (htu) - ported from proc_rules_sdtm and modulized as get_scope
#   03/22/2023 (htu) - added exist_rule_data, docstring and test cases
#    


import os
import json
from rulebuilder.echo_msg import echo_msg
from rulebuilder.read_rules import read_rules
from rulebuilder.get_existing_rule import get_existing_rule

def get_scope(rule_data, exist_rule_data: dict = {}):
    """
    Mappings from Class to Classes: Include:
ALL - ALL
EVT - EVENTS
FND - FINDINGS
INT - INTERVENTIONS
SPC - SPECIAL PURPOSE
TDM - TRIAL DESIGN

Mappings from Class, Domain to Classes: Include:
FND, FA - FINDINGS ABOUT

Mappings from Class to Domains:
AP - Domains: Include: AP--

NOT (***) in Class or Domain should be mapped to Exclude: instead of Include:

No Mapping - RELATIONSHIP
No Mapping - STUDY REFERENCE

    """
    # print(f"get_scope: Class Type: {type(rule_data['Class'])}")
    # unique_classes = ','.join(rule_data['Class'].unique())
    # unique_domains = ','.join(rule_data['Domain'].unique())
    # unique_classes = rule_data['Class'].unique().tolist()
    # unique_domains = rule_data['Domain'].unique().tolist()

    # Split each element by comma and create a new data frame 
    # df['Class'] = df['Class'].apply(lambda x: [i.strip() for i in x.split(',')])

    r_json = exist_rule_data.get("json", {}).get("Scope")
    if r_json is not None: 
        return r_json
    
    class_mapping = {"EVT": "EVENTS", "FND": "FINDINGS", "INT": "INTERVENTIONS",
        "SPC": "SPECIAL PURPOSE", "TDM": "TRIAL DESIGN"
    }
    df_rules = rule_data 
    for row in df_rules.itertuples(index=False):
        print(f"Class: {row.Class}, Domain: {row.Domain}")
        
    
    df_class = {}
    df_class['Class'] = rule_data['Class'].apply(
        lambda x: [i.strip() for i in x.split(',')])
    df_domain = {}
    df_domain["Domain"] = rule_data['Domain'].apply(
        lambda x: [i.strip() for i in x.split(',')])

    # Create a flattened list of all the elements in the column
    all_classes = [item for sublist in df_class['Class'] for item in sublist]
    all_domains = [item for sublist in df_domain['Domain']
                    for item in sublist]

    # Get the unique elements in the flattened list and create a list
    unique_classes = list(set(all_classes))
    unique_domains = list(set(all_domains))

    print (f"  Domain list: {unique_domains}")

    r_json = {
        "Classes": {
            "Include": unique_classes
        },
        "Domains": {
            "Include": unique_domains
        }
    }
    return r_json


# Test cases
if __name__ == "__main__":
    # set input parameters
    v_prg = __name__ + "::get_core"
    os.environ["g_lvl"] = "3"
    r_dir = "/Volumes/HiMacData/GitHub/data/core-rule-builder"
    existing_rule_dir = r_dir + "/data/output/json_rules1"
    yaml_file = r_dir + "/data/target/SDTM_and_SDTMIG_Conformance_Rules_v2.0.yaml"
    df_data = read_rules(yaml_file)

    # 1. Test with basic parameters
    v_stp = 1.0
    echo_msg(v_prg, v_stp, "Test Case 01: Basic Parameter", 1)
    rule_id = "CG0001"
    rule_data = df_data[df_data["Rule ID"] == rule_id]

    r_json = get_scope(rule_data)
    # print out the result
    print(json.dumps(r_json, indent=4))

    # Expected output:

   # 2. Test with parameters
    v_stp = 2.0
    echo_msg(v_prg, v_stp, "Test Case 02: With one rule id", 1)
    rule_id = "CG0053"
    rule_data = df_data[df_data["Rule ID"] == rule_id]
    d2_data = get_existing_rule(rule_id, existing_rule_dir)
    r_json = get_scope(rule_data, exist_rule_data=d2_data)
    # print out the result
    print(json.dumps(r_json, indent=4))

    # Expected output:

# End of File
