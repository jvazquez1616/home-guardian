# Home Guardian

Herramienta de seguridad para monitorear los dispositivos conectados a mi red casera, escrita en Python.

## ¿Qué hace?
- Escanea la red local y detecta qué dispositivos están conectados.
- Alerta cuando aparece un dispositivo desconocido.

## Cómo correrlo
1. Crear entorno virtual: `python3 -m venv .venv`
2. Activarlo: `source .venv/bin/activate`
3. Instalar dependencias: `pip install -r requirements.txt`
4. Correr: `python main.py`

## Estado del proyecto
🚧 En desarrollo — Fase 1: escáner de dispositivos.
Problemas en la primera fase:
1. Si tienes un VPN activo en tu computadore, desactivalo. No vas a poder escanear nada.
## Estado del proyecto
✅ Fase 1 completa — escáner de dispositivos funcionando.
🚧 Próximo: detección de dispositivos nuevos/desconocidos.
## Estado del proyecto
✅ Fase 1 completa — escáner de dispositivos.
✅ Fase 2 completa — detección de nuevos, alertas y vista de dispositivos ausentes.
🚧 Próximo: historial con base de datos (SQLite).
## Estado del proyecto
✅ Fase 1 completa — escáner de dispositivos.
✅ Fase 2 completa — detección de nuevos, alertas y vista de ausentes.
✅ Fase 3 completa — historial con base de datos SQLite + barra de progreso durante el escaneo.
🚧 Próximo: bloqueador de dominios estilo Pi-hole.
## Limitaciones conocidas
- El bloqueo por DNS no puede filtrar anuncios de YouTube, ya que YouTube sirve tanto videos como anuncios desde el mismo dominio (`googlevideo.com`). Bloquearlo bloquearía YouTube completo.
- Para ese caso específico, un enfoque como uBlock Origin (nivel navegador) o SNI/DPI filtering (nivel proxy, más avanzado) sería necesario — posible Fase futura.

## Estado del proyecto
✅ Fase 1 completa — escáner de dispositivos.
✅ Fase 2 completa — detección de nuevos, alertas y vista de ausentes.
✅ Fase 3 completa — historial con base de datos SQLite + barra de progreso.
✅ Fase 4 completa — bloqueador DNS estilo Pi-hole con lista negra ampliada (StevenBlack hosts).
🚧 Próximo: alertas en tiempo real (Telegram/correo).
## Investigación: Bloqueo de dispositivos en la red

### Intento 1: Firewall local con pf (macOS)
Implementado en `firewall.py`. Usa el firewall nativo de macOS (Packet Filter) para
bloquear tráfico hacia/desde IPs específicas.

**Resultado:** ✅ Funciona, pero con una limitación fundamental de arquitectura:
`pf` solo controla el tráfico que entra o sale de la propia Mac donde corre el
script. Como mi Mac no es el router de la red, esto NO bloquea el acceso a
internet de otros dispositivos (celulares, TVs, etc.) — solo bloquea la
comunicación entre mi Mac y ese dispositivo específico.

**Conclusión:** Útil como demostración de manejo de firewalls a nivel de sistema
operativo, pero no es una solución de bloqueo de red completa.

### Intento 2: ARP Spoofing (Man-in-the-Middle)
Implementado en `arp_block.py` usando scapy. La técnica: enviar respuestas ARP
falsificadas al dispositivo objetivo (haciéndole creer que mi Mac es el router)
y al router (haciéndole creer que mi Mac es el dispositivo objetivo), de forma
que todo el tráfico del objetivo pase por mi Mac, donde se descarta.

**Debugging realizado:**
1. Primer intento usó `scapy.send()` (Capa 3) — falló silenciosamente, con
   warnings de scapy indicando que faltaba especificar la MAC de destino Ethernet.
2. Corregido a `scapy.sendp()` (Capa 2) con frames Ethernet explícitos — confirmado
   con `tcpdump` que los paquetes ARP falsificados salían correctamente formados,
   cada 2 segundos, con la MAC correcta.
3. A pesar de que los paquetes salían bien, el dispositivo objetivo (iPhone) nunca
   perdió acceso a internet.

**Resultado:** ❌ No efectivo en esta red WiFi doméstica, a pesar de una
implementación técnicamente correcta.

**Hipótesis de por qué falla:**
- Muchos routers/access points WiFi modernos (incluso de ISP, no solo mesh)
  implementan protecciones de hardware/firmware que descartan tramas ARP
  "sospechosas" enviadas por otros clientes WiFi (no el router mismo).
- Esto es distinto a "AP/Client Isolation" (que se revisó y no estaba activo en
  este router) — parece ser una protección más profunda, posiblemente a nivel
  de chipset WiFi.
- ARP spoofing es notoriamente más confiable en redes cableadas (Ethernet)