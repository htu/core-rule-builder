# Purpose: RDecode Class in rule definition records 
# -----------------------------------------------------------------------------
# History: MM/DD/YYYY (developer) - description
#   03/22/2023 (htu) - initial coding 
# 

import os
import pandas as pd

def decode_classes(df_data):

    class_map = {"EVT": "EVENTS", "FND": "FINDINGS", "INT": "INTERVENTIONS",
                "SPC": "SPECIAL PURPOSE", "TDM": "TRIAL DESIGN"
                }
    df_class = {}
    df_class['Class'] = df_data['Class'].apply(
        lambda x: [class_map.get(i.strip()) for i in x.split(',')])
    print(df_class)
    r_lst = []
    return r_lst 


# Test cases
if __name__ == "__main__":
    # set input parameters
    v_prg = __name__ + "::decode_classes"
    os.environ["g_lvl"] = "3"

    d1 = {"1": "One", "2": "Two", "5": "Five"}

    # Sample DataFrame
    df_data = pd.DataFrame({"Class": ["EVT, INT", "EVT, INT", "EVT, INT"],
                      "Domain": ["NOT(DS, DV, EX)", "NOT(DS, DV, EX)", "NOT(DS, DV, EX)"]})
    d1 = decode_classes(df_data)

    # Define a function to convert a number to its corresponding word using the given dictionary


    def convert_num_to_word(num, lookup_dict):
        return lookup_dict.get(str(num), num)


    # Use applymap with a lambda function to apply the conversion function to each element of the DataFrame
    df = pd.DataFrame({"A": [1, 2, 3], "B": [4, 5, 6], "C": [7, 8, 9]})
    df = df.applymap(lambda x: convert_num_to_word(x, d1))

    # Output the resulting DataFrame
    print(df)
