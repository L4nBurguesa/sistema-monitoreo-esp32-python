# este módulo se encarga de cargar los datos desde el csv y de calcular
# todas las estadísticas que necesita el proyecto, como el promedio,
# el mínimo, el máximo, la desviación estándar y el promedio móvil.
# también clasifica el voltaje en bajo, normal o alto según unos umbrales.

# importamos pandas para manejar tablas de datos
import pandas as pd
# importamos numpy para operaciones numéricas, como el promedio móvil
import numpy as np
# desde config traemos la ruta del archivo csv
from config import CSV_FILE

def load_data():
    """Carga los datos del CSV y retorna un DataFrame de pandas"""
    try:
        # leemos el archivo csv con pandas
        df = pd.read_csv(CSV_FILE)
        # convertimos las columnas adc y voltaje a números 
        # # si algún valor no se puede convertir, lo reemplazamos con nan
        df['adc'] = pd.to_numeric(df['adc'], errors='coerce')
        df['voltaje'] = pd.to_numeric(df['voltaje'], errors='coerce')
        return df
    except Exception as e:
        # si hay error (por ejemplo el archivo no existe), mostramos el mensaje
        print(f"Error al cargar {CSV_FILE}: {e}")
        # devolvemos un dataframe vacío para que el programa no falle
        return pd.DataFrame()

def get_statistics():
    """calcula y devuelve un diccionario con las estadísticas básicas"""
    # cargamos los datos
    df = load_data()
    # si el dataframe está vacío, devolvemos un diccionario vacío
    if df.empty:
        return {}
    
    # construimos el diccionario con las estadísticas pedidas
    stats = {
        'muestras': len(df), # número total de mediciones
        'ultimo_adc': int(df['adc'].iloc[-1]) if not df['adc'].empty else 0, # último valor adc
        'ultimo_voltaje': float(df['voltaje'].iloc[-1]) if not df['voltaje'].empty else 0.0,
        'promedio_voltaje': float(df['voltaje'].mean()), # promedio de voltaje
        'min_voltaje': float(df['voltaje'].min()), # voltaje mínimo
        'max_voltaje': float(df['voltaje'].max()), # voltaje máximo
        'std_voltaje': float(df['voltaje'].std()), # desviación estándar
    }
    return stats

def moving_average(data, window=10):
    """Calcula el promedio móvil de una serie usando numpy"""
    # si la cantidad de datos es menor que la ventana, devolvemos los datos originales
    if len(data) < window:
        return data
    # usamos convolución para calcular el promedio móvil
    # creamos un kernel de unos de tamaño window, y lo normalizamos dividiendo por window
    # mode='valid' devuelve solo los puntos donde la ventana cabe completamente
    return np.convolve(data, np.ones(window)/window, mode='valid')

def classify_voltage(voltaje, bajo=1.0, alto=2.5):
    """Clasifica el voltaje según umbrales"""
    if voltaje < bajo:
        return "BAJO"
    elif voltaje > alto:
        return "ALTO"
    else:
        return "NORMAL"

def get_status():
    """Obtiene estadísticas + estado + promedio móvil del último valor"""
    stats = get_statistics()
    if not stats:
        return {}
    
    # Clasificación por umbral
    stats['estado'] = classify_voltage(stats['ultimo_voltaje'])
    
    # Calcular promedio móvil de los últimos 10 valores
    df = load_data()
    if len(df) >= 10:
        ultimos_voltajes = df['voltaje'].values[-50:]  # últimos 50 para suavizar
        # calculamos el promedio móvil
        mov_avg = moving_average(ultimos_voltajes, window=10)
        # nos quedamos con el último valor del promedio
        stats['promedio_movil'] = float(mov_avg[-1]) if len(mov_avg) > 0 else stats['ultimo_voltaje']
    else:
        # si hay pocos datos, el promedio móvil es el mismo que el último voltaje
        stats['promedio_movil'] = stats['ultimo_voltaje']
    
    return stats