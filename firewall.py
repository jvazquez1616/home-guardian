import subprocess
import os

ARCHIVO_ANCHOR = "/etc/pf.anchors/home-guardian"

def _existe_archivo():
    return os.path.exists(ARCHIVO_ANCHOR)

def _escribir_reglas(ips_bloqueadas):
    """Reescribe el archivo de reglas con la lista actual de IPs bloqueadas."""
    with open(ARCHIVO_ANCHOR, "w") as f:
        for ip in ips_bloqueadas:
            f.write(f"block drop quick from {ip} to any\n")
            f.write(f"block drop quick from any to {ip}\n")

def _recargar_pf():
    """Le dice a pf que recargue las reglas y se asegura que esté activo."""
    subprocess.run(["pfctl", "-f", "/etc/pf.conf"], check=True, capture_output=True)
    subprocess.run(["pfctl", "-e"], capture_output=True)  # activa pf si estaba apagado

def obtener_bloqueadas():
    if not _existe_archivo():
        return []
    with open(ARCHIVO_ANCHOR, "r") as f:
        lineas = f.readlines()
    ips = set()
    for linea in lineas:
        partes = linea.split()
        if "from" in partes:
            idx = partes.index("from")
            ip_candidata = partes[idx + 1]
            if ip_candidata != "any":
                ips.add(ip_candidata)
    return list(ips)

def bloquear_ip(ip):
    actuales = obtener_bloqueadas()
    if ip not in actuales:
        actuales.append(ip)
    _escribir_reglas(actuales)
    _recargar_pf()

def desbloquear_ip(ip):
    actuales = obtener_bloqueadas()
    actuales = [i for i in actuales if i != ip]
    _escribir_reglas(actuales)
    _recargar_pf()