# Purpose: Create a Container in a Cosmos DB
# -----------------------------------------------------------------------------
# History: MM/DD/YYYY (developer) - description
#   03/31/2023 (htu) - initial coding based on
#     https://learn.microsoft.com/en-us/python/api/overview/azure/cosmos-readme?view=azure-python#create-a-container
#
from azure.cosmos import exceptions
from rulebuilder.get_db_cfg import get_db_cfg


db = 'library'
ct = 'editor_rules_dev'
cfg = get_db_cfg(db_name=db, container_name=ct)
# json.dump(cfg,sys.stdout, indent=4)
dbc = cfg["db_conn"]
ctc = cfg["ct_conn"]


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


