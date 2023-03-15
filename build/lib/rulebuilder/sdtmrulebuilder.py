# Purpose: Build a CDISC Core Rule based on rule definition in a standard 
# -----------------------------------------------------------------------------
# History: MM/DD/YYYY (developer) - description
#   03/14/2023 (htu) - initial coding 
#   03/15/2023 (htu) - change "import yaml" to "import ruamel.yaml as yaml"
#  

import pandas as pd
import ruamel.yaml as yaml
import json
import ssl
import urllib.request

from .proc_sdtm_rules import proc_sdtm_rules


class SDTMRuleBuilder:
    def __init__(self,
                yaml_file="./data/target/SDTM_and_SDTMIG_Conformance_Rules_v2.0.yaml",
                core_base_url = "https://raw.githubusercontent.com/cdisc-org/conformance-rules-editor/main/public/schema/CORE-base.json",
                creator_url="https://rule-editor.cdisc.org/.auth/me",
                existing_rule_dir="./data/output/json_rules1",
                output_dir="./data/output"
                 ):
        # Variables:
        #   yaml_file           - contain rule definitions 
        #   core_base_url       - Core rule schema 
        #   creator_url         - to get user GUID
        #   existing_rule_dir   - folder containing all the existing rules
        #   output_dir          - folder where the new or updated rules will be output to
        # 
        self.yaml_file          = yaml_file 
        self.core_base_url      = core_base_url
        self.creator_url        = creator_url
        self.existing_rule_dir  = existing_rule_dir
        self.output_dir         = output_dir

    def get_schema(self,base_url=None):
        url = self.core_base_url if base_url is None else base_url 
        # Fetch the contents of the URL and parse it as JSON
        with urllib.request.urlopen(url) as response:
            raw_data = response.read().decode()
            json_data = json.loads(raw_data)
        return json_data

    def get_creator_id(self,creator_url=None):
        ctr_url = self.creator_url if creator_url is None else creator_url 
        with urllib.request.urlopen(ctr_url) as rsp:
            raw_data = rsp.read().decode()
            creator_data = json.loads(raw_data)
        print(f"Creator Data: {creator_data}")
        if creator_data.get("clientPrincipal") is None:
            creator_id = "dd0f9aa3-68f9-4825-84a4-86c8303daaff"
        else:
            creator_id = creator_data["clientPrincipal"].get("userId")
            if creator_id is None:
                creator_id = "dd0f9aa3-68f9-4825-84a4-86c8303daaff"
            else:
                print(f"creator_data['clientPrincipal'].get('userDetails')")
        return creator_id 

    def read_rules(self, yaml_file=None):
        yaml_file = self.yaml_file if yaml_file is None else yaml_file 
        # 1.2 Read rule definition file (YAML file)
        with open(yaml_file, "r") as f:
            yaml_data = yaml.safe_load(f)
        # print(yaml_data[0])

        # Create DataFrame from YAML data
        df_yaml = pd.DataFrame(yaml_data)
        return df_yaml 

    def build(self, rule_list=None):
        ssl._create_default_https_context = ssl._create_unverified_context
        # 1. get all the input variables
        creator_id = self.get_creator_id()
        df_yaml = self.read_rules()

        # 2. Build a rule template

        # Create the main JSON object with the specified properties
        json_obj = {
            "id": "example-id",
            "created": "2023-03-08T12:00:00Z",
            "changed": "2023-03-08T12:00:00Z",
            # "creator": {"id": str(uuid.uuid4())},
            "creator": {"id": creator_id},
            "content": "example-content",
            "json": {
                # "properties": json_data["properties"]
                "Check": None,
                "Core": None,
                "Description": None,
                "Outcome": {},
                "Rule_Type": None,
                "Sensitivity": None,
                "Authorities": [],
                "Scope": {},
                "Executability": None
            }
        }
        rule_list = ("CG0373", "CG0378", "CG0379") if rule_list is None else rule_list 
        proc_sdtm_rules(df_yaml, json_obj, rule_list,
                        self.existing_rule_dir,  self.output_dir)



# End of File 