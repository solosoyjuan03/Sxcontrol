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
            "/sx-woodpecker-os",
            "/sx-orange-page",
            "/sx-recruiter",
            "/sx-registros",
            "/sx-documento",
            "/sx-help",
            "/sx-mistico",
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
        self.assertIn("no debe presentarse como sustituto de asesoría legal individual", help_page)
        self.assertIn("esoterismo", mistico.lower())

    def test_blog_registra_las_nuevas_propuestas_el_5_de_octubre(self):
        response = self.client.get("/blog")
        page = response.get_data(as_text=True)

        self.assertEqual(response.status_code, 200)
        self.assertIn('datetime="2026-10-05"', page)
        self.assertIn("SX Documento", page)
        self.assertIn("SX Help", page)
        self.assertIn("SX Místico", page)
        self.assertIn("nombre SX Documento es provisional", page)

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
