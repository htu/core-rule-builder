# Purpose: Get json.Description for a rule 
# -----------------------------------------------------------------------------
# History: MM/DD/YYYY (developer) - description
#   03/14/2023 (htu) - 
#     1. ported from proc_rules_sdtm.py and modulized as get_desc
#     2. included the dependent methods: get_jmsg, compose_desc, and 
#        replace_operator
#   03/15/2023: added "import re" 
#    
#
import re 

def replace_operator(match):
    operator = match.group(1)
    if operator == "=":
        return "not equal to"
    elif operator == "^=":
        return " is  "
    elif operator == "in":
        return " not in ("   

def compose_desc(input_str: str):
    if input_str == None: 
        return None 
    # Define a regular expression pattern to match =, ^=, and in
    re_pattern = r"(\^=|=|\bin\b\()"
    return re.sub(re_pattern, replace_operator, input_str)


def get_jmsg(rule_data):
    r_condition = rule_data.iloc[0]["Condition"]
    r_rule = rule_data.iloc[0]["Rule"]
    print(f"Conditon: {r_condition}, Rule: {r_rule}")
    # r_desc1 = compose_desc(r_condition)
    r_desc1 = None
    r_desc2 = compose_desc(r_rule)
    r_desc3 = r_desc2 if r_desc1 is None else r_desc1 + " and " + r_desc2
    return r_desc3  


def get_desc(rule_data):
    return "Trigger error when " + get_jmsg(rule_data)

