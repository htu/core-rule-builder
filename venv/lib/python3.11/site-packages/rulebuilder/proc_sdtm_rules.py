# Purpose: Process all the rules from a df_data 
# -----------------------------------------------------------------------------
# History: MM/DD/YYYY (developer) - description
#   03/14/2023 (htu) - ported from proc_rules_sdtm as proc_sdtm_rules module
#   03/15/2023 (htu) - added "import ruamel.yaml as yaml" and a_yaml 
#  

from .proc_each_sdtm_rule import proc_each_sdtm_rule
from .output_rule2file import output_rule2file
import ruamel.yaml as yaml

def proc_sdtm_rules(df_data, rule_template, rule_ids: list,
                     in_rule_folder, out_rule_folder) -> None:
    # Group data by Rule ID
    grouped_data = df_data.groupby("Rule ID")
    # Loop through each Rule ID and print out required information
    for rule_id, group in grouped_data:
        if rule_id not in rule_ids:
            continue 
        # num_records = group.shape[0]
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
        rule_data = df_data[df_data["Rule ID"] == rule_id]
        a_json = proc_each_sdtm_rule(rule_data,rule_template, rule_id, in_rule_folder)
        a_json["content"] = None 
        a_yaml = yaml.dump(a_json, default_flow_style=False)
        output_rule2file(rule_id, a_json, a_yaml, out_rule_folder)

    # Collect basic stats and print them out
    num_records_processed = df_data.shape[0]
    num_unique_rule_id = grouped_data.ngroups
    print(f"Number of Records Processed: {num_records_processed}")
    print(f"Number of Unique Rule ID: {num_unique_rule_id}")


