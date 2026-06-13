# Sistema de monitoreo analógico con ESP32 y Python

**Estudiante:** Laura Burgos  
**Curso:** Programación Aplicada 2026-1  
**Fecha:** Junio/2026
**Repositorio:** https://github.com/L4nBurguesa/sistema-monitoreo-esp32-python

## Descripción general

Sistema completo de adquisición y monitoreo de datos analógicos usando un ESP32 y Python. El ESP32 lee un potenciómetro (o cualquier sensor analógico) y envía los datos por UART. En la PC, un programa en Python recibe los datos, los guarda en CSV, calcula estadísticas, genera gráficas, las muestra en una página web con Flask, ofrece un servidor socket para consultar el estado y envía información periódicamente a ThingSpeak.

## Hardware utilizado

- ESP32 DevKit V1
- Potenciómetro
- Protoboard y cables
- Conexión USB

### Conexiones

| Potenciómetro : Pin central (wiper) | Pin izquierdo | Pin derecho |  
 
| ESP32 : GPIO34 (ADC) |  3.3V | GND |



## Código del ESP32

El archivo `esp32_sensor.ino` contiene el programa que lee el ADC cada 100 ms y envía por el puerto serie líneas con el formato: `tiempo_ms,adc,voltaje`.

## Estructura del proyecto en Python

main.py # Lanza todos los hilos
config.py # Configuración (puerto, baud rate, rutas)
serial_reader.py # Lee el puerto serie y guarda en CSV
analyzer.py # Estadísticas con pandas/numpy
plotter.py # Genera gráficas (señal, histograma, promedio móvil)
socket_server.py # Servidor TCP en puerto 9000
thingspeak_client.py # Envío periódico a ThingSpeak
web_app.py # Servidor Flask con API HTML/JSON
requirements.txt # Dependencias Python
data/ # Archivos CSV (datos capturados)
static/plots/ # Imágenes PNG generadas
templates/index.html # Página web principal
README.md # Este archivo


## Instalación y ejecución (Ubuntu)

1. **Clonar el repositorio** :
  git clone https://github.com/USUARIO/sistema-monitoreo-esp32-python.git
   cd sistema-monitoreo-esp32-python

2. Crear entorno virtual e instalar dependencias:
  python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

3. Conectar el ESP32 y verificar el puerto:
   ls /dev/ttyUSB*

4. Configurar el puerto en config.py (editar SERIAL_PORT).
   
5. Ejecutar el sistema:
   python main.py



## Uso del sistema

Página web:
Abrir navegador en http://127.0.0.1:5000. Muestra:

  Estadísticas actualizadas (muestras, último ADC, voltaje, promedio, etc.)

  Gráficas de señal, histograma y promedio móvil

  Estado del sensor (Bajo/Normal/Alto)

Actualización automática cada 5 segundos.

Servidor socket:
En otra terminal
 nc localhost 9000

Devuelve un resumen de estadísticas en texto plano.

ThingSpeak:
El programa envía datos cada 15 segundos. Configurar tu THINGSPEAK_API_KEY en thingspeak_client.py (no subir la real al repositorio).


## Capturas de funcionamiento
<img width="947" height="658" alt="imagen" src="https://github.com/user-attachments/assets/37d98247-9fbb-4374-8b4e-335535def2d3" />

<img width="558" height="337" alt="imagen" src="https://github.com/user-attachments/assets/a9a16182-cc39-432d-995b-f3e637355a4a" />

<img width="1326" height="784" alt="imagen" src="https://github.com/user-attachments/assets/d251de16-60f8-4a32-82f7-309a63052788" />



## Problemas comunes y soluciones


No se abre /dev/ttyUSB0	-> Verificar conexión USB y permisos (dialout). En VirtualBox, capturar el dispositivo en Dispositivos → USB.
Error vmwgfx al iniciar Ubuntu	-> Cambiar controlador gráfico a VBoxSVGA y desactivar aceleración 3D.
Flask no responde	-> Asegurar que el puerto 5000 no esté ocupado. Usar netstat -tulpn.
ThingSpeak no recibe datos	-> Revisar API key y que el canal tenga fields 1-4 configurados.


## Notas

En la estructura sugerida por el proyecto aparecía un módulo data_store.py para manejar la escritura del archivo CSV. Sin embargo, durante el desarrollo decidí integrar esa funcionalidad directamente dentro de serial_reader.py. ¿Por qué? Porque la lectura del puerto serie y el guardado de los datos son dos tareas muy acopladas: cada línea que llega se escribe inmediatamente en el CSV, y no hay otra parte del sistema que necesite escribir en ese archivo. Al mantener la escritura dentro del mismo módulo que lee el puerto, el código se vuelve más sencillo de seguir y hay menos riesgo de errores de sincronización. Además, la función read_serial ya recibe el nombre del archivo como parámetro, lo que permite cambiar la ubicación fácilmente. En resumen, opté por una organización más compacta pero igualmente clara, y en la práctica el sistema funciona correctamente.
