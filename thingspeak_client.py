# este módulo envía periódicamente los últimos datos del sensor a la plataforma thingspeak.
# usa la biblioteca requests para hacer una petición http get cada 15 segundos.
# la api key de escritura no debe subirse a github. en este ejemplo aparece una real,
# pero tú deberás reemplazarla por la tuya y luego nunca la publiques.

import requests
import time
import threading
from analyzer import get_status

THINGSPEAK_API_KEY = "OU6B231ZFGV74VBX"
THINGSPEAK_URL = "https://api.thingspeak.com/update"

def send_to_thingspeak():
    """Envía los últimos datos a ThingSpeak (se ejecuta en un hilo periódico)"""
    while True:
        try:
            # obtenemos las estadísticas más recientes
            stats = get_status()
            # solo enviamos si hay al menos una muestra
            if stats and stats.get('muestras', 0) > 0:
                # convertimos el estado textual a número para thingspeak
                estado_num = {"BAJO": 1, "NORMAL": 2, "ALTO": 3}.get(stats.get('estado'), 0)
                
                # preparamos los parámetros de la petición get
                payload = {
                    'api_key': THINGSPEAK_API_KEY,
                    'field1': stats.get('ultimo_adc', 0),
                    'field2': stats.get('ultimo_voltaje', 0.0),
                    'field3': stats.get('promedio_movil', 0.0),
                    'field4': estado_num
                }
                
                # hacemos la petición a thingspeak
                response = requests.get(THINGSPEAK_URL, params=payload, timeout=5)
                if response.status_code == 200:
                    print("Datos enviados a ThingSpeak correctamente")
                else:
                    print(f"Error ThingSpeak: {response.status_code}")
            else:
                print("Aún no hay datos suficientes para enviar a ThingSpeak")
        except Exception as e:
            print(f"Error en envío a ThingSpeak: {e}")
        
        # esperamos 15 segundos antes del próximo envío (límite del plan gratuito)
        time.sleep(15)

def start_thingspeak_thread():
    """crea y arranca el hilo que envía datos a thingspeak"""
    thread = threading.Thread(target=send_to_thingspeak, daemon=True)
    thread.start()
    return thread