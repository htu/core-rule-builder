# Purpose: Get json.Scope for a rule 
# -----------------------------------------------------------------------------
# History: MM/DD/YYYY (developer) - description
#   03/14/2023 (htu) - ported from proc_rules_sdtm and modulized as get_scope
#    


def get_scope(rule_data):
    print(f"get_scope: Class Type: {type(rule_data['Class'])}")
    # unique_classes = ','.join(rule_data['Class'].unique())
    # unique_domains = ','.join(rule_data['Domain'].unique())
    # unique_classes = rule_data['Class'].unique().tolist()
    # unique_domains = rule_data['Domain'].unique().tolist()

    # Split each element by comma and create a new data frame 
    # df['Class'] = df['Class'].apply(lambda x: [i.strip() for i in x.split(',')])
    df_class = {}
    df_class['Class'] = rule_data['Class'].apply(
        lambda x: [i.strip() for i in x.split(',')])
    df_domain = {}
    df_domain["Domain"] = rule_data['Domain'].apply(
        lambda x: [i.strip() for i in x.split(',')])

    # Create a flattened list of all the elements in the column
    all_classes = [item for sublist in df_class['Class'] for item in sublist]
    all_domains = [item for sublist in df_domain['Domain']
                      for item in sublist]

    # Get the unique elements in the flattened list and create a list
    unique_classes = list(set(all_classes))
    unique_domains = list(set(all_domains))

    print (f"  Domain list: {unique_domains}")

    r_json = {
        "Classes": {
            "Include": unique_classes
        },
        "Domains": {
            "Include": unique_domains
        }
    }
    return r_json

