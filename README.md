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