from src.logging import logger 
from ensure import ensure_annotations 
from box import ConfigBox 
import json

@ensure_annotations
def store_json(data , filepath):
    with open(filepath , 'w') as fp:
        json.dump(data, fp)

@ensure_annotations 
def load_json(filepath):
    with open(filepath , 'r') as fp:
        data = json.load(fp)
    return ConfigBox(data)

    