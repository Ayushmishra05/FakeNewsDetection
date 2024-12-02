import logging 
from datetime import datetime 
import sys
import os 
from logging import StreamHandler , FileHandler

direc = 'logs'

filename = f"{direc}/{datetime.now().strftime('%H_%M_%d_%m_%Y')}.log"


os.makedirs(direc, exist_ok=True)
with open(filename , 'w') as fp:
    pass

logging.basicConfig(format= "%(asctime)s %(levelname)s %(message)s" , level=logging.INFO, handlers=[
    FileHandler(filename=filename , mode="w"), 
    StreamHandler(sys.stdout)
]
)


logger = logging.getLogger('News Detection')
