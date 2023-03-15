# Purpose: Output json content to a json and a yaml file 
# -----------------------------------------------------------------------------
# History: MM/DD/YYYY (developer) - description
#   03/14/2023 (htu) - ported from proc_rules_sdtm as output_rule2file module
#   03/15/2023 (htu) - added yaml_data as required input variable 
#  

import os 
import json 
  
def output_rule2file (rule_id, json_data, yaml_data, output_dir) -> None: 
    # 1. write to a yaml file first
    yaml_path = output_dir + '/rules_yaml'
    yaml_fn = rule_id + ".yaml"
    fn_yaml = yaml_path + '/' + yaml_fn
    # check if folder exist; if not, create it
    if not os.path.exists(yaml_path):
        os.makedirs(yaml_path)
    # write the YAML data to a file
    with open(fn_yaml, 'w') as f:
        f.write(yaml_data)

    # 2. write to a json file
    j_data = json_data 
    j_data["content"] = yaml_data
    j_path = output_dir + '/rules_json'
    j_fn = rule_id + ".json"
    fn_json = j_path + '/' + j_fn
    # check if folder exist; if not, create it
    if not os.path.exists(j_path):
        os.makedirs(j_path)
    # write to a json file 
    with open(fn_json, 'w') as f:
        json.dump(j_data, f, indent=4)


