from dnslib import DNSRecord, DNSHeader, RR, A
from dnslib.server import DNSServer, BaseResolver
import socket
import os
import time

CARPETA_SCRIPT = os.path.dirname(os.path.abspath(__file__))
ARCHIVO_LISTA_NEGRA = os.path.join(CARPETA_SCRIPT, "lista_negra.txt")
DNS_UPSTREAM = "8.8.8.8"

def cargar_lista_negra_desde_hosts(archivo_hosts):
    dominios = set()
    with open(archivo_hosts, "r") as f:
        for linea in f:
            linea = linea.strip()
            if linea.startswith("0.0.0.0") or linea.startswith("127.0.0.1"):
                partes = linea.split()
                if len(partes) >= 2:
                    dominios.add(partes[1].lower())
    return dominios

def cargar_lista_negra():
    dominios = set()

    with open(ARCHIVO_LISTA_NEGRA, "r") as f:
        dominios.update(linea.strip().lower() for linea in f if linea.strip())

    ruta_hosts = os.path.join(CARPETA_SCRIPT, "hosts_stevenblack.txt")
    if os.path.exists(ruta_hosts):
        dominios.update(cargar_lista_negra_desde_hosts(ruta_hosts))

    return dominios

class ResolverBloqueador(BaseResolver):
    def __init__(self):
        self.lista_negra = cargar_lista_negra()
        print(f"Lista negra cargada con {len(self.lista_negra)} dominios.")

    def resolve(self, request, handler):
        pregunta = request.q
        dominio = str(pregunta.qname).rstrip(".").lower()

        respuesta = request.reply()

        bloqueado = any(dominio == d or dominio.endswith("." + d) for d in self.lista_negra)

        if bloqueado:
            print(f"🚫 Bloqueado: {dominio}")
            respuesta.add_answer(RR(pregunta.qname, rdata=A("0.0.0.0"), ttl=60))
            return respuesta

        try:
            consulta_real = request.send(DNS_UPSTREAM, 53, timeout=3)
            respuesta_real = DNSRecord.parse(consulta_real)
            return respuesta_real
        except Exception as e:
            print(f"Error consultando DNS real para {dominio}: {e}")
            return respuesta


def iniciar_servidor_dns():
    resolver = ResolverBloqueador()
    servidor = DNSServer(resolver, port=53, address="127.0.0.1")
    print("Servidor DNS corriendo en 127.0.0.1:53 (Ctrl+C para detener)")
    servidor.start_thread()

    try:
        while servidor.isAlive():
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nDeteniendo servidor DNS...")


if __name__ == "__main__":
    iniciar_servidor_dns()