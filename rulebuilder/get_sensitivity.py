# Purpose: Get json.Sensitivity for a rule 
# -----------------------------------------------------------------------------
# History: MM/DD/YYYY (developer) - description
#   03/14/2023 (htu) - ported from proc_rules_sdtm as get_sensitivity module
#   03/15/2023 (htu) - added "import re"
#   03/21/2023 (htu) -
#     10. Rule Type and Sensitivity should be left null
#    

import re 

def get_sensitivity(rule_data):
    """
    ===============
    get_sensitivity
    ===============
    This method builds the json.Sensitivity element in the core rule.

    Parameters:
    -----------
    rule_data: dataframe
        a data frame containng all the records for a rule. It can be obtained from
        read_rules and select the records from the rule definition data frame.

    returns
    -------
        r_str: a string for json.Sensitivity

        possible sensitivities: 
          - Domain
          - Dataset
          - Study
          - Record
          - Variable
          - Term 


    Raises
    ------
    ValueError
        None

    """
 
    if not rule_data.empty:
        return None


    r_condition = rule_data.iloc[0]["Condition"]
    # r_rule = rule_data.iloc[0]["Rule"]
    r_str = "Record"
    if r_condition is not None:
        pattern = r"^(study|dataset|domain|variable|term)"
        # Use the re.search() method to search for the pattern in the input string
        match = re.search(pattern, r_condition, re.IGNORECASE)
        # Check if a match was found
        if match:
            # Convert the matched keyword to lowercase and capitalize the first letter
            r_str = match.group(1).lower().capitalize()
        else:
            # No match found
            print(f"No match found from {r_condition}")
    return r_str


    