from flask import Flask, request, jsonify
import subprocess
import os
import sys
from datetime import datetime

app = Flask(__name__)

# Carpeta donde están los scripts
SCRIPTS_DIR = os.path.join(os.path.dirname(__file__), 'NiryoScripts')

@app.route('/ejecutar', methods=['POST'])
def ejecutar_script():
    data = request.get_json()
    if not data or 'programa' not in data:
        return jsonify({'status': 'error', 'mensaje': 'Falta el parámetro "programa"'}), 400

    nombre_script = data['programa']
    script_path = os.path.join(SCRIPTS_DIR, f'{nombre_script}.py')
    python_cmd = 'python3' if sys.platform != 'win32' else 'python'

    if not os.path.isfile(script_path):
        return jsonify({'status': 'error', 'mensaje': f'El script "{nombre_script}" no existe'}), 404

    try:
        # Ejecuta el script de forma segura
        resultado = subprocess.run([python_cmd, script_path], capture_output=True, text=True, check=True)
        # Registro en log
        with open("log.txt", "a", encoding="utf-8") as log_file:
            log_file.write(f"[{datetime.now()}] Éxito: {nombre_script}\nSalida:\n{resultado.stdout}\n\n")
        return jsonify({
            'status': 'ok',
            'mensaje': f'Script "{nombre_script}" ejecutado correctamente',
        })
    except subprocess.CalledProcessError as e:
        # Registro en log de errores
        with open("log.txt", "a", encoding="utf-8") as log_file:
            log_file.write(f"[{datetime.now()}] ERROR: {nombre_script}\nError:\n{e.stderr}\n\n")
        return jsonify({
            'status': 'error',
            'mensaje': f'Error al ejecutar el script: {e.stderr.strip()}',
            'codigo': e.returncode
        }), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)