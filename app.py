import math

from flask import Flask, abort, redirect, render_template, request, url_for

# La aplicación concentra las rutas públicas y los cálculos usados por las páginas.
app = Flask(__name__)

SX_LIBRARY_AREAS = {
    "marketing": {
        "area_name": "Marketing",
        "area_description": "Libros y materiales sobre marketing, comunicación, marcas, mercados y estrategias para conectar proyectos con sus públicos.",
    },
    "educacion": {
        "area_name": "Educación",
        "area_description": "Libros y materiales sobre enseñanza, aprendizaje, pedagogía y recursos educativos.",
    },
}

SX_LIBRARY_REMOVED_EDUCATION_CATEGORIES = (
    "idiomas",
    "salud",
    "agro",
    "fantasia",
    "literatura",
    "pedagogia",
)


# Páginas generales del sitio y recursos de la comunidad.
@app.route("/")
def home():
    return render_template("index.html")


@app.route("/comunidad")
def comunidad():
    return render_template("Comunidad/comunidad.html")


@app.route("/comunidad/repositorios")
def comunidad_repositorios():
    return render_template("Comunidad/Repositorios/repositorios.html")


@app.route("/comunidad/colaboradores")
def comunidad_colaboradores():
    return render_template("Comunidad/Colaboradores/colaboradores.html")


@app.route("/comunidad/cumplimiento")
def comunidad_cumplimiento():
    return render_template("Comunidad/Cumplimiento/cumplimiento.html")


@app.route("/proyectos")
def proyectos():
    return render_template("Proyectos/proyectos.html")


# Las fichas informativas comparten una plantilla; cada ruta aporta los datos de
# un borrador y las decisiones que siguen pendientes para ese proyecto.
@app.route("/sx-library")
def sx_library():
    return render_template("Proyectos/SX_Library/library.html")


@app.route("/sx-library/derecho")
def sx_library_derecho():
    return render_template("Proyectos/SX_Library/Derecho/derecho.html")


@app.route("/sx-library/derecho/fundamentos-juridicos-colombia")
def sx_library_fundamentos_juridicos():
    return render_template(
        "Proyectos/SX_Library/Derecho/Fundamentos_juridicos_Colombia/fundamentos_juridicos_colombia.html"
    )


@app.route("/sx-library/software")
def sx_library_software():
    return render_template("Proyectos/SX_Library/Software/software.html")


@app.route("/sx-library/software/pensamiento-algoritmico")
def sx_library_pensamiento_algoritmico():
    return render_template(
        "Proyectos/SX_Library/Software/Pensamiento_algoritmico/pensamiento_algoritmico.html"
    )


@app.route("/sx-library/marketing")
def sx_library_marketing():
    return render_template("Proyectos/SX_Library/Marketing/marketing.html")


@app.route("/sx-library/marketing/investigacion-de-mercados")
def sx_library_investigacion_mercados():
    return render_template(
        "Proyectos/SX_Library/Marketing/Investigacion_mercados/investigacion_mercados.html"
    )


@app.route("/sx-library/marketing/plan-de-marketing")
def sx_library_plan_marketing():
    return render_template(
        "Proyectos/SX_Library/Marketing/Plan_marketing/plan_marketing.html"
    )


@app.route("/sx-library/marketing/plan-de-ventas")
def sx_library_plan_ventas():
    return render_template(
        "Proyectos/SX_Library/Marketing/Plan_ventas/plan_ventas.html"
    )


@app.route("/sx-library/marketing/plan-de-mejora")
def sx_library_plan_mejora():
    return render_template(
        "Proyectos/SX_Library/Marketing/Plan_mejora/plan_mejora.html"
    )


@app.route("/sx-library/educacion/educacion-digital")
def sx_library_educacion_digital():
    return render_template(
        "Proyectos/SX_Library/Educacion/Educacion_digital/educacion_digital.html"
    )


@app.route("/sx-library/educacion/educacion-inclusiva")
def sx_library_educacion_inclusiva():
    return render_template(
        "Proyectos/SX_Library/Educacion/Educacion_inclusiva/educacion_inclusiva.html"
    )


@app.route("/sx-library/educacion/inclusividad-legal")
def sx_library_inclusividad_legal():
    return render_template(
        "Proyectos/SX_Library/Educacion/Inclusividad_legal/inclusividad_legal.html"
    )


@app.route("/sx-library/educacion/pedagogia/educacion-digital")
def sx_library_educacion_digital_legacy():
    return redirect(url_for("sx_library_educacion_digital"), code=301)


@app.route("/sx-library/educacion/<subarea_slug>")
def sx_library_removed_education_category(subarea_slug):
    if subarea_slug not in SX_LIBRARY_REMOVED_EDUCATION_CATEGORIES:
        abort(404)
    return redirect(url_for("sx_library_area", area_slug="educacion"), code=301)


@app.route("/sx-library/<area_slug>")
def sx_library_area(area_slug):
    if area_slug in SX_LIBRARY_REMOVED_EDUCATION_CATEGORIES:
        return redirect(url_for("sx_library_area", area_slug="educacion"), code=301)
    area = SX_LIBRARY_AREAS.get(area_slug)
    if area is None:
        abort(404)
    return render_template(
        "Proyectos/SX_Library/area.html",
        area_slug=area_slug,
        **area,
    )


@app.route("/sx-library/paz-y-conflicto")
def sx_library_paz_y_conflicto():
    return render_template(
        "Proyectos/SX_Library/Derecho/Paz_y_conflicto/paz_y_conflicto.html"
    )


@app.route("/sx-woodpecker-os")
def sx_woodpecker_os():
    return render_template(
        "Proyectos/borrador.html",
        project_name="SX Woodpecker OS",
        summary=(
            "Una propuesta de sistema operativo basado en Debian, orientado al "
            "aseguramiento de calidad y seguridad en infraestructuras digitales."
        ),
        pending_details=[
            "Definir los componentes y herramientas que formarán parte del sistema.",
            "Establecer el alcance de las pruebas y los perfiles de infraestructura compatibles.",
            "Documentar requisitos, instalación, mantenimiento y ciclo de actualizaciones.",
        ],
    )


@app.route("/sx-orange-page")
def sx_orange_page():
    return render_template(
        "Proyectos/borrador.html",
        project_name="SX Orange Page",
        summary=(
            "Una propuesta de directorio local para consultar información general "
            "y datos de ubicación de comercios."
        ),
        pending_details=[
            "Definir las zonas y categorías incluidas en el directorio.",
            "Acordar cómo se verificará y actualizará la información publicada.",
            "Establecer criterios de privacidad y autorización para los datos.",
        ],
    )


@app.route("/sx-recruiter")
def sx_recruiter():
    return render_template(
        "Proyectos/borrador.html",
        project_name="SX Recruiter",
        summary=(
            "Una propuesta para reunir oportunidades laborales de distintos tipos "
            "dirigidas a personas de Latinoamérica."
        ),
        pending_details=[
            "Definir las fuentes y el proceso de revisión de cada oportunidad.",
            "Precisar las categorías, regiones y condiciones que se mostrarán.",
            "Establecer cómo se reportarán ofertas vencidas o información incorrecta.",
        ],
    )


@app.route("/sx-registros")
def sx_registros():
    return render_template(
        "Proyectos/borrador.html",
        project_name="SX Registros",
        summary=(
            "Una propuesta de canal oficial para registrar el interés en participar "
            "en los proyectos de SXcontrol."
        ),
        pending_details=[
            "Definir qué información sería necesaria y con qué propósito.",
            "Publicar las condiciones de privacidad y el tiempo de conservación de datos.",
            "Diseñar el proceso de revisión y respuesta antes de aceptar registros.",
        ],
    )


@app.route("/sx-documento")
def sx_documento():
    return render_template(
        "Proyectos/borrador.html",
        project_name="SX Documento",
        summary=(
            "Una propuesta de herramienta con campos guiados para organizar y "
            "dar formato a documentos según el estilo que necesite cada persona, "
            "por ejemplo APA 7."
        ),
        pending_details=[
            "Definir los tipos de documento y estilos de formato que se admitirán.",
            "Precisar los campos guiados, las reglas de formato y las opciones de exportación.",
            "Verificar las reglas editoriales vigentes antes de anunciar compatibilidad con APA 7.",
        ],
    )


@app.route("/sx-help")
def sx_help():
    return render_template(
        "Proyectos/borrador.html",
        project_name="SX Help",
        tagline="Orientación jurídica accesible para personas de escasos recursos.",
        summary=(
            "Una propuesta de espacio online para acercar información jurídica "
            "general y recursos de consulta, y servir como canal de orientación "
            "para denuncias ciudadanas de personas que enfrentan barreras para "
            "acceder a apoyo."
        ),
        pending_details=[
            "Definir los países, jurisdicciones y temas que cubriría el servicio.",
            "Definir el alcance del canal de denuncias, las entidades o mecanismos oficiales a los que podría orientar y cómo evitar prometer recepción o seguimiento de casos.",
            "Determinar si ofrecerá información general, atención gratuita, contacto con profesionales o una combinación de opciones.",
            "Establecer revisión por profesionales, privacidad, manejo seguro de datos sensibles y límites claros; la herramienta no debe presentarse como sustituto de asesoría legal individual ni de los canales oficiales de denuncia.",
        ],
    )


@app.route("/sx-mistico")
def sx_mistico():
    return render_template(
        "Proyectos/borrador.html",
        project_name="SX Místico",
        summary=(
            "Una propuesta de página dedicada al esoterismo, sus tradiciones, "
            "prácticas y contenidos relacionados."
        ),
        pending_details=[
            "Definir las temáticas, tradiciones y formatos de contenido que incluirá.",
            "Establecer criterios editoriales para distinguir información cultural de afirmaciones no verificadas.",
            "Diseñar la estructura de navegación y las secciones de la página.",
        ],
    )


@app.route("/sx-gestion-agil")
def sx_gestion_agil():
    return render_template(
        "Proyectos/borrador.html",
        project_name="SX Gestión Ágil",
        tagline="Organización empresarial con prácticas ágiles adaptables.",
        summary=(
            "Una propuesta de herramienta para ayudar a pequeñas empresas y "
            "negocios a organizar proyectos, tareas, prioridades y colaboración "
            "de equipo mediante prácticas ágiles ajustables a su operación."
        ),
        pending_details=[
            "Definir los tipos de negocio, tamaños de equipo y sectores a los que se dirigirá.",
            "Elegir qué prácticas ágiles ofrecerá y cómo adaptarlas a distintos flujos de trabajo sin imponer una metodología única.",
            "Determinar si incluirá seguimiento de tareas, proyectos, objetivos e indicadores, y qué información será necesaria.",
            "Establecer requisitos de privacidad, permisos por rol, respaldo de datos y posibles integraciones antes de desarrollar funciones.",
        ],
    )


# SX Nutria procesa el formulario en el servidor y presenta estimaciones educativas.
@app.route("/nutria", methods=["GET", "POST"])
def nutria():
    resultado = None

    if request.method == 'POST':
        try:
            # Convierte las entradas y valida rangos antes de realizar operaciones.
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

            # Estima energía diaria e IMC con los datos proporcionados.
            tmb = (10 * peso) + (6.25 * altura) - (5 * edad)

            if genero == 'hombre':
                tmb += 5
            else:
                tmb -= 161

            calorias_totales = round(tmb * actividad)
            imc = peso / (altura / 100) ** 2

            # Clasifica el IMC adulto para seleccionar un mensaje orientativo.
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

            # Asigna ejemplos y guías generales según el rango, no una dieta clínica.
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

            # Reúne las estimaciones y textos que consume la plantilla de resultados.
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
        # Informa entradas ausentes o no numéricas sin ocultar otros errores de código.
        except (ValueError, TypeError):
            resultado = {'error': 'Por favor, introduce valores numéricos válidos.'}

    # Conserva el formulario disponible en GET y vuelve a mostrar resultados en POST.
    return render_template(
        "Proyectos/SX_Nutria/nutria.html",
        resultado=resultado,
    )


# Servicios unifica las páginas de consultoría y tienda anteriores.
@app.route("/servicios")
def servicios():
    return render_template("Servicios/servicios.html")


@app.route("/consultoria")
@app.route("/tienda")
def servicios_anterior():
    return redirect(url_for("servicios"), code=301)


@app.route("/blog")
@app.route("/blog/noticias")
def blog():
    return render_template("Blog/blog.html")


# Permite ejecutar el servidor de desarrollo al iniciar este archivo directamente.
if __name__ == "__main__":
    app.run(debug=True)