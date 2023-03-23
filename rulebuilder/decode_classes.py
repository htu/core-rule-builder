# Purpose: RDecode Class in rule definition records 
# -----------------------------------------------------------------------------
# History: MM/DD/YYYY (developer) - description
#   03/22/2023 (htu) - initial coding 
#   03/23/2023 (htu) - added proc_ap_fa,dc_class and proc_exclude

import os
import re 
import pandas as pd

def decode_classes(df_data, df_map = None):
    """
    Decodes certain classes and domains in a Pandas DataFrame and adds the decoded values to new columns.

    Args:
        df_data (pandas.DataFrame): The DataFrame to be processed.
        df_map (dict, optional): A lookup table for mapping certain class and domain values to their decoded values.
            Defaults to None.

    Returns:
        pandas.DataFrame: The updated DataFrame with decoded values in new columns.
    """
    df = df_data 
    # 1. define a lookup table
    if df_map == None: 
        df_map = {
            "class": {"EVT": "EVENTS", "FND": "FINDINGS", "INT": "INTERVENTIONS",
                      "SPC": "SPECIAL PURPOSE", "TDM": "TRIAL DESIGN", "AP": "ASSOCIATE PERSONS"
                },
            "fa": {"FND:FA": "FINDINGS ABOUT"},
            "v_pat": re.compile("NOT\(([\w ,]+)\)")
        }
    v_pat = re.compile(
        "NOT\(([\w ,]+)\)") if not df_map.get("v_pat") else df_map.get("v_pat")

    # 2. define sub functiokns 
    # print(f"FF: {fa_class['FND:FA']}")
    def proc_ap_fa (i,v_class, v_domain):
        r_bool  = False
        # 4.1.a process FA and FND
        if v_class in ("AP") and v_domain in ("ALL"):
            df.iloc[i]["Class"] = "ALL"
            df.iloc[i]["Domain"] = "AP--"
            r_bool = True
        
        # 4.1.b process FA and FND
        k1 = v_class + ":" + v_domain
        if k1 == "FND:FA":
            df.iloc[i]["Class"] = df_map["fa"].get(k1)
            r_bool = True
        return r_bool 


    def dc_class(k) :
        x = k.strip()
        r_str = df_map["class"].get(x)
        # print(f" . {x} --> {r_str}")
        return x if r_str is None else r_str
    
    def proc_exclude(i, v_row, v_typ):
        # v_str = ", ".join(v_str) if isinstance(v_str, list) else v_str
        if v_typ == "class":
            v_str = v_row.Class.upper().strip()
        else:
           v_str = v_row.Domain.upper().strip()
        match = v_pat.search(v_str)
        if match:
            s_list = pd.Series(match.group(1).split(","))
        else:
            s_list = pd.Series(v_str.split(","))
        # l_str = s_list.apply(lambda x: [dc_class(x)])
        #l_str = s_list.apply([dc_class])
        # print(f"Before: {s_list} ")
        for j in range(len(s_list)):
            s_list[j] = dc_class(s_list[j])
        #print(f"After: {s_list} ")
        
        if match:
            if v_typ == "class":
                df.iloc[i]['Class'] = []
                df.iloc[i]['Classes_Exclude'] = s_list.tolist()
            if v_typ == "domain":
                df.iloc[i]['Domain'] = []
                df.iloc[i]['Domains_Exclude'] = s_list.tolist()
        else:
            if v_typ == "class":
                df.iloc[i]['Class'] = s_list.tolist()
            if v_typ == "domain":
                df.iloc[i]['Domain'] = s_list.tolist()

        # End of proc_exclude 

    # 3. add two columns in df
    df['Classes_Exclude'] = pd.Series([None] * len(df))
    df['Domains_Exclude'] = pd.Series([None] * len(df))

    # 4. loop through each record 
    # for row in df.itertuples(index=False):
    for i, row in df.iterrows():
        v_class = row.Class.upper().strip()
        v_domain = row.Domain.upper().strip()
        print(f"Row - {i} - Class: {v_class}, Domain: {v_domain}")
        # 4.1 mapping AP and its domain FA and its class
        if proc_ap_fa(i, v_class, v_domain):
            continue
        
        # 4.2 process Class exclude
        proc_exclude(i,row, "class")
        proc_exclude(i, row, "domain")

    return df 


# Test cases
if __name__ == "__main__":
    # set input parameters
    v_prg = __name__ + "::decode_classes"
    os.environ["g_lvl"] = "3"

    d1 = {"1": "One", "2": "Two", "5": "Five"}

    # Sample DataFrame
    df_data = pd.DataFrame({"Class": ["AP", "EVT, INT,  XX ", " FND ", "Not(AP)", "NOT(APRELSUB, POOLDEF, FA)","EVT, INT"],
                            "Domain": ["ALL", "NOT(DS, DV, EX)", "FA", "ALL", "Domain", "NOT(AE, DS, DV, EX)"]})
    d1 = decode_classes(df_data)
    print(f"D1: {d1}")

# End of File