import subprocess
from definitions import *

kibana = subprocess.Popen(KIBANA_PATH, creationflags=subprocess.CREATE_NEW_CONSOLE)
airflow_on_bash = subprocess.Popen('bash -c "airflow webserver -p 8887"', creationflags=subprocess.CREATE_NEW_CONSOLE)
ui = subprocess.Popen(UI_PATH, creationflags=subprocess.CREATE_NEW_CONSOLE)