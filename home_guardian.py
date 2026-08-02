import threading
import sys

from main import ejecutar_escaneo
from dns_server import iniciar_servidor_dns
from dashboard import iniciar_dashboard

def mostrar_menu():
    print("\n" + "=" * 40)
    print("🛡️  HOME GUARDIAN")
    print("=" * 40)
    print("1. Escanear la red ahora")
    print("2. Iniciar bloqueador DNS (Pi-hole)")
    print("3. Abrir dashboard web")
    print("4. Iniciar TODO (DNS + Dashboard juntos)")
    print("5. Salir")
    return input("\nElige una opción (1-5): ").strip()

def main():
    while True:
        opcion = mostrar_menu()

        if opcion == "1":
            ejecutar_escaneo()
        elif opcion == "2":
            iniciar_servidor_dns()
        elif opcion == "3":
            print("Dashboard disponible en: http://127.0.0.1:5000")
            iniciar_dashboard()
        elif opcion == "4":
            print("Iniciando DNS y Dashboard en segundo plano...")
            print("Dashboard disponible en: http://127.0.0.1:5000")
            hilo_dns = threading.Thread(target=iniciar_servidor_dns, daemon=True)
            hilo_dns.start()
            iniciar_dashboard()
        elif opcion == "5":
            print("👋 Hasta luego.")
            sys.exit(0)
        else:
            print("Opción inválida, intenta de nuevo.")

if __name__ == "__main__":
    main()