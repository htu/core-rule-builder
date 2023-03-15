# Purpose: Get json.Authorities for a rule 
# -----------------------------------------------------------------------------
# History: MM/DD/YYYY (developer) - description
#   03/14/2023 (htu) - ported from proc_rules_sdtm as get_authorities module
#    

def get_authorities(rule_data):
    # print(f"get_authorities: Rule Data: {rule_data}")
    # create a sample dataframe
    df_rules = rule_data

    # define authorities variables 
    r_a_cit = {"Cited_Guidance": None,
               "Document": None,
               "Item": None,
               "Section": None
               }
    r_cits = []
    r_a_ref = {"Origin": "SDTM and SDTMIG Conformance Rules",
               "Rule_Identifier": {
                   "Id": "CG0378",
                   "Version": "1"
               },
               "Version": "2.0",
               "Citations": r_cits
               }
    r_refs = []
    r_a_std = {"Name": "SDTMIG",
               "Version": "3.4",
               "References": r_refs
               }
    r_stds = []
    r_json = [{"Organization": "CDISC",
               "Standards": r_stds 
               }
              ]
    # loop through each row of the dataframe
    i = -1
    for row in df_rules.itertuples(index=False):
        i += 1
        rule_id         = df_rules.iloc[i]["Rule ID"]
        r_a_cit = {"Cited_Guidance": df_rules.iloc[i]["Cited Guidance"],
                   "Document": df_rules.iloc[i]["Document"],
                   "Item": df_rules.iloc[i]["Item"],
                   "Section": df_rules.iloc[i]["Section"]
                   }
        r_cits.append(r_a_cit) 
        print(f"Row {i}: {r_a_cit}") 
        r_a_ref = {"Origin": "SDTM and SDTMIG Conformance Rules",
                   "Rule_Identifier": {
                       "Id": rule_id,
                       "Version": df_rules.iloc[i]["Rule Version"]
                   },
                   "Version": "2.0",
                   "Citations": [r_a_cit]
                   }
        r_refs.append(r_a_ref) 
        r_a_std = {"Name": "SDTMIG",
                   "Version": df_rules.iloc[i]["SDTMIG Version"],
                   "References": [r_a_ref]
                   }
        r_stds.append(r_a_std) 

        # print(f"Row {i}: {df_rules.iloc[i]}")
        #print("Record:")
        # for col, value in zip(df_rules.columns, row):
        #  print(f"  {col}: {value}")
    return r_json 

