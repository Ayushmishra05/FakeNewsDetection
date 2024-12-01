import os 



files = [
    ".github/workflows/.gitkeep" , 
    f"src/__init__.py", 
    f"src/components/__init__.py", 
    f"src/utils/__init__.py", 
    f"src/utils/common.py", 
    f"src/config/__init__.py", 
    f"src/config/configuration.py", 
    f"src/pipeline/__init__.py", 
    f"src/entity/config_entity.py", 
    f"src/entity/__init__.py", 
    f"src/constants/__init__.py", 
    f"src/logging/__init__.py", 
    "config/config.yaml", 
    "params.yaml", 
    "schema.yaml", 
    "main.py", 
    "Dockerfile", 
    "setup.py", 
    "research/research.ipynb", 
    "templates/index.html", 
    "app.py"
]



for file in files:
    filedir, filename = os.path.split(file)
    if filedir != "":
        os.makedirs(filedir, exist_ok=True)
    if not os.path.exists(filename):
        with open(file , 'w') as fp:
            pass 
    