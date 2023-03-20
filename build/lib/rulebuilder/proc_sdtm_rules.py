# Purpose: Process all the rules from a df_data 
# -----------------------------------------------------------------------------
# History: MM/DD/YYYY (developer) - description
#   03/14/2023 (htu) - ported from proc_rules_sdtm as proc_sdtm_rules module
#   03/15/2023 (htu) - added "import ruamel.yaml as yaml" and a_yaml 
#   03/16/2023 (htu) - 
#     1. added df_selected to speed it up
#     2. added echo_msg to display the progress  
#   03/17/2023 (htu) - used isin for filtering selected rules 
#                    - added doctring and test case
#  

import ruamel.yaml as yaml
import os
from rulebuilder.echo_msg import echo_msg
from rulebuilder.read_rules import read_rules
from rulebuilder.get_creator_id import get_creator_id
from rulebuilder.proc_each_sdtm_rule import proc_each_sdtm_rule
from rulebuilder.output_rule2file import output_rule2file

def proc_sdtm_rules(df_data, rule_template, rule_ids: list,
                     in_rule_folder, out_rule_folder) -> None:
    """
    ===============
    proc_sdtm_rules
    ===============
    This method processes all the rule definition and produces a yaml 
    and json file.

    Parameters:
    -----------
    df_data: dataframe
        a data frame containing all the rule definitions and can be 
        returned from *read_rules* method. 
    rule_template: json
        a json content from reading a Core Rule Schema and can be returned
        from *get_schema* method. 
    rule_ids: list
        a list of rule ids that will be used to select rule definitions 
        to be used to generate yaml and json files for the rules. If not
        provided or if it is a empty list, all the rule definitions will be
        used. 
    in_rule_folder: str
        a folder containing all the existing rules
    out_rule_folder: str
        a folder where the new or updated rules will be output to

    returns
    -------
        None

    Raises
    ------
    ValueError
        None

    """
    # 1. get inputs
    v_prg = __name__ 
    v_stp = 1.0
    v_msg = "Processing SDTM rules..."
    echo_msg(v_prg, v_stp, v_msg,1)
    num_records_processed = df_data.shape[0]
    v_stp = 1.1
    v_msg = "INFO:Total number of records: " + str(num_records_processed)
    echo_msg(v_prg, v_stp, v_msg,2)
    
    # 2. Group data by Rule ID
    v_stp = 2.0 
    v_msg = "Grouping data by rules..."
    echo_msg(v_prg, v_stp, v_msg,1)
    num_selected = len(rule_ids)
    v_stp = 2.1 
    v_msg = "INFO:Selected number of rules: " + str(num_selected)
    echo_msg(v_prg, v_stp, v_msg,2)
    df_selected = df_data if num_selected==0 else df_data[
        df_data["Rule ID"].isin(rule_ids)]
    grouped_data = df_selected.groupby("Rule ID")

    # 3. Loop through each rule 
    v_stp = 3.0
    v_msg = "Looping through each rules..."
    echo_msg(v_prg, v_stp, v_msg,1)

    # Loop through each Rule ID and print out required information
    for rule_id, group in grouped_data:
        # if rule_id not in rule_ids: continue 
        num_records = group.shape[0]
        v_stp = 3.1
        v_msg = "  Rule ID: (" + rule_id + ") with " + str(num_records) + " records."
        echo_msg(v_prg, v_stp, v_msg,2)
        v_stp = 3.2
        v_msg = "INFO: Group {" + str(group) + "}"
        echo_msg(v_prg, v_stp, v_msg, 5)
        # print(f"Group: {group}")
        a_json = {} 
        # sdtmig_versions = ", ".join(group["SDTMIG Version"].unique())
        # documents = ", ".join(group["Document"].unique())
        # sections = ", ".join(group["Section"].unique())
        # items = ", ".join(group["Item"].unique())
        # if num_records > 1: 
            # print(f"Rule ID: {rule_id}\nNumber of Records: {num_records}")
            # print(f"SDTMIG Version: {sdtmig_versions}\nDocument: {documents}")
            # print(f"Section: {sections}\nItem: {items}\n")
        rule_data = None 
        rule_data = df_selected[df_data["Rule ID"] == rule_id]
        a_json = proc_each_sdtm_rule(rule_data,rule_template, rule_id, in_rule_folder)
        a_json["content"] = None 
        a_yaml = yaml.dump(a_json, default_flow_style=False)
        output_rule2file(rule_id, a_json, a_yaml, out_rule_folder)

    # Collect basic stats and print them out
    num_unique_rule_id = grouped_data.ngroups
    print(f"Number of Records Processed: {num_records_processed}")
    print(f"Number of Unique Rule ID: {num_unique_rule_id}")


# Test cases
if __name__ == "__main__":
    # set input parameters 
    os.environ["g_lvl"] = "3"
    v_prg = __name__ + "::proc_sdtm_rules"
    yaml_file = "./data/target/SDTM_and_SDTMIG_Conformance_Rules_v2.0.yaml"
    core_base_url = "https://raw.githubusercontent.com/cdisc-org/conformance-rules-editor/main/public/schema/CORE-base.json"
    creator_url="https://rule-editor.cdisc.org/.auth/me"
    existing_rule_dir="./data/output/json_rules1"
    output_dir="./data/output"
    df_yaml = read_rules(yaml_file)
    creator_id = get_creator_id(creator_url)
    json_obj = {
        "id": "example-id",
        "created": "2023-03-08T12:00:00Z",
        "changed": "2023-03-08T12:00:00Z",
        "creator": {"id": creator_id},
        "content": "example-content",
        "json": {}
    }
    # rule_list = ["CG0373", "CG0378", "CG0379"]
    # rule_list = ["CG0001"]
    rule_list = []

    # 1. Test with basic parameters
    v_stp = 1.0 
    echo_msg(v_prg, v_stp, "Test Case 01: Basic Parameter",1)

    proc_sdtm_rules(df_yaml, json_obj, rule_list,
                        existing_rule_dir,  output_dir)
    
    # Expected output:

# End of File
