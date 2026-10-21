#!/usr/bin/env python3
"""Builds the Smart Pix site: shared head/nav/footer + 5 pages. Output: site/*.html (full documents)."""
import json, os, html
HERE = os.path.dirname(os.path.abspath(__file__))
LOGO_PATHS = open(os.path.join(HERE, 'logo_paths.svg')).read()
WA_NUM = '5511910101324'
WA_PATH = 'M12 2a10 10 0 0 0-8.66 15l-1.3 4.76 4.88-1.28A10 10 0 1 0 12 2zm0 18.2a8.2 8.2 0 0 1-4.18-1.14l-.3-.18-2.9.76.78-2.83-.2-.29A8.2 8.2 0 1 1 12 20.2zm4.5-6.14c-.25-.12-1.46-.72-1.69-.8-.22-.08-.39-.12-.55.13-.16.24-.63.8-.77.96-.14.17-.28.19-.53.06-.25-.12-1.04-.38-1.98-1.22-.73-.65-1.23-1.46-1.37-1.7-.14-.25-.02-.38.11-.5.11-.11.25-.29.37-.43.12-.15.16-.25.25-.41.08-.17.04-.31-.02-.43-.06-.13-.55-1.33-.76-1.82-.2-.48-.4-.41-.55-.42h-.47c-.16 0-.43.06-.65.31-.22.24-.86.84-.86 2.04s.88 2.37 1 2.53c.12.17 1.73 2.64 4.2 3.7.59.25 1.05.4 1.4.52.59.19 1.13.16 1.55.1.47-.07 1.46-.6 1.67-1.18.2-.58.2-1.07.14-1.18-.06-.1-.22-.16-.47-.29z'
WA_SVG = f'<svg viewBox="0 0 24 24" aria-hidden="true" fill="currentColor"><path d="{WA_PATH}"/></svg>'
ARROW = '<svg viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14M13 6l6 6-6 6"/></svg>'
SITE = 'https://smartpix.com.br/'
AI = 'Ilustração IA'

def e(t): return html.escape(t, quote=True)
def img(name, alt, sizes='100vw', w=1536, h=863, lazy=True, small=800, cls='', style=''):
    big = f'{name}-{w}' if not name.endswith('.webp') else name
    return (f'<img src="img/{name}-{w}.webp" srcset="img/{name}-{small}.webp {small}w, img/{name}-{w}.webp {w}w" sizes="{sizes}" '
            f'alt="{e(alt)}" width="{w}" height="{h}"' + (' loading="lazy" decoding="async"' if lazy else ' fetchpriority="high"') +
            (f' class="{cls}"' if cls else '') + (f' style="{style}"' if style else '') + '>')
IMGS = {  # name: (w, h, small)
 'ai-install': (1536, 863, 800), 'ai-stage': (1536, 863, 800), 'ai-vitrine': (1536, 863, 800), 'ai-van': (1536, 863, 800), 'ai-facade': (1536, 863, 800),
 'ai-print3d': (1536, 863, 800), 'ai-whitelabel': (1536, 863, 800), 'ai-floor': (1500, 843, 800), 'ai-booth': (1200, 674, 700), 'ai-printer': (1500, 843, 800),
 'ai-materials': (1200, 674, 700), 'ai-roll': (1200, 674, 700), 'ai-macro': (1200, 594, 700), 'real-fabrica': (1440, 1440, 800)}
def pic(name, alt, sizes='100vw', lazy=True, cls='', style=''):
    w, h, s = IMGS[name]; return img(name, alt, sizes, w, h, lazy, s, cls, style)

def crumbs(path, name):
    return {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
      {"@type": "ListItem", "position": 1, "name": "Início", "item": SITE}, {"@type": "ListItem", "position": 2, "name": name, "item": SITE + path}]}
def head(title, desc, path, ld=None, page='index'):
    ldj = f'<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>' if ld else ''
    return f'''<!doctype html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
<link rel="canonical" href="{SITE}{path}">
<meta name="theme-color" content="#000000">
<meta property="og:type" content="website">
<meta property="og:locale" content="pt_BR">
<meta property="og:site_name" content="Smart Pix Impressão Digital">
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(desc)}">
<meta property="og:url" content="{SITE}{path}">
<meta property="og:image" content="{SITE}img/og.jpg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="Galpão de produção da Smart Pix em Atibaia, com o logo smart PIX">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="img/logo-180.png">
<link rel="apple-touch-icon" sizes="180x180" href="img/logo-180.png">
<link rel="preload" href="fonts/inter-latin-600-normal.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="css/site.css">
{ldj}
</head>
<body data-page="{page}">
<svg width="0" height="0" style="position:absolute" aria-hidden="true" focusable="false"><symbol id="sp-logo" viewBox="0 0 1000 1000"><circle cx="500" cy="500" r="500" fill="#bde000"/>{LOGO_PATHS}</symbol></svg>
<a class="skip" href="#conteudo">Pular para o conteúdo</a>
'''

NAV_ITEMS = [('solucoes.html', 'Soluções'), ('cenografia.html', 'Cenografia e agências'), ('projetos.html', 'Projetos'), ('./#problemas', 'Problemas'), ('./#duvidas', 'Dúvidas')]
def nav(active):
    links = ''.join(f'<li><a href="{h}"' + (' aria-current="page"' if h == active else '') + f'>{t}</a></li>' for h, t in NAV_ITEMS)
    sheet = ''.join(f'<li><a href="{h}">{t}</a></li>' for h, t in [('./', 'Início')] + NAV_ITEMS)
    wa = 'Olá, Smart Pix! Vim pelo site e quero falar sobre um projeto.'
    return f'''<header class="nav" id="nav">
  <div class="nav-in">
    <a class="brand" href="./" aria-label="Smart Pix Impressão Digital, página inicial"><svg aria-hidden="true"><use href="#sp-logo"/></svg><span class="wm">smart<b>PIX</b></span></a>
    <ul class="nav-links">{links}</ul>
    <div class="nav-act">
      <a class="nav-wa" href="https://wa.me/{WA_NUM}" data-wa="{e(wa)}" data-cta="nav-wa" aria-label="Falar no WhatsApp">{WA_SVG}</a>
      <a class="nav-cta" href="orcamento.html" data-cta="nav">Orçamento</a>
      <button class="menu-btn" id="menuBtn" type="button" aria-expanded="false" aria-controls="sheet" aria-label="Abrir menu"><span></span><span></span></button>
    </div>
  </div>
</header>
<div class="sheet-scrim" id="scrim"></div>
<nav class="sheet" id="sheet" aria-label="Menu">
  <ul>{sheet}</ul>
  <a class="btn btn-fill" href="orcamento.html" data-cta="sheet">Pedir orçamento</a>
  <a class="sheet-wa" href="https://wa.me/{WA_NUM}" data-wa="{e(wa)}" data-cta="sheet-wa">{WA_SVG}WhatsApp (11) 91010-1324</a>
</nav>
<main id="conteudo">
'''

def foot(scripts=()):
    s = ''.join(f'<script src="js/{x}" defer></script>' for x in ('site.js',) + tuple(scripts))
    return f'''</main>
<footer class="foot">
  <div class="wrap">
    <p class="foot-note">Imagens marcadas como “{AI}” foram geradas por inteligência artificial para ilustrar os tipos de projeto. Fotos marcadas como “Foto real” são da nossa produção. Por respeito aos clientes, o site não mostra marcas de terceiros.</p>
    <div class="foot-cols">
      <div><h2 class="foot-h">Soluções</h2><ul><li><a href="solucoes.html#lona">Lona sem emenda</a></li><li><a href="solucoes.html#smart-floor">Smart Floor</a></li><li><a href="solucoes.html#cenografia">Cenografia e estandes</a></li><li><a href="solucoes.html#letras-caixa">Letras-caixa e fachadas</a></li><li><a href="solucoes.html#vitrines">Vitrines e PDV</a></li><li><a href="solucoes.html#frota">Envelopamento de frota</a></li><li><a href="solucoes.html#impressao-3d">Impressão 3D</a></li></ul></div>
      <div><h2 class="foot-h">Para quem</h2><ul><li><a href="cenografia.html">Cenografia e montadoras</a></li><li><a href="cenografia.html#agencias">Agências e produtoras</a></li><li><a href="orcamento.html?perfil=Empresa">Empresas</a></li></ul></div>
      <div><h2 class="foot-h">Smart Pix</h2><ul><li><a href="./#quem-somos">Quem somos</a></li><li><a href="projetos.html">Projetos</a></li><li><a href="./#problemas">Problemas que resolvemos</a></li><li><a href="./#duvidas">Dúvidas</a></li></ul></div>
      <div><h2 class="foot-h">Contato</h2><ul><li><a href="orcamento.html">Pedir orçamento</a></li><li><a href="https://wa.me/{WA_NUM}" data-wa="Olá, Smart Pix! Vim pelo site." data-cta="footer-wa">WhatsApp (11) 91010-1324</a></li><li><a href="tel:+551124273880">(11) 2427-3880</a></li><li><a href="mailto:atendimento@smartpix.com.br">atendimento@smartpix.com.br</a></li><li><a href="https://www.instagram.com/smartpixoficial/" target="_blank" rel="noopener">Instagram</a></li></ul></div>
    </div>
    <div class="foot-legal">
      <p>© Smart Pix Impressão Digital · CNPJ 05.801.627/0001-65</p>
      <p>Av. São Paulo, 111, Alvinópolis, Atibaia, SP · Seg a sex, 8h às 18h</p>
    </div>
  </div>
</footer>
{s}
</body>
</html>
'''

FIX = [('smart floor', 'Smart Floor'), ('pdv', 'PDV'), ('3d', '3D'), ('smart pix', 'Smart Pix'), ('atibaia', 'Atibaia')]
def kicker(t):
    for a, b in FIX: t = t.replace(a, b)
    return f'<p class="kicker">{t[0].upper() + t[1:]}</p>'

def q(v): return 'orcamento.html?produto=' + v.replace(' ', '%20').replace('/', '%2F')

# ------------------------------------------------------------------ data
PRODUCTS = [
 # id, name, value(for quote), img, kicker, title, lead, bullets
 ('lona', 'Lona e backdrop', 'Lona / backdrop', 'ai-stage', 'lona sem emenda', 'Até 5 m. Uma peça só.', 'Backdrops, painéis de palco e fundos de foto sem a emenda cortando a imagem.',
  ['Até 5 m de largura numa peça só', 'Lona e lona backlight', 'Impressão UV LED, com a tinta curada na hora', 'Entrega e montagem com frota e equipe próprias']),
 ('smart-floor', 'Smart Floor', 'Smart Floor', 'ai-floor', 'smart floor', 'O chão também fala.', 'Piso vinílico impresso em UV LED, do tamanho exato do seu evento.',
  ['A maior área do estande vira mídia', 'Corredores, palcos, estandes e ativações', 'Sob medida para o espaço', 'Instalação pela equipe própria']),
 ('cenografia', 'Cenografia e estandes', 'Estande completo', 'ai-booth', 'cenografia · estandes', 'O cenário inteiro, num pedido só.', 'Para empresas de cenografia, montadoras e agências: a parte gráfica completa do estande ou do palco.',
  ['Lona, tecido, piso, ACM, PVC e adesivo', 'Impressão 3D para peças especiais', 'Entrega no pavilhão com frota própria', 'Montagem pela nossa equipe, se você precisar']),
 ('letras-caixa', 'Letras-caixa e fachadas', 'Letra-caixa / fachada', 'ai-facade', 'letras-caixa · fachadas', 'A marca em três dimensões.', 'Letras-caixa e fachadas em ACM e acrílico para lojas, recepções e cenários.',
  ['ACM e acrílico', 'Fachadas, recepções e cenários', 'Produção e instalação próprias']),
 ('vitrines', 'Vitrines e PDV', 'Vitrine / adesivo', 'ai-vitrine', 'vitrines · pdv', 'A loja vende antes da porta.', 'Adesivos de vitrine e materiais de ponto de venda, iguais em todas as lojas da rede.',
  ['Mesmo arquivo e mesma produção para todas as lojas', 'Adesivos para vitrine e PDV', 'Instalação sob consulta']),
 ('frota', 'Envelopamento de frota', 'Envelopamento de frota', 'ai-van', 'frota', 'A marca que roda a cidade.', 'Envelopamento de carros, vans e caminhões, com aplicação pela nossa equipe.',
  ['Carros, vans e caminhões', 'Impressão e aplicação na mesma empresa']),
 ('impressao-3d', 'Impressão 3D', 'Impressão 3D', 'ai-print3d', 'impressão 3d', 'Formas que a impressão plana não faz.', 'Peças cenográficas e displays em impressão 3D, na mesma produção da parte gráfica.',
  ['Peças cenográficas e displays', 'Produzidas junto com o resto do projeto']),
 ('materiais', 'Materiais', 'Outro', 'ai-materials', 'materiais', 'O material certo para cada peça.', 'Indicamos o substrato pelo uso: dentro ou fora, por quanto tempo, com ou sem luz.',
  ['Lona e lona backlight', 'Tecido', 'ACM e PVC expandido', 'Adesivo vinil e piso vinílico']),
]
CTA = {'lona': ('Orçar lona e backdrop', 'lona e backdrop sem emenda'), 'smart-floor': ('Orçar Smart Floor', 'o Smart Floor'), 'cenografia': ('Orçar um estande', 'cenografia e estandes'),
 'letras-caixa': ('Orçar letras-caixa', 'letras-caixa e fachadas'), 'vitrines': ('Orçar vitrines e PDV', 'vitrines e PDV'), 'frota': ('Orçar envelopamento', 'envelopamento de frota'),
 'impressao-3d': ('Orçar impressão 3D', 'impressão 3D'), 'materiais': ('Pedir indicação de material', 'qual material usar no meu projeto')}
PROBLEMS = [
 # slug, title, before_img, before_style/fx, after_img, problem, solution, quote product
 ('emenda', 'A emenda aparece na foto', 'ai-stage', 'seam', 'ai-stage',
  'Backdrop grande montado em faixas: a emenda corta o palco e aparece em todas as fotos do evento.',
  'Imprimimos até 5 m de largura numa peça só, em UV LED. O painel do palco sai inteiro.', 'Lona / backdrop'),
 ('cor', 'A cor muda de uma peça para outra', 'ai-booth', 'tone', 'ai-booth',
  'Lona de um fornecedor, tecido de outro, adesivo de um terceiro: o mesmo tom da marca sai diferente em cada peça.',
  'Toda a parte gráfica sai da mesma produção, em vez de três fornecedores diferentes.', 'Estande completo'),
 ('instalacao', 'A gráfica entrega, mas não instala', 'ai-whitelabel', 'dull', 'ai-install',
  'O material chega ao pavilhão em rolos, e alguém da sua equipe precisa montar tudo na janela curta de montagem.',
  'Frota e equipe de instalação próprias: levamos até o local e montamos.', 'Estande completo'),
 ('fornecedores', 'Cinco fornecedores para um estande', 'ai-materials', 'dull', 'ai-booth',
  'Um fornecedor para a lona, outro para o tecido, outro para o piso, outro para a letra-caixa e outro para a peça 3D. Cinco prazos e cinco riscos.',
  'Lona, tecido, piso, ACM, PVC, adesivo e impressão 3D num pedido só, com um responsável.', 'Estande completo'),
 ('piso', 'O piso do evento não comunica nada', 'ai-floor', 'floor', 'ai-floor',
  'Carpete cinza num evento que custou caro: o chão é a maior área do espaço e fica em branco.',
  'Smart Floor: piso vinílico impresso em UV LED, do tamanho exato do seu espaço.', 'Smart Floor'),
 ('sigilo', 'Seu cliente não pode ver o fornecedor', 'ai-whitelabel', 'tags', 'ai-whitelabel',
  'Você é agência, produtora ou empresa de cenografia e a produção terceirizada não deve aparecer para o seu cliente.',
  'Atuamos como parceiro de produção de agências e empresas de cenografia. A identificação da entrega é conversada no orçamento.', 'Estande completo'),
 ('lojas', 'Cada loja da rede com uma vitrine diferente', 'ai-vitrine', 'stores', 'ai-vitrine',
  'Cada loja contratou uma gráfica local, e a mesma campanha aparece com cores e acabamentos diferentes.',
  'Mesmo arquivo e mesma produção para todas as lojas da rede.', 'Vitrine / adesivo'),
 ('3d', 'A peça cenográfica 3D parece impossível', 'ai-print3d', 'blueprint', 'ai-print3d',
  'O projeto pede uma forma orgânica, grande e leve, e o fornecedor de impressão não faz.',
  'Impressão 3D na mesma produção da parte gráfica, para peças cenográficas e displays.', 'Impressão 3D'),
]
PROJ_Q = {'corporativo': 'Lona / backdrop', 'feiras': 'Estande completo', 'montagem': 'Estande completo', 'varejo': 'Vitrine / adesivo', 'fachadas': 'Letra-caixa / fachada', 'pisos': 'Smart Floor', 'frota': 'Envelopamento de frota', '3d': 'Impressão 3D', 'terceiros': 'Estande completo'}
PROJECTS = [
 # id, cat, title, img, line, bullets
 ('corporativo', 'eventos', 'Convenções e eventos corporativos', 'ai-stage', 'Palco, backdrop, piso e sinalização do evento.', ['Backdrop de palco até 5 m sem emenda', 'Smart Floor para corredores e palco', 'Sinalização e fundos de foto', 'Montagem na janela do evento']),
 ('feiras', 'feiras cenografia', 'Feiras e estandes', 'ai-booth', 'A parte gráfica completa do estande, pronta para a montadora.', ['Paredes em lona ou tecido', 'Piso impresso', 'Balcões, totens e letras-caixa', 'Entrega no pavilhão']),
 ('montagem', 'eventos cenografia', 'Montagem no local', 'ai-install', 'A mesma equipe que produz leva e instala.', ['Frota própria', 'Equipe de instalação própria', 'Montagem em eventos, lojas e fachadas']),
 ('varejo', 'varejo', 'Varejo e vitrines', 'ai-vitrine', 'A mesma campanha, igual em todas as lojas.', ['Adesivos de vitrine', 'Materiais de ponto de venda', 'Instalação sob consulta']),
 ('fachadas', 'varejo', 'Fachadas e letras-caixa', 'ai-facade', 'Identidade da marca em ACM e acrílico.', ['Letras-caixa', 'Fachadas em ACM', 'Recepções e ambientes internos']),
 ('pisos', 'eventos feiras', 'Pisos e ambientação', 'ai-floor', 'Smart Floor: o chão como mídia.', ['Piso vinílico impresso', 'Sob medida para o espaço', 'Corredores, palcos e ativações']),
 ('frota', 'frota', 'Envelopamento de frota', 'ai-van', 'Envelopamento de carros, vans e caminhões.', ['Projeto aplicado ao modelo do veículo', 'Impressão e aplicação próprias']),
 ('3d', 'cenografia', 'Cenografia em 3D', 'ai-print3d', 'Peças especiais em impressão 3D.', ['Formas orgânicas e displays', 'Produzidas junto com a parte gráfica']),
 ('terceiros', 'cenografia', 'Produção para agências e cenografia', 'ai-whitelabel', 'Você atende o seu cliente. A gente produz.', ['Parceiro de produção terceirizada', 'Identificação da entrega conversada no orçamento', 'Prazo de produção alinhado à data da montagem']),
]
FAQ = [
 ('Qual o maior tamanho que vocês imprimem sem emenda?', 'Até 5 metros de largura numa peça só, em impressão UV LED.'),
 ('Vocês fazem a instalação?', 'Sim. Temos frota própria e equipe de instalação: levamos até o local e montamos.'),
 ('Vocês atendem agências, produtoras e empresas de cenografia?', 'Sim. Atuamos como parceiro de produção para quem atende o cliente final. A identificação da entrega é conversada no orçamento.'),
 ('Onde vocês atendem?', 'A produção fica em Atibaia, perto de São Paulo. Para entregas e instalações em outras cidades, informe o local no orçamento.'),
 ('Em quais materiais vocês imprimem?', 'Lona, lona backlight, tecido, ACM, PVC expandido, adesivo vinil e piso vinílico. Também fazemos impressão 3D e cortes especiais.'),
 ('Preciso ter a arte pronta?', 'Não. Se tiver a arte, mande junto. Se não, conte a ideia e as medidas: o planejamento faz parte do serviço.'),
 ('Como peço um orçamento?', 'Pela página de orçamento: escolha o perfil e o produto, informe o que já souber e envie pelo WhatsApp ou por e-mail. A mensagem chega pronta para a nossa equipe.'),
 ('Qual o horário de atendimento?', 'Segunda a sexta, das 8h às 18h.'),
]

def ba_before(kind, im, alt):
    base = pic(im, alt, sizes='(max-width:900px) 100vw, 46rem')
    fx = {
      'seam': '<div class="fx fx-seam"><i style="left:22%"></i><i style="left:43%"></i><b style="left:22%">emenda</b><b style="left:43%">emenda</b></div>',
      'tone': '<div class="fx"><div class="fx-patch" style="left:48%;right:0;--f:hue-rotate(38deg) saturate(.65) brightness(.92)"></div><div class="fx-patch" style="left:0;width:22%;--f:saturate(.5) sepia(.35)"></div></div>',
      'dull': '',
      'floor': '<div class="fx"><div class="fx-patch" style="left:0;right:0;top:46%;--f:grayscale(1) brightness(.72) contrast(.85)"></div></div>',
      'tags': '<div class="fx" style="font:700 .7rem/1 var(--body);letter-spacing:.06em">' + ''.join(f'<span style="position:absolute;left:{x}%;top:{y}%;padding:.25rem .45rem;background:#efe6d2;color:#5a4a2a;border:1px solid #c9b88f;border-radius:3px;transform:rotate({r}deg)">ETIQUETA DO FORNECEDOR</span>' for x, y, r in [(14, 52, -6), (30, 62, 4), (22, 74, -3), (69, 48, 5)]) + '</div>',
      'stores': '<div class="fx"><div class="fx-patch" style="left:4%;width:15%;--f:hue-rotate(140deg) saturate(.8)"></div><div class="fx-patch" style="left:22%;width:21%;--f:hue-rotate(-60deg) brightness(.85)"></div></div>',
      'blueprint': '<div class="fx" style="background:repeating-linear-gradient(0deg,rgba(80,170,255,.18) 0 1px,transparent 1px 28px),repeating-linear-gradient(90deg,rgba(80,170,255,.18) 0 1px,transparent 1px 28px)"></div>',
    }[kind]
    style = {'dull': 'filter:grayscale(.75) brightness(.7)', 'blueprint': 'filter:grayscale(1) contrast(1.4) brightness(1.15)'}.get(kind, '')
    if style: base = base.replace('<img ', f'<img style="{style}" ', 1)
    return base + fx

# ------------------------------------------------------------------ pages
XL = [  # id, title, line, img, quote value, alt, theme
 ('lona', 'Lona sem emenda', 'Até 5 metros. Uma peça só.', 'ai-install', 'Lona / backdrop', 'Ilustração gerada por IA: equipe instalando um painel de lona de 5 metros num estande', 'dark'),
 ('smart-floor', 'Smart Floor', 'O chão também comunica.', 'ai-floor', 'Smart Floor', 'Ilustração gerada por IA: piso vinílico impresso em cores atravessando um salão de eventos', 'dark'),
]
GRID = [  # id, title, line, img, href, quote value, theme
 ('cenografia', 'Cenografia e estandes', 'O cenário inteiro, num pedido só.', 'ai-booth', 'solucoes.html#cenografia', 'Estande completo', 'dark'),
 ('letras-caixa', 'Letras-caixa e fachadas', 'A marca em três dimensões.', 'ai-facade', 'solucoes.html#letras-caixa', 'Letra-caixa / fachada', 'dark'),
 ('frota', 'Envelopamento de frota', 'A marca que roda a cidade.', 'ai-van', 'solucoes.html#frota', 'Envelopamento de frota', 'dark'),
 ('vitrines', 'Vitrines e PDV', 'A mesma campanha em todas as lojas.', 'ai-vitrine', 'solucoes.html#vitrines', 'Vitrine / adesivo', 'light'),
 ('impressao-3d', 'Impressão 3D', 'Formas que a impressão plana não faz.', 'ai-print3d', 'solucoes.html#impressao-3d', 'Impressão 3D', 'light'),
 ('materiais', 'Materiais', 'O material certo para cada peça.', 'ai-materials', 'solucoes.html#materiais', 'Outro', 'dark'),
]
def btns(primary, secondary, cta):
    return f'<div class="ctas"><a class="btn btn-fill" href="{primary[0]}" data-cta="{cta}">{primary[1]}</a><a class="btn btn-line" href="{secondary[0]}" data-cta="{cta}-more">{secondary[1]}</a></div>'

def page_home():
    ld = {"@context": "https://schema.org", "@graph": [
      {"@type": "LocalBusiness", "@id": SITE + "#empresa", "name": "Smart Pix Impressão Digital", "url": SITE, "image": SITE + "img/og.jpg", "logo": SITE + "img/logo.png",
       "description": "Gráfica digital especializada em eventos e cenografia: impressão UV LED de grande formato até 5 m sem emenda, Smart Floor, letras-caixa, vitrines, envelopamento de frota e impressão 3D, com frota e instalação próprias.",
       "telephone": "+55-11-91010-1324", "email": "atendimento@smartpix.com.br",
       "address": {"@type": "PostalAddress", "streetAddress": "Av. São Paulo, 111 - Alvinópolis", "addressLocality": "Atibaia", "addressRegion": "SP", "addressCountry": "BR"},
       "areaServed": {"@type": "City", "name": "Atibaia"}, "taxID": "05.801.627/0001-65",
       "hasMap": "https://www.google.com/maps/search/?api=1&query=Av.+S%C3%A3o+Paulo%2C+111%2C+Alvin%C3%B3polis%2C+Atibaia+SP",
       "openingHoursSpecification": [{"@type": "OpeningHoursSpecification", "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"], "opens": "08:00", "closes": "18:00"}],
       "sameAs": ["https://www.instagram.com/smartpixoficial/"],
       "knowsAbout": ["Impressão digital UV LED", "Cenografia para eventos", "Lona sem emenda 5 metros", "Piso vinílico impresso", "Letras-caixa", "Envelopamento de frota", "Impressão 3D"]},
      {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in FAQ]}]}
    h = head('Smart Pix | Impressão digital e cenografia em Atibaia, SP', 'Smart Pix Impressão Digital: grande formato em Atibaia, SP. Lona até 5 m sem emenda, cenografia, letras-caixa, Smart Floor e envelopamento de frota, com instalação própria.', '', ld, 'index') + nav('./')
    sw = [('#bde000', 'Lima'), ('#1f6bff', 'Azul'), ('#e5322d', 'Vermelho'), ('#ff7a00', 'Laranja'), ('#7b3fe4', 'Roxo'), ('#f2f2f2', 'Branco')]
    swatches = ''.join(f'<button type="button" class="swatch" role="radio" data-c="{c}" title="{n}" aria-label="{n}" aria-checked="{str(i == 0).lower()}" tabindex="{0 if i == 0 else -1}" style="--c:{c}"><i></i></button>' for i, (c, n) in enumerate(sw))
    hero = f'''
<section class="hero dark" aria-labelledby="h-hero">
  <div class="wrap hero-copy">
    <svg class="hero-mark" aria-hidden="true"><use href="#sp-logo"/></svg>
    <h1 id="h-hero" class="hero-title">Smart Pix</h1>
    <p class="hero-sub">Impressão digital em grande formato.</p>
    <p class="hero-note">Para eventos, cenografia e empresas. Em Atibaia, SP.</p>
    {btns(('orcamento.html', 'Pedir orçamento'), ('solucoes.html', 'Ver soluções'), 'hero')}
  </div>
  <figure class="hero-img">{pic('ai-stage', 'Ilustração gerada por IA: palco com painel de lona impressa em verde-limão e preto, sem emenda', lazy=False, sizes='100vw')}<figcaption class="tag">{AI}</figcaption></figure>
  <ul class="wrap hl" aria-label="Destaques">
    <li><b>5 m</b><span>de largura sem emenda</span></li>
    <li><b>UV LED</b><span>tinta curada na hora</span></li>
    <li><b>Frota própria</b><span>entrega e instalação</span></li>
    <li><b>Atibaia, SP</b><span>produção própria</span></li>
  </ul>
</section>'''
    xl = ''.join(f'''
<section class="tile tile-xl {t}" id="t-{i}" aria-labelledby="h-t-{i}">
  <div class="tile-copy"><h2 id="h-t-{i}" class="tile-title">{a}</h2><p class="tile-sub">{b}</p>{btns((q(v), 'Orçar'), ('solucoes.html#' + i, 'Saiba mais'), 'tile-' + i)}</div>
  <div class="tile-img">{pic(im, alt, sizes='100vw')}</div><span class="tag">{AI}</span>
</section>''' for i, a, b, im, v, alt, t in XL)
    grid = ''.join(f'''<div class="tile {t}" role="group" aria-labelledby="h-g-{i}">
    <div class="tile-copy"><h2 id="h-g-{i}" class="tile-title">{a}</h2><p class="tile-sub">{b}</p>{btns((q(v), 'Orçar'), (href, 'Saiba mais'), 'grid-' + i)}</div>
    <div class="tile-img">{pic(im, '', sizes='(max-width:734px) 100vw, 50vw')}</div><span class="tag">{AI}</span>
  </div>''' for i, a, b, im, href, v, t in GRID)
    tiles = f'<section class="tiles" aria-label="Soluções">{grid}</section>'
    who = f'''
<section class="sec" id="para-quem" aria-labelledby="h-who">
  <div class="wrap">
    <div class="sec-head center">{kicker('para quem')}<h2 id="h-who" class="h1">Feito para quem produz.</h2></div>
    <div class="who">
      <a class="who-i" href="cenografia.html" data-cta="who-ceno"><h3>Cenografia e montadoras</h3><p>Sua equipe projeta e monta. A gente produz toda a parte gráfica e entrega no pavilhão.</p><span class="more">Como trabalhamos juntos</span></a>
      <a class="who-i" href="cenografia.html#agencias" data-cta="who-ag"><h3>Agências e produtoras</h3><p>Produção terceirizada para os seus clientes: a gente produz, você entrega o projeto.</p><span class="more">Produzir com a gente</span></a>
      <a class="who-i" href="orcamento.html?perfil=Empresa" data-cta="who-emp"><h3>Empresas</h3><p>Eventos, lojas, fachada e frota com um fornecedor só, do arquivo à instalação.</p><span class="more">Pedir orçamento</span></a>
    </div>
  </div>
</section>'''
    studio = f'''
<section class="sec dark studio-sec" id="estudio" aria-labelledby="h-studio">
  <div class="wrap sec-head center">{kicker('estúdio 3D')}<h2 id="h-studio" class="h1">Veja a sua marca num estande.</h2><p class="lead">Digite o nome, escolha a cor e gire. Depois, é só orçar.</p></div>
  <div class="studio" id="studio">
    <div class="studio-stage" role="group" aria-label="Visualizador 3D do estande">
      <div class="studio-3d" role="img" aria-label="Estande com a sua marca: lona de 5 por 3 metros, piso Smart Floor, balcão, totem e letra-caixa.">{pic('ai-booth', '', cls='fallback')}<canvas id="studioCanvas" aria-hidden="true"></canvas></div>
      <div class="studio-labels" aria-hidden="true"><span data-part="lona">Lona 5 × 3 m</span><span data-part="piso">Smart Floor</span><span data-part="balcao">Balcão</span><span data-part="totem">Totem</span><span data-part="letra">Letra-caixa</span></div>
      <div class="studio-views" role="group" aria-label="Vista do estande"><button type="button" data-view="50" aria-pressed="false">Lateral</button><button type="button" data-view="25" aria-pressed="true">3/4</button><button type="button" data-view="0" aria-pressed="false">Frente</button></div>
    </div>
    <div class="wrap">
      <div class="studio-panel" role="group" aria-label="Monte seu estande">
        <div class="studio-field"><label for="brandName">Sua marca</label><input id="brandName" type="text" maxlength="22" autocomplete="organization" placeholder="Digite o nome" enterkeyhint="done"></div>
        <div class="studio-field"><label id="lblColor">Cor</label><div class="swatches" role="radiogroup" aria-labelledby="lblColor">{swatches}</div></div>
        <a class="btn btn-fill" id="studioQuote" href="orcamento.html?produto=Estande%20completo" data-cta="studio">Orçar este estande</a>
      </div>
      <p class="studio-out" id="studioOut"></p><p class="sr" id="studioLive" aria-live="polite"></p>
    </div>
  </div>
</section>'''
    about = f'''
<section class="sec" id="quem-somos" aria-labelledby="h-about">
  <div class="wrap">
    <div class="sec-head center">{kicker('quem somos')}<h2 id="h-about" class="h1">Do arquivo ao palco.</h2><p class="lead">A Smart Pix planeja, imprime, produz e instala. Com equipe e frota próprias, a partir do nosso galpão em Atibaia.</p></div>
    <div class="photo-duo">
      <figure class="photo"><img src="img/real-fabrica-1440.webp" srcset="img/real-fabrica-800.webp 800w, img/real-fabrica-1440.webp 1440w" sizes="(max-width:734px) 100vw, 36rem" alt="Galpão de produção da Smart Pix em Atibaia, com impressoras de grande formato e uma lona impressa estendida no chão" width="1440" height="1440" loading="lazy" decoding="async" style="object-position:50% 62%"><figcaption class="tag">Foto real · galpão em Atibaia</figcaption></figure>
      <figure class="photo"><img src="img/real-impressora-1000.webp" alt="Impressora UV LED da Smart Pix, com a marca smart PIX no carro de impressão" width="1000" height="460" loading="lazy" decoding="async"><figcaption class="tag">Foto real · impressão UV LED</figcaption></figure>
    </div>
    <ol class="steps">
      <li><span class="n">01</span><h3>Planejamento</h3><p>Você manda a ideia, as medidas e a data. A gente indica o material de cada peça.</p></li>
      <li><span class="n">02</span><h3>Impressão UV LED</h3><p>Grande formato, até 5 m sem emenda, na nossa produção.</p></li>
      <li><span class="n">03</span><h3>Acabamento</h3><p>Corte, montagem das peças e impressão 3D quando o projeto pede.</p></li>
      <li><span class="n">04</span><h3>Entrega e instalação</h3><p>Frota e equipe próprias levam e montam no local.</p></li>
    </ol>
  </div>
</section>'''
    tablist = ''.join(f'<li role="presentation"><button type="button" role="tab" id="t-{p[0]}" aria-controls="p-{p[0]}" aria-selected="{str(i == 0).lower()}" tabindex="{0 if i == 0 else -1}"><i aria-hidden="true">{i + 1:02d}</i>{p[1]}</button></li>' for i, p in enumerate(PROBLEMS))
    panels = ''
    for i, p in enumerate(PROBLEMS):
        slug, title, bimg, kind, aimg, prob, sol, prod = p
        qq = f'orcamento.html?origem=problema&amp;produto={e(prod).replace(" ", "%20").replace("/", "%2F")}&amp;problema={e(title).replace(" ", "%20")}'
        panels += f'''<div class="px-view" role="tabpanel" id="p-{slug}" aria-labelledby="t-{slug}"{' hidden' if i else ''}>
  <div class="ba" style="--x:50%">
    {pic(aimg, 'Ilustração gerada por IA. Com a Smart Pix: ' + sol, sizes='(max-width:900px) 100vw, 46rem')}
    <div class="before" aria-hidden="true">{ba_before(kind, bimg, '')}</div>
    <span class="badge-b">Antes</span><span class="badge-a">Com a Smart Pix</span>
    <button type="button" class="handle" role="slider" aria-label="Comparar antes e depois" aria-valuemin="0" aria-valuemax="100" aria-valuenow="50"><span><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M9 6l-6 6 6 6M15 6l6 6-6 6"/></svg></span></button>
    <span class="ai">{AI}</span>
  </div>
  <h3 class="sr">{title}</h3>
  <div class="px-text"><div><p class="lbl">O problema</p><p>{prob}</p></div><div class="sol"><p class="lbl">Como resolvemos</p><p>{sol}</p></div></div>
  <div class="px-foot"><p class="caption">Arraste a divisória para comparar.</p><a class="btn btn-fill" href="{qq}" data-cta="problem-{slug}">Resolver no meu projeto</a></div>
</div>'''
    problemas = f'''
<section class="sec dark" id="problemas" aria-labelledby="h-px">
  <div class="wrap">
    <div class="sec-head center">{kicker('problemas que resolvemos')}<h2 id="h-px" class="h1">Já passou por isso?</h2><p class="lead">Escolha um problema e arraste para ver o que muda com a Smart Pix.</p></div>
    <div class="px" id="px"><ul class="px-list" role="tablist" aria-label="Problemas">{tablist}</ul><div>{panels}</div></div>
  </div>
</section>'''
    faq = ''.join(f'<details><summary>{qq}<i aria-hidden="true"></i></summary><p>{a}</p></details>' for qq, a in FAQ)
    end = f'''
<section class="sec" id="duvidas" aria-labelledby="h-faq">
  <div class="wrap narrow"><div class="sec-head center">{kicker('dúvidas')}<h2 id="h-faq" class="h1">Antes de pedir.</h2></div><div class="faq">{faq}</div></div>
</section>
<section class="sec gray cta-end" aria-labelledby="h-cta">
  <div class="wrap center"><h2 id="h-cta" class="h1">Qual é o seu próximo projeto?</h2><p class="lead">Conte o que precisa. A mensagem chega pronta no nosso WhatsApp.</p>
    <div class="ctas"><a class="btn btn-fill" href="orcamento.html" data-cta="final">Pedir orçamento</a><a class="btn btn-line" href="https://wa.me/{WA_NUM}" data-wa="Olá, Smart Pix! Vim pelo site e quero falar sobre um projeto." data-cta="final-wa">Falar no WhatsApp</a></div>
  </div>
</section>'''
    return h + hero + xl + tiles + who + studio + about + problemas + end + foot(('studio.js', 'problems.js'))

def page_solucoes():
    h = head('Lona sem emenda, letra-caixa, frota e impressão 3D | Smart Pix', 'Lona e backdrop até 5 m sem emenda, Smart Floor, estandes, letras-caixa, vitrines, envelopamento de frota e impressão 3D. Produção UV LED em Atibaia, SP.', 'solucoes.html', crumbs('solucoes.html', 'Soluções'), 'solucoes') + nav('solucoes.html')
    sub = ''.join(f'<li><a href="#{p[0]}">{p[1]}</a></li>' for p in PRODUCTS)
    sec = ''
    for n, p in enumerate(PRODUCTS):
        pid, name, val, im, kick, title, lead, bul = p
        lis = ''.join(f'<li>{b}</li>' for b in bul)
        cta, wtxt = CTA[pid]
        sec += f'''
<section class="sec prod{' gray' if n % 2 else ''}" id="{pid}" aria-labelledby="h-{pid}">
  <div class="wrap">
    <div class="sec-head center">{kicker(name)}<h2 id="h-{pid}" class="h1">{title}</h2><p class="lead">{lead}</p>
      <div class="ctas"><a class="btn btn-fill" href="{q(val)}" data-cta="sol-{pid}">{cta}</a><a class="btn btn-line" href="https://wa.me/{WA_NUM}" data-wa="Olá, Smart Pix! Quero saber mais sobre {wtxt}." data-cta="sol-wa-{pid}">Tirar dúvida</a></div></div>
    <figure class="prod-img">{pic(im, 'Ilustração gerada por IA: ' + name, sizes='(max-width:1068px) 100vw, 67rem')}<figcaption class="tag">{AI}</figcaption></figure>
    <ul class="specs">{lis}</ul>
  </div>
</section>'''
    body = f'''
<section class="phero" aria-labelledby="h-page"><div class="wrap center"><h1 id="h-page" class="page-title">Soluções</h1><p class="page-sub">Cada peça no material certo. Produzida em Atibaia e instalada pela nossa equipe.</p></div></section>
<nav class="subnav" aria-label="Soluções"><div class="wrap"><ul id="subnav">{sub}</ul></div></nav>
{sec}
<section class="sec cta-end" aria-labelledby="h-cta"><div class="wrap center"><h2 id="h-cta" class="h1">Não achou o que procura?</h2><p class="lead">Conte o projeto. A gente indica o material.</p><div class="ctas"><a class="btn btn-fill" href="orcamento.html" data-cta="sol-final">Pedir orçamento</a><a class="btn btn-line" href="https://wa.me/{WA_NUM}" data-wa="Olá, Smart Pix! Tenho um projeto e quero indicação de material." data-cta="sol-final-wa">Falar no WhatsApp</a></div></div></section>
<script>
(function(){{var links=[].slice.call(document.querySelectorAll('#subnav a'));if(!('IntersectionObserver' in window))return;var io=new IntersectionObserver(function(es){{es.forEach(function(e){{if(e.isIntersecting){{links.forEach(function(a){{var on=a.getAttribute('href')==='#'+e.target.id;a.classList.toggle('on',on);if(on){{var u=a.parentNode.parentNode;u.scrollTo({{left:a.offsetLeft-u.offsetLeft-16,behavior:matchMedia('(prefers-reduced-motion: reduce)').matches?'auto':'smooth'}});}}}});}}}});}},{{rootMargin:'-45% 0px -50% 0px'}});document.querySelectorAll('.prod').forEach(function(s){{io.observe(s);}});}})();
</script>'''
    return h + body + foot()

def page_cenografia():
    h = head('Produção gráfica para cenografia e montadoras | Smart Pix', 'Parceiro de produção para empresas de cenografia, montadoras e agências: lona até 5 m sem emenda, piso, ACM e 3D num pedido só, com entrega no pavilhão.', 'cenografia.html', crumbs('cenografia.html', 'Para cenografia'), 'cenografia') + nav('cenografia.html')
    feats = [('Até 5 m sem emenda', 'Painéis grandes numa peça só, em UV LED.'), ('Um pedido só', 'Lona, tecido, piso, ACM, PVC, adesivo e impressão 3D com um responsável.'), ('Entrega no pavilhão', 'A frota própria leva o material até o local da montagem.'),
             ('Montagem ou só entrega', 'A nossa equipe instala, ou entrega para a sua equipe montar.'), ('Você fala com o seu cliente', 'A identificação da entrega é conversada no orçamento.'), ('Perto de São Paulo', 'Produção no nosso galpão em Atibaia.')]
    fh = ''.join(f'<div class="feat"><h3>{a}</h3><p>{b}</p></div>' for a, b in feats)
    steps = [('Você envia o projeto', 'Medidas, materiais, local e a janela de montagem.'), ('Orçamento', 'Com o prazo de produção alinhado à data do evento.'), ('Produção', 'Impressão UV LED e acabamento na nossa produção.'), ('Entrega ou montagem', 'No pavilhão, pela nossa frota e, se quiser, pela nossa equipe.')]
    sh = ''.join(f'<li><span class="n">{i + 1:02d}</span><h3>{a}</h3><p>{b}</p></li>' for i, (a, b) in enumerate(steps))
    body = f'''
<section class="phero" aria-labelledby="h-page"><div class="wrap center">{kicker('para cenografia e agências')}<h1 id="h-page" class="page-title">Sua produção,<br>nossa fábrica.</h1><p class="page-sub">Para quem projeta e monta estandes, palcos e ativações e precisa de uma produção gráfica que respeite a janela do pavilhão.</p>
  <div class="ctas"><a class="btn btn-fill" href="orcamento.html?perfil=Cenografia%20%2F%20montadora" data-cta="ceno-hero">Orçar um projeto</a><a class="btn btn-line" href="https://wa.me/{WA_NUM}" data-wa="Olá, Smart Pix! Sou de uma empresa de cenografia ou montadora e quero conversar sobre produção." data-cta="ceno-hero-wa">Falar como parceiro</a></div></div>
  <div class="wrap wide"><figure class="photo page-img"><img src="img/real-fabrica-1440.webp" srcset="img/real-fabrica-800.webp 800w, img/real-fabrica-1440.webp 1440w" sizes="(max-width:1068px) 100vw, 67rem" alt="Galpão de produção da Smart Pix em Atibaia, com impressoras de grande formato e uma lona impressa estendida no chão" width="1440" height="1440" fetchpriority="high" style="object-position:50% 60%"><figcaption class="tag">Foto real · nosso galpão em Atibaia</figcaption></figure></div></section>
<section class="sec gray" aria-labelledby="h-why"><div class="wrap"><div class="sec-head center">{kicker('por que terceirizar com a gente')}<h2 id="h-why" class="h1">O prazo da montagem vem primeiro.</h2><p class="lead">O atraso que mais custa é o que acontece no pavilhão. Por isso, a mesma empresa produz, entrega e instala.</p></div><div class="feats">{fh}</div></div></section>
<section class="sec dark" id="agencias" aria-labelledby="h-ag"><div class="wrap"><div class="sec-head center">{kicker('agências · produtoras')}<h2 id="h-ag" class="h1">Você atende o cliente.<br>A gente produz.</h2><p class="lead">Atuamos como parceiro de produção para agências e produtoras que precisam entregar sem montar uma gráfica.</p>
  <div class="ctas"><a class="btn btn-fill" href="orcamento.html?perfil=Ag%C3%AAncia%20%2F%20produtora" data-cta="ag">Orçar como agência</a></div></div>
  <figure class="prod-img">{pic('ai-whitelabel', 'Ilustração gerada por IA: rolos de lona embalados em papel kraft, sem identificação, ao lado de uma van branca', sizes='(max-width:1068px) 100vw, 67rem')}<figcaption class="tag">{AI}</figcaption></figure>
  <ul class="specs"><li>Um responsável do pedido à entrega</li><li>Identificação da entrega conversada no orçamento</li><li>Prazo de produção alinhado à data do evento</li></ul></div></section>
<section class="sec" aria-labelledby="h-how"><div class="wrap"><div class="sec-head center">{kicker('como funciona a parceria')}<h2 id="h-how" class="h1">Quatro passos, um responsável.</h2></div><ol class="steps">{sh}</ol>
  <figure class="prod-img" style="margin-top:var(--s8)">{pic('ai-install', 'Ilustração gerada por IA: equipe instalando um painel de 5 metros num estande, com uma van ao lado', sizes='(max-width:1068px) 100vw, 67rem')}<figcaption class="tag">{AI}</figcaption></figure></div></section>
<section class="sec gray" aria-labelledby="h-brief"><div class="wrap narrow"><div class="sec-head center">{kicker('para orçar mais rápido')}<h2 id="h-brief" class="h1">O que mandar no primeiro contato.</h2></div>
  <ul class="checks"><li>Medidas finais de cada peça</li><li>Material desejado, ou o uso da peça: dentro ou fora, com luz ou sem</li><li>Data, horário e local da montagem</li><li>Quantidade</li><li>Arte em alta resolução, se já tiver</li><li>Se precisa de instalação</li></ul>
  <div class="ctas center"><a class="btn btn-fill" href="orcamento.html?perfil=Cenografia%20%2F%20montadora" data-cta="ceno-brief">Montar o pedido</a></div></div></section>'''
    return h + body + foot()

def page_projetos():
    ld = {"@context": "https://schema.org", "@graph": [crumbs('projetos.html', 'Projetos'), {"@type": "ItemList", "name": "Tipos de projeto da Smart Pix", "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": p[2], "url": SITE + 'projetos.html#' + p[0]} for i, p in enumerate(PROJECTS)]}]}
    h = head('Projetos de eventos, feiras, vitrines e frota | Smart Pix', 'Tipos de projeto que a Smart Pix produz e instala a partir de Atibaia: convenções, feiras e estandes, vitrines, fachadas e letras-caixa, pisos e frota.', 'projetos.html', ld, 'projetos') + nav('projetos.html')
    chips = ''.join(f'<button type="button" class="chip" data-filter="{f}" aria-pressed="{str(f == "todos").lower()}">{t}</button>' for f, t in [('todos', 'Todos'), ('eventos', 'Eventos'), ('feiras', 'Feiras'), ('cenografia', 'Cenografia'), ('varejo', 'Varejo'), ('frota', 'Frota')])
    cards = ''
    for pid, cat, title, im, line, bul in PROJECTS:
        lis = ''.join(f'<li>{b}</li>' for b in bul)
        qp = PROJ_Q[pid].replace(' ', '%20').replace('/', '%2F')
        detail = f'<div class="pd-img">{pic(im, "Ilustração gerada por IA: " + title, sizes="46rem")}<span class="tag">{AI}</span></div><div class="pd-body">{kicker("tipo de projeto")}<h2 class="h2">{title}</h2><p class="lead">{line}</p><ul class="specs">{lis}</ul><div class="ctas"><a class="btn btn-fill" href="orcamento.html?origem=projetos&amp;produto={qp}" data-cta="pd-{pid}">Orçar um projeto assim</a></div></div>'
        cards += f'<article class="card" id="{pid}" data-id="{pid}" data-cat="{cat}"><div class="card-img">{pic(im, "", sizes="(max-width:734px) 100vw, (max-width:1068px) 50vw, 22rem")}<span class="tag">{AI}</span></div><div class="card-body"><h2 class="card-t">{title}</h2><p>{line}</p><button type="button" class="card-open" aria-haspopup="dialog">Ver o que entregamos<span class="sr"> em {title.lower()}</span></button></div><div class="card-detail" hidden>{detail}</div></article>'
    body = f'''
<section class="phero" aria-labelledby="h-page"><div class="wrap center"><h1 id="h-page" class="page-title">Projetos</h1><p class="page-sub">Do palco à frota: os tipos de projeto que produzimos e instalamos.</p></div></section>
<section class="sec" aria-label="Tipos de projeto" style="padding-top:0"><div class="wrap">
  <div class="pbar"><div class="chips" role="group" aria-label="Filtrar por tipo">{chips}</div><p class="caption" id="pcount" aria-live="polite">{len(PROJECTS)} tipos de projeto</p></div>
  <div class="pgrid" id="pgrid">{cards}</div>
  <p class="notice">Por respeito aos nossos clientes, não mostramos marcas de terceiros. As imagens desta página são ilustrações geradas por IA de cada tipo de projeto.</p>
</div></section>
<dialog class="pd" id="pd" aria-labelledby="pd-title"><span class="pd-grab" aria-hidden="true"></span><button type="button" class="pd-close" data-close aria-label="Fechar"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" aria-hidden="true"><path d="M6 6l12 12M18 6L6 18"/></svg></button><div class="pd-content"></div></dialog>'''
    return h + body + foot(('projects.js',))

def page_orcamento():
    h = head('Orçamento de impressão grande formato | Smart Pix Atibaia', 'Peça orçamento de lona, piso, letra-caixa, estande ou envelopamento: informe medidas, data e local e envie pelo WhatsApp ou e-mail. Seg a sex, 8h às 18h.', 'orcamento.html', {'@context': 'https://schema.org', '@graph': [crumbs('orcamento.html', 'Orçamento'), {'@type': 'ContactPage', 'name': 'Orçamento Smart Pix', 'url': SITE + 'orcamento.html'}]}, 'orcamento') + nav('orcamento.html')
    prods = ['Estande completo', 'Lona / backdrop', 'Smart Floor', 'Tecido', 'Letra-caixa / fachada', 'Vitrine / adesivo', 'Envelopamento de frota', 'Impressão 3D', 'Outro']
    po = ''.join(f'<label class="opt"><input type="checkbox" name="produto" value="{p}"><span>{p}</span></label>' for p in prods)
    perf = ''.join(f'<label class="opt"><input type="radio" name="perfil" value="{p}"><span>{p}</span></label>' for p in ['Cenografia / montadora', 'Agência / produtora', 'Empresa'])
    def rad(name, opts): return ''.join(f'<label class="opt"><input type="radio" name="{name}" value="{o}"><span>{o}</span></label>' for o in opts)
    def stp(n, lbl, unit, d, v):
        unit_sr = 'unidades' if n == 'q' else 'metros'
        return f'<div class="f"><label for="q-{n}">{lbl} <span class="sr">({unit_sr})</span></label><div class="stepper"><button type="button" data-step="{n}" data-d="-{d}" aria-label="Diminuir {lbl.lower()}">−</button><input id="q-{n}" name="{n}" type="number" inputmode="{'numeric' if n == 'q' else 'decimal'}" min="{1 if n == 'q' else 0}" step="{1 if n == 'q' else 0.1}" value="{v}"><em aria-hidden="true">{unit}</em><button type="button" data-step="{n}" data-d="{d}" aria-label="Aumentar {lbl.lower()}">+</button></div></div>'
    body = f'''
<section class="phero" aria-labelledby="h-page"><div class="wrap center"><h1 id="h-page" class="page-title">Orçamento</h1><p class="page-sub">Conte o que precisa. A primeira etapa leva menos de um minuto.</p></div></section>
<section class="sec" style="padding-top:0" aria-label="Formulário de orçamento"><div class="wrap">
  <form class="q" id="qform" novalidate>
    <div class="q-panel">
      <div class="q-prog" aria-hidden="true"><p id="stTxt">Etapa 1 de 2 · O essencial</p><div class="q-bar"><i id="st2"></i></div></div>
      <fieldset aria-describedby="err1"><legend>Você é <small>obrigatório</small></legend><div class="opts">{perf}</div></fieldset>
      <fieldset aria-describedby="err1"><legend>O que você precisa? <small>obrigatório · pode marcar mais de um</small></legend><div class="opts">{po}</div></fieldset>
      <fieldset><legend>Seus dados</legend><div class="grid2"><div class="f"><label for="q-nome">Nome <span>(obrigatório)</span></label><input id="q-nome" name="nome" type="text" autocomplete="name" required aria-required="true" aria-describedby="err1"></div><div class="f"><label for="q-empresa">Empresa <span>(opcional)</span></label><input id="q-empresa" name="empresa" type="text" autocomplete="organization"></div></div></fieldset>
      <p class="err" id="err1" role="alert"></p>
      <div class="q-nav"><button type="button" class="btn btn-line" id="goStep2" data-cta="quote-step2">Adicionar detalhes</button><p class="hint" style="margin:0">Ou envie agora pelo resumo.</p></div>
      <div id="step2" hidden tabindex="-1" aria-labelledby="h-step2"><h2 class="sr" id="h-step2">Etapa 2 de 2: detalhes</h2>
        <fieldset><legend>Peça principal <small>se já souber</small></legend><div class="grid3">{stp('w', 'Largura', 'm', '0.5', '')}{stp('h', 'Altura', 'm', '0.5', '')}{stp('q', 'Quantidade', 'un.', '1', '1')}</div></fieldset>
        <fieldset><legend>Quando e onde</legend><div class="grid2"><div class="f"><label for="q-data">Data do evento ou da entrega</label><input id="q-data" name="data" type="date"></div><div class="f"><label for="q-local">Cidade e local <span>(opcional)</span></label><input id="q-local" name="local" type="text" autocomplete="address-level2" placeholder="Ex.: São Paulo, SP"></div></div>
          <fieldset class="sub"><legend class="lbl">Instalação</legend><div class="opts">{rad('inst', ['Com instalação', 'Só a produção', 'Não sei ainda'])}</div></fieldset>
          <fieldset class="sub"><legend class="lbl">Arte</legend><div class="opts">{rad('arte', ['Tenho a arte pronta', 'Preciso de ajuda com a arte'])}</div></fieldset></fieldset>
        <fieldset><legend>Algo mais?</legend><div class="f"><label for="q-detalhe">Detalhes <span>(opcional)</span></label><textarea id="q-detalhe" name="detalhe" placeholder="Ex.: dois backdrops, piso para o palco e montagem na véspera do evento"></textarea></div>
          <fieldset class="sub"><legend class="lbl">Como nos conheceu? <span>(opcional)</span></legend><div class="opts">{rad('origem', ['Google', 'Instagram', 'Indicação', 'Já sou cliente'])}</div></fieldset></fieldset>
        <p class="hint">Tem a arte? Depois de enviar, mande o arquivo pelo próprio WhatsApp ou para atendimento@smartpix.com.br.</p>
      </div>
    </div>
    <div class="sum" id="resumo" role="region" aria-labelledby="h-sum">
      <div class="sum-head"><b id="h-sum">Resumo do pedido</b></div>
      <div class="sum-body">
        <dl id="sumList"></dl><p class="sr" id="sumLive" aria-live="polite"></p>
        <div style="display:flex;justify-content:space-between;align-items:baseline;border-top:1px solid var(--line);padding-top:.875rem"><span class="small" style="color:var(--ink-muted)">Área total</span><b id="sumArea" class="num sum-area empty">a definir</b></div>
        <p class="badge" id="seam" hidden></p>
        <p class="badge warn" id="urgent" hidden>Evento próximo: envie o pedido o quanto antes para confirmarmos o prazo.</p>
        <p class="badge warn" id="past" hidden>Essa data já passou. Confira o dia do evento.</p>
        <p class="err" id="errS" role="alert"></p>
        <div class="sent" id="sent" role="status" hidden><p><b>Pedido aberto no WhatsApp.</b> Não abriu? Copie a mensagem e envie para (11) 91010-1324.</p><button type="button" class="btn btn-line btn-sm" id="copyMsg">Copiar mensagem</button></div>
        <a class="btn btn-fill" id="sendWa" href="https://wa.me/{WA_NUM}" target="_blank" rel="noopener" data-cta="quote-wa">Enviar pelo WhatsApp</a>
        <a class="btn btn-line" id="sendMail" href="mailto:atendimento@smartpix.com.br" data-cta="quote-mail" style="min-height:3rem">Enviar por e-mail</a>
        <small>Seg a sex, 8h às 18h · A mensagem abre pronta no seu aplicativo</small>
      </div>
    </div>
  </form>
  <div class="contacts">
    <div><b>Telefone</b><a class="contact-v" href="tel:+551124273880">(11) 2427-3880</a><button type="button" class="copy" data-copy="(11) 2427-3880">Copiar número</button></div>
    <div><b>E-mail, para mandar a arte</b><a class="contact-v" href="mailto:atendimento@smartpix.com.br">atendimento@smartpix.com.br</a><button type="button" class="copy" data-copy="atendimento@smartpix.com.br">Copiar e-mail</button></div>
    <div><b>Produção</b><span>Av. São Paulo, 111 · Alvinópolis · Atibaia, SP</span><a class="link" href="https://www.google.com/maps/search/?api=1&amp;query=Av.+S%C3%A3o+Paulo%2C+111%2C+Alvin%C3%B3polis%2C+Atibaia+SP" target="_blank" rel="noopener">Como chegar ›</a></div>
  </div>
</div></section>'''
    return h + body + foot(('quote.js',))

PAGES = {'index.html': page_home, 'solucoes.html': page_solucoes, 'cenografia.html': page_cenografia, 'projetos.html': page_projetos, 'orcamento.html': page_orcamento}
if __name__ == '__main__':
    for fn, f in PAGES.items():
        open(os.path.join(HERE, fn), 'w').write(f())
    print('built', list(PAGES))
