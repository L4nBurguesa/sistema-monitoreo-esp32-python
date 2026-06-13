# este es el programa principal. su tarea es lanzar todos los hilos
# que ejecutan las diferentes partes del sistema:
# - lectura del puerto serie y guardado en csv
# - servidor socket para consultar el estado
# - envío periódico a thingspeak
# - servidor web flask
# luego se queda esperando hasta que el usuario presione ctrl+c

import threading
import time
from config import SERIAL_PORT, BAUD_RATE, CSV_FILE
from serial_reader import read_serial
from socket_server import start_socket_server
from thingspeak_client import start_thingspeak_thread
import web_app # importamos todo el módulo, no solo una función

if __name__ == "__main__":
    print("Iniciando sistema de monitoreo...")
    
    # creamos un evento que servirá para detener los hilos de forma ordenada
    stop_event = threading.Event()

    # hilo 1: lectura serial y guardado en csv
    # el target es la función read_serial, y le pasamos sus argumentos como una tupla
    serial_thread = threading.Thread(
        target=read_serial,
        args=(SERIAL_PORT, BAUD_RATE, CSV_FILE, stop_event),
        daemon=True # si el hilo principal termina, este también se cierra
    )
    serial_thread.start()
    print("Hilo de lectura serial iniciado.")

    # hilo 2: servidor socket (escucha en el puerto 9000)
    socket_thread = threading.Thread(target=start_socket_server, daemon=True)
    socket_thread.start()
    print("Servidor socket iniciado en puerto 9000.")

    # hilo 3: envío periódico a thingspeak
    # start_thingspeak_thread ya crea y devuelve un hilo daemon
    thingspeak_thread = start_thingspeak_thread()
    print("Hilo de ThingSpeak iniciado.")

    # hilo 4: servidor web flask
    # web_app.run_flask es la función que arranca el servidor
    flask_thread = threading.Thread(target=web_app.run_flask, daemon=True)
    flask_thread.start()
    print("Servidor Flask iniciado en http://127.0.0.1:5000")

    # mantenemos el programa principal vivo
    # mientras no se interrumpa, solo esperamos un segundo cada ciclo
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nDeteniendo el sistema...")
        # activamos el evento para que el hilo serial termine su bucle
        stop_event.set()
        # esperamos hasta 2 segundos a que el hilo serial termine (opcional)
        serial_thread.join(timeout=2)
        print("Sistema detenido.")