# Purpose: Get json.Rule_Type for a rule 
# -----------------------------------------------------------------------------
# History: MM/DD/YYYY (developer) - description
#   03/14/2023 (htu) - ported from proc_rules_sdtm as get_rtype module
#   03/15/2023 (htu) - added "import re"
#    

import re 

def get_rtype(rule_data):
    # possible rule type: 
    #  - Dataset Contents Check against Define XML and Library Metadata
    #  - Dataset Metadata Check
    #  - Dataset Metadata Check against Define XML
    #  - Define-XML
    #  - Domain Presence Check
    #  - Record Data
    #  - Value Level Metadata Check against Define XML
    #  - Variable Metadata Check
    #  - Variable Metadata Check against Define XML
    r_condition = rule_data.iloc[0]["Condition"]
    # r_rule = rule_data.iloc[0]["Rule"]
    r_str = "Record Data"
    if r_condition is not None:
        pattern = r"^(study|dataset)"
        # Use the re.search() method to search for the pattern in the input string
        match = re.search(pattern, r_condition, re.IGNORECASE)
        # Check if a match was found
        if match:
            # Convert the matched keyword to lowercase and capitalize the first letter
            r_str = match.group(1).lower().capitalize()
        else:
            # No match found
            print (f"No match found from {r_condition}")
    return r_str 


    