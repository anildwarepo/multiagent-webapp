from dotenv import load_dotenv
from pathlib import Path 

def load_env():
    env_path = Path('.') / 'secrets.env'
    load_dotenv(dotenv_path=env_path)

load_env()