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
#   03/20/2023 (htu) - 
#     1. worked on issues 01 and 02 and added rename_keys 
#     2. added cnt_published 
#   03/22/2023 (htu) - used build_rule_yaml to get a_yaml 
#   03/24/2023 (htu) - added reset_index(drop=True) to resolve subset index issue
#   03/29/2023 (htu) -
#     1. removed rule_template and it gets it from get_existing_rule
#     2. added s_version, s_class, s_domain 
#   03/30/2023 (htu) - 
#     1. used and tested proc_each_yaml
#     2. added log_dir and log files 
#   04/03/2023 (htu): 
#     1. added pub2db, db_name and ct_name parameters
#     2. used get_db_cfg, create_log_dir and publish_a_rule 
#   04/04/2023 (htu) - 
#     1. added get_doc_stats and step 1.42 
#     2. added r_ids to publish_a_rule
#   04/05/2023 (htu) - 
#     1. added get_db_rule for getting rule doce from DB
#     2. updated get_existing_rule parameters at step 3.4 
#     3. updated proc_each_yaml parameters at step 3.5
#  

# import ruamel.yaml as yaml
import os
import pandas as pd
import sys 
import json 
from rulebuilder.echo_msg import echo_msg
from rulebuilder.read_rules import read_rules
# from rulebuilder.get_creator_id import get_creator_id
from rulebuilder.get_existing_rule import get_existing_rule
# from rulebuilder.proc_each_sdtm_rule import proc_each_sdtm_rule
from rulebuilder.output_rule2file import output_rule2file
from rulebuilder.build_rule_yaml import build_rule_yaml
from rulebuilder.proc_each_yaml import proc_each_yaml
from dotenv import load_dotenv
# from datetime import datetime, timezone
import datetime as dt 
from rulebuilder.create_log_dir import create_log_dir
from rulebuilder.get_db_cfg import get_db_cfg
from rulebuilder.publish_a_rule import publish_a_rule
from rulebuilder.get_doc_stats import get_doc_stats

def proc_sdtm_rules(df_data=None, in_rule_folder:str=None, 
                    out_rule_folder:str=None, 
                    rule_ids: list = ["CG0001"],s_version: list = [], 
                    s_class: list = [], s_domain: list = [],
                    wrt2log: int = 0, pub2db: int = 0,
                    get_db_rule: int = 0,
                    db_name:str=None, ct_name:str=None 
                    ) -> None:
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

    Comments from Gerry Campion:  
    *01. For the yaml files, only the contents within the json property are 
        required. The other properties are only required in the json file.
    *02. The property names in the yaml file should not have underscores. The 
        property names in the json file should have underscores.
    03. I recommend copying the sample yaml rule into the rule editor. The 
        schema will alert you of most of the structure issues.
    *04. Variable, Condition, and Rule columns should be mapped to comments in
        the beginning of the YAML file (comments start with #) (see table 
        above). These won't appear in the json property in the json file 
        because json does not allow comments.
    05. I would like to see an example with different Class and Domain other 
        than ALL
    *06. If Item is empty, don't include the Item property for the citation
    *07. Replace Check: Check: null with Check: null
    *08. Don't add Core.Id
    09. Description and Outcome.Message - I'm curious how you are generating 
        these?
    *10. Rule Type and Sensitivity should be left null
    11. I noticed these samples include rules merged from multiple rows in 
        the source spreadsheet. I was expecting to see a sample for each row 
        in the spreadsheet. Then, a second step would merge the rules from 
        multiple rows for each rule id and also merge them with the rule ids 
        in the core database. Is this following a different strategy?


    """
    v_prg = __name__ 
    st_all = dt.datetime.now()
    load_dotenv()
    now_utc = dt.datetime.now(dt.timezone.utc)
    w2log = os.getenv("write2log")
    log_dir = os.getenv("log_dir")
    job_id = now_utc.strftime("%Y%m%d_%H%M%S")
    rst_fn = log_dir + "/crb-" + job_id + ".xlsx"
    w2log = 0 if w2log is None else int(w2log)
    if w2log > wrt2log:
        wrt2log = w2log 
    # 0. set up log first 
    log_cfg = create_log_dir(job_id=job_id, fn_root="crb", fn_sufix="xlsx", 
                             wrt2log=wrt2log)
    log_fdir = log_cfg["log_fdir"]

    # 1. get inputs
    # -----------------------------------------------------------------------
    v_stp = 1.0
    v_msg = "Check input parameters..."
    echo_msg(v_prg, v_stp, v_msg,1)
    yaml_file = os.getenv("yaml_file")

    if df_data is None:
        v_stp = 1.1
        v_msg = "Get Rule Data from " + yaml_file
        echo_msg(v_prg, v_stp, v_msg, 2)
        if not os.path.isfile(yaml_file):
            v_stp = 1.11
            v_msg = "Could not find file - " + yaml_file
            return 
        df_data = read_rules(yaml_file)

    if in_rule_folder is None:
        in_rule_folder = os.getenv("existing_rule_dir")

    if out_rule_folder is None:
        out_rule_folder = os.getenv("output_dir")

    if not os.path.exists(in_rule_folder):
        v_stp = 1.1
        v_msg = "Could not find input rule folder: " + in_rule_folder
        echo_msg(v_prg, v_stp, v_msg,2)
        return 

    if not os.path.exists(out_rule_folder):
        v_stp = 1.2
        v_msg = "Could not find output rule folder: " + out_rule_folder
        echo_msg(v_prg, v_stp, v_msg,2)
        v_msg = "Making dir - " + out_rule_folder
        echo_msg(v_prg, v_stp, v_msg, 2)
        os.makedirs(out_rule_folder)

    num_records_processed = df_data.shape[0]
    v_stp = 1.3
    if num_records_processed < 1:
        v_msg = "No record find in the rule definition data set."
        echo_msg(v_prg, v_stp, v_msg,0)
        return
    else:
        v_msg = "INFO:Total number of records: " + str(num_records_processed)
        echo_msg(v_prg, v_stp, v_msg,2)

    v_stp = 1.4 
    if pub2db > 0:
        if db_name is None and ct_name is None:
            v_msg = "When publishing to a DB, database and container names are required."
            echo_msg(v_prg, v_stp, v_msg, 0)
            return
        db_cfg = get_db_cfg(db_name=db_name,ct_name=ct_name)
        if 'ct_conn' not in db_cfg.keys(): 
            v_msg = "Could not create container connection for C/D: {ct_name}/{db_name}"
            echo_msg(v_prg, v_stp, v_msg, 0)
            return
        v_stp = 1.42
        r_ids = get_doc_stats(db=db_name,ct=ct_name,wrt2file=wrt2log)

    # 2. Group data by Rule ID
    # -----------------------------------------------------------------------
    v_stp = 2.0 
    v_msg = "Filtering and Grouping data..."
    echo_msg(v_prg, v_stp, v_msg,1)
    
    # 2.1 select by standard version
    v_stp = 2.1 
    num_selected = len(s_version)
    df = df_data if num_selected == 0 else df_data[
        df_data["SDTMIG Version"].isin(s_version)]
    v_msg = "Select by IG Version (" + ", ".join(s_version) + "): " + str(df.shape[0])
    echo_msg(v_prg, v_stp, v_msg,2)

    # 2.2 select by class
    v_stp = 2.2
    num_selected = len(s_class)
    df = df if num_selected == 0 else df[df["Class"].isin(s_class)]
    v_msg = "Select by Class (" + ", ".join(s_class) + "): " + str(df.shape[0])
    echo_msg(v_prg, v_stp, v_msg, 2)

    # 2.3 select by domain 
    v_stp = 2.3
    num_selected = len(s_domain)
    df = df if num_selected == 0 else df[df["Domain"].isin(s_domain)]
    v_msg = "Select by Domain (" + ", ".join(s_domain) + "): " + str(df.shape[0])
    echo_msg(v_prg, v_stp, v_msg, 2)

    # 2.4 select by rule ids
    v_stp = 2.4
    num_selected = len(rule_ids)
    df = df if num_selected == 0 else df[df["Rule ID"].isin(rule_ids)]
    v_msg = "Select by Rule IDs (" + ", ".join(rule_ids) + "): " + str(df.shape[0])
    echo_msg(v_prg, v_stp, v_msg, 2)

    v_msg  = "INFO:Selected number of rules: " + str(df.shape[0])
    v_msg += "/" + str(num_records_processed)
    echo_msg(v_prg, v_stp, v_msg,1)

    # 3. Loop through each rule 
    # -----------------------------------------------------------------------

    v_stp = 3.0
    v_msg = "Group the rules and looping through each rules..."
    echo_msg(v_prg, v_stp, v_msg,1)

    grouped_data = df.groupby("Rule ID")

    # Loop through each Rule ID and print out required information

    df_log = pd.DataFrame(columns=["rule_id", "core_id",  "user_id", "guid_id", 
                                   "created", "changed", "rule_status", "version", 
                                   "class", "domain", "variable", "rule_type", 
                                   "document", "section", "sensitivity",
                                   "publish_status"])
    rows = []
    fn_sufix = now_utc.strftime("%dT%H%M%S.txt")
    for rule_id, group in grouped_data:
        st_row = dt.datetime.now()
        log_fn = f"{log_fdir}/{rule_id}-{fn_sufix}" 
        os.environ["log_fn"] = log_fn
        # if rule_id not in rule_ids: continue 
        num_records = group.shape[0]
        row = {"rule_id": None, "core_id": None,  "user_id": None,"guid_id":None, 
               "created": None, "changed": None, "rule_status": None,"version":None,
               "class":None, "domain": None,"variable":None, "rule_type": None,
               "document": None, "section": None, "sensitivity": None, 
               "publish_status": None}
        row.update({"rule_id":rule_id})

        # 3.1 show rule id and number of records in the group
        v_stp = 3.1
        v_msg = "  Rule ID: (" + rule_id + ") with " + str(num_records) + " records."
        echo_msg(v_prg, v_stp, v_msg,2)
        
        # 3.2 display the group if message level is 5 or over
        v_stp = 3.2
        v_msg = "INFO: Group {" + str(group) + "}"
        echo_msg(v_prg, v_stp, v_msg, 5)
        # print(f"Group: {group}")

        # 3.3 select the records for the group 
        v_stp = 3.3
        v_msg = "Select the records for rule id = " + rule_id 
        echo_msg(v_prg, v_stp, v_msg, 3)
        a_json = {} 
        rule_data = None 
        # rule_data = df_selected[df_data["Rule ID"] == rule_id]
        rule_data = df[df["Rule ID"] == rule_id]
        rule_data = rule_data.reset_index(drop=True)

        # 3.4 read in the existing rule
        v_stp = 3.4 
        rule_obj = get_existing_rule(rule_id, in_rule_folder, 
                                     get_db_rule=get_db_rule, r_ids=r_ids,
                                     db_name=db_name,ct_name=ct_name,
                                     use_yaml_content=False)
        print("------------------------------------------")
        json.dump(rule_obj, sys.stdout, indent=4)

        # 3.5 process the rule 
        # 
        # a_json = proc_each_sdtm_rule(
        #     rule_data, rule_obj, rule_id, in_rule_folder, cnt_published)
        v_stp = 3.5 
        a_json = proc_each_yaml(rule_id,rule_data, rule_obj=rule_obj,
                                rule_dir=in_rule_folder,r_ids=r_ids,
                                get_db_rule=get_db_rule,db_name=db_name,ct_name=ct_name)
        a = a_json 
        r_status = a.get("status")
        if r_status is None or r_status != "new":
            r_status = a.get("json", {}).get("Core", {}).get("Status")
        row.update({"core_id": a.get("json",{}).get("Core",{}).get("Id")})
        row.update({"user_id": a.get("creator",{}).get("id")})
        row.update({"guid_id": a.get("id")})
        row.update({"created": a.get("created")})
        row.update({"changed": a.get("changed")})
        row.update({"rule_status": r_status})
        row.update({"rule_type": a.get("json", {}).get("Rule_Type")})
        row.update({"sensitivity": a.get(
            "json", {}).get("Sensitivity")})

        row.update(
            {"version": rule_data["SDTMIG Version"].str.cat(sep="; ")})

        v_classes = list(
            set([c for classes in rule_data['Class'] for c in classes]))
        v_c = ", ".join(v_classes)
        row.update({"class": v_c  })

        v_doms = list(
            set([d for doms in rule_data['Domain'] for d in doms]))
        v_d = ", ".join(v_doms)
        row.update({"domain": v_d })

        row.update({"variable": rule_data["Variable"].str.cat(sep = "; ")})
        row.update({"document": rule_data["Document"].str.cat(sep = "; ")})
        row.update({"section": rule_data["Section"].str.cat(sep = "; ")})
        # Append row to list of rows

        # 3.6 build yaml content
        a_json["content"] = None 
        # # Only get json for YAML
        # dict_yaml = a_json["json"]
        # print(f"Dict Keys: {dict_yaml.keys()}")
        # # Replace "_" with " " for columns
        # d_yaml = rename_keys(dict_yaml, '_', ' ')
        # a_yaml = yaml.dump(d_yaml, default_flow_style=False)
        a_yaml = build_rule_yaml(rule_data,a_json)

        # 3.7 output the rule to json and yaml files
        output_rule2file(rule_id, a_json, a_yaml, out_rule_folder)

        # 3.8 publish the rule 
        if pub2db == 1:
            a_row= publish_a_rule(rule_id=rule_id,db_cfg=db_cfg,r_ids=r_ids)
            row.update({"publish_status": a_row["publish_status"]})

        # 3.9 Append the status record to rows
        rows.append(row)
        et_row = dt.datetime.now()
        st = st_row.strftime("%Y-%m-%d %H:%M:%S")
        et = et_row.strftime("%Y-%m-%d %H:%M:%S")
        v_msg = f"The job {job_id} for {rule_id} was done between: {st} and {et}"
        echo_msg(v_prg, v_stp, v_msg,1)

    # End of for rule_id, group in grouped_data

    # Collect basic stats and print them out
    v_stp = 4.0 
    v_msg = "Get statistics..."
    num_unique_rule_id = grouped_data.ngroups
    v_msg = "Number of Records Processed: " + str(num_records_processed)
    v_msg += "\n   Number of Unique Rule ID: " + str(num_unique_rule_id)
    echo_msg(v_prg, v_stp, v_msg,2)

    v_stp = 4.1
    v_msg = "Output result to " + rst_fn + "..." 
    echo_msg(v_prg, v_stp, v_msg,2)
    df_log = pd.DataFrame.from_records(rows)
    df_log.to_excel(rst_fn, index=False)

    et_all = dt.datetime.now()
    st = st_all.strftime("%Y-%m-%d %H:%M:%S")
    et = et_all.strftime("%Y-%m-%d %H:%M:%S")
    v_msg = f"The job {job_id} was done between: {st} and {et}"
    echo_msg(v_prg, v_stp, v_msg,1)


# Test cases
if __name__ == "__main__":
    # set input parameters 
    os.environ["g_lvl"] = "5"
    v_prg = __name__ + "::proc_sdtm_rules"
    # rule_list = ["CG0373", "CG0378", "CG0379"]
    rule_list = ["CG0001"]
    # rule_list = []

    # 1. Test with basic parameters
    v_stp = 1.0 
    echo_msg(v_prg, v_stp, "Test Case 01: Basic Parameter",1)

    # proc_sdtm_rules(rule_ids=["CG0006"], wrt2log=True)
    # proc_sdtm_rules(rule_ids=["CG0006"], wrt2log=True)
    
    # Expected output:
    # 2. Test publishing rules 
    v_stp = 2.0 
    echo_msg(v_prg, v_stp, "Test Case 02: Publish Rules",1)
    db = 'library'
    ct = 'core_rules_dev'
    # proc_sdtm_rules(rule_ids=["CG0063"], wrt2log=True,pub2db=1,db_name=db,ct_name=ct)
    # proc_sdtm_rules(rule_ids=[], wrt2log=True,pub2db=1,db_name=db,ct_name=ct)

    # Publish to dev environme t
    ct = 'editor_rules_dev'
    # proc_sdtm_rules(rule_ids=["CG0001","CG0015", "CG0063"], wrt2log=True, pub2db=1, 
    #                 get_db_rule=1, db_name=db, ct_name=ct)

    # proc_sdtm_rules(rule_ids=["CG0002","CG0027","CG0015", "CG0063"], wrt2log=True,
    #                pub2db=1, db_name=db, ct_name=ct)
    proc_sdtm_rules(rule_ids=[], wrt2log=True, pub2db=1,
                    get_db_rule=1, db_name=db, ct_name=ct)


# End of File

