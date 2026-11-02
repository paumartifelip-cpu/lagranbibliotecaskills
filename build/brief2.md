# Encargo: escribir skills por profesión (español de España, tono cercano)

Contexto: una web para alumnos de 40-60 años con profesiones normales (oficios, comercio, salud, servicios, autónomos, pequeña empresa). Cada "skill" es una idea de instrucciones guardadas para ChatGPT/Codex que les ayuda a AUTOMATIZAR su negocio, GANAR MÁS DINERO o tener MÁS LIBERTAD (trabajar menos horas / no depender de ellos).

Debes escribir EXACTAMENTE 12 skills por cada profesión que te asigno, en un archivo de texto con este formato (una línea por skill, 5 campos separados por `|`, SIN usar el carácter `|` dentro del texto):

## Nombre de la profesión
Nombre de la skill|qué hace (verbo en 3ª persona del indicativo, minúscula, SIN punto final)|qué datos tiene que pedirme (empieza con sustantivo; "mis tarifas, el tipo de cliente y…")|qué entrega cada vez (un resultado concreto y útil)|XY

- Nombre: estilo "El Presupuestador de Obras", "La Recordadora", "El de Urgencias". Únicos dentro de la profesión, concretos y fáciles de reconocer (evita "El de Reseñas" genérico repetido en cada profesión: ponle contexto, p. ej. "El de Reseñas del Taller").
- Los campos 2, 3 y 4 deben ser ESPECÍFICOS del oficio, con vocabulario real de esa profesión (nada de "un mensaje", "el tema", "un plan" sueltos). Cada campo entre 8 y 25 palabras. Frase completa y natural cuando se lea dentro de: «Crea una skill llamada «N» que {campo2}. Para hacerlo bien, tiene que pedirme {campo3}. Cada vez que se use, debe entregarme {campo4}.»
- Campo 5, dos letras: X = objetivo (G = ganar más dinero, T = ahorrar tiempo/automatizar, L = libertad: delegar, trabajar menos, negocio que funciona sin mí). Y = función (V ventas/captar clientes, C atención y comunicación con clientes, M marketing y redes, A administración/facturas/cobros/números, O organización/agenda/operativa, E equipo/colaboradores, F formar/enseñar/documentar).
- Por profesión reparte aproximadamente: 5 G, 4 T, 3 L; y cubre varias funciones (V, C, M, A, O, E, F). Incluye al menos: una de precios/ingresos, una de captar clientes u oportunidades, una de comunicación, una de organización/documentación, y 2 de "libertad" (negocio sin mí / trabajar menos horas / ingresos recurrentes) adaptadas a la profesión.
- Piensa en las tareas REALES y dolorosas de esa profesión; evita relleno y no repitas ideas entre profesiones. Nada ilegal ni promesas médicas/legales (en salud y legal, "para revisión del profesional").
- Mira las primeras líneas de /Users/polo/lagranbibliotecaskills/build/prof1.txt (esas tienen 19, tú harás 12) como ejemplo del nivel de calidad y concreción esperado.
- Escribe el archivo con la herramienta Write en la ruta indicada. Al terminar, comprueba con Bash que cada línea de skill tiene 5 campos (`awk -F'|' 'NF!=5 && !/^##/'`) y el número de líneas (12 por profesión). Responde solo con "OK" y el recuento.

IMPORTANTE (segunda tanda): estas profesiones salen de una encuesta real de alumnos. Adapta cada profesión a la realidad de quien la ejerce: si es empleado/funcionario/estudiante/jubilado/en paro, las skills de "ganar más dinero" pueden ser ingresos extra, subir de puesto, encontrar trabajo, freelance o negocio paralelo con sus conocimientos, y las de "libertad" pueden ser teletrabajo, ahorrar horas, reducir dependencia del sueldo o disfrutar el tiempo; si ejerce por cuenta propia, aplica negocio/clientes. Usa vocabulario real y específico de cada profesión (herramientas, documentos y situaciones típicas). Hispanohablantes de España y Latinoamérica: evita regionalismos extremos.
