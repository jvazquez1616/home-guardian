
'Version: 1.0'
'''import scapy.all as scapy

'def escanear_red(ip_rango):
    # Crea una solicitud ARP (pregunta "¿quién tiene esta IP?")
    arp_request = scapy.ARP(pdst=ip_rango)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    paquete = broadcast / arp_request

    # Envía el paquete y espera respuestas (timeout de 2 segundos)
    respuestas = scapy.srp(paquete, timeout=2, verbose=False)[0]

    dispositivos = []
    for enviado, recibido in respuestas:
        dispositivos.append({"ip": recibido.psrc, "mac": recibido.hwsrc})

    return dispositivos

def mostrar_resultado(dispositivos):
    print("IP\t\t\tMAC")
    print("-" * 40)
    for d in dispositivos:
        print(f"{d['ip']}\t\t{d['mac']}")

if __name__ == "__main__":
    # Cambia esto por el rango de tu red (normalmente es así)
    rango = "192.168.1.1/24"
    dispositivos = escanear_red(rango)
    mostrar_resultado(dispositivos)'''

'version: 2.0'
'''
import scapy.all as scapy
import json
import os

ARCHIVO_CONOCIDOS = "dispositivos_conocidos.json"


def escanear_red(ip_rango, intentos=3):
    dispositivos_dict = {}

    for i in range(intentos):
        arp_request = scapy.ARP(pdst=ip_rango)
        broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
        paquete = broadcast / arp_request

        respuestas = scapy.srp(paquete, timeout=3, verbose=False, iface="en0")[0]

        for enviado, recibido in respuestas:
            dispositivos_dict[recibido.hwsrc] = recibido.psrc

    dispositivos = [{"ip": ip, "mac": mac} for mac, ip in dispositivos_dict.items()]
    return dispositivos

def cargar_conocidos():
    if not os.path.exists(ARCHIVO_CONOCIDOS):
        return []
    with open(ARCHIVO_CONOCIDOS, "r") as f:
        return json.load(f)

def guardar_conocidos(dispositivos):
    with open(ARCHIVO_CONOCIDOS, "w") as f:
        json.dump(dispositivos, f, indent=2)

def comparar_dispositivos(actuales, conocidos):
    macs_conocidas = {d["mac"] for d in conocidos}
    nuevos = [d for d in actuales if d["mac"] not in macs_conocidas]
    return nuevos

def mostrar_resultado(dispositivos, titulo=None):
    if titulo:
        print(f"\n{titulo}")
    print("IP\t\t\tMAC")
    print("-" * 40)
    if not dispositivos:
        print("(ninguno)")
    for d in dispositivos:
        print(f"{d['ip']}\t\t{d['mac']}")

if __name__ == "__main__":
    rango = "192.168.1.1/24"

    conocidos = cargar_conocidos()
    actuales = escanear_red(rango)

    mostrar_resultado(actuales, "📡 Dispositivos conectados ahora:")

    if conocidos:
        nuevos = comparar_dispositivos(actuales, conocidos)
        if nuevos:
            mostrar_resultado(nuevos, "🚨 ¡ALERTA! Dispositivos nuevos detectados:")
        else:
            print("\n✅ No hay dispositivos nuevos. Todo normal.")

        # Dispositivos conocidos que NO están conectados ahora mismo
        macs_actuales = {d["mac"] for d in actuales}
        desconectados = [d for d in conocidos if d["mac"] not in macs_actuales]
        mostrar_resultado(desconectados, "📴 Conocidos pero no conectados ahora:")
    else:
        print("\nPrimera vez corriendo el escáner — guardando estos como dispositivos conocidos.")
        nuevos = []

    # Combina conocidos + nuevos, sin duplicar por MAC
    macs_existentes = {d["mac"] for d in conocidos}
    actualizados = conocidos + [d for d in actuales if d["mac"] not in macs_existentes]

    guardar_conocidos(actualizados)

    '''

import scapy.all as scapy
import db

def escanear_red(ip_rango, intentos=3):
    dispositivos_dict = {}

    for i in range(intentos):
        arp_request = scapy.ARP(pdst=ip_rango)
        broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
        paquete = broadcast / arp_request
        respuestas = scapy.srp(paquete, timeout=3, verbose=False, iface="en0")[0]

        for enviado, recibido in respuestas:
            dispositivos_dict[recibido.hwsrc] = recibido.psrc

    return [{"ip": ip, "mac": mac} for mac, ip in dispositivos_dict.items()]

def mostrar_resultado(dispositivos, titulo=None):
    if titulo:
        print(f"\n{titulo}")
    print("IP\t\t\tMAC")
    print("-" * 40)
    if not dispositivos:
        print("(ninguno)")
    for d in dispositivos:
        print(f"{d['ip']}\t\t{d['mac']}")

if __name__ == "__main__":
    rango = "192.168.1.1/24"

    db.crear_tablas()
    actuales = escanear_red(rango)

    mostrar_resultado(actuales, "📡 Dispositivos conectados ahora:")

    nuevos = []
    for d in actuales:
        es_nuevo = db.registrar_dispositivo(d["mac"], d["ip"])
        if es_nuevo:
            nuevos.append(d)

    if nuevos:
        mostrar_resultado(nuevos, "🚨 ¡ALERTA! Dispositivos nuevos detectados:")
    else:
        print("\n✅ No hay dispositivos nuevos. Todo normal.")

    todos = db.obtener_todos_los_dispositivos()
    macs_actuales = {d["mac"] for d in actuales}
    desconectados = [d for d in todos if d["mac"] not in macs_actuales]
    mostrar_resultado(
        [{"ip": d["ip"], "mac": d["mac"]} for d in desconectados],
        "📴 Conocidos pero no conectados ahora:"
    )