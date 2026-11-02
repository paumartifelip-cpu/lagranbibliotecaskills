# Encargo: AÑADIR 10 skills más a cada profesión (español, tono cercano)

Contexto: web para alumnos de 40-60 años con profesiones normales. Cada "skill" es una idea de instrucciones guardadas para ChatGPT/Codex que les ayuda a AUTOMATIZAR su trabajo, GANAR MÁS DINERO o tener MÁS LIBERTAD. Ya existen skills para cada profesión; los alumnos dicen que hay pocas. Tú añades 10 NUEVAS por profesión, MUY específicas del oficio.

1. Lee /Users/polo/lagranbibliotecaskills/build/existing.txt: contiene, bajo cada "## Profesión", los nombres de las skills que YA existen. No repitas esas ideas ni sus nombres; busca tareas reales distintas y dolorosas de esa profesión (documentos concretos, situaciones típicas, herramientas, normas, temporadas, tipos de cliente, errores frecuentes, etc.). Piensa como alguien que ejerce esa profesión a diario.
2. Escribe un archivo con el formato (una línea por skill, 5 campos separados por `|`, SIN usar el carácter `|` ni puntos finales dentro del texto):

## Título EXACTO de la profesión (copiado tal cual del encargo)
Nombre de la skill|qué hace (verbo en 3ª persona del indicativo, minúscula, sin punto final)|qué datos tiene que pedirme (empieza con sustantivo)|qué entrega cada vez (resultado concreto)|XY

- X = G (ganar más dinero), T (ahorrar tiempo/automatizar) o L (libertad: delegar, trabajar menos, negocio que funciona sin mí). Y = UNA de estas letras exactas: V (vender/captar clientes), C (atención y comunicación con clientes), M (marketing y redes), A (administración, facturas, cobros, números), O (organización/agenda/operativa), E (equipo/colaboradores), F (formar/enseñar/documentar). No uses otras letras.
- Reparto por profesión: 4 G, 3 T, 3 L, y varía las funciones Y (prioriza las que menos aparecen en la lista existente).
- Nombres concretos y únicos ("El de las Revisiones de Caldera", no "El de Reseñas"). Campos 2, 3 y 4 de 8 a 25 palabras, frases naturales y completas, vocabulario real del oficio; nada de "un mensaje", "el tema", "un plan" sueltos.
- Si la persona es empleado/funcionario/jubilado/estudiante/en paro, adapta: ingresos extra, subir de puesto, encontrar trabajo, negocio paralelo, teletrabajo, ahorrar horas. Nada ilegal; en salud y derecho, siempre "para revisión del profesional".
3. Al terminar, comprueba con Bash: `awk -F'|' 'NF!=5 && !/^##/' archivo` (debe salir vacío), que cada línea de skill acabe en dos letras válidas, y que hay 10 líneas por profesión. Responde solo "OK" y el recuento.
