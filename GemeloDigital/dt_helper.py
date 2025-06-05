import os
import requests
import json
from dotenv import load_dotenv

# Cargar variables de entorno desde .env
load_dotenv()

TENANT_ID = os.getenv("TENANT_ID")
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
API_CLIENT_ID = os.getenv("API_CLIENT_ID")
API_URL = os.getenv("API_URL")

def get_access_token():
    url = f"https://login.microsoftonline.com/{TENANT_ID}/oauth2/v2.0/token"
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    data = {
        "grant_type": "client_credentials",
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "scope": f"api://{API_CLIENT_ID}/.default"
    }

    response = requests.post(url, data=data, headers=headers)
    if response.status_code == 200:
        return response.json().get("access_token")
    else:
        print("Error al obtener token:", response.text)
        return None

def get_twin_data(endpoint, token):
    url = f"{API_URL}/api/{endpoint}"
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        print("Error al obtener datos del twin:", response.text)
        return None

def put_twin_data(endpoint, body, token):
    url = f"{API_URL}/api/{endpoint}"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    response = requests.put(url, headers=headers, data=json.dumps(body))
    if response.status_code in [200, 204]:
        return True
    else:
        print("Error al hacer PUT:", response.text)
        return False
    
def reportar_error_estado(twin_id="Twin/RobotArm"):
    token = get_access_token()
    if token:
        put_twin_data(twin_id, {
            "estado": "Error"
        }, token)

def avisar_advertencia(endpoint="Twin/RobotArm"):
    token = get_access_token()
    if token:
        resultado = put_twin_data(endpoint, {"estado": "Advertencia"}, token)
        if not resultado:
            print("Error al enviar estado 'Advertencia' al Twin.")
    else:
        print("No se pudo obtener token para avisar de advertencia.")