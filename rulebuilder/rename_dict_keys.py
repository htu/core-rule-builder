# Purpose: Rename nested keys in a dictionary object 
# -----------------------------------------------------------------------------
# History: MM/DD/YYYY (developer) - description
#   03/20/2023 (htu) - initial coding 
#
#

import json

def rename_dict_keys (a_dict, str_a: str="_", str_b: str=" "):
    """
    =================
    rename_dict_keys 
    =================
    This method renames keys nested in a python dictionary object. 

    Parameters:
    -----------
    a_dict: dict
        a dict object 

    returns
    -------
        dict_modified 

    Raises
    ------
    ValueError
        None

    """

    d = a_dict 
    for key in d.keys():
        if str_a in key:
            new_key = key.replace(str_a, str_b)
            d[new_key] = d.pop(key)
    return d 

# Output: {'key one': 1, 'key two': 2, 'key three': {'nested key one': 3, 'nested key two': 4}}

# Test cases
if __name__ == "__main__":
    d = {'key_one': 1, 'key_two': 2, 'key_three': {
        'nested_key_one': 3, 'nested_key_two': 4,
        'lvl_3': {'l3a':5, 'l3b':6 }}}
    
    json.dumps(d, indent=4)
    d = rename_dict_keys(d, '_', " ")
    
    print(d)
