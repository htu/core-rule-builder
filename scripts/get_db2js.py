# Purpose: Copy all the rules in the dev environment to a local folder 
# History: MM/DD/YYYY (developer) - description
#   03/03/2023 (htu) - based on an example code sent by Gerry Campion
#   03/06/2023 (htu) - installed python-dotenv and made load_dotenv to work
#   03/07/2023 (htu) - added code to make the detination folder
#  
import os 
from os import getenv
from sys import path
from dotenv import load_dotenv

path.insert(0, "./")

from transformer.transformer_cosmosdb import CosmosdbTransformer
from transformer.transformer_json import JSONTransformer
from transformer.transformer_yaml import YAMLTransformer
from transformer.transformer import Transformer
from transformer.transformations_crog import (
    all_transformations,
)

# Load environment variables from .env file
load_dotenv()
print( f"DEV_COSMOS_URL={ getenv('DEV_COSMOS_URL')}" ) 

# print (f"Env: {getenv('DEV_COSMOS_URL')}")

dev_transformer = CosmosdbTransformer(
    getenv("DEV_COSMOS_URL"),
    getenv("DEV_COSMOS_KEY"),
    getenv("DEV_COSMOS_DATABASE"),
    getenv("DEV_COSMOS_CONTAINER"),
)

# python -c "import dotenv; print(dotenv.__version__)"

js_dir = getenv('WORKING_DIR') + "/json_rules"

if not os.path.exists(js_dir):
    os.makedirs(js_dir)
    print(f"Created folder '{js_dir}'")
else:
    print(f"Folder '{js_dir}' already exists")

json_transformer = JSONTransformer(f"{js_dir}")

Transformer.replace_rules(
    from_transformer=dev_transformer, to_transformer=json_transformer
)
