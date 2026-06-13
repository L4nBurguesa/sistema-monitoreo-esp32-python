# este módulo se encarga de leer los datos que envía el esp32 por el puerto usb
# y guardarlos en un archivo csv línea por línea

# importo la biblioteca para manejar el puerto serie
# serial_reader.py
import serial
import time
import csv
from datetime import datetime

def read_serial(port, baudrate, csv_filename, stop_event):
    print(f"Intentando abrir puerto {port} a {baudrate} baudios...")
    try:
        ser = serial.Serial(port, baudrate, timeout=1)
        time.sleep(2)
        print("Puerto abierto correctamente.")
    except Exception as e:
        print(f"ERROR: No se pudo abrir el puerto {port}: {e}")
        return

    try:
        with open(csv_filename, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['timestamp', 'tiempo_ms', 'adc', 'voltaje'])
            print(f"Archivo CSV creado: {csv_filename}")
            
            while not stop_event.is_set():
                line = ser.readline().decode('utf-8', errors='ignore').strip()
                if line:
                    print(f"Recibido: {line}")  # Muestra crudo lo que llega
                    parts = line.split(',')
                    if len(parts) >= 3:
                        now = datetime.now().isoformat()
                        writer.writerow([now, parts[0], parts[1], parts[2]])
                        csvfile.flush()
                        print(f"Guardado: {parts}")
                    else:
                        print(f"Formato incorrecto: {line}")
    except Exception as e:
        print(f"Error durante la lectura/escritura: {e}")
    finally:
        ser.close()
        print("Puerto cerrado.")