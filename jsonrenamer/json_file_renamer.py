import os
import json
import re 

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
            core_id = json_data["json"]["Core"].get("Id")
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

    def get_file_name(self, filename, fn_root, core_id, rule_id):
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
        r_filename = fn_root + ".json"
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
                    core_id = self.get_core_id(json_data)
                    fn_root = core_id
                    # get rule id for each file
                    rule_id = self.get_rule_id(json_data)
                    new_filename = self.get_file_name(filename, fn_root, core_id, rule_id) 
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
