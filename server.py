from flask import Flask, request, jsonify
import subprocess
import os
from datetime import datetime, timedelta
import threading
import time
import signal
from bbdd_robot.csv_handler import guardar_tiempos_en_csv, procesar_csv_tiempos

app = Flask(__name__)

SCRIPTS_DIR = os.path.join(os.path.dirname(__file__), 'NiryoScripts')
python_cmd = r'C:\Users\j.miguelez.yague\Documents\GitHub\TFG_Mates_BackendServer\venv\Scripts\python.exe'

script_thread = None
stop_event = threading.Event()
last_script = None
script_actual = None
script_start_time = None
script_process = None  # Proceso externo en ejecución

tiempo_total_activo = timedelta()
tiempo_total_inactivo = timedelta()
ultimo_cambio_estado = datetime.now()
estado_robot = 'inactivo'
ultima_fecha = datetime.now().date()

log_lock = threading.Lock()  # Nuevo: para sincronizar acceso a log

def comprobar_conexion():
    script_path = os.path.join(SCRIPTS_DIR, 'comprobar_conexion_robot.py')
    try:
        resultado = subprocess.run([python_cmd, script_path], capture_output=True, text=True, timeout=5)
        salida = resultado.stdout.strip()
        return salida == "ok"
    except Exception:
        return False
    
def actualizar_tiempos():
    global tiempo_total_activo, tiempo_total_inactivo, ultimo_cambio_estado, estado_robot, ultima_fecha

    ahora = datetime.now()
    hoy = ahora.date()

    if estado_robot == 'activo':
        tiempo_total_activo += ahora - ultimo_cambio_estado
    else:
        tiempo_total_inactivo += ahora - ultimo_cambio_estado

    if hoy != ultima_fecha:
        guardar_tiempos_en_csv(
            ultima_fecha,
            tiempo_total_activo.total_seconds() / 60,
            tiempo_total_inactivo.total_seconds() / 60
        )
        tiempo_total_activo = timedelta()
        tiempo_total_inactivo = timedelta()
        ultima_fecha = hoy

    ultimo_cambio_estado = ahora

def ejecutar_en_bucle(nombre_script):
    global stop_event, script_actual, script_start_time, script_process
    script_path = os.path.join(SCRIPTS_DIR, f'{nombre_script}.py')
    script_actual = nombre_script
    script_start_time = datetime.now()

    while not stop_event.is_set():
        if not os.path.isfile(script_path):
            print(f"El script {nombre_script} no existe")
            break

        try:
            # Lanzar proceso y guardarlo
            script_process = subprocess.Popen([python_cmd, script_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

            # Esperar a que termine o a que se pida stop
            while True:
                if stop_event.is_set():
                    # Terminar proceso si sigue vivo
                    if script_process.poll() is None:
                        if os.name == 'nt':
                            script_process.terminate()
                        else:
                            script_process.send_signal(signal.SIGINT)
                        script_process.wait(timeout=5)
                    break
                retcode = script_process.poll()
                if retcode is not None:
                    break
                time.sleep(0.2)

            # Capturar salida y error
            stdout, stderr = script_process.communicate(timeout=1)
            with open("log.txt", "a", encoding="utf-8") as log_file:
                log_file.write(f"[{datetime.now()}] Script ciclo: {nombre_script}\nSalida:\n{stdout}\nErrores:\n{stderr}\n\n")

        except subprocess.TimeoutExpired:
            # Si no termina en tiempo, lo matamos
            script_process.kill()
            stdout, stderr = script_process.communicate()
            with open("log.txt", "a", encoding="utf-8") as log_file:
                log_file.write(f"[{datetime.now()}] Timeout en script {nombre_script}\nSalida:\n{stdout}\nErrores:\n{stderr}\n\n")
        except Exception as e:
            with open("log.txt", "a", encoding="utf-8") as log_file:
                log_file.write(f"[{datetime.now()}] ERROR en script {nombre_script}: {str(e)}\n\n")
            break

        # Pequeña pausa antes de reiniciar el script en el bucle
        time.sleep(1)

    script_actual = None
    script_start_time = None
    script_process = None

@app.route('/ejecutar', methods=['POST'])
def ejecutar_script():
    global script_thread, stop_event, last_script, script_actual, script_start_time, estado_robot

    data = request.get_json()
    if not data or 'programa' not in data:
        return jsonify({'status': 'error', 'mensaje': 'Falta el parámetro "programa"'}), 400

    nombre_script = data['programa']

    if script_thread and script_thread.is_alive():
        if script_actual == nombre_script:
            return jsonify({'status': 'ok', 'mensaje': f'El script "{nombre_script}" ya está ejecutándose'})
        else:
            stop_event.set()
            script_thread.join(timeout=10)
            estado_robot = 'inactivo'
            actualizar_tiempos()

    if not comprobar_conexion():
        return jsonify({'status': 'error', 'mensaje': 'Robot no conectado o inaccesible'}), 503

    stop_event.clear()
    last_script = nombre_script
    script_actual = nombre_script
    script_start_time = datetime.now()

    estado_robot = 'activo'
    actualizar_tiempos()

    script_thread = threading.Thread(target=ejecutar_en_bucle, args=(nombre_script,))
    script_thread.start()

    return jsonify({'status': 'ok', 'mensaje': f'Script "{nombre_script}" iniciado en bucle'})

@app.route('/parar', methods=['POST'])
def parar_script():
    global stop_event, script_thread, script_actual, script_start_time, script_process, estado_robot

    if script_thread and script_thread.is_alive():
        stop_event.set()
        if script_process and script_process.poll() is None:
            if os.name == 'nt':
                script_process.terminate()
            else:
                script_process.send_signal(signal.SIGINT)
            script_process.wait(timeout=5)

        script_thread.join(timeout=10)

        estado_robot = 'inactivo'
        actualizar_tiempos()

        script_actual = None
        script_start_time = None

        return jsonify({'status': 'ok', 'mensaje': 'Ejecución detenida'})
    else:
        return jsonify({'status': 'error', 'mensaje': 'No hay ningún script en ejecución'}), 404

@app.route('/restart', methods=['POST'])
def reiniciar_robot():
    global stop_event, script_thread, script_actual, script_process, estado_robot

    nombre_script = "robot_restart"
    script_path = os.path.join(SCRIPTS_DIR, f'{nombre_script}.py')

    if script_thread and script_thread.is_alive():
        stop_event.set()
        if script_process and script_process.poll() is None:
            if os.name == 'nt':
                script_process.terminate()
            else:
                script_process.send_signal(signal.SIGINT)
            script_process.wait(timeout=5)
        script_thread.join(timeout=10)

        estado_robot = 'inactivo'
        actualizar_tiempos()

        script_actual = None

    if not comprobar_conexion():
        return jsonify({'status': 'error', 'mensaje': 'Robot no conectado o inaccesible'}), 503

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
    global stop_event, script_thread, script_actual, script_process, estado_robot

    nombre_script = "calibrar_robot"
    script_path = os.path.join(SCRIPTS_DIR, f'{nombre_script}.py')

    if script_thread and script_thread.is_alive():
        stop_event.set()
        if script_process and script_process.poll() is None:
            if os.name == 'nt':
                script_process.terminate()
            else:
                script_process.send_signal(signal.SIGINT)
            script_process.wait(timeout=5)
        script_thread.join(timeout=10)

        estado_robot = 'inactivo'
        actualizar_tiempos()

        script_actual = None

    if not comprobar_conexion():
        return jsonify({'status': 'error', 'mensaje': 'Robot no conectado o inaccesible'}), 503

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

LOG_FILE = 'log.txt'
LAST_POSITION = 0
LAST_CONTENT = ""

@app.route('/logs/latest')
def get_latest_logs():
    global LAST_POSITION, LAST_CONTENT

    if not os.path.exists(LOG_FILE):
        return jsonify({"log": ""})

    with log_lock:
        try:
            with open(LOG_FILE, 'r', encoding='utf-8') as f:
                f.seek(LAST_POSITION)
                new_data = f.read()
                if new_data:
                    LAST_POSITION = f.tell()
                    LAST_CONTENT = new_data
                    return jsonify({"log": new_data})
                else:
                    return jsonify({"log": False})
        except Exception:
            # Fallback: Reiniciar lectura desde el principio
            try:
                with open(LOG_FILE, 'r', encoding='utf-8') as f:
                    contenido = f.read()
                    LAST_POSITION = f.tell()
                    LAST_CONTENT = contenido
                    return jsonify({"log": contenido})
            except Exception as fallback_error:
                return jsonify({"log": "", "error": str(fallback_error)}), 500

'''@app.route('/status', methods=['GET'])
def estado_script():
    if not comprobar_conexion():
        return jsonify({'status': 'error', 'mensaje': 'Robot no conectado o inaccesible'}), 503

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
        })'''

if __name__ == '__main__':
    procesar_csv_tiempos()
    app.run(host='0.0.0.0', port=5000)