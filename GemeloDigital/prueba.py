from dt_helper import get_access_token, get_twin_data, put_twin_data
import os
import time

def main():
    try:
        # 1. Obtener token
        token = get_access_token()
        print("Token obtenido correctamente.")

        # 2. Definir endpoint del Twin
        endpoint = f"Twin/RobotArm"

        # 3. GET del Twin
        twin_data = get_twin_data(endpoint, token)
        print("Datos del Twin:")
        print(twin_data)

        time.sleep(15)  # Espera de 2 segundos

          # 4. PUT del campo 'informes' con nuevo valor 3
        nuevo_estado = {
            "informes": 4
        }
        resultado = put_twin_data(endpoint, nuevo_estado, token)
        if resultado:
            print("Información actualizada correctamente en 'informes'")
        else:
            print("Falló la actualización de 'informes'")

        # 5. Confirmar con un segundo GET
        twin_data_actualizado = get_twin_data(endpoint, token)
        print("Datos del Twin actualizados:")
        print(twin_data_actualizado)

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
