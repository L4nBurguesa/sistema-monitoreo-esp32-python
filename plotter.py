# este módulo se encarga de generar las tres gráficas obligatorias:
# 1) señal del sensor en el tiempo
# 2) histograma de voltajes
# 3) señal original junto con su promedio móvil
# las guarda como imágenes png dentro de la carpeta static/plots/

# primero configuramos matplotlib para que use el backend 'agg'
# esto evita que intente abrir una ventana gráfica (útil en servidores)
import matplotlib
matplotlib.use('Agg')  # Para que no intente abrir ventanas
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from config import CSV_FILE
import os

# carpeta donde se guardarán las gráficas
PLOTS_DIR = 'static/plots'

def ensure_dir():
    """Crea la carpeta de gráficas si no existe"""
    if not os.path.exists(PLOTS_DIR):
        os.makedirs(PLOTS_DIR)

def plot_signal():
    """Gráfica 1: Señal en función del tiempo (índice)"""
    ensure_dir()
    df = pd.read_csv(CSV_FILE)
    if df.empty:
        print("No hay datos para graficar señal")
        return
    
    plt.figure(figsize=(10, 5))
    # dibujamos un histograma con 20 barras, color verde, bordes negros y algo de transparencia
    plt.plot(df.index, df['voltaje'], color='blue', linewidth=1)
    plt.xlabel('Número de muestra')
    plt.ylabel('Voltaje (V)')
    plt.title('Señal del sensor en el tiempo')
    plt.grid(True) # cuadrícula
    plt.tight_layout() # ajusta los márgenes
    # guardamos la imagen en la carpeta static/plots
    plt.savefig(f'{PLOTS_DIR}/sensor_tiempo.png')
    plt.close() # cerramos la figura para liberar memoria
    print("Gráfica de señal guardada")

def plot_histogram():
    """Gráfica 2: Histograma de voltajes"""
    ensure_dir()
    df = pd.read_csv(CSV_FILE)
    if df.empty:
        print("No hay datos para histograma")
        return
    
    plt.figure(figsize=(10, 5))
    plt.hist(df['voltaje'], bins=20, color='green', edgecolor='black', alpha=0.7)
    plt.xlabel('Voltaje (V)')
    plt.ylabel('Frecuencia')
    plt.title('Histograma de mediciones')
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(f'{PLOTS_DIR}/histograma.png')
    plt.close()
    print("Histograma guardado")

def plot_moving_average(window=10):
    """Gráfica 3: Promedio móvil junto con la señal original"""
    ensure_dir()
    df = pd.read_csv(CSV_FILE)
    if df.empty or len(df) < window:
        print("Datos insuficientes para promedio móvil")
        return
    
    # calculamos el promedio móvil usando convolución
    mov_avg = np.convolve(df['voltaje'].values, np.ones(window)/window, mode='valid')
    # los índices para el promedio empiezan en window-1 (porque los primeros puntos no tienen ventana completa)
    indices = range(window-1, len(df))
    
    plt.figure(figsize=(10, 5))
    # la señal original en gris semitransparente
    plt.plot(df['voltaje'], alpha=0.5, label='Señal original', color='gray')
    
    # el promedio móvil en rojo, línea más gruesa
    plt.plot(indices, mov_avg, color='red', linewidth=2, label=f'Promedio móvil (ventana={window})')
    plt.xlabel('Número de muestra')
    plt.ylabel('Voltaje (V)')
    plt.title('Promedio móvil del sensor')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(f'{PLOTS_DIR}/promedio_movil.png')
    plt.close()
    print("Gráfica de promedio móvil guardada")

def generate_all_plots():
    """Genera las tres gráficas"""
    plot_signal()
    plot_histogram()
    plot_moving_average()