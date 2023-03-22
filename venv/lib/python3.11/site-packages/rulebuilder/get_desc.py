# Purpose: Get json.Description for a rule 
# -----------------------------------------------------------------------------
# History: MM/DD/YYYY (developer) - description
#   03/14/2023 (htu) - 
#     1. ported from proc_rules_sdtm.py and modulized as get_desc
#     2. included the dependent methods: get_jmsg, compose_desc, and 
#        replace_operator
#   03/15/2023: added "import re" 
#   03/21/2023 (htu) - 
#     1. added docstring and test cases
#     2. combine the compose_desc into replace_operator 
#     3. extracted out replace_operator function 
#     4. extracted out get_jmsg
#    
#
import pandas as pd
import os 
from rulebuilder.echo_msg import echo_msg
from rulebuilder.get_jmsg import get_jmsg


def get_desc(rule_data):
    """
    Returns a string describing the trigger condition based on the given rule data.

    Args:
        rule_data: A Pandas DataFrame containing the rule data.

    Returns:
        A string describing the trigger condition.

    Raises:
        None.
    """
    jmsg = get_jmsg(rule_data)
    print(f"jmsg: {jmsg}")  # Debugging print statement
    desc = "Trigger error when " + jmsg
    print(f"desc: {desc}")  # Debugging print statement
    return desc

# Test cases
if __name__ == "__main__":
    v_prg = __name__ + "::get_desc"
    os.environ["g_lvl"] = "1"
    v_stp = 1.0
    echo_msg(v_prg, v_stp, "Test Case 01: Basic Parameter",1)

    # Create a test dataframe
    data = {'Condition': ['a = b'], 'Rule': ['c in (1, 2, 3)']}
    df = pd.DataFrame(data)

    # Test case 1: Test the function with a given rule data
    assert get_desc(df) == 'Trigger error when a not equal to b and c not in (1, 2, 3)'

    # Test case 2: Test the function with None values in the rule data
    data2 = {'Condition': [None], 'Rule': ['a = b']}
    df2 = pd.DataFrame(data2)
    assert get_desc(df2) == 'Trigger error when a not equal to b'

    # Test case 3: Test the function with an unknown operator in the rule data
    data3 = {'Condition': ['a ^ b'], 'Rule': ['c in (1, 2, 3)']}
    df3 = pd.DataFrame(data3)
    assert get_desc(df3) == 'Trigger error when a ^ b and c not in (1, 2, 3)'

    # Test case 4: Test the function with multiple conditions and rules
    data4 = {'Condition': ['a = b', 'c = d'], 'Rule': ['e in (1, 2, 3)', 'f = g']}
    df4 = pd.DataFrame(data4)
    assert get_desc(
        df4) == 'Trigger error when a not equal to b and e not in (1, 2, 3)'

    print("All test cases passed.")
