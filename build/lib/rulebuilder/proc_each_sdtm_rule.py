# Purpose: Process a CDISC Core Rule 
# -----------------------------------------------------------------------------
# History: MM/DD/YYYY (developer) - description
#   03/14/2023 (htu) - ported from proc_rules_sdtm as proc_each_sdtm_rule module
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



def proc_each_sdtm_rule (rule_data,rule_tmp, rule_id: str, in_rule_folder):
    print (f"Rule_ID: {rule_id}")
    # print (f"Rule Data: {rule_data}")
    # print(f"Schema Data: {rule_tmp.keys()}")
    rule_obj = rule_tmp
    
    # get existing rule if it exists
    json_exist_rule = get_existing_rule(rule_id, in_rule_folder)

    # get rule GUID 
    rule_obj["id"] = get_rule_guid(json_exist_rule)
    
    # format the date and time as a string in the format "2023-03-08T12:00:00Z"
    rule_obj["created"] = json_exist_rule.get("created")
    rule_obj["changed"] = json_exist_rule.get("changed") 
    
    # get json Core 
    rule_obj["json"]["Core"] = get_core(rule_id)
    
    # get json Description
    # print(f"Rule Data: {rule_data.iloc[0]['Condition']}")
    rule_obj["json"]["Description"] = get_desc(rule_data)

    # get json Message 
    rule_obj["json"]["Outcome"] = {"Message": get_jmsg(rule_data)} 

    # get json Rule_Type
    rule_obj["json"]["Rule_Type"] = get_rtype(rule_data)
    
    # get json Sensitivity
    rule_obj["json"]["Sensitivity"] = get_sensitivity(rule_data)

    # get json Authorities 
    rule_obj["json"]["Authorities"] = get_authorities(rule_data)

    # get json Scope       
    rule_obj["json"]["Scope"] = get_scope(rule_data)

    # get json Exeutability 
    rule_obj["json"]["Executability"] = get_executability(rule_data)

    # get checks
    rule_obj["json"]["Check"] = {"Check": get_check(rule_data)}  

    # print out the result 
    # print(json.dumps(rule_obj, indent=4))
    
    return rule_obj

