import { Course } from '../types';

export const COURSES: Course[] = [
  {
    id: 'tech-software',
    title: 'Técnico en Desarrollo de Software',
    icon: '💻',
    color: 'from-emerald-500 to-teal-700',
    bgColor: 'bg-emerald-50 text-emerald-900 border-emerald-200',
    description: 'Malla curricular oficial del Técnico en Desarrollo de Software: Lógica de programación, Desarrollo Web, Bases de Datos SQL y NoSQL, Git y APIs REST.',
    nodes: [
      {
        id: 'tech-1',
        title: 'Algoritmos y Variables',
        unit: 1,
        unitTitle: 'Módulo 1: Fundamentos de Lógica y Programación',
        description: 'Entrada y salida de datos, variables, tipos primitivos y lógica secuencial.',
        totalLessons: 3,
        iconName: 'Terminal',
        exercises: [
          {
            id: 'tech-1-1',
            type: 'multiple_choice',
            title: 'Concepto de Variable',
            question: 'En desarrollo de software, ¿qué es una variable?',
            options: [
              'Un espacio reservado en memoria para almacenar un valor que puede cambiar',
              'Un cable físico dentro de la computadora',
              'Un comando para apagar el sistema operativo',
              'Un tipo de base de datos no relacional'
            ],
            correctAnswer: 'Un espacio reservado en memoria para almacenar un valor que puede cambiar',
            explanation: 'Una variable es un identificador asociado a un espacio en memoria donde guardamos datos durante la ejecución de un programa.'
          },
          {
            id: 'tech-1-2',
            type: 'fill_blank',
            title: 'Declaración e Impresión',
            question: 'Completa la instrucción para asignar el nombre de usuario e imprimir la bienvenida:',
            codeSnippet: 'usuario ___ "Carlos"\nprint(f"Bienvenido Técnico {usuario}")',
            options: ['=', '==', '=>', 'let'],
            correctAnswer: '=',
            explanation: 'El operador asigna el valor "Carlos" a la variable usuario.'
          },
          {
            id: 'tech-1-3',
            type: 'code_blocks',
            title: 'Ordena el Algoritmo Secuencial',
            question: 'Ordena el algoritmo para calcular la suma de dos números ingresados por un usuario:',
            codeBlocks: [
              'num1 = int(input("Ingrese primer número:"))',
              'num2 = int(input("Ingrese segundo número:"))',
              'suma = num1 + num2',
              'print(f"La suma es: {suma}")'
            ],
            correctOrder: [
              'num1 = int(input("Ingrese primer número:"))',
              'num2 = int(input("Ingrese segundo número:"))',
              'suma = num1 + num2',
              'print(f"La suma es: {suma}")'
            ],
            explanation: 'Un algoritmo sigue una secuencia lógica: Capturar entradas -> Procesar datos -> Mostrar salida.'
          }
        ]
      },
      {
        id: 'tech-2',
        title: 'Estructuras Condicionales',
        unit: 1,
        unitTitle: 'Módulo 1: Fundamentos de Lógica y Programación',
        description: 'Toma de decisiones lógicas en software usando operadores relacionales y bloques if / else.',
        totalLessons: 3,
        iconName: 'GitBranch',
        exercises: [
          {
            id: 'tech-2-1',
            type: 'multiple_choice',
            title: 'Evaluación Lógica',
            question: '¿Qué resultado produce la expresión booleana: (10 >= 5) and (3 == 4)?',
            options: ['False', 'True', 'None', 'Error de sintaxis'],
            correctAnswer: 'False',
            explanation: '10 >= 5 es True, pero 3 == 4 es False. En una operación AND, si una de las condiciones es falsa, el resultado final es False.'
          },
          {
            id: 'tech-2-2',
            type: 'fill_blank',
            title: 'Validación de Acceso',
            question: 'Completa la validación para verificar si un estudiante es mayor de edad:',
            codeSnippet: 'if edad >= 18:\n    print("Acceso concedido")\n___:\n    print("Acceso denegado")',
            options: ['else', 'elif', 'otherwise', 'except'],
            correctAnswer: 'else',
            explanation: 'El bloque else se ejecuta cuando la condición del if resulta ser falsa.'
          },
          {
            id: 'tech-2-3',
            type: 'find_bug',
            title: 'Encuentra el Bug en la Condición',
            question: 'Toca la línea que comete el error de usar asignación (=) en lugar de comparación (==):',
            codeSnippet: `rol = "administrador"
if rol = "administrador":
    print("Acceso total al sistema")`,
            bugLine: 2,
            correctAnswer: 'if rol = "administrador":',
            explanation: 'En condicionales se debe usar el operador de comparación ==. Un solo signo = asigna valores y produce SyntaxError.'
          }
        ]
      },
      {
        id: 'tech-3',
        title: 'Bucles e Iteración',
        unit: 1,
        unitTitle: 'Módulo 1: Fundamentos de Lógica y Programación',
        description: 'Repetición eficiente de código con bucles for y while.',
        totalLessons: 3,
        iconName: 'RotateCw',
        exercises: [
          {
            id: 'tech-3-1',
            type: 'multiple_choice',
            title: 'Bucle Indefinido',
            question: '¿Qué bucle se recomienda cuando NO sabemos cuántas veces se repetirá una condición?',
            options: ['Bucle while', 'Bucle for', 'Condicional if', 'Función return'],
            correctAnswer: 'Bucle while',
            explanation: 'El bucle while repite instrucciones mientras una condición sea verdadera, ideal cuando el número de iteraciones es incierto.'
          },
          {
            id: 'tech-3-2',
            type: 'code_blocks',
            title: 'Procesar Lista de Clientes',
            question: 'Ordena el código para iterar e imprimir cada usuario de la lista:',
            codeBlocks: [
              'usuarios = ["Ana", "Pedro", "Sofía"]',
              'for u in usuarios:',
              '    print(f"Usuario registrado: {u}")'
            ],
            correctOrder: [
              'usuarios = ["Ana", "Pedro", "Sofía"]',
              'for u in usuarios:',
              '    print(f"Usuario registrado: {u}")'
            ],
            explanation: 'El bucle for in extrae ordenadamente cada elemento de una colección.'
          }
        ]
      },
      {
        id: 'tech-4',
        title: 'Funciones y Modularidad',
        unit: 1,
        unitTitle: 'Módulo 1: Fundamentos de Lógica y Programación',
        description: 'Diseño de software modular, reusabilidad de código y retornos de función.',
        totalLessons: 3,
        iconName: 'Code',
        exercises: [
          {
            id: 'tech-4-1',
            type: 'multiple_choice',
            title: 'Principio de Modularidad',
            question: '¿Cuál es la ventaja principal de empaquetar código en funciones?',
            options: [
              'Evitar la duplicación de código y facilitar el mantenimiento',
              'Aumentar el tamaño del archivo ejecutable',
              'Eliminar la necesidad de usar bases de datos',
              'Hacer que el programa corra sin conexión a internet'
            ],
            correctAnswer: 'Evitar la duplicación de código y facilitar el mantenimiento',
            explanation: 'Las funciones permiten reutilizar lógica y mantener un código limpio (DRY: Don\'t Repeat Yourself).'
          },
          {
            id: 'tech-4-2',
            type: 'fill_blank',
            title: 'Cálculo de Impuesto',
            question: 'Completa la función que retorna el precio con el 19% de IVA:',
            codeSnippet: 'def calcular_iva(precio):\n    ___ precio * 1.19',
            options: ['return', 'print', 'send', 'output'],
            correctAnswer: 'return',
            explanation: 'La instrucción return devuelve el resultado del cálculo al código que invocó la función.'
          }
        ]
      },
      {
        id: 'tech-5',
        title: 'HTML5 Semántico y Estructura',
        unit: 2,
        unitTitle: 'Módulo 2: Desarrollo Web Frontend',
        description: 'Creación de interfaces estructuradas con HTML5, etiquetas semánticas y formularios.',
        totalLessons: 3,
        iconName: 'Layout',
        exercises: [
          {
            id: 'tech-5-1',
            type: 'multiple_choice',
            title: 'HTML Semántico',
            question: '¿Cuál de las siguientes es una etiqueta semántica correcta de HTML5 para encabezados principales de sitio?',
            options: ['<header>', '<div class="head">', '<top>', '<heading>'],
            correctAnswer: '<header>',
            explanation: '<header> indica explícitamente a navegadores y buscadores el encabezado semántico del documento.'
          },
          {
            id: 'tech-5-2',
            type: 'fill_blank',
            title: 'Formulario de Login',
            question: 'Completa la etiqueta de entrada de texto para contraseñas seguras:',
            codeSnippet: '<input type="___" placeholder="Ingresa tu clave">',
            options: ['password', 'text', 'hidden', 'key'],
            correctAnswer: 'password',
            explanation: 'El tipo type="password" oculta los caracteres ingresados por el usuario como puntos de seguridad.'
          },
          {
            id: 'tech-5-3',
            type: 'code_blocks',
            title: 'Estructura una Página Semántica',
            question: 'Ordena la maqueta HTML5 recomendada para un módulo técnico:',
            codeBlocks: [
              '<header><h1>Panel Técnico</h1></header>',
              '<main><section>Contenido</section></main>',
              '<footer>© 2026 Técnico en Desarrollo de Software</footer>'
            ],
            correctOrder: [
              '<header><h1>Panel Técnico</h1></header>',
              '<main><section>Contenido</section></main>',
              '<footer>© 2026 Técnico en Desarrollo de Software</footer>'
            ],
            explanation: 'Una página bien estructurada separa la cabecera (<header>), contenido principal (<main>) y pie de página (<footer>).'
          }
        ]
      },
      {
        id: 'tech-6',
        title: 'CSS3 Layout y Estilos',
        unit: 2,
        unitTitle: 'Módulo 2: Desarrollo Web Frontend',
        description: 'Estilizado de aplicaciones con CSS3, modelo de caja, Flexbox y diseños adaptables.',
        totalLessons: 3,
        iconName: 'Box',
        exercises: [
          {
            id: 'tech-6-1',
            type: 'multiple_choice',
            title: 'Flexbox Centrado',
            question: '¿Qué propiedad de CSS Flexbox alinea los elementos en el eje principal horizontal?',
            options: ['justify-content', 'align-items', 'flex-direction', 'display-grid'],
            correctAnswer: 'justify-content',
            explanation: 'justify-content controla la distribución y alineación a lo largo del eje principal en Flexbox.'
          },
          {
            id: 'tech-6-2',
            type: 'fill_blank',
            title: 'Modelo de Caja',
            question: 'Completa la propiedad para agregar espacio INTERNO entre el borde y el contenido:',
            codeSnippet: '.card {\n  ___: 16px;\n}',
            options: ['padding', 'margin', 'border', 'spacing'],
            correctAnswer: 'padding',
            explanation: 'padding es el relleno interno de la caja, mientras que margin es la separación externa.'
          }
        ]
      },
      {
        id: 'tech-7',
        title: 'JavaScript y Eventos DOM',
        unit: 2,
        unitTitle: 'Módulo 2: Desarrollo Web Frontend',
        description: 'Dinamismo en la web: Selección de elementos HTML, eventos clic e interacción del usuario.',
        totalLessons: 3,
        iconName: 'Component',
        exercises: [
          {
            id: 'tech-7-1',
            type: 'multiple_choice',
            title: 'Selección en el DOM',
            question: '¿Cómo se selecciona un elemento con id="btnGuardar" en JavaScript moderno?',
            options: [
              'document.querySelector("#btnGuardar")',
              'document.getElement("btnGuardar")',
              'window.findId("btnGuardar")',
              'select("#btnGuardar")'
            ],
            correctAnswer: 'document.querySelector("#btnGuardar")',
            explanation: 'document.querySelector utiliza selectores CSS estándar para localizar elementos en el DOM.'
          },
          {
            id: 'tech-7-2',
            type: 'fill_blank',
            title: 'Escuchar el Clic',
            question: 'Completa para ejecutar una función cuando el usuario hace clic en un botón:',
            codeSnippet: 'boton.addEventListener("___", () => {\n  alert("¡Guardado!");\n});',
            options: ['click', 'onclick', 'press', 'tap'],
            correctAnswer: 'click',
            explanation: 'addEventListener registra eventos como "click", "submit", "change", etc.'
          }
        ]
      },
      {
        id: 'tech-8',
        title: 'Bases de Datos y Modelo ER',
        unit: 3,
        unitTitle: 'Módulo 3: Bases de Datos Relacionales y SQL',
        description: 'Diseño de bases de datos, llaves primarias (PK), llaves foráneas (FK) y normalización.',
        totalLessons: 3,
        iconName: 'Database',
        exercises: [
          {
            id: 'tech-8-1',
            type: 'multiple_choice',
            title: 'Llave Primaria (Primary Key)',
            question: '¿Cuál es la función principal de una Primary Key (PK) en una tabla de base de datos relacional?',
            options: [
              'Identificar de forma única e irrepetible cada registro o fila de la tabla',
              'Conectar la base de datos con el servidor web mediante internet',
              'Cifrar los mensajes de correo electrónico de los usuarios',
              'Aumentar la velocidad del procesador de la computadora'
            ],
            correctAnswer: 'Identificar de forma única e irrepetible cada registro o fila de la tabla',
            explanation: 'La PK (Primary Key) garantiza la unicidad e integridad de las filas en una tabla relacional.'
          },
          {
            id: 'tech-8-2',
            type: 'fill_blank',
            title: 'Relación de Tablas',
            question: 'Para vincular una tabla Pedidos con la tabla Clientes, agregamos en Pedidos la clave ___ de Clientes:',
            codeSnippet: 'TABLA Pedidos (\n  id_pedido INT PRIMARY KEY,\n  id_cliente INT REFERENCES Clientes\n)',
            options: ['foránea', 'secundaria', 'terciaria', 'cruzada'],
            correctAnswer: 'foránea',
            explanation: 'Una llave foránea (Foreign Key) crea una referencia a la llave primaria de otra tabla para mantener integridad referencial.'
          }
        ]
      },
      {
        id: 'tech-9',
        title: 'Consultas SQL (SELECT & JOIN)',
        unit: 3,
        unitTitle: 'Módulo 3: Bases de Datos Relacionales y SQL',
        description: 'Extracción de información con sentencias SQL, filtros WHERE y combinación de tablas con JOIN.',
        totalLessons: 3,
        iconName: 'Layers',
        exercises: [
          {
            id: 'tech-9-1',
            type: 'multiple_choice',
            title: 'Consulta Básica SQL',
            question: '¿Qué comando SQL selecciona todas las columnas de la tabla "estudiantes"?',
            options: [
              'SELECT * FROM estudiantes;',
              'GET ALL FROM estudiantes;',
              'SHOW TABLES estudiantes;',
              'FETCH EVERYTHING estudiantes;'
            ],
            correctAnswer: 'SELECT * FROM estudiantes;',
            explanation: 'El asterisco (*) en SELECT especifica que se deben traer todas las columnas disponibles.'
          },
          {
            id: 'tech-9-2',
            type: 'code_blocks',
            title: 'Consulta con Filtro y Orden',
            question: 'Ordena la sentencia SQL para obtener usuarios activos ordenados por nombre:',
            codeBlocks: [
              'SELECT nombre, email',
              'FROM usuarios',
              'WHERE estado = "activo"',
              'ORDER BY nombre ASC;'
            ],
            correctOrder: [
              'SELECT nombre, email',
              'FROM usuarios',
              'WHERE estado = "activo"',
              'ORDER BY nombre ASC;'
            ],
            explanation: 'El orden estándar de cláusulas SQL es: SELECT -> FROM -> WHERE -> ORDER BY.'
          },
          {
            id: 'tech-9-3',
            type: 'fill_blank',
            title: 'Unión de Tablas',
            question: 'Completa la cláusula para cruzar la tabla Estudiantes con la tabla Cursos:',
            codeSnippet: 'SELECT e.nombre, c.curso\nFROM estudiantes e\nINNER ___ cursos c ON e.id_curso = c.id;',
            options: ['JOIN', 'UNION', 'CONNECT', 'LINK'],
            correctAnswer: 'JOIN',
            explanation: 'INNER JOIN combina filas de dos o más tablas en base a una columna relacionada común.'
          }
        ]
      },
      {
        id: 'tech-10',
        title: 'Manipulación SQL (DML)',
        unit: 3,
        unitTitle: 'Módulo 3: Bases de Datos Relacionales y SQL',
        description: 'Operaciones de inserción, actualización y eliminación de registros (INSERT, UPDATE, DELETE).',
        totalLessons: 3,
        iconName: 'Database',
        exercises: [
          {
            id: 'tech-10-1',
            type: 'multiple_choice',
            title: 'Insertar Registros',
            question: '¿Qué instrucción SQL se utiliza para agregar un nuevo registro en una tabla?',
            options: [
              'INSERT INTO tabla (col1) VALUES (val1);',
              'ADD NEW RECORD TO tabla;',
              'CREATE ROW EN tabla;',
              'UPDATE tabla ADD val1;'
            ],
            correctAnswer: 'INSERT INTO tabla (col1) VALUES (val1);',
            explanation: 'INSERT INTO es la sentencia DML estándar para guardar nuevos registros en SQL.'
          },
          {
            id: 'tech-10-2',
            type: 'find_bug',
            title: 'Peligro en UPDATE sin WHERE',
            question: 'Toca la línea de la consulta que actualizaría accidentalmente TODOS los registros si no agregas WHERE:',
            codeSnippet: `UPDATE productos
SET precio = 1500
-- ¡Olvido peligroso del WHERE id = 5!`,
            bugLine: 2,
            correctAnswer: 'SET precio = 1500',
            explanation: 'Si ejecutas un UPDATE sin la cláusula WHERE, la base de datos modificará el valor en el 100% de las filas de la tabla.'
          }
        ]
      },
      {
        id: 'tech-11',
        title: 'Control de Versiones con Git',
        unit: 4,
        unitTitle: 'Módulo 4: Backend, APIs REST y Git',
        description: 'Gestión de repositorios de código, commits, ramas (branches) y colaboración en GitHub.',
        totalLessons: 3,
        iconName: 'GitBranch',
        exercises: [
          {
            id: 'tech-11-1',
            type: 'multiple_choice',
            title: 'Guardar Estado en Git',
            question: '¿Qué comando de Git guarda una instantánea (snapshot) de los cambios preparados en el repositorio local?',
            options: [
              'git commit -m "Mensaje"',
              'git push origin main',
              'git save --all',
              'git checkout -b main'
            ],
            correctAnswer: 'git commit -m "Mensaje"',
            explanation: 'git commit empaqueta los cambios del staging area y crea un punto de control en el historial del proyecto.'
          },
          {
            id: 'tech-11-2',
            type: 'code_blocks',
            title: 'Flujo de Trabajo Git',
            question: 'Ordena la secuencia típica para enviar un cambio local a un repositorio remoto:',
            codeBlocks: [
              'git add .',
              'git commit -m "Agrega módulo de notas"',
              'git push origin main'
            ],
            correctOrder: [
              'git add .',
              'git commit -m "Agrega módulo de notas"',
              'git push origin main'
            ],
            explanation: 'El flujo Git es: Preparar archivos (git add) -> Confirmar historial (git commit) -> Subir a la nube (git push).'
          }
        ]
      },
      {
        id: 'tech-12',
        title: 'Backend y APIs REST',
        unit: 4,
        unitTitle: 'Módulo 4: Backend, APIs REST y Git',
        description: 'Servidores web, métodos HTTP (GET, POST, PUT, DELETE) y formato JSON para comunicación entre sistemas.',
        totalLessons: 3,
        iconName: 'Terminal',
        exercises: [
          {
            id: 'tech-12-1',
            type: 'multiple_choice',
            title: 'Métodos HTTP',
            question: '¿Qué método HTTP debe emplearse en una API RESTful para crear un nuevo recurso en el servidor?',
            options: ['POST', 'GET', 'DELETE', 'PATCH'],
            correctAnswer: 'POST',
            explanation: 'POST se usa para enviar datos al servidor con el fin de crear un nuevo elemento o recurso.'
          },
          {
            id: 'tech-12-2',
            type: 'fill_blank',
            title: 'Código de Estado HTTP',
            question: 'El código de respuesta HTTP que indica que un recurso se encontró y procesó con éxito es el ___:',
            codeSnippet: 'res.status(___).json({ mensaje: "Operación exitosa" });',
            options: ['200', '404', '500', '301'],
            correctAnswer: '200',
            explanation: 'El código HTTP 200 OK es la respuesta estándar de éxito para peticiones HTTP procesadas correctamente.'
          }
        ]
      },
      {
        id: 'tech-13',
        title: 'Calidad de Software y Debugging',
        unit: 4,
        unitTitle: 'Módulo 4: Backend, APIs REST y Git',
        description: 'Pruebas unitarias, depuración de errores, arquitectura en capas y principios Clean Code.',
        totalLessons: 3,
        iconName: 'Code',
        exercises: [
          {
            id: 'tech-13-1',
            type: 'multiple_choice',
            title: 'Pruebas Unitarias',
            question: '¿Qué evalúa una prueba unitaria (Unit Test) en desarrollo de software?',
            options: [
              'Verifica que un módulo o función individual funcione de forma aislada correctamente',
              'Comprueba si la pantalla de la computadora tiene suficientes píxeles',
              'Mide la velocidad del proveedor de servicio de internet',
              'Verifica el diseño del logo en las redes sociales'
            ],
            correctAnswer: 'Verifica que un módulo o función individual funcione de forma aislada correctamente',
            explanation: 'Las pruebas unitarias testean la unidad más pequeña de código asegún los requerimientos esperados.'
          },
          {
            id: 'tech-13-2',
            type: 'fill_blank',
            title: 'Manejo de Excepciones',
            question: 'Completa la estructura para capturar errores de ejecución sin congelar la aplicación:',
            codeSnippet: 'try:\n    resultado = 10 / 0\n___ ZeroDivisionError:\n    print("Error: No se puede dividir por cero")',
            options: ['except', 'catch', 'error', 'finally'],
            correctAnswer: 'except',
            explanation: 'El bloque try / except captura excepciones durante la ejecución permitiendo una recuperación limpia.'
          }
        ]
      },
      {
        id: 'tech-14',
        title: 'Fundamentos NoSQL y JSON/BSON',
        unit: 5,
        unitTitle: 'Módulo 5: Bases de Datos NoSQL y MongoDB',
        description: 'Diferencias entre SQL y NoSQL, modelos orientados a documentos, estructura JSON/BSON y escalabilidad.',
        totalLessons: 3,
        iconName: 'Database',
        exercises: [
          {
            id: 'tech-14-1',
            type: 'multiple_choice',
            title: 'Modelado NoSQL',
            question: '¿Cuál es la característica principal de las bases de datos NoSQL orientadas a documentos como MongoDB?',
            options: [
              'Almacenan datos en documentos flexibles tipo JSON en lugar de tablas con esquemas rígidos',
              'Solo permiten guardar valores numéricos enteros',
              'Exigen obligatoriamente sentencias SQL JOIN para realizar cualquier consulta',
              'No permiten guardar datos en disco y solo funcionan en memoria RAM'
            ],
            correctAnswer: 'Almacenan datos en documentos flexibles tipo JSON en lugar de tablas con esquemas rígidos',
            explanation: 'NoSQL permite modelos de datos flexibles y dinámicos estructurados como documentos JSON/BSON.'
          },
          {
            id: 'tech-14-2',
            type: 'fill_blank',
            title: 'Sintaxis de Colección JSON',
            question: 'Completa el campo para definir un arreglo con las tecnologías de un documento:',
            codeSnippet: '{\n  "desarrollador": "Ana",\n  "skills": ___ "Node.js", "MongoDB", "Express" ]\n}',
            options: ['[', '{', '(', '<'],
            correctAnswer: '[',
            explanation: 'En formato JSON estándar, las listas o arreglos de elementos se delimitan con corchetes [ ].'
          },
          {
            id: 'tech-14-3',
            type: 'find_bug',
            title: 'Sintaxis Estricta de JSON',
            question: 'Toca la línea que comete el error de incluir una coma final no permitida en JSON:',
            codeSnippet: `{
  "usuario": "Carlos",
  "edad": 22,
}`,
            bugLine: 3,
            correctAnswer: '  "edad": 22,',
            explanation: 'En la especificación estricta del formato JSON no se permiten comas finales (trailing commas) en el último atributo.'
          }
        ]
      },
      {
        id: 'tech-15',
        title: 'Operaciones CRUD en MongoDB',
        unit: 5,
        unitTitle: 'Módulo 5: Bases de Datos NoSQL y MongoDB',
        description: 'Manipulación y consulta de datos en colecciones con insertOne, find, updateOne y deleteOne.',
        totalLessons: 3,
        iconName: 'Layers',
        exercises: [
          {
            id: 'tech-15-1',
            type: 'multiple_choice',
            title: 'Consultas en MongoDB',
            question: '¿Qué método de MongoDB se utiliza para buscar todos los documentos que cumplan con un criterio?',
            options: [
              'db.coleccion.find({ estado: "activo" })',
              'SELECT * FROM coleccion WHERE estado = activo;',
              'db.coleccion.searchAll("activo")',
              'getDocuments(estado == "activo")'
            ],
            correctAnswer: 'db.coleccion.find({ estado: "activo" })',
            explanation: 'El método .find() toma un objeto de filtro en formato JSON para retornar los documentos coincidentes.'
          },
          {
            id: 'tech-15-2',
            type: 'code_blocks',
            title: 'Actualizar Documento',
            question: 'Ordena la instrucción de MongoDB para modificar el precio de un producto:',
            codeBlocks: [
              'db.productos.updateOne(',
              '  { _id: "p101" },',
              '  { $set: { precio: 1200 } }',
              ')'
            ],
            correctOrder: [
              'db.productos.updateOne(',
              '  { _id: "p101" },',
              '  { $set: { precio: 1200 } }',
              ')'
            ],
            explanation: 'updateOne() recibe primero el filtro del documento y luego la operación de actualización como $set.'
          },
          {
            id: 'tech-15-3',
            type: 'fill_blank',
            title: 'Inserción de Documento',
            question: 'Completa la instrucción para insertar un nuevo documento en la colección de usuarios:',
            codeSnippet: 'db.usuarios.___({ nombre: "Laura", rol: "admin" })',
            options: ['insertOne', 'addOne', 'createRow', 'push'],
            correctAnswer: 'insertOne',
            explanation: 'insertOne() es la función nativa para almacenar un documento en una colección de MongoDB.'
          }
        ]
      }
    ]
  }
];

export const INITIAL_PROFILE = {
  name: 'Estudiante Técnico',
  avatar: '💻',
  xp: 180,
  streak: 4,
  currentCourse: 'tech-software',
  completedNodeIds: ['tech-1'],
  nodeStars: { 'tech-1': 3 },
  league: 'Plata' as const,
  equippedSkin: 'default' as const,
  inventory: ['default' as const],
  dailyGoalXp: 50,
  todayXp: 30,
  lastActiveDate: new Date().toISOString().split('T')[0],
  totalLessonsCompleted: 3
};

export const INITIAL_LEAGUE_MEMBERS = [
  { id: '1', name: 'Laura_DevTech', avatar: '👩‍💻', xp: 450, rank: 1, badge: '🔥' },
  { id: '2', name: 'Carlos_SQL', avatar: '🗄️', xp: 390, rank: 2, badge: '⚡' },
  { id: '3', name: 'BytePico', avatar: '🐦', xp: 320, rank: 3, badge: '✨' },
  { id: '4', name: 'Estudiante Técnico (Tú)', avatar: '💻', xp: 180, isUser: true, rank: 4 },
  { id: '5', name: 'Marcos_Backend', avatar: '⚙️', xp: 110, rank: 5 },
  { id: '6', name: 'Sofia_Git', avatar: '🌿', xp: 75, rank: 6 }
];
