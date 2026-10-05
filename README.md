# SXcontrol

SXcontrol es una aplicación web desarrollada con Flask. Reúne páginas informativas y proyectos interactivos; entre ellos, **SX Nutria**, una guía educativa de alimentación para personas adultas.

El correo **solosoyjuan03@gmail.com** es el único medio de contacto directo publicado en el sitio. Los botones abren una ventana de redacción de Gmail con destinatario y asunto preparados; la persona revisa y envía el mensaje desde su cuenta. Los enlaces a repositorios se mantienen para consultar código y colaborar técnicamente, no como canales de contacto.

Las contribuciones económicas voluntarias pueden transferirse al número Nequi **318 004 2374** desde Nequi o desde otro banco que permita enviar dinero a Nequi. El sitio solo muestra el dato; no procesa pagos ni solicita información financiera. Antes de confirmar una transferencia, verifica el destinatario y el monto.

## Funcionalidades actuales

- Páginas de inicio, comunidad, proyectos, servicios (consultoría y tienda) y blog.
- El Blog está dedicado a noticias y avances del proyecto organizados por fecha.
- Comunidad incluye páginas para consultar repositorios, conocer cómo colaborar y revisar cumplimiento, principios comunitarios y pruebas.
- SX Library presenta una biblioteca digital en preparación con colecciones temáticas de libros.
- SX Woodpecker OS, SX Orange Page, SX Recruiter y SX Registros tienen fichas informativas locales con su estado y aspectos de planificación pendientes; esas páginas no significan que los productos estén publicados ni habilitan registros o servicios.
- SX Documento (nombre provisional), SX Help y SX Místico tienen fichas de borrador para documentar sus propósitos y decisiones pendientes. SX Help propone orientación jurídica accesible para personas de escasos recursos; no está disponible como asesoría legal.
- SX Nutria incluye secciones desplegables de introducción, documentación, guía alimentaria, recomendaciones generales de salud y calculadora.
- La calculadora estima el gasto energético diario, el IMC y una distribución general de macronutrientes a partir de los datos ingresados.
- Los resultados incluyen recomendaciones educativas orientativas según el rango de IMC, ejemplos de alimentos y una guía flexible de porciones.
- La página está diseñada para mantener abierta la calculadora al entrar y después de enviar el formulario.

> **Aviso:** SX Nutria es una herramienta educativa, no un servicio médico. Sus cálculos y recomendaciones no son diagnósticos ni sustituyen la atención de profesionales de salud. El IMC es una medida orientativa y no permite diagnosticar por sí solo una condición.

## Requisitos

- Python 3.10 o posterior.
- Las dependencias listadas en [`requirements.txt`](requirements.txt).

## Instalación y ejecución local

En Windows PowerShell:

```powershell
git clone https://github.com/solosoyjuan03/Sxcontrol.git
cd Sxcontrol
py -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
python app.py
```

Luego abre <http://127.0.0.1:5000> en el navegador. Para salir del entorno virtual:

```powershell
deactivate
```

La aplicación también define un `Procfile` para ejecutarse con Gunicorn en plataformas compatibles:

```text
web: gunicorn app:app
```

## Estructura principal

```text
app.py                         Rutas y lógica de la aplicación Flask
templates/                     Plantillas HTML
  Blog/blog.html                Noticias y avances del proyecto
  Comunidad/                    Portada, repositorios, colaboradores y cumplimiento
  Proyectos/SX_Nutria/          Página y calculadora SX Nutria
  Proyectos/SX_Library/         Biblioteca digital SX Library
  Proyectos/borrador.html       Ficha compartida para proyectos en preparación
  Servicios/                    Consultoría y productos
static/css/style.css            Estilos
tests/Comunidad/Cumplimiento/   Pruebas automatizadas del sitio
requirements.txt                Dependencias de Python
Procfile                        Comando de inicio para despliegue
```

## Avances del proyecto

### Implementado

- Aplicación Flask con rutas para las páginas principales del sitio.
- SX Nutria con cinco secciones desplegables y calculadora como primera sección.
- Fichas de borrador accesibles desde el catálogo para SX Woodpecker OS, SX Orange Page, SX Recruiter y SX Registros.
- Fichas de borrador para SX Documento, SX Help y SX Místico; sus alcances siguen sujetos a definición.
- Estimaciones de gasto energético, distribución general de macronutrientes e IMC para adultos.
- Recomendaciones educativas según el rango de IMC, incluyendo bajo peso, rango de referencia, sobrepeso y categorías de obesidad.
- Orientación general sobre alimentación, porciones y condiciones de salud, con avisos para consultar a profesionales cuando sea necesario.
- Validación de entradas de la calculadora y exclusión del entorno virtual y archivos temporales mediante `.gitignore`.

### Cómo registrar próximos avances

Al completar una mejora, actualiza esta sección con:

1. La función terminada y el área del proyecto que afecta.
2. Cambios importantes para quien usa o instala la aplicación.
3. Pruebas o verificaciones ejecutadas.

Procura describir lo que efectivamente está implementado y probado. Si una función sigue en desarrollo, indícala como pendiente y no como terminada.

### Pruebas automatizadas

Las pruebas funcionales del sitio están en `tests/Comunidad/Cumplimiento/` y se ejecutan desde la raíz del proyecto con:

```powershell
python -m unittest discover -s tests -v
```

Estas pruebas cubren rutas y navegación, redirecciones de servicios, acceso a la página de cumplimiento y validación básica de la calculadora. No sustituyen una auditoría de seguridad ni una revisión legal.

## Flujo recomendado para contribuir

Antes de empezar, actualiza tu copia local:

```powershell
git pull origin main
```

Después de implementar y revisar una mejora:

```powershell
git status
git add .
git commit -m "Describe el cambio"
git push origin main
```

Usa mensajes de commit breves y descriptivos. No agregues al repositorio el entorno virtual (`venv`), secretos, contraseñas ni archivos `.env`.

## Fuentes de referencia de SX Nutria

- [Guía Alimentaria de Canadá — Health Canada](https://www.canada.ca/en/health-canada/services/food-nutrition/canada-food-guide.html)
- [Alimentación saludable — Organización Mundial de la Salud](https://www.who.int/news-room/fact-sheets/detail/healthy-diet)
- [Hypertension Canada](https://hypertension.ca/)
- [Diabetes Canada](https://www.diabetes.ca/)
- [Heart & Stroke — Alimentación saludable](https://www.heartandstroke.ca/healthy-living/healthy-eating)
