from flask import Flask, render_template, request, redirect, url_for
import db
import firewall

app = Flask(__name__)

@app.route("/")
def inicio():
    dispositivos = db.obtener_todos_los_dispositivos()
    bloqueadas = firewall.obtener_bloqueadas()
    return render_template("index.html", dispositivos=dispositivos, bloqueadas=bloqueadas)

@app.route("/bloquear", methods=["POST"])
def bloquear():
    ip = request.form.get("ip")
    if ip:
        firewall.bloquear_ip(ip)
    return redirect(url_for("inicio"))

@app.route("/desbloquear", methods=["POST"])
def desbloquear():
    ip = request.form.get("ip")
    if ip:
        firewall.desbloquear_ip(ip)
    return redirect(url_for("inicio"))


def iniciar_dashboard():
    app.run(debug=False, port=5000, use_reloader=False)


if __name__ == "__main__":
    iniciar_dashboard()