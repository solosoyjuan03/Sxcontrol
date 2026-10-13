import math
import os
import secrets
import sqlite3
from datetime import datetime
from pathlib import Path

from flask import Flask, abort, redirect, render_template, request, session, url_for

# La aplicación concentra las rutas públicas y los cálculos usados por las páginas.
app = Flask(__name__)

# Clave para firmar las cookies de sesión y para validar el acceso al panel.
app.secret_key = os.environ.get("FLASK_SECRET_KEY", secrets.token_hex(32))

# La sesión del panel dura 7 días sin volver a pedir credenciales.
app.config["PERMANENT_SESSION_LIFETIME"] = __import__("datetime").timedelta(days=7)

# Credenciales del panel: correo autorizado y clave de acceso (variables de entorno o valores por defecto).
ADMIN_CORREO = os.environ.get("ADMIN_CORREO", "solosoyjuan03@gmail.com")
app.config["BLOG_ADMIN_KEY"] = os.environ.get("BLOG_ADMIN_KEY", "sxcontrol2026")

# Ruta de la base de datos SQLite del blog, junto a app.py.
BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "blog.db"

MESES_ES = {
    1: "enero", 2: "febrero", 3: "marzo", 4: "abril", 5: "mayo", 6: "junio",
    7: "julio", 8: "agosto", 9: "septiembre", 10: "octubre", 11: "noviembre", 12: "diciembre",
}


def init_db():
    """Crea las tablas del sitio si aún no existen."""
    with sqlite3.connect(DB_PATH) as conexion:
        conexion.execute(
            """
            CREATE TABLE IF NOT EXISTS entradas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                fecha TEXT NOT NULL,
                titulo TEXT NOT NULL,
                cuerpo TEXT NOT NULL,
                creada TEXT NOT NULL
            )
            """
        )
        # Textos editables de las páginas: fichas de borrador y cualquier otra sección.
        # Cada fila guarda un campo de texto identificado por su clave única.
        conexion.execute(
            """
            CREATE TABLE IF NOT EXISTS textos (
                clave TEXT PRIMARY KEY,
                contenido TEXT NOT NULL,
                actualizada TEXT NOT NULL
            )
            """
        )
        # Áreas de SX Library (Derecho, Software, Marketing, Educación, etc.).
        conexion.execute(
            """
            CREATE TABLE IF NOT EXISTS library_areas (
                slug TEXT PRIMARY KEY,
                nombre TEXT NOT NULL,
                descripcion TEXT NOT NULL,
                posicion INTEGER NOT NULL DEFAULT 0
            )
            """
        )
        # Libros de SX Library, vinculados a un área. Si tiene url, el enlace
        # apunta a la página propia del libro; si no, se muestra como en preparación.
        conexion.execute(
            """
            CREATE TABLE IF NOT EXISTS library_libros (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                area_slug TEXT NOT NULL REFERENCES library_areas(slug),
                titulo TEXT NOT NULL,
                autor TEXT NOT NULL,
                descripcion TEXT NOT NULL,
                url TEXT,
                posicion INTEGER NOT NULL DEFAULT 0
            )
            """
        )


# Textos iniciales de las fichas de borrador. Actúan como respaldo cuando la
# base de datos no tiene una edición guardada para esa clave.
TEXTOS_BASE = {
    "sx-woodpecker-os": {
        "titulo": "SX Woodpecker OS",
        "resumen": (
            "Una propuesta de sistema operativo basado en Debian, orientado al "
            "aseguramiento de calidad y seguridad en infraestructuras digitales."
        ),
        "pendientes": [
            "Definir los componentes y herramientas que formarán parte del sistema.",
            "Establecer el alcance de las pruebas y los perfiles de infraestructura compatibles.",
            "Documentar requisitos, instalación, mantenimiento y ciclo de actualizaciones.",
        ],
    },
    "sx-orange-page": {
        "titulo": "SX Orange Page",
        "resumen": (
            "Una propuesta de directorio local para consultar información general "
            "y datos de ubicación de comercios."
        ),
        "pendientes": [
            "Definir las zonas y categorías incluidas en el directorio.",
            "Acordar cómo se verificará y actualizará la información publicada.",
            "Establecer criterios de privacidad y autorización para los datos.",
        ],
    },
    "sx-recruiter": {
        "titulo": "SX Recruiter",
        "resumen": (
            "Una propuesta para reunir oportunidades laborales de distintos tipos "
            "dirigidas a personas de Latinoamérica."
        ),
        "pendientes": [
            "Definir las fuentes y el proceso de revisión de cada oportunidad.",
            "Precisar las categorías, regiones y condiciones que se mostrarán.",
            "Establecer cómo se reportarán ofertas vencidas o información incorrecta.",
        ],
    },
    "sx-registros": {
        "titulo": "SX Registros",
        "resumen": (
            "Una propuesta de canal oficial para registrar el interés en participar "
            "en los proyectos de SXcontrol."
        ),
        "pendientes": [
            "Definir qué información sería necesaria y con qué propósito.",
            "Publicar las condiciones de privacidad y el tiempo de conservación de datos.",
            "Diseñar el proceso de revisión y respuesta antes de aceptar registros.",
        ],
    },
    "sx-documento": {
        "titulo": "SX Documento",
        "resumen": (
            "Una propuesta de herramienta con campos guiados para organizar y "
            "dar formato a documentos según el estilo que necesite cada persona, "
            "por ejemplo APA 7."
        ),
        "pendientes": [
            "Definir los tipos de documento y estilos de formato que se admitirán.",
            "Precisar los campos guiados, las reglas de formato y las opciones de exportación.",
            "Verificar las reglas editoriales vigentes antes de anunciar compatibilidad con APA 7.",
        ],
    },
    "sx-help": {
        "titulo": "SX Help",
        "eslogan": "Orientación jurídica accesible para personas de escasos recursos.",
        "resumen": (
            "Una propuesta de espacio online para acercar información jurídica "
            "general y recursos de consulta, y servir como canal de orientación "
            "para denuncias ciudadanas de personas que enfrentan barreras para "
            "acceder a apoyo."
        ),
        "pendientes": [
            "Definir los países, jurisdicciones y temas que cubriría el servicio.",
            "Definir el alcance del canal de denuncias, las entidades o mecanismos oficiales a los que podría orientar y cómo evitar prometer recepción o seguimiento de casos.",
            "Determinar si ofrecerá información general, atención gratuita, contacto con profesionales o una combinación de opciones.",
            "Establecer revisión por profesionales, privacidad, manejo seguro de datos sensibles y límites claros; la herramienta no debe presentarse como sustituto de asesoría legal individual ni de los canales oficiales de denuncia.",
        ],
    },
    "sx-mistico": {
        "titulo": "SX Místico",
        "resumen": (
            "Una propuesta de página dedicada al esoterismo, sus tradiciones, "
            "prácticas y contenidos relacionados."
        ),
        "pendientes": [
            "Definir las temáticas, tradiciones y formatos de contenido que incluirá.",
            "Establecer criterios editoriales para distinguir información cultural de afirmaciones no verificadas.",
            "Diseñar la estructura de navegación y las secciones de la página.",
        ],
    },
    "sx-gestion-agil": {
        "titulo": "SX Gestión Ágil",
        "eslogan": "Organización empresarial con prácticas ágiles adaptables.",
        "resumen": (
            "Una propuesta de herramienta para ayudar a pequeñas empresas y "
            "negocios a organizar proyectos, tareas, prioridades y colaboración "
            "de equipo mediante prácticas ágiles ajustables a su operación."
        ),
        "pendientes": [
            "Definir los tipos de negocio, tamaños de equipo y sectores a los que se dirigirá.",
            "Elegir qué prácticas ágiles ofrecerá y cómo adaptarlas a distintos flujos de trabajo sin imponer una metodología única.",
            "Determinar si incluirá seguimiento de tareas, proyectos, objetivos e indicadores, y qué información será necesaria.",
            "Establecer requisitos de privacidad, permisos por rol, respaldo de datos y posibles integraciones antes de desarrollar funciones.",
        ],
    },
    "nutria-intro": {
        "titulo": "SX Nutria — Introducción",
        "resumen": "Página educativa de alimentación para personas adultas.",
    },
}

# Formato: clave -> (nombre visible, lista de campos editables)
CAMPOS_TEXTO = {
    "sx-woodpecker-os": ["titulo", "resumen", "pendientes"],
    "sx-orange-page": ["titulo", "resumen", "pendientes"],
    "sx-recruiter": ["titulo", "resumen", "pendientes"],
    "sx-registros": ["titulo", "resumen", "pendientes"],
    "sx-documento": ["titulo", "resumen", "pendientes"],
    "sx-help": ["titulo", "eslogan", "resumen", "pendientes"],
    "sx-mistico": ["titulo", "resumen", "pendientes"],
    "sx-gestion-agil": ["titulo", "eslogan", "resumen", "pendientes"],
}

ETIQUETAS_CAMPO = {
    "titulo": "Título",
    "eslogan": "Eslogan (opcional)",
    "resumen": "Resumen",
    "pendientes": "Puntos pendientes (un punto por línea)",
}


# Áreas iniciales de SX Library, respaldo cuando la base de datos está vacía.
AREAS_BASE = {
    "derecho": {"nombre": "Derecho", "descripcion": "Lecturas sobre derechos, convivencia y resolución pacífica de conflictos.", "posicion": 1},
    "software": {"nombre": "Software", "descripcion": "Libros y materiales sobre programación, ingeniería de software y herramientas digitales.", "posicion": 2},
    "marketing": {"nombre": "Marketing", "descripcion": "Marketing, comunicación, marcas y estrategias para conectar con distintos públicos.", "posicion": 3},
    "educacion": {"nombre": "Educación", "descripcion": "Enseñanza, aprendizaje, pedagogía y recursos educativos.", "posicion": 4},
}

# Libros iniciales con página propia (url) o solo ficha en el área.
LIBROS_BASE = [
    ("derecho", "Paz y conflicto", "Juan D. Henao", "Una introducción a las ideas de paz, los niveles de conflicto y las condiciones sociales que influyen en su desarrollo. Versión de trabajo en tres capítulos.", "/sx-library/paz-y-conflicto", 1),
    ("derecho", "Fundamentos jurídicos de Colombia", "Juan D. Henao", "Tres capítulos sobre la estructura jurídica colombiana: normas, derechos y rutas de consulta institucional.", "/sx-library/derecho/fundamentos-juridicos-colombia", 2),
    ("software", "Pensamiento algorítmico", "Juan D. Henao", "Tres unidades sobre fundamentos del razonamiento algorítmico, la Revolución 4.0 y el diseño de algoritmos.", "/sx-library/software/pensamiento-algoritmico", 1),
    ("marketing", "Investigación de mercados", "Juan D. Henao", "Guía introductoria en tres capítulos: definir y diseñar el estudio, recopilar información y analizar los resultados.", "/sx-library/marketing/investigacion-de-mercados", 1),
    ("marketing", "Plan de marketing", "Juan D. Henao", "Historial de la empresa, mezcla de marketing e implementación con responsables e indicadores.", "/sx-library/marketing/plan-de-marketing", 2),
    ("marketing", "Plan de ventas", "Juan D. Henao", "Objetivos y pronósticos fundamentados, proceso de ventas e implementación con mejora continua.", "/sx-library/marketing/plan-de-ventas", 3),
    ("marketing", "Plan de mejora", "Juan D. Henao", "Integra investigación, plan de marketing y ventas para diagnosticar brechas y ejecutar mejoras con seguimiento.", "/sx-library/marketing/plan-de-mejora", 4),
    ("educacion", "Educación digital", "Juan D. Henao", "Tres capítulos sobre aprendizaje virtual, autogestión y uso responsable de herramientas digitales.", "/sx-library/educacion/educacion-digital", 1),
    ("educacion", "Educación inclusiva", "Juan D. Henao", "Guía de trabajo sobre barreras para el aprendizaje y la participación, diseño accesible y apoyos que respetan la diversidad.", "/sx-library/educacion/educacion-inclusiva", 2),
    ("educacion", "Inclusividad legal en educación", "Juan D. Henao", "Guía de consulta sobre deberes, normas colombianas, fechas de aplicación y rutas de actuación institucional.", "/sx-library/educacion/inclusividad-legal", 3),
]


def sembrar_library():
    """Carga las áreas y libros iniciales solo si las tablas están vacías."""
    with sqlite3.connect(DB_PATH) as conexion:
        if conexion.execute("SELECT COUNT(*) FROM library_areas").fetchone()[0] == 0:
            conexion.executemany(
                "INSERT INTO library_areas (slug, nombre, descripcion, posicion) VALUES (?, ?, ?, ?)",
                [(s, d["nombre"], d["descripcion"], d["posicion"]) for s, d in AREAS_BASE.items()],
            )
        if conexion.execute("SELECT COUNT(*) FROM library_libros").fetchone()[0] == 0:
            conexion.executemany(
                "INSERT INTO library_libros (area_slug, titulo, autor, descripcion, url, posicion) VALUES (?, ?, ?, ?, ?, ?)",
                LIBROS_BASE,
            )


def areas_library():
    """Devuelve las áreas de SX Library ordenadas por su posición."""
    with sqlite3.connect(DB_PATH) as conexion:
        conexion.row_factory = sqlite3.Row
        filas = conexion.execute(
            "SELECT slug, nombre, descripcion FROM library_areas ORDER BY posicion, nombre"
        ).fetchall()
    return [dict(fila) for fila in filas]


def libros_library(area_slug=None):
    """Devuelve los libros de un área (o todos), ordenados por posición."""
    with sqlite3.connect(DB_PATH) as conexion:
        conexion.row_factory = sqlite3.Row
        if area_slug:
            filas = conexion.execute(
                "SELECT id, area_slug, titulo, autor, descripcion, url FROM library_libros WHERE area_slug = ? ORDER BY posicion, id",
                (area_slug,),
            ).fetchall()
        else:
            filas = conexion.execute(
                "SELECT id, area_slug, titulo, autor, descripcion, url FROM library_libros ORDER BY area_slug, posicion, id"
            ).fetchall()
    return [dict(fila) for fila in filas]


# Áreas con página propia en plantillas fijas; las demás usan la plantilla genérica.
AREAS_PLANTILLA_FIJA = {"derecho", "software"}


def obtener_textos(clave):
    """Devuelve los textos de una ficha: los guardados en la base de datos o los iniciales."""
    datos = {"titulo": "", "eslogan": "", "resumen": "", "pendientes": ""}
    datos.update(TEXTOS_BASE.get(clave, {}))
    datos["pendientes"] = "\n".join(datos.get("pendientes", []))
    with sqlite3.connect(DB_PATH) as conexion:
        for campo in CAMPOS_TEXTO.get(clave, []):
            fila = conexion.execute(
                "SELECT contenido FROM textos WHERE clave = ?", (f"{clave}:{campo}",)
            ).fetchone()
            if fila:
                datos[campo] = fila[0]
    return datos


def formatear_fecha(iso):
    """Convierte '2026-10-08' en '8 de octubre de 2026' para mostrar en el blog."""
    try:
        fecha = datetime.strptime(iso, "%Y-%m-%d").date()
    except ValueError:
        return iso
    return f"{fecha.day} de {MESES_ES[fecha.month]} de {fecha.year}"


def entradas_blog():
    """Devuelve las entradas guardadas en la base de datos, de la más reciente a la más antigua."""
    with sqlite3.connect(DB_PATH) as conexion:
        conexion.row_factory = sqlite3.Row
        filas = conexion.execute(
            "SELECT id, fecha, titulo, cuerpo FROM entradas ORDER BY fecha DESC, id DESC"
        ).fetchall()
    return [
        {
            "id": fila["id"],
            "fecha": fila["fecha"],
            "fecha_texto": formatear_fecha(fila["fecha"]),
            "titulo": fila["titulo"],
            "parrafos": [p.strip() for p in fila["cuerpo"].split("\n") if p.strip()],
        }
        for fila in filas
    ]


init_db()
sembrar_library()

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


# Las fichas informativas comparten plantilla y textos; cada ruta consulta la
# base de datos (o los textos iniciales) según la clave del proyecto.
FICHAS = {
    "sx-woodpecker-os": "/sx-woodpecker-os",
    "sx-orange-page": "/sx-orange-page",
    "sx-recruiter": "/sx-recruiter",
    "sx-registros": "/sx-registros",
    "sx-documento": "/sx-documento",
    "sx-help": "/sx-help",
    "sx-mistico": "/sx-mistico",
    "sx-gestion-agil": "/sx-gestion-agil",
}


def render_ficha(clave):
    textos = obtener_textos(clave)
    pendientes = [p.strip() for p in textos["pendientes"].split("\n") if p.strip()]
    return render_template(
        "Proyectos/borrador.html",
        project_name=textos["titulo"],
        tagline=textos["eslogan"] or None,
        summary=textos["resumen"],
        pending_details=pendientes,
    )


for _clave, _ruta in FICHAS.items():
    def _vista(clave=_clave):
        return render_ficha(clave)
    # El endpoint conserva el nombre de la función original para no romper url_for existentes.
    app.add_url_rule(_ruta, _clave.replace("-", "_"), _vista)


@app.route("/sx-library")
def sx_library():
    return render_template(
        "Proyectos/SX_Library/library.html",
        areas_bd=areas_library(),
    )


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
    # Si el slug existe como área registrada (base de datos), se muestra;
    # solo las categorías eliminadas que ya no existen redirigen a Educación.
    existe = sqlite3.connect(DB_PATH).execute(
        "SELECT 1 FROM library_areas WHERE slug = ?", (area_slug,)
    ).fetchone()
    if not existe and area_slug in SX_LIBRARY_REMOVED_EDUCATION_CATEGORIES:
        return redirect(url_for("sx_library_area", area_slug="educacion"), code=301)
    # La descripción y el nombre del área pueden venir editados desde /admin.
    area = SX_LIBRARY_AREAS.get(area_slug) or {}
    fila = sqlite3.connect(DB_PATH).execute(
        "SELECT nombre, descripcion FROM library_areas WHERE slug = ?", (area_slug,)
    ).fetchone()
    if fila is None and not area:
        abort(404)
    return render_template(
        "Proyectos/SX_Library/area.html",
        area_slug=area_slug,
        area_name=fila[0] if fila else area["area_name"],
        area_description=fila[1] if fila else area["area_description"],
        libros=libros_library(area_slug),
    )


@app.route("/sx-library/paz-y-conflicto")
def sx_library_paz_y_conflicto():
    return render_template(
        "Proyectos/SX_Library/Derecho/Paz_y_conflicto/paz_y_conflicto.html"
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
    return render_template("Blog/blog.html", entradas_bd=entradas_blog())


# Panel único de administración: entradas del blog y textos de las fichas.
# Requiere iniciar sesión con el correo autorizado y la clave; la sesión
# persiste en una cookie firmada, así que no vuelve a pedirse en cada acción.
@app.route("/admin", methods=["GET", "POST"])
def admin():
    # Inicio de sesión: valida correo + clave y guarda la sesión.
    if request.method == "POST" and request.form.get("accion") == "login":
        correo = request.form.get("correo", "").strip().lower()
        clave = request.form.get("clave", "")
        if correo == ADMIN_CORREO.lower() and clave == app.config["BLOG_ADMIN_KEY"]:
            session["admin"] = correo
            session.permanent = True
            return redirect("/admin")
        return render_template("Admin/login.html", error="Correo o clave incorrectos."), 401

    # Cerrar sesión.
    if request.method == "POST" and request.form.get("accion") == "salir":
        session.pop("admin", None)
        return redirect("/admin")

    # Autoautenticación: si no hay sesión activa, se muestra primero el login.
    if "admin" not in session:
        return render_template("Admin/login.html")

    mensaje = None
    error = None

    # Sección 1: registrar una entrada nueva del blog.
    if request.method == "POST" and request.form.get("accion") == "entrada":
        fecha = request.form.get("fecha", "").strip()
        titulo = request.form.get("titulo", "").strip()
        cuerpo = request.form.get("cuerpo", "").strip()
        if not fecha or not titulo or not cuerpo:
            error = "Completa la fecha, el título y el contenido."
        else:
            try:
                datetime.strptime(fecha, "%Y-%m-%d")
            except ValueError:
                error = "La fecha debe tener formato AAAA-MM-DD, por ejemplo 2026-10-13."
        if not error:
            with sqlite3.connect(DB_PATH) as conexion:
                conexion.execute(
                    "INSERT INTO entradas (fecha, titulo, cuerpo, creada) VALUES (?, ?, ?, ?)",
                    (fecha, titulo, cuerpo, datetime.now().isoformat(timespec="seconds")),
                )
            mensaje = "Entrada registrada. Ya aparece en el Blog."

    # Sección 2: guardar los textos editados de una ficha.
    if request.method == "POST" and request.form.get("accion") == "textos":
        clave_ficha = request.form.get("clave", "")
        if clave_ficha not in CAMPOS_TEXTO:
            abort(400)
        ahora = datetime.now().isoformat(timespec="seconds")
        with sqlite3.connect(DB_PATH) as conexion:
            for campo in CAMPOS_TEXTO[clave_ficha]:
                contenido = request.form.get(campo, "").strip()
                if campo == "titulo" and not contenido:
                    continue
                conexion.execute(
                    """
                    INSERT INTO textos (clave, contenido, actualizada)
                    VALUES (?, ?, ?)
                    ON CONFLICT(clave) DO UPDATE SET contenido = excluded.contenido,
                        actualizada = excluded.actualizada
                    """,
                    (f"{clave_ficha}:{campo}", contenido, ahora),
                )
        mensaje = "Textos guardados. Ya aparecen en la página del proyecto."

    # Sección 3: crear un área nueva de SX Library.
    if request.method == "POST" and request.form.get("accion") == "area":
        slug = request.form.get("slug", "").strip().lower().replace(" ", "-")
        nombre = request.form.get("nombre_area", "").strip()
        descripcion = request.form.get("descripcion_area", "").strip()
        if not slug or not nombre or not descripcion:
            error = "Completa el identificador, el nombre y la descripción del área."
        elif not slug.replace("-", "").isalnum():
            error = "El identificador solo puede tener letras, números y guiones."
        else:
            try:
                with sqlite3.connect(DB_PATH) as conexion:
                    posicion = conexion.execute(
                        "SELECT COALESCE(MAX(posicion), 0) + 1 FROM library_areas"
                    ).fetchone()[0]
                    conexion.execute(
                        "INSERT INTO library_areas (slug, nombre, descripcion, posicion) VALUES (?, ?, ?, ?)",
                        (slug, nombre, descripcion, posicion),
                    )
                mensaje = f"Área {nombre} creada. Ya aparece en SX Library."
            except sqlite3.IntegrityError:
                error = "Ya existe un área con ese identificador."

    # Sección 4: registrar un libro nuevo en un área.
    if request.method == "POST" and request.form.get("accion") == "libro":
        area_slug = request.form.get("area_slug", "")
        titulo = request.form.get("titulo_libro", "").strip()
        autor = request.form.get("autor", "").strip()
        descripcion = request.form.get("descripcion_libro", "").strip()
        url = request.form.get("url_libro", "").strip()
        if area_slug not in {a["slug"] for a in areas_library()}:
            error = "Selecciona un área válida."
        elif not titulo or not autor or not descripcion:
            error = "Completa el título, el autor y la descripción del libro."
        else:
            with sqlite3.connect(DB_PATH) as conexion:
                posicion = conexion.execute(
                    "SELECT COALESCE(MAX(posicion), 0) + 1 FROM library_libros WHERE area_slug = ?",
                    (area_slug,),
                ).fetchone()[0]
                conexion.execute(
                    "INSERT INTO library_libros (area_slug, titulo, autor, descripcion, url, posicion) VALUES (?, ?, ?, ?, ?, ?)",
                    (area_slug, titulo, autor, descripcion, url or None, posicion),
                )
            mensaje = f"Libro {titulo} registrado en el área."

    # Sección 5: eliminar un libro (pide el id en el formulario).
    if request.method == "POST" and request.form.get("accion") == "borrar_libro":
        id_libro = request.form.get("id_libro", "")
        if id_libro.isdigit():
            with sqlite3.connect(DB_PATH) as conexion:
                conexion.execute("DELETE FROM library_libros WHERE id = ?", (int(id_libro),))
            mensaje = "Libro eliminado."

    # La ficha mostrada en el editor se elige con ?clave=... (GET) o desde el último POST.
    clave_seleccionada = request.values.get("clave", "sx-woodpecker-os")
    if clave_seleccionada not in CAMPOS_TEXTO:
        clave_seleccionada = "sx-woodpecker-os"
    return render_template(
        "Admin/admin.html",
        clave_seleccionada=clave_seleccionada,
        fichas=[(c, TEXTOS_BASE[c]["titulo"]) for c in CAMPOS_TEXTO],
        campos=CAMPOS_TEXTO[clave_seleccionada],
        etiquetas=ETIQUETAS_CAMPO,
        textos=obtener_textos(clave_seleccionada),
        areas_bd=areas_library(),
        libros_bd=libros_library(),
        mensaje=mensaje,
        error=error,
    )


# Permite ejecutar el servidor de desarrollo al iniciar este archivo directamente.
if __name__ == "__main__":
    app.run(debug=True)