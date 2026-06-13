# socket_server.py
# este módulo implementa un servidor tcp que escucha en el puerto 9000.
# cuando un cliente se conecta, le envía un resumen de las estadísticas
# en texto plano y cierra la conexión.

import socket
import threading
import json
from analyzer import get_status # usamos las estadísticas calculadas

def handle_client(conn, addr):
    """Atiende a un cliente, envía estadísticas y cierra la conexión"""
    print(f"Cliente conectado desde {addr}")
    try:
        stats = get_status()
        if stats:
            # construimos la respuesta en texto plano
            response = f"""
=== ESTADO DEL SISTEMA ===
Muestras: {stats.get('muestras', 0)}
Último ADC: {stats.get('ultimo_adc', 0)}
Último voltaje: {stats.get('ultimo_voltaje', 0.0):.2f} V
Promedio voltaje: {stats.get('promedio_voltaje', 0.0):.2f} V
Mínimo: {stats.get('min_voltaje', 0.0):.2f} V
Máximo: {stats.get('max_voltaje', 0.0):.2f} V
Desviación estándar: {stats.get('std_voltaje', 0.0):.2f} V
Promedio móvil: {stats.get('promedio_movil', 0.0):.2f} V
Estado: {stats.get('estado', 'DESCONOCIDO')}
=========================
"""
        else:
            response = "Error: No hay datos disponibles aún.\n"
        # enviamos la respuesta codificada a bytes
        conn.sendall(response.encode())
    except Exception as e:
        print(f"Error enviando datos: {e}")
    finally:
        conn.close() # cerramos la conexión con el cliente

def start_socket_server(host='127.0.0.1', port=9000):
    """inicia el servidor tcp y se queda escuchando indefinidamente"""
    # creamos un socket tcp (af_inet = ipv4, sock_stream = tcp)
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # esta opción permite reutilizar la dirección y puerto inmediatamente después de cerrar
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    # asociamos el socket a la dirección y puerto
    server.bind((host, port))
    # comenzamos a escuchar, con una cola máxima de 5 conexiones pendientes
    server.listen(5)
    print(f"Servidor socket escuchando en {host}:{port}")

    while True:
        conn, addr = server.accept()
        # cada cliente se atiende en un hilo para no bloquear la aceptación de otros
        client_thread = threading.Thread(target=handle_client, args=(conn, addr))
        client_thread.start()