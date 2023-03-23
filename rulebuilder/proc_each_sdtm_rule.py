# Purpose: Process a CDISC Core Rule 
# -----------------------------------------------------------------------------
# History: MM/DD/YYYY (developer) - description
#   03/14/2023 (htu) - ported from proc_rules_sdtm as proc_each_sdtm_rule module
#   03/21/2023 (htu) - 
#     1. resolved: 07. Replace Check: Check: null with Check: null
#     2. added v_status and return existing rule if it is Published
#   03/22/2023 (htu) - added logic to use json_exist_rule
#    

from .get_existing_rule import get_existing_rule
from .get_rule_guid import get_rule_guid
from .get_core import get_core
from .get_desc import get_desc, get_jmsg

from .get_rtype import get_rtype
from .get_sensitivity import get_sensitivity
from .get_authorities import get_authorities
from .get_scope import get_scope


from .get_executability import get_executability
from .get_check import get_check



def proc_each_sdtm_rule (rule_data,rule_tmp, rule_id: str, in_rule_folder,cnt_published):
    print (f"Rule_ID: {rule_id}")
    # print (f"Rule Data: {rule_data}")
    # print(f"Schema Data: {rule_tmp.keys()}")
    rule_obj = rule_tmp
    
    # get existing rule if it exists
    json_exist_rule = get_existing_rule(rule_id, in_rule_folder)
    v_status = json_exist_rule.get("json",{}).get("Core",{}).get("Status")
    v_autho = get_authorities(rule_data, exist_rule_data=json_exist_rule)
    if v_status == "Published":
        cnt_published += 1
        json_exist_rule["json"]["Authorities"] = v_autho 
        return json_exist_rule
    
    # get rule GUID 
    rule_obj["id"] = get_rule_guid(json_exist_rule)
    
    # format the date and time as a string in the format "2023-03-08T12:00:00Z"
    rule_obj["created"] = json_exist_rule.get("created")
    rule_obj["changed"] = json_exist_rule.get("changed") 
    
    # get json Core 
    rule_obj["json"]["Core"] = get_core(
        rule_id, exist_rule_data=json_exist_rule)
    
    # get json Description
    # print(f"Rule Data: {rule_data.iloc[0]['Condition']}")
    rule_obj["json"]["Description"] = get_desc(
        rule_data, exist_rule_data=json_exist_rule)

    # get json Message 
    v_jmsg = get_jmsg(rule_data, exist_rule_data=json_exist_rule)
    rule_obj["json"]["Outcome"] = {"Message": v_jmsg}

    # get json Rule_Type
    rule_obj["json"]["Rule_Type"] = get_rtype(
        rule_data, exist_rule_data=json_exist_rule)
    
    # get json Sensitivity
    rule_obj["json"]["Sensitivity"] = get_sensitivity(
        rule_data, exist_rule_data=json_exist_rule)

    # get json Authorities 
    rule_obj["json"]["Authorities"] = v_autho

    # get json Scope       
    rule_obj["json"]["Scope"] = get_scope(rule_data)

    # get json Exeutability 
    rule_obj["json"]["Executability"] = get_executability(rule_data)

    # get checks
    # rule_obj["json"]["Check"] = {"Check": get_check(rule_data)}  
    rule_obj["json"]["Check"] = get_check(rule_data)  

    # print out the result 
    # print(json.dumps(rule_obj, indent=4))
    
    return rule_obj


