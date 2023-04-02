# Purpose: Publish CORE rules to Cosmos DB
# -----------------------------------------------------------------------------
# History: MM/DD/YYYY (developer) - description
#   03/31/2023 (htu) - initial coding based on
#     https://learn.microsoft.com/en-us/python/api/overview/azure/cosmos-readme?view=azure-python#create-a-container
#
import os 
import pandas as pd
from dotenv import load_dotenv
from rulebuilder.echo_msg import echo_msg
from azure.cosmos import exceptions
from rulebuilder.get_db_cfg import get_db_cfg
from rulebuilder.publish_a_rule import publish_a_rule


def publish_rules (rule_ids:list=["CG0001"], doc_ids:list=[],
                   rule_dir:str=None, db_cfg = None 
                   ):
    v_prg = __name__
    # 1.0 check input parameters
    v_stp = 1.0
    v_msg = "Publishing rules..."
    echo_msg(v_prg, v_stp, v_msg, 1)

    if len(rule_ids) == 0 and len(doc_ids == 0):
        v_stp = 1.1
        v_msg = "No rule id nor doc id is provided. "
        echo_msg(v_prg, v_stp, v_msg, 0)
        return
    
    if rule_dir is None:
        v_stp = 1.2
        load_dotenv()
        rule_dir = os.getenv("rule_json_dir")
        output_dir = os.getenv("output_dir")
        if rule_dir is None:
            rule_dir = output_dir + "/rules_json"
        if not os.path.exists(rule_dir):
            v_msg = f"Could not find rule_dir: {rule_dir}"
            echo_msg(v_prg, v_stp, v_msg, 0)
            return

    if db_cfg is None:
        v_stp = 1.3
        v_msg = "Non database connection is defined and provided."
        echo_msg(v_prg, v_stp, v_msg, 0)
        return

    ctc = db_cfg.get("ct_conn")
    if ctc is None:
        v_stp = 1.4
        v_msg = "Non container connection is defined and provided."
        echo_msg(v_prg, v_stp, v_msg, 0)
        return
    
    df_log = pd.DataFrame(columns=["rule_id", "core_id",  "user_id", "guid_id", 
                                   "created", "changed", "status", "version",
                                   "publish_status" ]
                        )
    df_row = {"rule_id": None, "core_id": None,  "user_id": None, "guid_id": None,
           "created": None, "changed": None, "status": None, "version": None,
           "publish_status": None}
    rows = [] 

 
    
    # 2.0 loop through rule list
    if len(rule_ids) > 0:
        for r in rule_ids: 
            publish_a_rule(rule_id=r, rule_dir=rule_dir,db_cfg=db_cfg)
    
    # 3.0 loop through document list
    if len(doc_ids) > 0:
        for d in doc_ids:
            publish_a_rule(
                doc_id=d, rule_dir=rule_dir, db_cfg=db_cfg)



query = "SELECT * FROM c"
query_options = {'enable_cross_partition_query': True}


total_documents = list(ctc.query_items(
    query='SELECT VALUE COUNT(1) FROM c',
    enable_cross_partition_query=True
))[0]

print(
    f"Total number of documents in container '{db}': {total_documents}")


# assume you have already obtained the container client object and assigned it to 'ctc'

document_id = '9959136a-523f-4546-9520-ffa22cda8867'

try:
    document = ctc.read_item(item=document_id, partition_key=document_id)
    print(document)
except exceptions.CosmosResourceNotFoundError:
    print(f"Document with id '{document_id}' not found.")

# Retrieve the document you want to replace
doc_id = '9959136a-523f-4546-9520-ffa22cda8867'
doc_link = f"/dbs/{db}/colls/{ct}/docs/{doc_id}"
document = ctc.read_item(item=doc_link)

# Replace the document with a new one
new_document = {'id': '9959136a-523f-4546-9520-ffa22cda8867',
                'name': 'New name', 'age': 30}
ctc.replace_item(item=new_document, body=new_document)
