import os
from dotenv import load_dotenv
import requests

load_dotenv()

TOKEN = os.getenv("AAGfVlWZcBZ3D4FGuDsNNcIjVsQL2d9GxdI")
CHAT_ID = os.getenv("8628692015")

def enviar_alerta_telegram(mensaje):
    if not TOKEN or not CHAT_ID:
        print("⚠️ No se configuró TELEGRAM_TOKEN o TELEGRAM_CHAT_ID en .env, no se envió alerta.")
        return

    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    datos = {"chat_id": CHAT_ID, "text": mensaje}

    try:
        respuesta = requests.post(url, data=datos, timeout=5)
        if respuesta.status_code != 200:
            print(f"Error enviando alerta: {respuesta.text}")
    except Exception as e:
        print(f"Error de conexión al enviar alerta: {e}")