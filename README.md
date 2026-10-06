# SXcontrol

SXcontrol es una aplicación web desarrollada con Flask. Reúne páginas informativas y proyectos interactivos; entre ellos, **SX Nutria**, una guía educativa de alimentación para personas adultas.

La idea de SXcontrol como comunidad y la elaboración de sus programas de software se atribuyen a **Juan David Henao**, conocido también como **Juan D. Henao** y **solosoyjuan**, de Roldanillo, Valle del Cauca, Colombia. Lleva más de dos años trabajando en estos proyectos desde su etapa en el SENA, refinando la idea con docentes y colegas. Durante el proceso asumió temporalmente el papel de CIO y actualmente es CEO del proyecto comunitario SXcontrol. Su filosofía es: «El acto más dignificante es pensar en algo más que en nosotros mismos».

El correo **solosoyjuan03@gmail.com** es el único medio de contacto directo publicado en el sitio. Los botones abren una ventana de redacción de Gmail con destinatario y asunto preparados; la persona revisa y envía el mensaje desde su cuenta. Los enlaces a repositorios se mantienen para consultar código y colaborar técnicamente, no como canales de contacto.

Las contribuciones económicas voluntarias pueden transferirse al número Nequi **318 004 2374** desde Nequi o desde otro banco que permita enviar dinero a Nequi. El sitio solo muestra el dato; no procesa pagos ni solicita información financiera. Antes de confirmar una transferencia, verifica el destinatario y el monto.

## Funcionalidades actuales

- Páginas de inicio, comunidad, proyectos, servicios (consultoría y tienda) y blog.
- El Blog está dedicado a noticias y avances del proyecto organizados por fecha.
- Comunidad incluye información sobre los sistemas operativos oficiales de desarrollo de SXcontrol (Windows IoT y Linux Mint), páginas para consultar repositorios, conocer cómo colaborar y revisar cumplimiento, principios comunitarios y pruebas.
- SX Library presenta colecciones temáticas, los tres capítulos digitales de *Paz y conflicto*, de Juan D. Henao, y versiones de trabajo de *Educación digital*, *Educación inclusiva*, *Inclusividad legal en educación*, *Fundamentos jurídicos de Colombia*, *Pensamiento algorítmico*, *Investigación de mercados*, *Plan de marketing*, *Plan de ventas* y *Plan de mejora*.
- Las áreas principales de SX Library son Derecho, Software, Marketing y Educación. Los libros se muestran directamente dentro de cada área; Educación digital está disponible como versión de trabajo en Educación, sin niveles de subáreas.
- SX Woodpecker OS, SX Orange Page, SX Recruiter y SX Registros tienen fichas informativas locales con su estado y aspectos de planificación pendientes; esas páginas no significan que los productos estén publicados ni habilitan registros o servicios.
- SX Documento (nombre provisional), SX Help, SX Místico y SX Gestión Ágil tienen fichas de borrador para documentar sus propósitos y decisiones pendientes. SX Help propone orientación jurídica accesible y orientación sobre denuncias ciudadanas, pero no está disponible como asesoría legal ni canal operativo de denuncias. SX Gestión Ágil propone organizar proyectos, tareas y equipos de negocios mediante prácticas ágiles adaptables; no es una herramienta disponible.
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
    library.html                 Catálogo y colecciones de la biblioteca
    area.html                    Página compartida para áreas en preparación
    Derecho/                     Página y libros del área de Derecho
      derecho.html               Catálogo del área de Derecho
      Paz_y_conflicto/           Archivos propios del libro Paz y conflicto
        paz_y_conflicto.html     Página con los tres capítulos del libro
      Fundamentos_juridicos_Colombia/ Archivos propios del libro
        fundamentos_juridicos_colombia.html Tres capítulos sobre Derecho colombiano
    Software/                    Página y libros del área de Software
      software.html              Catálogo del área de Software
      Pensamiento_algoritmico/   Archivos propios del libro Pensamiento algorítmico
        pensamiento_algoritmico.html Tres unidades sobre fundamentos, Revolución 4.0 y diseño algorítmico
    Educacion/                   Área y libros de Educación
      Educacion_digital/          Archivos del libro Educación digital
        educacion_digital.html   Libro digital organizado en tres capítulos
      Educacion_inclusiva/        Archivos del libro Educación inclusiva
        educacion_inclusiva.html Guía pedagógica breve en tres capítulos
      Inclusividad_legal/         Archivos del libro Inclusividad legal en educación
        inclusividad_legal.html  Tres capítulos breves con normas y fuentes oficiales
    Marketing/                   Área y libros de Marketing
      marketing.html              Catálogo del área de Marketing
      Investigacion_mercados/     Archivos del libro Investigación de mercados
        investigacion_mercados.html Tipos, fases y estructura del informe final
      Plan_marketing/             Archivos del libro Plan de marketing
        plan_marketing.html       Tres capítulos sobre historial, mezcla e implementación
      Plan_ventas/                 Archivos del libro Plan de ventas
        plan_ventas.html           Tres capítulos sobre integración, proceso y seguimiento comercial
      Plan_mejora/                 Archivos del libro Plan de mejora
        plan_mejora.html           Integración de planes, ejecución de mejoras y Cuadro de Mando Integral
    area.html                    Página del área de Educación y las áreas en preparación
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
- Fichas de borrador para SX Documento, SX Help, SX Místico y SX Gestión Ágil; sus alcances siguen sujetos a definición.
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
