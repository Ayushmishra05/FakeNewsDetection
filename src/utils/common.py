from src.logging import logger 
from ensure import ensure_annotations 
from box import ConfigBox 
import json
import pickle

@ensure_annotations
def store_json(data , filepath):
    with open(filepath , 'w') as fp:
        json.dump(data, fp)

@ensure_annotations 
def load_json(filepath):
    with open(filepath , 'r') as fp:
        data = json.load(fp)
    return ConfigBox(data)

@ensure_annotations 
def load_pickle_file(filepath):
    with open(filepath , 'rb') as fp:
        return pickle.load(fp)
    