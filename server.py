from flask import Flask, request, jsonify
import subprocess
import os
import sys
from datetime import datetime
import threading
import time

app = Flask(__name__)

SCRIPTS_DIR = os.path.join(os.path.dirname(__file__), 'NiryoScripts')
python_cmd = r'C:\Users\j.miguelez.yague\Documents\GitHub\TFG_Mates_BackendServer\venv\Scripts\python.exe'

script_thread = None
stop_event = threading.Event()
last_script = None
script_actual = None
script_start_time = None


def ejecutar_en_bucle(nombre_script):
    global stop_event, script_actual, script_start_time
    script_path = os.path.join(SCRIPTS_DIR, f'{nombre_script}.py')
    script_actual = nombre_script
    script_start_time = datetime.now()

    while not stop_event.is_set():
        if not os.path.isfile(script_path):
            print(f"El script {nombre_script} no existe")
            break

        try:
            resultado = subprocess.run([python_cmd, script_path], capture_output=True, text=True)
            with open("log.txt", "a", encoding="utf-8") as log_file:
                log_file.write(f"[{datetime.now()}] Script ciclo: {nombre_script}\nSalida:\n{resultado.stdout}\n\n")
        except subprocess.CalledProcessError as e:
            with open("log.txt", "a", encoding="utf-8") as log_file:
                log_file.write(f"[{datetime.now()}] ERROR ciclo: {nombre_script}\nError:\n{e.stderr}\n\n")

        time.sleep(1)

    script_actual = None
    script_start_time = None


@app.route('/ejecutar', methods=['POST'])
def ejecutar_script():
    global script_thread, stop_event, last_script, script_actual, script_start_time

    data = request.get_json()
    if not data or 'programa' not in data:
        return jsonify({'status': 'error', 'mensaje': 'Falta el parámetro "programa"'}), 400

    nombre_script = data['programa']
    if script_thread and script_thread.is_alive():
        return jsonify({'status': 'error', 'mensaje': 'Ya hay un script ejecutándose'}), 409

    stop_event.clear()
    last_script = nombre_script
    script_actual = nombre_script
    script_start_time = datetime.now()
    script_thread = threading.Thread(target=ejecutar_en_bucle, args=(nombre_script,))
    script_thread.start()

    return jsonify({'status': 'ok', 'mensaje': f'Script "{nombre_script}" iniciado en bucle'})


@app.route('/parar', methods=['POST'])
def parar_script():
    global stop_event, script_thread, script_actual, script_start_time

    if script_thread and script_thread.is_alive():
        stop_event.set()
        script_thread.join(timeout=2)
        script_actual = None
        script_start_time = None
        return jsonify({'status': 'ok', 'mensaje': 'Ejecución detenida'})
    else:
        return jsonify({'status': 'error', 'mensaje': 'No hay ningún script en ejecución'}), 404


@app.route('/restart', methods=['POST'])
def reiniciar_robot():
    nombre_script = "robot_restart"
    script_path = os.path.join(SCRIPTS_DIR, f'{nombre_script}.py')

    if not os.path.isfile(script_path):
        return jsonify({'status': 'error', 'mensaje': 'Script "robot_restart" no encontrado'}), 404

    try:
        resultado = subprocess.run([python_cmd, script_path], capture_output=True, text=True, check=True)
        return jsonify({
            'status': 'ok',
            'mensaje': 'Script "robot_restart" ejecutado correctamente',
            'salida': resultado.stdout.strip()
        })
    except subprocess.CalledProcessError as e:
        return jsonify({
            'status': 'error',
            'mensaje': f'Error al ejecutar "robot_restart": {e.stderr.strip()}',
            'codigo': e.returncode
        }), 500


@app.route('/calibrar', methods=['POST'])
def calibrar_robot():
    nombre_script = "calibrar_robot"
    script_path = os.path.join(SCRIPTS_DIR, f'{nombre_script}.py')

    if not os.path.isfile(script_path):
        return jsonify({'status': 'error', 'mensaje': 'Script de calibración no encontrado'}), 404

    try:
        resultado = subprocess.run([python_cmd, script_path], capture_output=True, text=True, check=True)
        return jsonify({'status': 'ok', 'mensaje': 'Calibración ejecutada correctamente'})
    except subprocess.CalledProcessError as e:
        return jsonify({
            'status': 'error',
            'mensaje': f'Error durante calibración: {e.stderr.strip()}',
            'codigo': e.returncode
        }), 500


@app.route('/status', methods=['GET'])
def estado_script():
    if script_thread and script_thread.is_alive():
        return jsonify({
            'status': 'ejecutando',
            'script': script_actual,
            'inicio': script_start_time.isoformat() if script_start_time else None
        })
    else:
        return jsonify({
            'status': 'inactivo',
            'script': None,
            'inicio': None
        })


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)