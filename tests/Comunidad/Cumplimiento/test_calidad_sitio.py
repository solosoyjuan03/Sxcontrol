import unittest

from app import app


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
            "/sx-library/software",
            "/sx-library/marketing",
            "/sx-library/educacion",
            "/sx-library/salud",
            "/sx-library/agro",
            "/sx-library/fantasia",
            "/sx-library/literatura",
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
        software_area = self.client.get("/sx-library/software").get_data(as_text=True)
        self.assertIn('href="/sx-library/software"', library)
        self.assertIn("Software", software_area)
        self.assertIn("Área en preparación", software_area)
        self.assertIn("programación, desarrollo de software", software_area)
        for area_name in ("Derecho", "Software", "Marketing", "Educación", "Salud", "Agro", "Fantasía", "Literatura"):
            self.assertIn(area_name, library)
        for area_slug, area_name in (
            ("marketing", "Marketing"),
            ("educacion", "Educación"),
            ("salud", "Salud"),
            ("agro", "Agro"),
            ("fantasia", "Fantasía"),
            ("literatura", "Literatura"),
        ):
            with self.subTest(area=area_name):
                area_page = self.client.get(f"/sx-library/{area_slug}").get_data(as_text=True)
                self.assertIn(f'href="/sx-library/{area_slug}"', library)
                self.assertIn(f"<title>{area_name} - SX Library</title>", area_page)
                self.assertIn("Área en preparación", area_page)
                if area_slug == "literatura":
                    self.assertIn("filosofía", area_page.lower())
                    self.assertIn("filosofía", library.lower())
        self.assertIn('href="/sx-library/paz-y-conflicto"', library)
        self.assertIn("Derecho · Primera obra digital", library)
        self.assertIn("Paz y conflicto", library)
        self.assertIn("Leer el libro", library)
        self.assertIn("Paz y", book)
        self.assertIn("Capítulo 1", book)
        self.assertIn("Capítulos", book)
        self.assertNotIn("Unidad 1", book)
        self.assertIn("Juan D. Henao", book)
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
        self.assertIn("Paz y conflicto", page)
        self.assertIn("tres capítulos", page)
        self.assertIn("ocho áreas", page)
        self.assertIn("Fantasía y Literatura", page)
        self.assertIn("SX Gestión Ágil", page)
        self.assertIn("SX Help", page)
        self.assertIn("diecinueve pruebas automatizadas", page)

    def test_blog_agrupa_las_novedades_en_fechas_desplegables(self):
        response = self.client.get("/blog")
        page = response.get_data(as_text=True)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(page.count('<details class="noticias-fecha">'), 3)
        self.assertIn('<summary><time datetime="2026-10-06">6 de octubre de 2026</time></summary>', page)
        self.assertIn('<summary><time datetime="2026-10-04">4 de octubre de 2026</time></summary>', page)
        self.assertIn('<summary><time datetime="2026-10-05">5 de octubre de 2026</time></summary>', page)
        self.assertEqual(page.count('class="noticias-fecha-contenido"'), 3)
        self.assertNotIn('<details class="noticias-fecha" open>', page)
        self.assertLess(page.index('datetime="2026-10-06"'), page.index('datetime="2026-10-05"'))
        self.assertLess(page.index('datetime="2026-10-05"'), page.index('datetime="2026-10-04"'))

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
