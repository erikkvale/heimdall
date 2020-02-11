import os
from pathlib import Path
from dotenv import load_dotenv

env_path = Path("../") / ".env"
load_dotenv(dotenv_path=env_path)

KAFKA_TOPIC = os.getenv("KAFKA_TOPIC")
KAFKA_BOOTSTRAP_SERVER = os.getenv("KAFKA_BOOTSTRAP_SERVER")
APACHE_ACCESS_LOG_FILE_PATH = os.getenv("APACHE_ACCESS_LOG_FILE_PATH")

if __name__ == "__main__":
    print(env_path)

