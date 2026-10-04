import math

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

            if (
                not all(math.isfinite(value) for value in (peso, altura, actividad))
                or not 30 <= peso <= 300
                or not 100 <= altura <= 250
                or not 18 <= edad <= 120
                or genero not in {'hombre', 'mujer'}
                or actividad not in {1.2, 1.375, 1.55, 1.725}
            ):
                raise ValueError

            tmb = (10 * peso) + (6.25 * altura) - (5 * edad)

            if genero == 'hombre':
                tmb += 5
            else:
                tmb -= 161

            calorias_totales = round(tmb * actividad)
            imc = peso / (altura / 100) ** 2

            if imc < 16:
                categoria_imc = 'Bajo peso marcado'
                recomendacion_imc = (
                    'Este IMC bajo es una señal de alarma, no un diagnóstico. '
                    'Solicita una valoración de salud pronto, especialmente si '
                    'has perdido peso sin proponértelo o tienes otros síntomas.'
                )
            elif imc < 18.5:
                categoria_imc = 'Bajo peso'
                recomendacion_imc = (
                    'El IMC está por debajo del rango de referencia. Considera '
                    'consultar con un profesional de salud para revisar tu '
                    'alimentación, antecedentes y posibles causas.'
                )
            elif imc < 25:
                categoria_imc = 'Rango de referencia'
                recomendacion_imc = (
                    'Mantén hábitos sostenibles de alimentación variada y '
                    'actividad física adecuados para ti.'
                )
            elif imc < 30:
                categoria_imc = 'Sobrepeso'
                recomendacion_imc = (
                    'El IMC está en el rango de sobrepeso. Es una señal para '
                    'revisar hábitos y otros indicadores de salud con un '
                    'profesional; evita dietas extremas.'
                )
            elif imc < 35:
                categoria_imc = 'Obesidad clase I'
                recomendacion_imc = (
                    'El IMC está en el rango de obesidad clase I. Se recomienda '
                    'una valoración profesional integral y un plan de salud '
                    'individualizado, sin estigmas ni medidas extremas.'
                )
            elif imc < 40:
                categoria_imc = 'Obesidad clase II'
                recomendacion_imc = (
                    'El IMC está en el rango de obesidad clase II. Conviene '
                    'solicitar una valoración profesional integral para recibir '
                    'apoyo y opciones de cuidado individualizadas.'
                )
            else:
                categoria_imc = 'Obesidad clase III'
                recomendacion_imc = (
                    'El IMC está en el rango de obesidad clase III. Se recomienda '
                    'concertar una valoración profesional integral para revisar '
                    'la salud y acordar opciones de cuidado individualizadas.'
                )

            if imc < 18.5:
                enfoque_alimentario = (
                    'Prioriza comidas completas y alimentos nutritivos con buena '
                    'densidad de energía. El IMC por sí solo no permite saber la '
                    'causa del bajo peso ni determinar tus necesidades.'
                )
                fuentes_carbohidratos = (
                    'Avena preparada con leche o bebida de soya, arroz, papa, '
                    'maíz, pan integral, frijoles, lentejas y frutas.'
                )
                fuentes_proteina = (
                    'Huevos, yogur o leche, queso, pescado, pollo, tofu, frijoles, '
                    'lentejas y garbanzos; incorpora una fuente en cada comida '
                    'principal.'
                )
                fuentes_grasas = (
                    'Aguacate, crema de cacahuate o frutos secos, semillas y aceite '
                    'de oliva; puedes agregarlos a avena, arroz o verduras.'
                )
                guia_porciones = (
                    'En cada comida combina una fuente de proteína, un alimento '
                    'con almidón (arroz, papa, maíz, avena o pan) y verduras o '
                    'fruta. Añade grasas nutritivas para enriquecer la comida; no '
                    'es necesario limitar porciones con el método de medio plato.'
                )
                rutina_comidas = (
                    'Como estructura flexible, prueba 3 comidas principales y '
                    '2–3 colaciones nutritivas si te resulta difícil comer '
                    'suficiente: yogur con avena, pan con huevo o fruta con crema '
                    'de cacahuate. Si hay pérdida de peso involuntaria o IMC menor '
                    'de 16, consulta pronto con un profesional.'
                )
            elif imc < 25:
                enfoque_alimentario = (
                    'Busca variedad y equilibrio sin necesidad de seguir una '
                    'dieta restrictiva. Elige alimentos que se adapten a tus '
                    'preferencias, cultura y presupuesto.'
                )
                fuentes_carbohidratos = (
                    'Avena, arroz integral, maíz, papa, pan integral, frijoles, '
                    'lentejas, frutas enteras y verduras.'
                )
                fuentes_proteina = (
                    'Frijoles, lentejas, garbanzos, huevos, pescado, pollo, tofu, '
                    'yogur natural o frutos secos.'
                )
                fuentes_grasas = (
                    'Aguacate, nueces, semillas y aceites vegetales como el de '
                    'oliva o canola.'
                )
                guia_porciones = (
                    'Una guía visual flexible es llenar aproximadamente la mitad '
                    'del plato con verduras y fruta, un cuarto con proteína y un '
                    'cuarto con granos integrales o tubérculos.'
                )
                rutina_comidas = (
                    'Distribuye las comidas de acuerdo con tu horario y hambre; '
                    'por ejemplo, 3 comidas principales y una colación si la '
                    'necesitas. No hay una frecuencia única obligatoria.'
                )
            else:
                enfoque_alimentario = (
                    'Prioriza cambios graduales y sostenibles; el IMC no define '
                    'por sí solo qué debes comer ni implica que debas seguir una '
                    'dieta extrema.'
                )
                fuentes_carbohidratos = (
                    'Avena, arroz integral, maíz, papa, frijoles, lentejas, '
                    'verduras y frutas enteras. Prefiere agua en lugar de bebidas '
                    'azucaradas la mayoría de las veces.'
                )
                fuentes_proteina = (
                    'Frijoles, lentejas, garbanzos, huevos, pescado, pollo, tofu '
                    'o yogur natural; combínalos con verduras y una porción de '
                    'granos integrales o tubérculos.'
                )
                fuentes_grasas = (
                    'Aguacate, nueces, semillas y aceites vegetales; sírvelos en '
                    'cantidades moderadas y evita depender de frituras o '
                    'productos ultraprocesados.'
                )
                guia_porciones = (
                    'En comida y cena, usa como referencia medio plato de '
                    'verduras, un cuarto de proteína y un cuarto de arroz integral, '
                    'maíz, papa u otro alimento con almidón. Ajusta las cantidades '
                    'a tu hambre y necesidades con orientación profesional; no '
                    'hagas recortes drásticos.'
                )
                rutina_comidas = (
                    'Una rutina práctica puede ser 3 comidas principales y una '
                    'colación planificada solo si tienes hambre o tu horario lo '
                    'requiere. Evita saltarte comidas para compensar; la cantidad '
                    'y frecuencia adecuadas varían entre personas.'
                )

            resultado = {
                'calorias': calorias_totales,
                'carbohidratos': round(calorias_totales * 0.50 / 4),
                'proteina': round(calorias_totales * 0.20 / 4),
                'grasas': round(calorias_totales * 0.30 / 9),
                'imc': round(imc, 1),
                'categoria_imc': categoria_imc,
                'recomendacion_imc': recomendacion_imc,
                'enfoque_alimentario': enfoque_alimentario,
                'fuentes_carbohidratos': fuentes_carbohidratos,
                'fuentes_proteina': fuentes_proteina,
                'fuentes_grasas': fuentes_grasas,
                'guia_porciones': guia_porciones,
                'rutina_comidas': rutina_comidas,
            }
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