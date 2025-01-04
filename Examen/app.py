from flask import Flask, render_template, request, session, redirect, url_for

app = Flask(__name__)
app.secret_key = "supersecretkey"  # Necesario para usar sesiones

# Ruta para el menú principal
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/pregunta_1", methods=["GET", "POST"])
def pregunta_1():
    resultado = None
    if request.method == "POST":
        nombre = request.form["nombre"]
        edad = int(request.form["edad"])
        tarros = int(request.form["tarros"])

        total_sin_descuento = tarros * 9000
        if 18 <= edad <= 30:
            descuento = 0.15
        elif edad > 30:
            descuento = 0.25
        else:
            descuento = 0.0

        total_con_descuento = total_sin_descuento * (1 - descuento)
        descuento_aplicado = total_sin_descuento * descuento

        resultado = {
            "nombre": nombre,
            "total_sin_descuento": total_sin_descuento,
            "descuento_porcentaje": int(descuento * 100),  # Convertir a porcentaje
            "descuento_aplicado": descuento_aplicado,
            "total_con_descuento": total_con_descuento
        }

    return render_template("pregunta_1.html", resultado=resultado)

# Ruta para el formulario 2
@app.route("/pregunta_2", methods=["GET", "POST"])
def pregunta_2():
    mensaje = None
    if request.method == "POST":
        usuario = request.form["usuario"]
        contrasena = request.form["contrasena"]

        # Validar credenciales
        if usuario == "juan" and contrasena == "admin":
            session["usuario"] = "juan"
            session["rol"] = "administrador"
            return redirect(url_for("bienvenida"))
        elif usuario == "pepe" and contrasena == "user":
            session["usuario"] = "pepe"
            session["rol"] = "usuario"
            return redirect(url_for("bienvenida"))
        else:
            mensaje = "Usuario o contraseña incorrectos"

    return render_template("pregunta_2.html", mensaje=mensaje)


# Ruta para la bienvenida después de iniciar sesión
@app.route("/bienvenida")
def bienvenida():
    if "usuario" in session:
        usuario = session["usuario"]
        rol = session["rol"]
        return render_template("bienvenida.html", usuario=usuario, rol=rol)
    else:
        return redirect(url_for("pregunta_2"))


# Ruta para cerrar sesión
@app.route("/logout")
def logout():
    session.clear()  # Limpiar la sesión
    return redirect(url_for("pregunta_2"))

if __name__ == "__main__":
    app.run(debug=True)
