# web_app.py
# este módulo crea una aplicación web con flask.
# muestra las estadísticas y las gráficas, y también ofrece
# una api para actualizar los datos sin recargar la página.

from flask import Flask, render_template, jsonify
import analyzer
import plotter
import os
import threading
import time

app = Flask(__name__)

@app.route('/')
def index():
    """Página principal"""
    stats = analyzer.get_status()
    # renderizamos la plantilla index.html que está en la carpeta templates
    return render_template('index.html', stats=stats)

@app.route('/stats')
def stats_api():
    """API para obtener estadísticas en JSON"""
    stats = analyzer.get_status()
    return jsonify(stats)

@app.route('/refresh_plots')
def refresh_plots():
    """Forzar regeneración de gráficas"""
    plotter.generate_all_plots()
    return jsonify({'status': 'Gráficas actualizadas'})

def run_flask():
    """Inicia el servidor Flask en un hilo separado"""
    # debug false para evitar que intente recargarse solo (conflicto con hilos)
    # use_reloader false evita que flask cree un segundo proceso
    app.run(host='0.0.0.0', port=5000, debug=False, use_reloader=False)

def start_flask_thread():
    """Lanza Flask en un hilo para que no bloquee el hilo principal"""
    flask_thread = threading.Thread(target=run_flask)
    flask_thread.daemon = True
    flask_thread.start()

def run_flask():
    app.run(host='0.0.0.0', port=5000, debug=False, use_reloader=False)
