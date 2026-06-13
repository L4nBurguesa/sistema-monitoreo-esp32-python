# este archivo guarda las configuraciones que usan varios módulos.
# así evitamos escribir los mismos valores en muchos lugares.

# puerto serie donde está conectado el esp32.
# puede ser /dev/ttyUSB0 o /dev/ttyACM0.
# para saber cuál es, desconecta el esp32, ejecuta 'ls /dev/tty*',
# luego conecta y vuelve a ejecutar; el que aparece nuevo es el puerto.
SERIAL_PORT = '/dev/ttyUSB0'

# velocidad de comunicación con el esp32.
# debe coincidir con la que programaste en el esp32 (por ejemplo 115200).
BAUD_RATE = 115200

# ruta del archivo csv donde se guardarán los datos del sensor.
# la carpeta 'data' debe existir, o la crea el programa al guardar.
CSV_FILE = 'data/sensor_data.csv'