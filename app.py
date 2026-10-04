from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/comunidad")
def comunidad():
    return render_template("Comunidad/comunidad.html")


@app.route("/proyectos")
def proyectos():
    return render_template("Proyectos/proyectos.html")


@app.route("/nutria", methods=["GET", "POST"])
def nutria():
    resultado = None

    if request.method == 'POST':
        try:
            genero = request.form.get('genero')
            peso = float(request.form.get('peso'))
            altura = float(request.form.get('altura'))
            edad = int(request.form.get('edad'))
            actividad = float(request.form.get('actividad'))

            tmb = (10 * peso) + (6.25 * altura) - (5 * edad)

            if genero == 'hombre':
                tmb += 5
            else:
                tmb -= 161

            calorias_totales = round(tmb * actividad)

            resultado = {'calorias': calorias_totales}
        except (ValueError, TypeError):
            resultado = {'error': 'Por favor, introduce valores numéricos válidos.'}

    return render_template(
        "Proyectos/SX_Nutria/nutria.html",
        resultado=resultado,
    )


@app.route("/consultoria")
def consultoria():
    return render_template("Consultoria/consultoria.html")


@app.route("/tienda")
def tienda():
    return render_template("Tienda/tienda.html")


@app.route("/blog")
def blog():
    return render_template("Blog/blog.html")


if __name__ == "__main__":
    app.run(debug=True)