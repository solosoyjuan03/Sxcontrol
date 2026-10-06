import unittest
from html.parser import HTMLParser

from app import app


class AnalizadorEstructuraHTML(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids = set()
        self.duplicate_ids = set()
        self.fragments = []
        self.section_parents = {}
        self.stack = []

    def handle_starttag(self, tag, attrs):
        attributes = dict(attrs)
        element_id = attributes.get("id")
        if element_id:
            if element_id in self.ids:
                self.duplicate_ids.add(element_id)
            self.ids.add(element_id)
        href = attributes.get("href", "")
        if href.startswith("#"):
            self.fragments.append(href[1:])
        if tag == "section" and element_id:
            self.section_parents[element_id] = next(
                (
                    parent_id
                    for parent_tag, parent_id in reversed(self.stack)
                    if parent_tag == "section" and parent_id
                ),
                None,
            )
        if tag not in {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "param", "source", "track", "wbr"}:
            self.stack.append((tag, element_id))

    def handle_endtag(self, tag):
        for index in range(len(self.stack) - 1, -1, -1):
            if self.stack[index][0] == tag:
                del self.stack[index:]
                break


# Pruebas funcionales para rutas públicas, navegación y entradas de SX Nutria.
class PruebasCalidadSitio(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Reutiliza el cliente Flask con modo de pruebas para las solicitudes locales.
        app.config.update(TESTING=True)
        cls.client = app.test_client()

    def test_paginas_principales_responden_y_tienen_navegacion_comun(self):
        # Comprueba que las páginas principales compartan los elementos de navegación.
        paths = (
            "/",
            "/comunidad",
            "/comunidad/repositorios",
            "/comunidad/colaboradores",
            "/comunidad/cumplimiento",
            "/proyectos",
            "/nutria",
            "/sx-library",
            "/sx-library/derecho",
            "/sx-library/derecho/fundamentos-juridicos-colombia",
            "/sx-library/software",
            "/sx-library/software/pensamiento-algoritmico",
            "/sx-library/marketing",
            "/sx-library/marketing/investigacion-de-mercados",
            "/sx-library/marketing/plan-de-marketing",
            "/sx-library/marketing/plan-de-ventas",
            "/sx-library/marketing/plan-de-mejora",
            "/sx-library/educacion",
            "/sx-library/educacion/educacion-digital",
            "/sx-library/educacion/educacion-inclusiva",
            "/sx-library/educacion/inclusividad-legal",
            "/sx-library/paz-y-conflicto",
            "/sx-woodpecker-os",
            "/sx-orange-page",
            "/sx-recruiter",
            "/sx-registros",
            "/sx-documento",
            "/sx-help",
            "/sx-mistico",
            "/sx-gestion-agil",
            "/servicios",
            "/blog",
        )

        for path in paths:
            with self.subTest(path=path):
                response = self.client.get(path)
                self.assertEqual(response.status_code, 200)
                page = response.get_data(as_text=True)
                self.assertIn('name="viewport"', page)
                self.assertIn('aria-label="SXcontrol, inicio"', page)
                self.assertIn('href="/"', page)

    def test_catalogo_enlaza_a_los_borradores_sin_presentarlos_como_lanzados(self):
        response = self.client.get("/proyectos")
        page = response.get_data(as_text=True)

        self.assertEqual(response.status_code, 200)
        for path in (
            "/sx-woodpecker-os",
            "/sx-orange-page",
            "/sx-recruiter",
            "/sx-registros",
            "/sx-documento",
            "/sx-help",
            "/sx-mistico",
            "/sx-gestion-agil",
        ):
            with self.subTest(path=path):
                self.assertIn(f'href="{path}"', page)

        for path in (
            "/sx-woodpecker-os",
            "/sx-orange-page",
            "/sx-recruiter",
            "/sx-registros",
            "/sx-documento",
            "/sx-help",
            "/sx-mistico",
            "/sx-gestion-agil",
        ):
            with self.subTest(path=path):
                draft = self.client.get(path).get_data(as_text=True)
                self.assertIn("Borrador del proyecto", draft)
                self.assertIn("todavía está en preparación", draft)
                self.assertIn("Aspectos por definir", draft)

    def test_fichas_nuevas_reflejan_sus_propositos_y_limites(self):
        documento = self.client.get("/sx-documento").get_data(as_text=True)
        help_page = self.client.get("/sx-help").get_data(as_text=True)
        mistico = self.client.get("/sx-mistico").get_data(as_text=True)

        self.assertIn("APA 7", documento)
        self.assertIn("Nombre provisional", self.client.get("/proyectos").get_data(as_text=True))
        self.assertIn("SX Help", help_page)
        self.assertIn("Eslogan propuesto", help_page)
        self.assertIn("Orientación jurídica accesible para personas de escasos recursos", help_page)
        self.assertIn("denuncias ciudadanas", help_page)
        self.assertIn("canales oficiales de denuncia", help_page)
        self.assertIn("no debe presentarse como sustituto de asesoría legal individual", help_page)
        self.assertIn("orientación sobre denuncias ciudadanas", self.client.get("/proyectos").get_data(as_text=True))
        self.assertIn("esoterismo", mistico.lower())

    def test_comunidad_documenta_los_sistemas_operativos_de_desarrollo(self):
        page = self.client.get("/comunidad").get_data(as_text=True)

        self.assertIn("Sistemas operativos oficiales de desarrollo", page)
        self.assertIn("Windows IoT", page)
        self.assertIn("Linux Mint", page)
        self.assertIn("no constituye una clasificación universal", page)

    def test_sx_gestion_agil_presenta_su_proposito_y_estado_de_propuesta(self):
        catalog = self.client.get("/proyectos").get_data(as_text=True)
        draft = self.client.get("/sx-gestion-agil").get_data(as_text=True)

        self.assertIn("SX Gestión Ágil", catalog)
        self.assertIn("prácticas ágiles adaptables", catalog)
        self.assertIn("Borrador del proyecto", draft)
        self.assertIn("pequeñas empresas y negocios", draft)
        self.assertIn("sin imponer una metodología única", draft)
        self.assertIn("privacidad", draft)
        self.assertIn("todavía está en preparación", draft)

    def test_sx_library_enlaza_y_muestra_el_libro_paz_y_conflicto(self):
        library = self.client.get("/sx-library").get_data(as_text=True)
        law_area = self.client.get("/sx-library/derecho").get_data(as_text=True)
        response = self.client.get("/sx-library/paz-y-conflicto")
        book = response.get_data(as_text=True)

        self.assertEqual(response.status_code, 200)
        self.assertIn('href="/sx-library/derecho"', library)
        self.assertIn("Explora por área", library)
        self.assertIn("Derecho", law_area)
        self.assertIn("Paz y conflicto", law_area)
        self.assertIn('href="/sx-library/paz-y-conflicto"', law_area)

        legal_basics = self.client.get(
            "/sx-library/derecho/fundamentos-juridicos-colombia"
        ).get_data(as_text=True)
        self.assertIn("Fundamentos jurídicos de Colombia", law_area)
        self.assertIn("Autor: Juan D. Henao", law_area)
        self.assertIn(
            'href="/sx-library/derecho/fundamentos-juridicos-colombia"', law_area
        )
        self.assertIn(
            "<title>Fundamentos jurídicos de Colombia - SX Library</title>",
            legal_basics,
        )
        self.assertIn("Autor: Juan D. Henao", legal_basics)
        self.assertIn("Capítulo 1. Introducción al Derecho y sus fuentes", legal_basics)
        self.assertIn("Capítulo 2. Constitución y derechos en Colombia", legal_basics)
        self.assertIn("Capítulo 3. Interpretación jurídica", legal_basics)
        self.assertIn("Finalidades del Derecho", legal_basics)
        self.assertIn("Fuentes formales", legal_basics)
        self.assertIn("Fuentes materiales", legal_basics)
        self.assertIn("Fuentes históricas", legal_basics)
        self.assertIn("artículo 230", legal_basics)
        self.assertIn("El valor de un precedente depende", legal_basics)
        self.assertIn("Derecho público", legal_basics)
        self.assertIn("Derecho privado", legal_basics)
        self.assertIn("Derecho objetivo", legal_basics)
        self.assertIn("derecho subjetivo", legal_basics)
        self.assertIn("no deben presentarse sin matices", legal_basics)
        self.assertIn("Estado social de derecho", legal_basics)
        self.assertIn("artículo 95", legal_basics)
        self.assertIn("Acción de tutela", legal_basics)
        self.assertIn("Acción popular", legal_basics)
        self.assertIn("Acción de grupo", legal_basics)
        self.assertIn("Métodos clásicos de interpretación", legal_basics)
        self.assertIn("Literal o gramatical", legal_basics)
        self.assertIn("sistemático", legal_basics)
        self.assertIn("histórico", legal_basics)
        self.assertIn("teleológico", legal_basics)
        self.assertIn("T-760 de 2008", legal_basics)
        self.assertIn("T-622 de 2016", legal_basics)
        self.assertIn("C-551 de 2003", legal_basics)
        self.assertEqual(legal_basics.count('id="capitulo-1"'), 1)
        self.assertEqual(legal_basics.count('id="capitulo-2"'), 1)
        self.assertEqual(legal_basics.count('id="capitulo-3"'), 1)
        for chapter_anchor in ("capitulo-1", "capitulo-2", "capitulo-3"):
            self.assertIn(f'href="#{chapter_anchor}"', legal_basics)
        self.assertIn("Fuentes bibliográficas y jurídicas", legal_basics)
        self.assertIn("Teoría pura del derecho", legal_basics)
        self.assertIn("El concepto de derecho", legal_basics)
        self.assertIn("Curso de argumentación jurídica", legal_basics)
        self.assertIn("secretariasenado.gov.co/senado/basedoc/constitucion_politica_1991.html", legal_basics)
        self.assertIn("corteconstitucional.gov.co/relatoria/2008/T-760-08.htm", legal_basics)
        self.assertIn('href="/sx-library/derecho"', legal_basics)
        self.assertIn("consulta asesoría jurídica profesional", legal_basics)
        software_area = self.client.get("/sx-library/software").get_data(as_text=True)
        self.assertIn('href="/sx-library/software"', library)
        self.assertIn("Software", software_area)
        self.assertIn("Colección en desarrollo", software_area)
        self.assertIn("programación, desarrollo de software", software_area)
        algorithmic_thinking = self.client.get(
            "/sx-library/software/pensamiento-algoritmico"
        ).get_data(as_text=True)
        self.assertIn("Pensamiento algorítmico", software_area)
        self.assertIn(
            'href="/sx-library/software/pensamiento-algoritmico"', software_area
        )
        self.assertIn(
            "<title>Pensamiento algorítmico - SX Library</title>",
            algorithmic_thinking,
        )
        self.assertIn("Autor: Juan D. Henao", algorithmic_thinking)
        self.assertIn("Versión de trabajo", algorithmic_thinking)
        self.assertIn('href="/sx-library/software"', algorithmic_thinking)
        for chapter_title in (
            "Unidad 1. Fundamentos del pensamiento algorítmico",
            "Unidad 2. Algoritmos y Revolución 4.0",
            "Unidad 3. Diseño e implementación de algoritmos",
        ):
            with self.subTest(chapter=chapter_title):
                self.assertIn(chapter_title, algorithmic_thinking)
        for chapter_anchor in ("capitulo-1", "capitulo-2", "capitulo-3"):
            self.assertEqual(algorithmic_thinking.count(f'id="{chapter_anchor}"'), 1)
            self.assertIn(f'href="#{chapter_anchor}"', algorithmic_thinking)
        self.assertIn("Retornar resultado", algorithmic_thinking)
        self.assertIn("Aprendizaje supervisado", algorithmic_thinking)
        self.assertIn("range(1, 11)", algorithmic_thinking)
        self.assertIn("cualitativos", algorithmic_thinking)
        self.assertIn("sistemas abiertos", algorithmic_thinking)
        self.assertIn("Anexo_1.pdf", algorithmic_thinking)
        self.assertIn("Nota editorial y recursos", algorithmic_thinking)
        for route in (
            "/sx-library/paz-y-conflicto",
            "/sx-library/derecho/fundamentos-juridicos-colombia",
            "/sx-library/educacion/educacion-digital",
            "/sx-library/software/pensamiento-algoritmico",
        ):
            with self.subTest(book_route=route):
                parser = AnalizadorEstructuraHTML()
                parser.feed(self.client.get(route).get_data(as_text=True))
                self.assertEqual(parser.duplicate_ids, set())
                self.assertEqual(set(parser.fragments) - parser.ids, set())
        peace_parser = AnalizadorEstructuraHTML()
        peace_parser.feed(self.client.get("/sx-library/paz-y-conflicto").get_data(as_text=True))
        for chapter_id, section_id in (
            ("capitulo-1", "conceptos-de-paz"),
            ("capitulo-2", "teorias-conflicto"),
            ("capitulo-3", "educacion-paz"),
        ):
            self.assertEqual(peace_parser.section_parents[section_id], chapter_id)
        education_area = self.client.get("/sx-library/educacion").get_data(as_text=True)
        digital_education = self.client.get(
            "/sx-library/educacion/educacion-digital"
        ).get_data(as_text=True)
        self.assertIn("Libros de Educación", education_area)
        self.assertIn("Educación digital", education_area)
        self.assertIn("Educación inclusiva", education_area)
        self.assertIn("Inclusividad legal en educación", education_area)
        self.assertIn(
            'href="/sx-library/educacion/educacion-digital"',
            education_area,
        )
        self.assertNotIn("Subáreas de Educación", education_area)
        self.assertNotIn("Pedagogía", education_area)
        self.assertNotIn("Idiomas", education_area)
        self.assertIn('<title>Educación digital - SX Library</title>', digital_education)
        self.assertNotIn("Pedagogía", digital_education)
        self.assertIn("Autor: Juan D. Henao", digital_education)
        self.assertIn("Versión de trabajo", digital_education)
        self.assertIn('href="/sx-library/educacion"', digital_education)
        for chapter_title in (
            "Capítulo 1. Aprender y organizarse en entornos virtuales",
            "Capítulo 2. Autoformación y autogestión",
            "Capítulo 3. Plataformas digitales y uso responsable",
        ):
            with self.subTest(chapter=chapter_title):
                self.assertIn(chapter_title, digital_education)
        self.assertEqual(digital_education.count('id="capitulo-1"'), 1)
        self.assertEqual(digital_education.count('id="capitulo-2"'), 1)
        self.assertEqual(digital_education.count('id="capitulo-3"'), 1)
        self.assertIn("Nota editorial", digital_education)
        self.assertIn("no se presentan aquí como citas verificadas", digital_education)
        inclusive_education = self.client.get(
            "/sx-library/educacion/educacion-inclusiva"
        ).get_data(as_text=True)
        self.assertIn("<title>Educación inclusiva - SX Library</title>", inclusive_education)
        self.assertIn("Autor: Juan D. Henao", inclusive_education)
        self.assertIn('href="/sx-library/educacion"', inclusive_education)
        for chapter_title in (
            "Capítulo 1. Inclusión y barreras",
            "Capítulo 2. Enseñanza accesible y apoyos",
            "Capítulo 3. Participación y mejora",
        ):
            with self.subTest(chapter=chapter_title):
                self.assertIn(chapter_title, inclusive_education)
        for topic in (
            "barreras",
            "Diseño Universal para el Aprendizaje",
            "ajustes y apoyos",
            "escuchando a cada estudiante",
        ):
            with self.subTest(topic=topic):
                self.assertIn(topic, inclusive_education)
        inclusive_parser = AnalizadorEstructuraHTML()
        inclusive_parser.feed(inclusive_education)
        self.assertEqual(inclusive_parser.duplicate_ids, set())
        self.assertEqual(set(inclusive_parser.fragments) - inclusive_parser.ids, set())
        legal_inclusion = self.client.get(
            "/sx-library/educacion/inclusividad-legal"
        ).get_data(as_text=True)
        self.assertIn(
            "<title>Inclusividad legal en educación - SX Library</title>",
            legal_inclusion,
        )
        self.assertIn("Autor: Juan D. Henao", legal_inclusion)
        self.assertIn('href="/sx-library/educacion"', legal_inclusion)
        for chapter_title in (
            "Capítulo 1. Derecho a la educación inclusiva",
            "Capítulo 2. Deberes y fechas de aplicación",
            "Capítulo 3. Rutas y consecuencias",
        ):
            with self.subTest(chapter=chapter_title):
                self.assertIn(chapter_title, legal_inclusion)
        for citation in (
            "4 de julio de 1991",
            "Ley 115 de 1994",
            "Ley 1346 de 2009",
            "27 de febrero de 2013",
            "29 de agosto de 2017",
            "11 de noviembre de 2013",
            "art. 2.3.3.5.2.3.3",
            "PIAR",
            "28 de febrero de 2018",
            "12 a 36 meses",
            "10 a 15 salarios mínimos",
            "régimen controlado",
            "cancelación de licencia",
            "falta disciplinaria",
            "no existe una única sanción",
            "Fuentes oficiales",
        ):
            with self.subTest(citation=citation):
                self.assertIn(citation, legal_inclusion)
        self.assertGreaterEqual(legal_inclusion.count("https://"), 10)
        legal_parser = AnalizadorEstructuraHTML()
        legal_parser.feed(legal_inclusion)
        self.assertEqual(legal_parser.duplicate_ids, set())
        self.assertEqual(set(legal_parser.fragments) - legal_parser.ids, set())
        for area_name in ("Derecho", "Software", "Marketing", "Educación"):
            self.assertIn(area_name, library)
        for area_slug, area_name in (
            ("marketing", "Marketing"),
            ("educacion", "Educación"),
        ):
            with self.subTest(area=area_name):
                area_page = self.client.get(f"/sx-library/{area_slug}").get_data(as_text=True)
                self.assertIn(f'href="/sx-library/{area_slug}"', library)
                self.assertIn(f"<title>{area_name} - SX Library</title>", area_page)
                if area_slug == "educacion":
                    self.assertIn("Colección en crecimiento", area_page)
                    self.assertIn("Libros de Educación", area_page)
                    self.assertIn("Educación digital", area_page)
                    self.assertNotIn("Subáreas de Educación", area_page)
        self.assertNotIn('href="/sx-library/salud"', library)
        self.assertNotIn('href="/sx-library/agro"', library)
        self.assertNotIn('href="/sx-library/fantasia"', library)
        self.assertNotIn('href="/sx-library/literatura"', library)
        for legacy_slug in (
            "idiomas",
            "salud",
            "agro",
            "fantasia",
            "literatura",
            "pedagogia",
        ):
            response = self.client.get(f"/sx-library/{legacy_slug}")
            self.assertEqual(response.status_code, 301)
            self.assertEqual(
                response.headers["Location"],
                "/sx-library/educacion",
            )
            former_category_response = self.client.get(
                f"/sx-library/educacion/{legacy_slug}"
            )
            self.assertEqual(former_category_response.status_code, 301)
            self.assertEqual(
                former_category_response.headers["Location"],
                "/sx-library/educacion",
            )
        previous_book_route = self.client.get(
            "/sx-library/educacion/pedagogia/educacion-digital"
        )
        self.assertEqual(previous_book_route.status_code, 301)
        self.assertEqual(
            previous_book_route.headers["Location"],
            "/sx-library/educacion/educacion-digital",
        )
        self.assertIn('href="/sx-library/paz-y-conflicto"', library)
        self.assertIn("Derecho · Libro destacado", library)
        self.assertIn("Autor: Juan D. Henao", library)
        self.assertIn("Paz y conflicto", library)
        self.assertIn("Leer el libro", library)
        self.assertIn("Paz y", book)
        self.assertIn("Capítulo 1", book)
        self.assertIn("Capítulos", book)
        self.assertNotIn("Unidad 1", book)
        self.assertIn("Juan D. Henao", book)
        self.assertIn("Autor: Juan D. Henao", book)
        self.assertIn("Paz negativa", book)
        self.assertIn("Paz positiva", book)
        self.assertIn("Cultura de paz", book)
        self.assertIn("Intrapersonal", book)
        self.assertIn("Factores y relaciones de poder", book)
        self.assertIn("Referencias para profundizar", book)
        self.assertIn("Capítulo 2. Teorías y enfoques para la resolución pacífica de conflictos", book)
        self.assertIn("Perspectivas para comprender el conflicto", book)
        self.assertIn("Negociación: construir acuerdos directamente", book)
        self.assertIn("Mediación: diálogo con apoyo de una tercera persona", book)
        self.assertIn("Arbitraje: decisión de una tercera persona", book)
        self.assertIn("Comunicación asertiva", book)
        self.assertIn("Escucha activa", book)
        self.assertIn("Colaboración", book)
        self.assertIn('href="#capitulo-2"', book)
        self.assertIn("La participación obligatoria, el carácter vinculante", book)
        self.assertIn("Capítulo 3. Educación para la paz y los derechos humanos", book)
        self.assertIn("Educar para la paz", book)
        self.assertIn("Derechos humanos y respeto por la diversidad", book)
        self.assertIn("Diálogo inclusivo", book)
        self.assertIn("Justicia restaurativa", book)
        self.assertIn("Foros comunitarios", book)
        self.assertIn("Declaración Universal de Derechos Humanos", book)
        self.assertIn('href="#capitulo-3"', book)
        self.assertEqual(book.count('id="capitulo-1"'), 1)
        self.assertEqual(book.count('id="capitulo-2"'), 1)
        self.assertEqual(book.count('id="capitulo-3"'), 1)

    def test_sx_library_marketing_enlaza_al_libro_de_investigacion_de_mercados(self):
        area_response = self.client.get("/sx-library/marketing")
        area = area_response.get_data(as_text=True)
        book_response = self.client.get(
            "/sx-library/marketing/investigacion-de-mercados"
        )
        book = book_response.get_data(as_text=True)

        self.assertEqual(area_response.status_code, 200)
        self.assertIn("<title>Marketing - SX Library</title>", area)
        self.assertIn("Investigación de mercados", area)
        self.assertIn("Autor: Juan D. Henao", area)
        self.assertIn(
            'href="/sx-library/marketing/investigacion-de-mercados"',
            area,
        )
        self.assertIn("Colección en crecimiento", area)

        self.assertEqual(book_response.status_code, 200)
        self.assertIn(
            "<title>Investigación de mercados - SX Library</title>",
            book,
        )
        self.assertIn("Autor: Juan D. Henao", book)
        self.assertIn('href="/sx-library/marketing"', book)
        for chapter_title in (
            "Capítulo 1. Definir y diseñar el estudio",
            "Capítulo 2. Recopilar información",
            "Capítulo 3. Analizar y decidir",
        ):
            with self.subTest(chapter=chapter_title):
                self.assertIn(chapter_title, book)
        for topic in (
            "problema de investigación",
            "prueba piloto",
            "privacidad",
            "muestra de conveniencia",
            "Tipos de investigación de mercados",
            "Investigación exploratoria",
            "Investigación descriptiva",
            "Investigación causal",
            "mixtos",
            "explicaciones alternativas",
            "Estructura del informe de investigación",
            "Protocolo previo e informe final",
            "Resumen ejecutivo",
            "Referencias:",
            "Anexos:",
            "no se deben inventar datos",
            "Fuentes para profundizar",
        ):
            with self.subTest(topic=topic):
                self.assertIn(topic, book)
        for chapter_anchor in ("capitulo-1", "capitulo-2", "capitulo-3"):
            self.assertEqual(book.count(f'id="{chapter_anchor}"'), 1)
            self.assertIn(f'href="#{chapter_anchor}"', book)

        parser = AnalizadorEstructuraHTML()
        parser.feed(book)
        self.assertEqual(parser.duplicate_ids, set())
        self.assertEqual(set(parser.fragments) - parser.ids, set())

    def test_sx_library_marketing_muestra_plan_de_marketing_en_tres_capitulos(self):
        area_response = self.client.get("/sx-library/marketing")
        area = area_response.get_data(as_text=True)
        book_response = self.client.get("/sx-library/marketing/plan-de-marketing")
        book = book_response.get_data(as_text=True)

        self.assertEqual(area_response.status_code, 200)
        self.assertIn("Plan de marketing", area)
        self.assertIn("Autor: Juan D. Henao", area)
        self.assertIn(
            'href="/sx-library/marketing/plan-de-marketing"',
            area,
        )
        self.assertEqual(book_response.status_code, 200)
        self.assertIn("<title>Plan de marketing - SX Library</title>", book)
        self.assertIn("Autor: Juan D. Henao", book)
        self.assertIn('href="/sx-library/marketing"', book)
        for chapter_title in (
            "Capítulo 1. El historial de la empresa como punto de partida",
            "Capítulo 2. Adaptar la mezcla de marketing a cada etapa",
            "Capítulo 3. Implementar, medir y ajustar",
        ):
            with self.subTest(chapter=chapter_title):
                self.assertIn(chapter_title, book)
        for topic in (
            "historial de la empresa",
            "4P",
            "8P",
            "matriz ampliada de 16 dimensiones",
            "ciclo de vida",
            "indicadores",
            "No hay una lista universal única",
            "no inventes cifras",
        ):
            with self.subTest(topic=topic):
                self.assertIn(topic, book)
        self.assertEqual(book.count('id="capitulo-1"'), 1)
        self.assertEqual(book.count('id="capitulo-2"'), 1)
        self.assertEqual(book.count('id="capitulo-3"'), 1)

        parser = AnalizadorEstructuraHTML()
        parser.feed(book)
        self.assertEqual(parser.duplicate_ids, set())
        self.assertEqual(set(parser.fragments) - parser.ids, set())

    def test_sx_library_marketing_muestra_plan_de_ventas_integrado(self):
        area_response = self.client.get("/sx-library/marketing")
        area = area_response.get_data(as_text=True)
        book_response = self.client.get("/sx-library/marketing/plan-de-ventas")
        book = book_response.get_data(as_text=True)

        self.assertEqual(area_response.status_code, 200)
        self.assertIn("Plan de ventas", area)
        self.assertIn("Autor: Juan D. Henao", area)
        self.assertIn('href="/sx-library/marketing/plan-de-ventas"', area)
        self.assertEqual(book_response.status_code, 200)
        self.assertIn("<title>Plan de ventas - SX Library</title>", book)
        self.assertIn("Autor: Juan D. Henao", book)
        self.assertIn('href="/sx-library/marketing"', book)
        for chapter_title in (
            "Capítulo 1. Integrar investigación de mercados y marketing",
            "Capítulo 2. Diseñar objetivos y proceso comercial",
            "Capítulo 3. Implementar, acompañar y mejorar",
        ):
            with self.subTest(chapter=chapter_title):
                self.assertIn(chapter_title, book)
        for topic in (
            "hallazgos relevantes",
            "no es lo mismo que la meta",
            "Etapas del proceso de ventas",
            "Conversión por etapa",
            "Relación responsable con clientes",
            "no suponerse",
        ):
            with self.subTest(topic=topic):
                self.assertIn(topic, book)
        for chapter_anchor in ("capitulo-1", "capitulo-2", "capitulo-3"):
            self.assertEqual(book.count(f'id="{chapter_anchor}"'), 1)
            self.assertIn(f'href="#{chapter_anchor}"', book)

        parser = AnalizadorEstructuraHTML()
        parser.feed(book)
        self.assertEqual(parser.duplicate_ids, set())
        self.assertEqual(set(parser.fragments) - parser.ids, set())

    def test_sx_library_marketing_muestra_plan_de_mejora_y_balanced_scorecard(self):
        area_response = self.client.get("/sx-library/marketing")
        area = area_response.get_data(as_text=True)
        book_response = self.client.get("/sx-library/marketing/plan-de-mejora")
        book = book_response.get_data(as_text=True)

        self.assertEqual(area_response.status_code, 200)
        self.assertIn("Plan de mejora", area)
        self.assertIn("Autor: Juan D. Henao", area)
        self.assertIn('href="/sx-library/marketing/plan-de-mejora"', area)
        self.assertEqual(book_response.status_code, 200)
        self.assertIn("<title>Plan de mejora - SX Library</title>", book)
        self.assertIn("Autor: Juan D. Henao", book)
        self.assertIn('href="/sx-library/marketing"', book)
        for chapter_title in (
            "Capítulo 1. Integrar los tres planes y establecer el diagnóstico",
            "Capítulo 2. Diseñar y ejecutar la mejora",
            "Capítulo 3. Cuadro de Mando Integral",
        ):
            with self.subTest(chapter=chapter_title):
                self.assertIn(chapter_title, book)
        for topic in (
            "Investigación de mercados",
            "Plan de marketing",
            "Plan de ventas",
            "ciclo Planear-Hacer-Verificar-Actuar",
            "Balanced Scorecard",
            "Financiera o de sostenibilidad",
            "Clientes y grupos de interés",
            "Procesos internos",
            "Aprendizaje y crecimiento",
            "no contiene metas ni resultados reales",
        ):
            with self.subTest(topic=topic):
                self.assertIn(topic, book)
        for chapter_anchor in ("capitulo-1", "capitulo-2", "capitulo-3"):
            self.assertEqual(book.count(f'id="{chapter_anchor}"'), 1)
            self.assertIn(f'href="#{chapter_anchor}"', book)

        parser = AnalizadorEstructuraHTML()
        parser.feed(book)
        self.assertEqual(parser.duplicate_ids, set())
        self.assertEqual(set(parser.fragments) - parser.ids, set())

    def test_blog_registra_las_nuevas_propuestas_el_5_de_octubre(self):
        response = self.client.get("/blog")
        page = response.get_data(as_text=True)

        self.assertEqual(response.status_code, 200)
        self.assertIn('datetime="2026-10-05"', page)
        self.assertIn("SX Documento", page)
        self.assertIn("SX Help", page)
        self.assertIn("SX Místico", page)
        self.assertIn("nombre SX Documento es provisional", page)
        self.assertIn("las catorce pruebas automatizadas pasaron", page)
        self.assertIn("otros bancos que permitan enviar dinero a Nequi", page)
        self.assertIn("Autoría, seudónimos y filosofía de SXcontrol", page)
        self.assertIn("solosoyjuan", page)

    def test_blog_registra_la_conexion_de_git_local_y_remoto_el_6_de_octubre(self):
        response = self.client.get("/blog")
        page = response.get_data(as_text=True)

        self.assertEqual(response.status_code, 200)
        self.assertIn('<time datetime="2026-10-06">6 de octubre de 2026</time>', page)
        self.assertIn("Automatización del repositorio local y remoto", page)
        self.assertIn("main", page)
        self.assertIn("origin/main", page)
        self.assertIn("La subida no ocurre automáticamente con cada edición", page)
        self.assertIn("Sistemas operativos oficiales de desarrollo", page)
        self.assertIn("Windows IoT", page)
        self.assertIn("Linux Mint", page)
        self.assertIn("no una clasificación universal", page)
        self.assertIn("SX Library organiza sus libros por áreas", page)
        self.assertIn("SX Library simplifica sus áreas", page)
        self.assertIn("directamente dentro de su área principal", page)
        self.assertIn("Paz y conflicto", page)
        self.assertIn("tres capítulos", page)
        self.assertIn("ocho áreas", page)
        self.assertIn("Fantasía y Literatura", page)
        self.assertIn("SX Gestión Ágil", page)
        self.assertIn("SX Help", page)
        self.assertIn("diecinueve pruebas automatizadas", page)
        self.assertIn("Educación reúne nuevas subáreas de SX Library", page)
        self.assertIn("Derecho, Software, Marketing y Educación como áreas principales", page)
        self.assertIn("Nuevo libro de investigación de mercados", page)
        self.assertIn("analizar los resultados para tomar decisiones", page)

    def test_blog_agrupa_las_novedades_en_fechas_desplegables(self):
        response = self.client.get("/blog")
        page = response.get_data(as_text=True)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(page.count('<details class="noticias-fecha">'), 6)
        self.assertIn('<summary><time datetime="2026-10-06">6 de octubre de 2026</time></summary>', page)
        self.assertIn('<summary><time datetime="2026-10-04">4 de octubre de 2026</time></summary>', page)
        self.assertIn('<summary><time datetime="2026-10-05">5 de octubre de 2026</time></summary>', page)
        self.assertIn('<summary><time datetime="2026-09-25">25 de septiembre de 2026</time></summary>', page)
        self.assertIn('<summary><time datetime="2026-09-24">24 de septiembre de 2026</time></summary>', page)
        self.assertIn('<summary><time datetime="2026-09-23">23 de septiembre de 2026</time></summary>', page)
        self.assertIn("Nuevos libros digitales en SX Library", page)
        self.assertIn("Inicio del historial de SXcontrol", page)
        self.assertEqual(page.count('class="noticias-fecha-contenido"'), 6)
        self.assertNotIn('<details class="noticias-fecha" open>', page)
        self.assertLess(page.index('datetime="2026-10-06"'), page.index('datetime="2026-10-05"'))
        self.assertLess(page.index('datetime="2026-10-05"'), page.index('datetime="2026-10-04"'))
        self.assertLess(page.index('datetime="2026-10-04"'), page.index('datetime="2026-09-25"'))
        self.assertLess(page.index('datetime="2026-09-25"'), page.index('datetime="2026-09-24"'))
        self.assertLess(page.index('datetime="2026-09-24"'), page.index('datetime="2026-09-23"'))

    def test_pagina_de_calidad_documenta_pruebas_automatizadas_y_manuales(self):
        response = self.client.get("/comunidad/cumplimiento")
        page = response.get_data(as_text=True)

        self.assertEqual(response.status_code, 200)
        self.assertIn("Pruebas automatizadas", page)
        self.assertIn("unittest", page)
        self.assertIn("Flask test_client", page)
        self.assertIn("Comprobaciones manuales", page)
        self.assertIn("Playwright", page)
        self.assertIn("No se realizaron transferencias reales", page)

    def test_blog_documenta_el_contacto_unificado_y_el_envio_manual(self):
        response = self.client.get("/blog")
        page = response.get_data(as_text=True)

        self.assertEqual(response.status_code, 200)
        self.assertIn("Contacto y documentación del sitio", page)
        self.assertIn("solosoyjuan03@gmail.com", page)
        self.assertIn("El sitio no transmite mensajes automáticamente", page)

    def test_rutas_anteriores_de_servicios_redirigen_a_la_pagina_unificada(self):
        for path in ("/consultoria", "/tienda"):
            with self.subTest(path=path):
                response = self.client.get(path)
                self.assertEqual(response.status_code, 301)
                self.assertEqual(response.headers["Location"], "/servicios")

    def test_comunidad_enlaza_a_cumplimiento_sin_enlaces_vacios(self):
        response = self.client.get("/comunidad")
        page = response.get_data(as_text=True)

        self.assertEqual(response.status_code, 200)
        self.assertIn('href="/comunidad/cumplimiento"', page)
        self.assertNotIn('href="#"', page)

    def test_comunidad_reconoce_la_autoria_del_proyecto_y_su_software(self):
        response = self.client.get("/comunidad")
        page = response.get_data(as_text=True)

        self.assertEqual(response.status_code, 200)
        self.assertIn("Origen y autoría", page)
        self.assertIn("Juan David Henao", page)
        self.assertIn("Juan D. Henao", page)
        self.assertIn("solosoyjuan", page)
        self.assertIn("Roldanillo, Valle del Cauca, Colombia", page)
        self.assertIn("La idea de crear SXcontrol como comunidad", page)
        self.assertIn("elaboración de sus programas de software", page)
        self.assertIn("durante más de dos años", page)
        self.assertIn("SENA", page)
        self.assertIn("docentes y colegas", page)
        self.assertIn("temporalmente el papel de CIO", page)
        self.assertIn("actualmente es CEO", page)
        self.assertIn("El acto más dignificante es pensar en algo más que en nosotros mismos", page)
        self.assertIn("Filosofía de Juan D. Henao (solosoyjuan)", page)

    def test_comunidad_muestra_el_numero_nequi_y_aclara_que_no_procesa_pagos(self):
        response = self.client.get("/comunidad")
        page = response.get_data(as_text=True)

        self.assertEqual(response.status_code, 200)
        self.assertIn("Apoya económicamente a SXcontrol", page)
        self.assertIn("Nequi: 318 004 2374", page)
        self.assertIn("desde la aplicación Nequi o desde otro banco", page)
        self.assertIn("verifica el destinatario y el monto antes de confirmar", page)
        self.assertIn("Este sitio no procesa pagos", page)

    def test_pagina_cumplimiento_expone_el_estado_de_licencia_y_pruebas(self):
        response = self.client.get("/comunidad/cumplimiento")
        page = response.get_data(as_text=True)

        self.assertEqual(response.status_code, 200)
        self.assertIn("Estado documental", page)
        self.assertIn("no incluye un archivo de licencia", page)
        self.assertIn("tests/Comunidad/Cumplimiento/", page)

    def test_correo_es_el_unico_medio_de_contacto_directo_del_sitio(self):
        expected_link = "to=solosoyjuan03%40gmail.com"
        services_page = self.client.get("/servicios").get_data(as_text=True)
        compliance_page = self.client.get("/comunidad/cumplimiento").get_data(as_text=True)
        projects_page = self.client.get("/proyectos").get_data(as_text=True)
        collaborators_page = self.client.get("/comunidad/colaboradores").get_data(as_text=True)

        self.assertIn(expected_link, services_page)
        self.assertIn(expected_link, compliance_page)
        self.assertIn(expected_link, projects_page)
        self.assertIn(expected_link, collaborators_page)
        self.assertIn("solosoyjuan03@gmail.com", compliance_page)
        self.assertIn("único medio de contacto directo", projects_page)
        self.assertIn("único medio de contacto directo", collaborators_page)
        self.assertIn("mail.google.com/mail/?view=cm", services_page)
        self.assertIn('target="_blank" rel="noopener noreferrer"', services_page)
        self.assertNotIn(
            "contacto@sxcontrol.org",
            services_page + compliance_page + projects_page + collaborators_page,
        )
        self.assertNotIn("mailto:", services_page + compliance_page + projects_page + collaborators_page)
        self.assertNotIn("/issues", collaborators_page)
        self.assertNotIn("/pulls", collaborators_page)

    def test_calculadora_presenta_resultado_para_una_entrada_valida(self):
        # Un envío válido debe mostrar estimaciones dentro de la misma página.
        response = self.client.post(
            "/nutria",
            data={
                "genero": "hombre",
                "peso": "70",
                "altura": "175",
                "edad": "30",
                "actividad": "1.55",
            },
        )
        page = response.get_data(as_text=True)

        self.assertEqual(response.status_code, 200)
        self.assertIn("Tus Resultados Estimados", page)
        self.assertIn('aria-live="polite"', page)

    def test_calculadora_rechaza_valores_fuera_de_rango(self):
        # Entradas fuera de rango deben mostrar un error accesible al usuario.
        response = self.client.post(
            "/nutria",
            data={
                "genero": "desconocido",
                "peso": "0",
                "altura": "0",
                "edad": "17",
                "actividad": "9",
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn('role="alert"', response.get_data(as_text=True))


if __name__ == "__main__":
    unittest.main()
