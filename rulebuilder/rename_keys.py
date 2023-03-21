# Purpose: Rename nested keys in a dictionary object
# -----------------------------------------------------------------------------
# History: MM/DD/YYYY (developer) - description
#   03/20/2023 (htu) - initial coding
#
#

import re

def rename_keys(d, regex:re = r'[_]', replacement:str = " ", mapping=None):
    """
    Rename keys in a dictionary object recursively
    :param d: the input dictionary object
    :param mapping: a dictionary containing the old key names as keys and the new key names as values
    :param regex: a regular expression pattern to match against key names
    :param replacement: the character to replace the matched pattern with
    :return: the modified dictionary object
    """
    if mapping is None:
        mapping = {}
    if isinstance(d, dict):
        for k1, v1 in list(d.items()):
            if k1 in mapping:
                k2 = mapping[k1]
            elif re.search(regex, k1):
                k2 = re.sub(regex, replacement, k1)
                # k2 = re.sub(re2,replacement,k2)
            else:
                k2 = k1
            d[k2] = d.pop(k1)
            if isinstance(v1, dict):
                d[k2] = rename_keys(v1, regex, replacement, mapping)
            elif isinstance(v1, list):
                for i, item in enumerate(v1):
                    v1[i] = rename_keys(item,  regex, replacement, mapping)
    return d



# Test cases
if __name__ == "__main__":
    d = {'a_1': 1, 'b__1': {'c': 2, 'd___1': 3, 'e-1': {'f-1': 4, 'g__1': 5}}}
    mapping = {}
    regex = r'[_-]'
    replacement = ' '
    d = rename_keys(d, regex, replacement, mapping)
    print(d)
    # Output: {'a 1': 1, 'b  1': {'c': 2, 'd   1': 3, 'e 1': {'f 1': 4, 'g  1': 5}}}


