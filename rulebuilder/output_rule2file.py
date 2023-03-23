# Purpose: Output json content to a json and a yaml file 
# -----------------------------------------------------------------------------
# History: MM/DD/YYYY (developer) - description
#   03/14/2023 (htu) - ported from proc_rules_sdtm as output_rule2file module
#   03/15/2023 (htu) - added yaml_data as required input variable 
#   03/21/2023 (htu) - added docstring and test cases  
#   03/22/2023 (htu) - added v_status 

import os
import json


def output_rule2file(rule_id, json_data, yaml_data, output_dir) -> None:
    """
    Writes YAML and JSON data to files in the specified output directory.

    Args:
    rule_id (str): Identifier for the rule.
    json_data (dict): Dictionary containing JSON data.
    yaml_data (str): String containing YAML data.
    output_dir (str): Path to the output directory where files will be written.

    Returns:
    None.
    """
    # Form a file name 
    v_status = json_data.get("json", {}).get("Core", {}).get("Status")
    yaml_fn = rule_id + "-" + v_status + ".yaml"
    # Write YAML data to a file
    yaml_path = output_dir + '/rules_yaml'
    
    fn_yaml = yaml_path + '/' + yaml_fn
    if not os.path.exists(yaml_path):
        os.makedirs(yaml_path)
    with open(fn_yaml, 'w') as f:
        f.write(yaml_data)

    # Write JSON data to a file
    j_data = json_data
    j_data["content"] = yaml_data
    j_path = output_dir + '/rules_json'
    j_fn = rule_id + ".json"
    fn_json = j_path + '/' + j_fn
    if not os.path.exists(j_path):
        os.makedirs(j_path)
    with open(fn_json, 'w') as f:
        json.dump(j_data, f, indent=4)


if __name__ == '__main__':
    # Test case 1
    rule_id = "test_rule"
    json_data = {"key": "value"}
    yaml_data = "key: value\n"
    output_dir = "./output"
    output_rule2file(rule_id, json_data, yaml_data, output_dir)

    # Test case 2
    rule_id = "another_rule"
    json_data = {"name": "John", "age": 30}
    yaml_data = "name: John\nage: 30\n"
    output_dir = "./output"
    output_rule2file(rule_id, json_data, yaml_data, output_dir)


