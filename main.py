import scapy.all as scapy

def escanear_red(ip_rango):
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
    mostrar_resultado(dispositivos)