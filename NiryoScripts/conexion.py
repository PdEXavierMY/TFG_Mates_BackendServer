import subprocess
import platform
import socket
import ipaddress
from concurrent.futures import ThreadPoolExecutor

def obtener_red_local():
    # Obtener IP local
    hostname = socket.gethostname()
    local_ip = socket.gethostbyname(hostname)

    # Asumimos máscara 255.255.255.0 (/24)
    red = ipaddress.IPv4Network(local_ip + "/24", strict=False)
    return red

def ping_ip(ip):
    param = "-n" if platform.system().lower() == "windows" else "-c"
    try:
        subprocess.check_output(["ping", param, "1", str(ip)], stderr=subprocess.DEVNULL)
        try:
            host = socket.gethostbyaddr(str(ip))[0]
        except socket.herror:
            host = "Desconocido"
        return (str(ip), host)
    except subprocess.CalledProcessError:
        return None

def escanear_red(red):
    dispositivos = []
    with ThreadPoolExecutor(max_workers=100) as executor:
        for result in executor.map(ping_ip, red.hosts()):
            if result:
                dispositivos.append(result)
    return dispositivos

if __name__ == "__main__":
    red = obtener_red_local()
    print(f"Escaneando red {red}...\n")
    dispositivos = escanear_red(red)

    print("Dispositivos encontrados:")
    for idx, (ip, host) in enumerate(dispositivos, 1):
        print(f"{idx}. IP: {ip} - HOST: {host}")
