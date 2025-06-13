# Sistema de Control y Supervisión del Brazo Robótico con Gemelo Digital

Este repositorio contiene el código fuente desarrollado para la implementación de un sistema de supervisión y control de un brazo robótico **Niryo Ned2**, integrado con un **gemelo digital en Azure** y respaldado por una arquitectura de almacenamiento y servidor local.

## Estructura del repositorio

### 📁 `NiryoScripts/`
Contiene los scripts en Python responsables de ejecutar los distintos comportamientos del brazo robótico. Utiliza la librería `pyniryo` para controlar los movimientos, capturar estados y ejecutar acciones físicas programadas.

### 📁 `GemeloDigital/`
Incluye el código necesario para conectar con el gemelo digital en **Microsoft Azure**, permitiendo leer y actualizar información del nodo correspondiente mediante llamadas API. Aquí se define la lógica para el intercambio de datos con la nube.

### 📁 `bbdd_robot/`
Contiene los scripts encargados del tratamiento y almacenamiento de datos generados por el sistema. Los datos se guardan en:
- Un archivo Excel (formato `.xlsx`) con múltiples tablas para ejecuciones, errores y actividad.
- Un archivo `.csv` diario que se actualiza dinámicamente según el uso.

### 📄 `log.txt`
Archivo de texto utilizado como registro de actividad del servidor. Guarda mensajes informativos, errores y eventos importantes para facilitar el seguimiento y la depuración del sistema.

### 🐍 `server.py`
Script principal que implementa el servidor local y define la **API REST** utilizada por el sistema. Gestiona la comunicación entre el robot, la base de datos, el gemelo digital y la aplicación Android conectada.

---

> ⚙️ Proyecto desarrollado como parte de un Trabajo de Fin de Grado para demostrar la viabilidad técnica del control de sistemas robotizados conectados a gemelos digitales en entornos industrialesa través de llamdas REST.
