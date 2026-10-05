import unittest

from app import app


class PruebasCalidadSitio(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        app.config.update(TESTING=True)
        cls.client = app.test_client()

    def test_paginas_principales_responden_y_tienen_navegacion_comun(self):
        paths = (
            "/",
            "/comunidad",
            "/comunidad/repositorios",
            "/comunidad/colaboradores",
            "/comunidad/cumplimiento",
            "/proyectos",
            "/nutria",
            "/sx-library",
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

    def test_calculadora_presenta_resultado_para_una_entrada_valida(self):
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
