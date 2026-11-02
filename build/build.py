import re, json, html, pathlib
ROOT = pathlib.Path(__file__).resolve().parent.parent
SCR = pathlib.Path('/private/tmp/claude-501/-Users-polo-lagranbibliotecaskills/95fbb9c6-3e9a-4436-8da3-92b3f0308f9d/scratchpad')
src = (SCR/'site.html').read_text()
areas = json.loads((SCR/'data.json').read_text())
lines = [l for l in (ROOT/'build/prompts.txt').read_text().splitlines() if l and not l.startswith('#')]
assert len(lines) == sum(len(a['skills']) for a in areas)

# ---- CSS: reuse original style block + extras
css = re.search(r'<style>(.*?)</style>', src, re.S).group(1)
css += """
/* ===== multipágina ===== */
.band-in { grid-template-columns: 1fr !important; padding-block: 48px 72px; }
.band.small .band-in { padding-block: 36px 60px; }
.band.small h1 { font-size: clamp(40px, 8vw, 84px); }
.topnav { z-index: 20; }
.topnav a.on { background: #FFF0DC; color: var(--accent); }
.brand { font-weight: 800; letter-spacing: -.02em; color: var(--fg) !important; }
.cta-row { display: flex; gap: 12px; flex-wrap: wrap; margin-top: 8px; }
.btn { display: inline-flex; align-items: center; gap: 8px; text-decoration: none; font-weight: 700; padding: 14px 26px; border-radius: 999px; background: #fff; color: var(--accent); box-shadow: 0 10px 24px rgba(150,70,10,.25); }
.btn.alt { background: rgba(255,255,255,.25); color: #fff; box-shadow: none; border: 1px solid rgba(255,255,255,.6); }
.cards2 { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; }
.bigcard { display: flex; flex-direction: column; gap: 10px; text-decoration: none; color: var(--fg); background: var(--card); border: 1px solid #fff; border-radius: 28px; padding: 28px; box-shadow: 0 14px 40px rgba(190,120,50,.12); }
.bigcard:hover { transform: translateY(-3px); } .bigcard { transition: transform .2s; }
.bigcard .k { font-size: 56px; font-weight: 800; line-height: 1; color: var(--accent); }
.bigcard h3 { margin: 0; font-size: 24px; } .bigcard p { margin: 0; color: var(--muted); }
.bigcard .go { font-weight: 700; color: var(--accent); }
.skillgrid { display: flex; flex-direction: column; gap: 14px; padding: 16px 20px 22px; }
.sk { border: 1px solid var(--line); background: #fff; border-radius: 20px; padding: 18px 20px; display: flex; flex-direction: column; gap: 10px; }
.sk-h { display: flex; flex-direction: column; }
.sk-h b { font-size: 18px; } .sk-h span { color: var(--muted); font-size: 15px; }
.sk pre { font-size: 13.5px; padding: 14px 16px; border-radius: 16px; }
.sk .copy { padding: 10px 22px; min-height: 42px; font-size: 14px; }
.sk[hidden] { display: none; }
.area-note { padding: 14px 26px 0; }
.stepnav-wrap { position: sticky; top: 80px; z-index: 5; }
footer { text-align: center; }
@media (max-width: 640px) { .cards2 { grid-template-columns: 1fr; } .topnav-in { justify-content: flex-start; } }
"""
css = re.sub(r'\.skills li\b[^{]*\{[^}]*\}', '', css)  # drop old list styles not needed
(ROOT/'styles.css').write_text(css)

def nav(active):
    items = [('index.html','Inicio','home'),('paso-a-paso.html','Paso a paso','pasos'),('skills.html','Biblioteca · 228 skills','skills')]
    on = ' class="on" aria-current="page"'
    a = ''.join('<a href="%s"%s>%s</a>' % (h, on if k==active else '', t) for h,t,k in items)
    return f'<div class="topnav"><div class="topnav-in">{a}</div></div>'

def head(title, desc):
    return f'''<!doctype html>
<html lang="es"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>{title}</title><meta name="description" content="{desc}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500&family=Outfit:wght@300;400;500;600;700;800&display=swap">
<link rel="stylesheet" href="styles.css"></head><body>'''

def band(eyebrow, h1, lead, small=False, cta=''):
    return f'''<div class="band{' small' if small else ''}"><span class="blob b1" aria-hidden="true"></span><span class="blob b2" aria-hidden="true"></span><span class="blob b3" aria-hidden="true"></span>
<div class="band-in"><div class="band-txt"><p class="eyebrow">{eyebrow}</p><h1>{h1}</h1><p class="lead">{lead}</p>{cta}</div></div></div>'''

FOOT = '<footer>Clase en directo · IA para Vivir Mejor · Contrata sin Plata</footer></div><script src="app.js"></script></body></html>'

# ---- INDEX
index = head('Skills · la gran biblioteca', 'Los mensajes de la clase para crear tus skills y 228 ideas con su mensaje listo para copiar.') + \
 band('Clase en directo · IA para Vivir Mejor · Contrata sin Plata', 'Skills<br>la gran<br>biblioteca',
 'Los mensajes de la clase para crear tus skills y <b>228 ideas</b>, cada una con su mensaje listo para pegar en ChatGPT o Codex. Pulsa <b>Copiar</b> y cambia lo que va entre <span class="ph"><b>[corchetes]</b></span>.',
 cta='<div class="cta-row"><a class="btn" href="paso-a-paso.html">Empezar el paso a paso →</a><a class="btn alt" href="skills.html">Ver las 228 skills</a></div>') + \
 nav('home') + '''<div class="wrap">
<section class="block" id="que-es"><div class="block-head"><p class="block-eyebrow">Para empezar</p><h2 class="block-title">Qué es una skill</h2><p class="block-lead">Unas instrucciones que le das a la IA una vez y usa siempre.</p></div>
<div class="compare"><div class="bad"><h3>Sin skill</h3><p>Cada vez que pides algo, tienes que volver a explicar cómo lo quieres.</p></div><div class="good"><h3>Con skill</h3><p>Lo explicas una sola vez. La IA lo recuerda y lo hace siempre igual de bien.</p></div></div></section>
<section class="block"><div class="block-head"><p class="block-eyebrow">Dos caminos</p><h2 class="block-title">¿Por dónde quieres empezar?</h2></div>
<div class="cards2">
<a class="bigcard" href="paso-a-paso.html"><span class="k">11</span><h3>Paso a paso</h3><p>Descubre tus tareas, crea tu skill, pruébala, corrígela y compártela. Cada paso con su mensaje para copiar.</p><span class="go">Ir al paso a paso →</span></a>
<a class="bigcard" href="skills.html"><span class="k">228</span><h3>Biblioteca de skills</h3><p>Ideas en 19 áreas. Cada una con un texto «Crea una skill que…» listo para copiar y pegar en ChatGPT o Codex.</p><span class="go">Ir a la biblioteca →</span></a>
</div></section>
<section class="block"><div class="block-head"><p class="block-eyebrow">Cómo se usa</p><h2 class="block-title">En 3 movimientos</h2></div>
<div class="how3"><div><div class="n">1</div><h3>Elige</h3><p>Busca tu área en la biblioteca o sigue el paso a paso.</p></div><div><div class="n">2</div><h3>Copia</h3><p>Pulsa el botón y el mensaje queda copiado.</p></div><div><div class="n">3</div><h3>Pega</h3><p>Pégalo en ChatGPT o Codex, contesta sus preguntas y guarda tu skill.</p></div></div></section>
''' + FOOT
(ROOT/'index.html').write_text(index)

# ---- PASO A PASO (reuse steps from original)
m = re.search(r'<main class="steps">(.*?)</main>', src, re.S)
steps_html = m.group(1)
nav_steps = re.search(r'<nav aria-label="Pasos">(.*?)</nav>', src, re.S).group(1)
pasos = head('Paso a paso · Skills', 'Los 11 pasos para crear tu skill, cada uno con su mensaje para copiar.') + \
 band('Apartado 1 · Paso a paso', 'Los 11<br>pasos', 'En cada paso: copia el mensaje, cambia lo que va entre <b>[corchetes]</b> y pégalo en ChatGPT o Codex.', small=True) + \
 nav('pasos') + f'<div class="wrap"><nav aria-label="Pasos">{nav_steps}</nav><main class="steps">{steps_html}</main>' + \
 '<div class="cta-row"><a class="btn" style="background:linear-gradient(135deg,#F58A4B,#C9441A);color:#fff" href="skills.html">Ahora elige tu skill en la biblioteca →</a></div>' + FOOT
(ROOT/'paso-a-paso.html').write_text(pasos)

# ---- SKILLS
UNIV = ("Que use siempre mi tono y mis ejemplos, y que, si falta algún dato, me lo pregunte en lugar de inventarlo. "
        "Antes de crearla, hazme las preguntas que necesites, de una en una, y dame la skill completa lista para guardar.")
def prompt(name, does, inp, out):
    return (f"Crea una skill llamada «{name}» que {does}. Para hacerlo bien, tiene que pedirme {inp}. "
            f"Cada vez que se use, debe entregarme {out}. " + UNIV)
i = 0; total = 0; sections = []; chips = []
for a in areas:
    cards = []
    for s in a['skills']:
        does, inp, out = lines[i].split('|'); i += 1
        p = prompt(s['n'], does, inp, out)
        assert 3 <= len(re.findall(r'[.!?](?:\s|$)', p)) <= 6, p
        cards.append(f'<article class="sk"><div class="sk-h"><b>{html.escape(s["n"])}</b><span>{html.escape(s["d"])}</span></div>'
                     f'<div class="prompt"><pre>{html.escape(p)}</pre><button class="copy" type="button">Copiar</button></div></article>')
    n = len(cards); total += n
    sections.append(f'<details class="area" id="area-{a["id"]}"{" open" if a["id"]==1 else ""}><summary><span class="area-num">{a["id"]:02d}</span><span class="area-title">{html.escape(a["title"])}</span><span class="area-count">{n} skills</span></summary><div class="skillgrid">{"".join(cards)}</div></details>')
    chips.append(f'<a href="#area-{a["id"]}">{a["id"]:02d} {html.escape(a["title"])}</a>')
skills = head('Biblioteca de skills · 228 ideas', '228 ideas de skills con su mensaje listo para copiar y pegar en ChatGPT o Codex.') + \
 band('Apartado 2 · Biblioteca', f'<span style="display:block">{total} skills</span>', 'Elige la tuya, pulsa <b>Copiar</b> y pégala en ChatGPT o Codex. La IA te hará las preguntas y creará tu skill.', small=True) + \
 nav('skills') + f'''<div class="wrap"><section class="block" id="biblioteca">
<div class="how3"><div><div class="n">1</div><h3>Busca tu área</h3><p>Primero la de tu profesión, después las generales: ventas, redes, correo.</p></div><div><div class="n">2</div><h3>Elige 3, no 30</h3><p>Pásalas por el filtro de las 3 preguntas (paso 2). Tu equipo de 3.</p></div><div><div class="n">3</div><h3>Copia y pega</h3><p>Pulsa Copiar y pégalo en ChatGPT o Codex. Hazla tuya con el paso a paso.</p></div></div>
<input class="search" id="q" type="search" placeholder="Buscar entre las {total} skills (ej. correo, reseñas, precios)…" aria-label="Buscar skills">
<nav class="areanav" aria-label="Áreas">{"".join(chips)}</nav>
<div id="areas" style="display:flex;flex-direction:column;gap:12px">{"".join(sections)}</div>
<p class="empty" id="empty">No hay skills con esa búsqueda. Prueba otra palabra.</p></section>''' + FOOT
(ROOT/'skills.html').write_text(skills)

# ---- JS
js = re.search(r'<script>(.*?)</script>', src, re.S).group(1)
js = js.replace("var text = pre.textContent", "var pre = btn.parentElement.querySelector('pre');\n      var text = pre.textContent") if False else js
js = js.replace("a.querySelectorAll('li')", "a.querySelectorAll('.sk')")
(ROOT/'app.js').write_text(js)
print('ok', total)
