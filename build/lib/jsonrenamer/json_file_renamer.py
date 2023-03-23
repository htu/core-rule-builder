# Purpose: Rename the json files based on json.Core.Id value and 
#          json.Authorities.Standards.References.Rule_Identifier.Id  
# History: MM/DD/YYYY (developer) - description
#   03/13/2023 (htu) - converted from the rename_json_files in 
#              the rule-transformations repo  
#   03/14/2023 (htu) - added extract_rules and write_rules2xlsx
# 

import os
import json
import re 
import pandas as pd


class JsonFileRenamer:
    def __init__(self, input_folder_path, output_folder_path):
        self.input_folder_path = input_folder_path
        self.output_folder_path = output_folder_path
        self.stat_cnts = {"total": 0, "renamed": 0, "skipped": 0, "dupped": 0, 
                          "ruleid_used": 0, "coreid_used": 0}

    def get_core_id(self, j_data):
        # Get the value of Core.Id from the JSON file if it exists, otherwise use the original filename
        core_id = None 
        if "json" in j_data and "Core" in j_data["json"]:
            core_id = j_data["json"]["Core"].get("Id")
        return core_id

    def get_rule_id(self, j_data):
        rule_id = None
        if "json" in j_data and "Authorities" in j_data["json"]:
            j_auth = j_data["json"]["Authorities"][0]
            # print (f"json.Authorities: {j_auth}")
            if "Standards" in j_auth and "References" in j_auth["Standards"][0]:
                j_refr = j_auth["Standards"][0].get("References")
                # print(f"json.Authorities[0].Standards.References: {j_refr}")
                if "Rule_Identifier" in j_refr[0] and "Id" in j_refr[0]["Rule_Identifier"]:
                    rule_id = j_refr[0]["Rule_Identifier"].get("Id")
        return rule_id 

    def get_file_name(self, filename, fn_root, core_id, rule_id,r_status):
        if core_id is None and rule_id is not None and re.match("^CG", rule_id):
            fn_root = rule_id
            self.stat_cnts["ruleid_used"] += 1
        # Use Core.Id or the original filename as the new file name
        if fn_root is None:
            self.stat_cnts["skipped"] += 1
            fn_root = filename.split(".")[0]
        else:
            fn_parts = fn_root.split(".")
            # print(f"FN Parts: {fn_parts}; RuleID: {rule_id}")
            if re.match("^CORE", fn_root) :
                fn_root = fn_root if rule_id is None else rule_id + '-' + core_id
                self.stat_cnts["renamed"] += 1
            else:
                if re.match("^CG", fn_parts[-1]):
                    fn_root = fn_parts[-1] + "-" + ".".join(fn_parts[:-1])
                    self.stat_cnts["renamed"] += 1
                else:
                    self.stat_cnts["coreid_used"] += 1
        r_filename = fn_root + "-" + str(r_status) + ".json"
        return r_filename

    def rename_files(self):
        # Create the output folder if it does not exist
        if not os.path.exists(self.output_folder_path):
            os.makedirs(self.output_folder_path)

        # Iterate through each file in the folder
        for filename in os.listdir(self.input_folder_path):
            # Check if file is a JSON file
            if filename.endswith(".json"):
                # Open the JSON file
                self.stat_cnts["total"] += 1
                with open(os.path.join(self.input_folder_path, filename)) as f:
                    print(f" - Processing {f.name}...")
                    json_data = json.load(f)
                    # Get the value
                    v_status = json_data.get(
                        "json", {}).get("Core", {}).get("Status")
                    core_id = self.get_core_id(json_data)
                    fn_root = core_id
                    # get rule id for each file
                    rule_id = self.get_rule_id(json_data)
                    new_filename = self.get_file_name(filename, fn_root, core_id, rule_id, v_status) 
                    # we need to check if the target file exists
                    if os.path.exists(os.path.join(self.output_folder_path, new_filename)):
                        self.stat_cnts["dupped"] += 1 
                        print (f"   File - {new_filename}: exists.")
                        new_filename = core_id + "-" + str(self.stat_cnts["dupped"]) + ".json"
                    # Write the JSON data to the new file
                    with open(os.path.join(self.output_folder_path, new_filename), 'w') as f2:
                        json.dump(json_data, f2, indent=4)
                    if core_id is None:
                        print (f"   Skipped: {f.name}")
                    else:
                        print (f"   Renamed: {new_filename} ")

        print(f"Total: {self.stat_cnts['total']}\nRenamed: {self.stat_cnts['renamed']}")
        print(f"Skipped: {self.stat_cnts['skipped']}\nDupped: {self.stat_cnts['dupped']}")
        print(f"RuleID Used: {self.stat_cnts['ruleid_used']}\nCoreID Used: {self.stat_cnts['coreid_used']}")


    def extract_rules(self):
        # Create an empty dataframe
        df = pd.DataFrame(columns=["core_id","rule_id","id", "created", "changed", 
                                   "json.Core.Id", "json.Core.Version",
                                   "json.Core.Status", "json.Rule_Type", "json.Sensitivity",
                                   "json.Description", "json.Outcome", "json.Authorities",
                                   "json.Scope", "json.Scope.Classes.Include", 
                                   "json.Scope.Domains.Include",
                                   "json.Check", "content"])

        # Loop through all JSON files in the folder
        rows = []
        for filename in os.listdir(self.input_folder_path):
            if filename.endswith(".json"):
                # Read JSON file
                with open(os.path.join(self.input_folder_path, filename)) as f:
                    data = json.load(f)

                # Extract required fields if they exist
                row = {"core_id": None, "rule_id": None, "id": None, "created": None, "changed": None, 
                       "json.Core.Id": None,
                       "json.Core.Version": None, "json.Core.Status": None, "json.Rule_Type": None,
                       "json.Sensitivity": None, "json.Description": None, "json.Outcome": None,
                       "json.Authorities": None, "json.Scope": None, "json.Scope.Classes.Include": None,
                       "json.Scope.Domains.Include": None, "json.Check": None, "content": None}
                core_id = self.get_core_id(data)
                rule_id = self.get_rule_id(data)

                row.update({"core_id": core_id})
                row.update({"rule_id": rule_id})
                row.update({"id": data.get("id")})
                row.update({"created": data.get("created")})
                row.update({"changed": data.get("changed")})
                row.update({"json.Core.Id": data.get(
                    "json", {}).get("Core", {}).get("Id")})
                row.update({"json.Core.Version": data.get(
                    "json", {}).get("Core", {}).get("Version")})
                row.update({"json.Core.Status": data.get(
                    "json", {}).get("Core", {}).get("Status")})
                row.update({"json.Rule_Type": data.get("json", {}).get("Rule_Type")})
                row.update({"json.Sensitivity": data.get(
                    "json", {}).get("Sensitivity")})
                row.update({"json.Description": data.get(
                    "json", {}).get("Description")})
                row.update({"json.Outcome": data.get("json", {}).get("Outcome")})
                row.update({"json.Authorities": data.get(
                    "json", {}).get("Authorities")})
                row.update({"json.Scope": data.get("json", {}).get("Scope")})
                row.update({"json.Scope.Classes.Include": data.get("json", {}).get(
                    "Scope", {}).get("Classes", {}).get("Include")})
                row.update({"json.Scope.Domains.Include": data.get("json", {}).get(
                    "Scope", {}).get("Domains", {}).get("Include")})
                row.update({"json.Check": data.get("json", {}).get("Check")})
                row.update({"content": data.get("content")})

                # Append row to list of rows
                rows.append(row)

        # Create dataframe from list of rows
        df = pd.DataFrame.from_records(rows)
        return df 
    

    def write_rules2xlsx(self, xlsx_file, df_rules = None ):
        # Write dataframe to xlsx file
        if not os.path.exists(self.output_folder_path):
            os.makedirs(self.output_folder_path)

        opf_name = os.path.join(self.output_folder_path, xlsx_file)

        if df_rules is None:  
            df_rules = self.extract_rules()
        df_rules.to_excel(opf_name, index=False)
        print(f"Output to {opf_name}")


# End of the file
