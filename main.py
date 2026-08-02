import scapy.all as scapy
import db
from tqdm import tqdm
import threading
import time
from alertas import enviar_alerta_telegram

def escanear_red(ip_rango, intentos=3):
    dispositivos_dict = {}
    pasos_por_intento = 15
    total_pasos = intentos * pasos_por_intento

    with tqdm(total=total_pasos, desc="Escaneando red", unit="paso") as barra:
        for i in range(intentos):
            resultado = {}

            def hacer_escaneo():
                arp_request = scapy.ARP(pdst=ip_rango)
                broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
                paquete = broadcast / arp_request
                resultado["respuestas"] = scapy.srp(paquete, timeout=3, verbose=False, iface="en0")[0]

            hilo = threading.Thread(target=hacer_escaneo)
            hilo.start()

            pasos_dados = 0
            while hilo.is_alive() and pasos_dados < pasos_por_intento:
                time.sleep(3 / pasos_por_intento)
                barra.update(1)
                pasos_dados += 1

            hilo.join()

            if pasos_dados < pasos_por_intento:
                barra.update(pasos_por_intento - pasos_dados)

            for enviado, recibido in resultado["respuestas"]:
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


def ejecutar_escaneo():
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
        lista_texto = "\n".join([f"- IP: {d['ip']} MAC: {d['mac']}" for d in nuevos])
        enviar_alerta_telegram(f"🚨 Dispositivo(s) nuevo(s) detectado(s) en tu red:\n{lista_texto}")
    else:
        print("\n✅ No hay dispositivos nuevos. Todo normal.")

    todos = db.obtener_todos_los_dispositivos()
    macs_actuales = {d["mac"] for d in actuales}
    desconectados = [d for d in todos if d["mac"] not in macs_actuales]
    mostrar_resultado(
        [{"ip": d["ip"], "mac": d["mac"]} for d in desconectados],
        "📴 Conocidos pero no conectados ahora:"
    )


if __name__ == "__main__":
    ejecutar_escaneo()