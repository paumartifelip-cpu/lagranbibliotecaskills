import re, json, html, pathlib, glob
ROOT = pathlib.Path(__file__).resolve().parent.parent
B = ROOT/'build'
areas = json.loads((B/'areas.json').read_text())
old = [l for l in (B/'prompts.txt').read_text().splitlines() if l and not l.startswith('#')]
UNIV = ("Que use siempre mi tono y mis ejemplos, y que, si falta algún dato, me lo pregunte en lugar de inventarlo. "
        "Antes de crearla, hazme las preguntas que necesites, de una en una, y dame la skill completa lista para guardar.")
def prompt(name, does, inp, out):
    does = does.strip().rstrip('.')
    return (f"Crea una skill llamada «{name}» que {does}. Para hacerlo bien, tiene que pedirme {inp.strip().rstrip('.')}. "
            f"Cada vez que se use, debe entregarme {out.strip().rstrip('.')}. " + UNIV)
def sentences(p): return len(re.findall(r'[.!?](?:\s|$)', p))

AF = {1:'V',2:'C',3:'M',4:'M',5:'M',6:'C',7:'O',8:'E',9:'A',10:'F',11:'V',12:'C',13:'C',14:'V',15:'V',16:'V',17:'M',18:'F',19:'O'}
AG = {1:'G',2:'T',3:'G',4:'G',5:'G',6:'T',7:'L',8:'T',9:'G',10:'G',11:'G',12:'T',13:'T',14:'G',15:'G',16:'G',17:'G',18:'L',19:'L'}
PROF_AREAS = {11,12,13,14,15,16,17}

cats = []   # [cid, title, kind]
S = []      # [id, name, desc, prompt, g, f, cid]
warn = []
i = 0
for a in areas:
    cid = ('p' if a['id'] in PROF_AREAS else 't') + 'a%d' % a['id']
    cats.append([cid, a['title'], 'prof' if a['id'] in PROF_AREAS else 'tarea'])
    for s in a['skills']:
        does, inp, out = old[i].split('|'); i += 1
        p = prompt(s['n'], does, inp, out)
        S.append([len(S), s['n'], s['d'], p, AG[a['id']], AF[a['id']], cid])
assert i == len(old)

files = sorted(glob.glob(str(B/'prof*.txt')), key=lambda f: int(re.search(r'prof(\d+)', f).group(1)))
pc = 0
for f in files:
    cur = None
    for ln in pathlib.Path(f).read_text().splitlines():
        ln = ln.strip()
        if not ln: continue
        if ln.startswith('##'):
            title = ln.lstrip('# ').strip()
            if title.lower().startswith('libertad'):
                cur = 'tlib'; cats.append([cur, title, 'tarea'])
            else:
                pc += 1; cur = 'p%d' % pc; cats.append([cur, title, 'prof'])
            continue
        parts = [x.strip() for x in ln.split('|')]
        if len(parts) == 5 and len(parts[4]) == 2 and parts[4][1] not in 'VCMAOEF': parts[4] = parts[4][0] + 'O'
        if len(parts) != 5 or len(parts[4]) != 2 or parts[4][0] not in 'GTL' or parts[4][1] not in 'VCMAOEF':
            warn.append((f, ln[:70])); continue
        n, does, inp, out, code = parts
        p = prompt(n, does, inp, out)
        if not 3 <= sentences(p) <= 6:
            warn.append(('frases', ln[:70])); continue
        d = does[0].upper() + does[1:].rstrip('.') + '.'
        S.append([len(S), n, d, p, code[0], code[1], cur])
for w in warn: print('SALTADA', w)

SECTORS = ['Salud, belleza y deporte','Educación y formación','Tecnología, datos e IA','Oficios, construcción e ingeniería','Comercio, hostelería y turismo','Administración, finanzas y legal','Creativos, medios y marketing','Transporte, logística, seguridad y campo','Tu situación y emprender']
RULES = [
 ('Tu situación y emprender', ['jubilado','en paro','estudiante','ama de casa','voluntariado','pastor','prejubilado','autónomo','emprendedor','dueño de pequeña','directivo','venta directa','consultor y formador','coaches','coach,','artesano','autolavado']),
 ('Salud, belleza y deporte', ['salud','médico','dental','fisio','psicolog','farmacia','veterin','enfermer','cuidado de mayores','peluquer','tatuaj','gimnasio','entrenador']),
 ('Educación y formación', ['profesorado','academia','docente','educador','profesor de idiomas']),
 ('Tecnología, datos e IA', ['informático','programador','ciberseguridad','consultor de ia','analista de datos','project manager']),
 ('Transporte, logística, seguridad y campo', ['transporte','taxista','logística','seguridad','emergencias','agricultura','agroforestal','jardinería','limpieza']),
 ('Oficios, construcción e ingeniería', ['fontanería','reformas','taller','arquitectura','ingenier','mantenimiento','operaciones','administrador de fincas','venta de autopartes']),
 ('Creativos, medios y marketing', ['fotograf','escritor','creativos','diseñador','creador de contenido','marketing','periodista','productor','director de arte','músico','agencia de marketing']),
 ('Comercio, hostelería y turismo', ['restaurantes','turismo','bar y','tienda','panadería','casa rural','bodas','vendedor','cajero','comercial','chef','hotel','inmobiliaria','alimentación']),
 ('Administración, finanzas y legal', ['abogado','gestoría','seguros','asesoría','banca','contable','contador','administrativo','funcionario','recursos humanos','asesor']),
]
def sector_of(t):
    tl = t.lower()
    for sec, kws in RULES:
        if any(k in tl for k in kws): return sec
    return None
cnt = {}
for s in S: cnt[s[6]] = cnt.get(s[6], 0) + 1
cats = [c + [cnt.get(c[0], 0), sector_of(c[1]) if c[2]=='prof' else ''] for c in cats if cnt.get(c[0], 0)]
for c in cats:
    if c[2]=='prof' and not c[4]: print('SIN SECTOR', c[1])
(ROOT/'skills-data.js').write_text('window.SECTORS=' + json.dumps(SECTORS, ensure_ascii=False) + ';\nwindow.CATS=' + json.dumps(cats, ensure_ascii=False, separators=(',', ':')) +
    ';\nwindow.SKILLS=' + json.dumps(S, ensure_ascii=False, separators=(',', ':')) + ';\n')
TOTAL = len(S); NPROF = sum(1 for c in cats if c[2] == 'prof')

# ---- CSS
(ROOT/'styles.css').write_text((B/'style.css').read_text())

WIRE = """<svg class="wire" viewBox="0 0 520 330" fill="none" stroke="#0A0A0A" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
<rect x="10" y="150" width="130" height="190" rx="12" fill="#F5F4F2"/><rect x="24" y="170" width="46" height="60" rx="6" fill="#EADCD3"/><rect x="80" y="170" width="46" height="46" rx="6"/><path d="M80 232h46M80 242h46M80 252h30M24 260h102v30H24z"/>
<rect x="168" y="120" width="104" height="210" rx="20" fill="#fff" stroke-width="2.4"/><rect x="180" y="160" width="80" height="70" rx="6" fill="#EADCD3"/><path d="M180 160l80 70M184 246h50M184 258h36M184 270h60"/>
<rect x="290" y="150" width="96" height="86" rx="10" fill="#F5F4F2"/><rect x="304" y="172" width="20" height="20" rx="3"/><path d="M308 176l12 12M320 176l-12 12M334 176h36M334 186h36M304 206h66M304 216h66M304 226h40"/>
<rect x="320" y="256" width="104" height="74" rx="12" fill="#F2E3C4"/><rect x="354" y="272" width="36" height="36" rx="5" fill="#F5F4F2"/><path d="M338 290h68M372 274v32"/>
<rect x="400" y="10" width="140" height="230" rx="14" fill="#F5F4F2"/><circle cx="416" cy="26" r="4"/><circle cx="430" cy="26" r="4"/><rect x="414" y="42" width="92" height="76" rx="6" fill="#EADCD3"/><path d="M414 42l92 76M460 42v76"/><rect x="414" y="132" width="106" height="70" rx="8"/><path d="M426 148h40M426 160h60M426 172h30"/>
</svg>"""

def nav(active):
    items = [('index.html','Inicio','home'),('cuestionario.html','Cuestionario','quiz'),('skills.html',f'Biblioteca · {TOTAL}','skills'),('paso-a-paso.html','Paso a paso','pasos')]
    on = ' class="on" aria-current="page"'
    a = ''.join('<a href="%s"%s>%s</a>' % (h, on if k == active else '', t) for h, t, k in items)
    return f'<div class="topnav"><div class="topnav-in">{a}</div></div>'
def head(title, desc, pg):
    return f"""<!doctype html>
<html lang="es"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>{title}</title><meta name="description" content="{desc}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=IBM+Plex+Mono:wght@400;500&display=swap">
<link rel="stylesheet" href="styles.css"></head><body data-page="{pg}">"""
def band(eyebrow, h1, lead, small=False, cta='', wire=False):
    return f"""<header class="band{' small' if small else ''}"><div class="band-in"><p class="eyebrow">{eyebrow}</p><h1>{h1}</h1><p class="lead">{lead}</p>{cta}</div>{WIRE if wire else ''}</header>"""
FOOT = '<footer>Clase en directo · IA para Vivir Mejor · Contrata sin Plata</footer>'
SCRIPTS = '<div id="packbar" class="packbar" hidden></div><script src="skills-data.js"></script><script src="app.js"></script></body></html>'
def page(name, html_): (ROOT/name).write_text(html_)

page('index.html', head('Skills · la gran biblioteca', f'Más de {TOTAL} skills por profesión con su mensaje listo para copiar.', 'home') + nav('home') +
 band('Contrata sin Plata · IA para Vivir Mejor', 'Skills,<br>la gran<br>biblioteca.',
 f'<b>{TOTAL} skills</b> para <b>{NPROF} profesiones</b> que te ayudan a automatizar tu trabajo, ganar más y tener más libertad. Cada una con su mensaje listo para pegar en ChatGPT o Codex.',
 cta='<div class="cta-row"><a class="btn" href="cuestionario.html">Descubre tus skills en 1 minuto →</a><a class="btn alt" href="skills.html">Ver la biblioteca</a></div>', wire=True) + f"""<div class="wrap">
<section class="block"><div class="block-head"><p class="block-eyebrow">Tres caminos</p><h2 class="block-title">¿Por dónde quieres empezar?</h2></div>
<div class="cards3">
<a class="bigcard" href="cuestionario.html"><span class="k">1 min</span><h3>Cuestionario</h3><p>Dinos tu profesión, tu objetivo y qué te quita tiempo. Te recomendamos tus mejores skills.</p><span class="go">Hacer el cuestionario →</span></a>
<a class="bigcard" href="skills.html"><span class="k">{TOTAL}</span><h3>Biblioteca</h3><p>Busca por profesión, por tarea o por objetivo. Cada skill con su texto «Crea una skill que…» para copiar.</p><span class="go">Ir a la biblioteca →</span></a>
<a class="bigcard" href="paso-a-paso.html"><span class="k">11</span><h3>Paso a paso</h3><p>Crea, prueba, corrige y comparte tu skill. Cada paso con su mensaje para copiar.</p><span class="go">Ir al paso a paso →</span></a>
</div></section>
<section class="block" id="que-es"><div class="block-head"><p class="block-eyebrow">Para empezar</p><h2 class="block-title">Qué es una skill</h2><p class="block-lead">Unas instrucciones que le das a la IA una vez y usa siempre.</p></div>
<div class="compare"><div class="bad"><h3>Sin skill</h3><p>Cada vez que pides algo, tienes que volver a explicar cómo lo quieres.</p></div><div class="good"><h3>Con skill</h3><p>Lo explicas una sola vez. La IA lo recuerda y lo hace siempre igual de bien.</p></div></div></section>
<section class="block"><div class="block-head"><p class="block-eyebrow">Para qué sirven</p><h2 class="block-title">Tres objetivos</h2></div>
<div class="how3"><div><div class="n">💰</div><h3>Ganar más</h3><p>Captar clientes, subir precios, vender mejor y no dejar dinero sin cobrar.</p></div><div><div class="n">⏱</div><h3>Automatizar</h3><p>Que la IA haga las tareas repetitivas: mensajes, presupuestos, informes.</p></div><div><div class="n">🕊</div><h3>Libertad</h3><p>Delegar, documentar y tener un trabajo que no dependa de ti a todas horas.</p></div></div></section>
""" + FOOT + '</div>' + SCRIPTS)

steps = (B/'steps.html').read_text(); stepsnav = (B/'stepsnav.html').read_text()
page('paso-a-paso.html', head('Paso a paso · Skills', 'Los 11 pasos para crear tu skill.', 'pasos') + nav('pasos') +
 band('Apartado 1 · Paso a paso', 'Los 11<br>pasos.', 'En cada paso: copia el mensaje, cambia lo que va entre <b>[corchetes]</b> y pégalo en ChatGPT o Codex.', small=True) +
 f'<div class="wrap"><nav aria-label="Pasos">{stepsnav}</nav><main class="steps">{steps}</main>' +
 '<div class="cta-row"><a class="btn" href="skills.html">Ahora elige tu skill en la biblioteca →</a></div>' + FOOT + '</div>' + SCRIPTS)

groups = ''
for sec in SECTORS:
    items = sorted([c for c in cats if c[2]=='prof' and c[4]==sec], key=lambda c: c[1].lower())
    if items:
        groups += f'<optgroup label="{html.escape(sec)}">' + ''.join(f'<option value="{c[0]}">{html.escape(c[1])}</option>' for c in items) + '</optgroup>'
FN = [('V','Conseguir clientes y vender'),('C','Atender clientes y contestar mensajes'),('M','Redes, marketing y contenido'),('A','Facturas, cobros y números'),('O','Organizarme y llevar la agenda'),('E','Gestionar equipo y colaboradores'),('F','Enseñar, explicar y documentar')]
fn = ''.join(f'<label class="pill"><input type="checkbox" name="f" value="{k}"><span>{t}</span></label>' for k, t in FN)
page('cuestionario.html', head('Cuestionario · Encuentra tus skills', 'Responde 4 preguntas y te recomendamos tus mejores skills.', 'quiz') + nav('quiz') +
 band('Apartado 3 · Cuestionario', 'Tus skills<br>en 1 minuto.', 'Contesta 4 preguntas rápidas y te recomendamos las skills que más te pueden ayudar. Luego eliges con cuáles empezar.', small=True) + f"""<div class="wrap">
<form id="quiz" class="quiz">
<fieldset><legend><span class="qn">1</span> ¿A qué te dedicas?</legend><select id="q-prof" aria-label="Profesión"><option value="">— Elige tu profesión —</option>{groups}<option value="otra">Otra / no la veo en la lista</option></select><p class="hint">Está ordenada por sectores. Si no aparece la tuya, elige la más parecida o «Otra» y te damos skills generales.</p></fieldset>
<fieldset><legend><span class="qn">2</span> ¿Qué quieres conseguir sobre todo?</legend><div class="opts3">
<label class="card-opt"><input type="radio" name="g" value="G" checked><span><b>💰 Ganar más dinero</b><small>Más clientes, mejores precios, cobrar a tiempo.</small></span></label>
<label class="card-opt"><input type="radio" name="g" value="T"><span><b>⏱ Automatizar y ahorrar tiempo</b><small>Que la IA haga lo repetitivo.</small></span></label>
<label class="card-opt"><input type="radio" name="g" value="L"><span><b>🕊 Tener más libertad</b><small>Delegar y depender menos de ti.</small></span></label></div></fieldset>
<fieldset><legend><span class="qn">3</span> ¿Qué te quita más tiempo? <small>(marca las que quieras)</small></legend><div class="pills">{fn}</div></fieldset>
<fieldset><legend><span class="qn">4</span> ¿Cuántas recomendaciones quieres ver?</legend><div class="pills"><label class="pill"><input type="radio" name="n" value="5"><span>5</span></label><label class="pill"><input type="radio" name="n" value="10" checked><span>10</span></label><label class="pill"><input type="radio" name="n" value="20"><span>20</span></label></div></fieldset>
<button class="copy big" type="submit" id="quiz-go">Ver mis skills</button>
</form>
<section id="quiz-res" class="block" hidden></section>""" + FOOT + '</div>' + SCRIPTS)

page('skills.html', head(f'Biblioteca de skills · {TOTAL} ideas', f'{TOTAL} skills por profesión, tarea y objetivo, con su mensaje listo para copiar.', 'skills') + nav('skills') +
 band('Apartado 2 · Biblioteca', f'{TOTAL} skills.', 'Elige tu profesión, o busca por palabra. Pulsa <b>Copiar</b> y pégalo en ChatGPT o Codex. Guarda con ⭐ las que quieras.', small=True) + f"""<div class="wrap">
<section class="block" id="biblioteca">
<input class="search" id="q" type="search" placeholder="Busca tu profesión o una tarea: abogado, presupuestos, reseñas, cobrar…" aria-label="Buscar skills">
<div id="sugg" class="sugg" hidden></div>
<div class="filters">
<div class="fgroup"><span class="flabel">Objetivo</span><div class="chips" id="f-goal"></div></div>
<div class="fgroup"><span class="flabel">Qué te quita tiempo</span><div class="chips" id="f-func"></div></div>
</div>
<div class="tabs" role="tablist"><button type="button" class="tab on" data-kind="prof">Por profesión <b id="n-prof"></b></button><button type="button" class="tab" data-kind="tarea">Por tarea <b id="n-tarea"></b></button></div>
<div id="picker"></div>
<div class="crumb" id="crumb" hidden></div>
<p class="status" id="status" aria-live="polite"></p>
<div id="list" class="list"></div>
<button type="button" class="more" id="more" hidden>Mostrar más</button>
</section>""" + FOOT + '</div>' + SCRIPTS)
print('ok', TOTAL, 'skills,', NPROF, 'profesiones,', len(cats), 'categorías')
