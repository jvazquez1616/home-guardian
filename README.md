# 🛡️ Home Guardian

Herramienta de seguridad de red casera escrita en Python. Escanea los dispositivos
conectados a tu red, detecta dispositivos nuevos/desconocidos, bloquea dominios de
publicidad y tracking (estilo Pi-hole), envía alertas en tiempo real por Telegram,
y ofrece un dashboard web para gestionar todo.

## Funcionalidades

- 📡 **Escáner de red** — detecta todos los dispositivos conectados (IP + MAC) usando ARP.
- 🚨 **Detección de dispositivos nuevos** — te alerta cuando algo desconocido se conecta.
- 💾 **Historial con SQLite** — guarda cuándo se vio cada dispositivo por primera y última vez.
- 🚫 **Bloqueador DNS estilo Pi-hole** — bloquea anuncios y tracking a nivel de red.
- 📲 **Alertas por Telegram** — notificaciones al instante en tu celular.
- 🌐 **Dashboard web** — interfaz visual para ver dispositivos y bloquear IPs.
- 🧱 **Firewall local (pf)** — bloquea tráfico entre tu Mac y dispositivos específicos.

## Cómo instalarlo

1. Clona el repositorio y entra a la carpeta.
2. Crea el entorno virtual:

python3 -m venv .venv
source .venv/bin/activate

3. Instala las dependencias:

pip install -r requirements.txt

4. (Opcional, para alertas) Crea un archivo `.env` en la raíz del proyecto:

TELEGRAM_TOKEN=tu_token_de_botfather
TELEGRAM_CHAT_ID=tu_chat_id

## Cómo usarlo

Corre el menú principal (necesita `sudo` porque el escáner y el DNS requieren permisos de red):

sudo python home_guardian.py

Vas a ver un menú con estas opciones:
1. Escanear la red ahora
2. Iniciar bloqueador DNS (Pi-hole)
3. Abrir dashboard web
4. Iniciar todo junto (DNS + Dashboard)
5. Salir

## Solución de problemas

- **El escáner no detecta ningún dispositivo:** desactiva cualquier VPN activa en tu
  computadora antes de escanear — el tráfico de una VPN pasa por una interfaz virtual
  y bloquea la detección ARP en tu red local.
- **El bloqueador DNS no encuentra `lista_negra.txt`:** asegúrate de correr el comando
  desde la carpeta raíz del proyecto, no desde otra ubicación.

## Limitaciones conocidas

- **YouTube:** el bloqueo por DNS no puede filtrar anuncios de YouTube, ya que sirve
  tanto videos como anuncios desde el mismo dominio (`googlsevideo.com`). Bloquearlo
  bloquearía YouTube por completo. Alternativas: uBlock Origin (nivel navegador) o
  SNI/DPI filtering (nivel proxy, más avanzado).
- **Firewall local (`pf`):** solo bloquea tráfico entre la propia Mac y un dispositivo
  específico — no bloquea el acceso a internet de otros dispositivos, ya que la Mac
  no es el router de la red.

## Investigación: intentos de bloqueo de dispositivos en la red

### Intento 1 — Firewall local con `pf` (macOS)
Implementado en `firewall.py`, usa el firewall nativo de macOS.

**Resultado:** ✅ Funciona, pero con la limitación de arquitectura ya descrita arriba
— solo protege el tráfico de la propia Mac, no de toda la red.

### Intento 2 — ARP Spoofing (Man-in-the-Middle)
Implementado en `arp_block.py` con scapy. La técnica: enviar respuestas ARP
falsificadas al dispositivo objetivo (haciéndole creer que la Mac es el router) y al
router (haciéndole creer que la Mac es el dispositivo objetivo), para que todo el
tráfico pase por la Mac y ahí se descarte.

**Debugging realizado:**
1. Primer intento con `scapy.send()` (Capa 3) — falló silenciosamente, con warnings
   indicando falta de MAC de destino Ethernet.
2. Corregido a `scapy.sendp()` (Capa 2) con frames Ethernet explícitos — confirmado
   con `tcpdump` que los paquetes salían bien formados cada 2 segundos.
3. A pesar de paquetes correctos, el dispositivo objetivo nunca perdió acceso a
   internet.

**Resultado:** ❌ No efectivo en esta red WiFi doméstica, pese a una implementación
técnicamente correcta.

**Hipótesis:**
- Muchos routers/APs WiFi modernos (incluso de ISP) descartan tramas ARP
  "sospechosas" enviadas por clientes que no son el router, a nivel de
  hardware/firmware — distinto de "AP/Client Isolation" (revisado y descartado).
- ARP spoofing es notoriamente más confiable en redes cableadas (Ethernet) que en
  WiFi, por este tipo de protecciones a nivel de radio.

**Aprendizaje clave:** implementar correctamente una técnica de ataque no garantiza
que sea efectiva — el entorno real de red puede neutralizarla. Lección valiosa de
seguridad ofensiva: la teoría y el laboratorio no siempre se traducen directo a la
práctica en redes reales.

### Próximo intento — Deauth Attack (802.11)
Requiere modo monitor + inyección de paquetes, no soportado nativamente por macOS.
Plan: usar un adaptador WiFi externo compatible (Alfa AWUS036NHA o similar) dentro
de una VM con Kali Linux (UTM), usando aircrack-ng. Pendiente de hardware.

## Estado del proyecto

- ✅ Fase 1 — escáner de dispositivos.
- ✅ Fase 2 — detección de nuevos, alertas y vista de ausentes.
- ✅ Fase 3 — historial con base de datos SQLite + barra de progreso.
- ✅ Fase 4 — bloqueador DNS estilo Pi-hole con lista negra ampliada (StevenBlack hosts).
- ✅ Fase 5 — alertas en tiempo real por Telegram.
- ✅ Fase 6 — dashboard web + firewall local (pf) + investigación de ARP spoofing.
- ✅ Punto de entrada unificado (`home_guardian.py` con menú).
- 🚧 Próximo — deauth attack con hardware externo (pendiente de adaptador WiFi).

## Tecnologías usadas

Python · Scapy · Flask · SQLite · dnslib · python-telegram-bot · pf (macOS)
