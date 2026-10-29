#!/usr/bin/env python3
"""Verificador do site Smart Pix. Só biblioteca padrão do Python 3.

Uso (na raiz do repositório):
    python3 site/build.py                      # gera os .html
    python3 scripts/verificar_site.py          # confere site/
    python3 scripts/verificar_site.py _site    # confere a pasta publicada (montada por scripts/montar_publicacao.sh)
    INDEXAR=1 python3 scripts/verificar_site.py

Lê as mesmas variáveis do build: SITE_URL, INDEXAR e GTM_ID (vazia = não definida).
Código de saída: 0 sem erros, 1 com erros, 2 se a pasta não existe ou não tem .html.

O que confere em cada .html da raiz da pasta:
  1. Links internos (<a>, <link>, <area>, <form action>, <use>) apontam para um arquivo que existe,
     e a âncora (#id) existe na página de destino.
  2. Todo arquivo referenciado existe: src, srcset, imagesrcset, poster, og:image, twitter:image,
     url() do CSS (inline e de todos os .css da pasta) e caminhos 'img/…', 'js/…', 'css/…', 'fonts/…'
     escritos nos .js (menos js/vendor/, que é de terceiros) e nos <script> inline.
     Caminho começando com "/" é erro (no GitHub Pages de projeto ele sai do site).
  3. IDs duplicados (só o atributo id; data-id não conta) e referências por ID (for, aria-labelledby,
     aria-describedby, aria-controls, aria-owns, list, form) que apontam para nada. Um id que aparece
     entre aspas num .js conta como criado pelo script.
  4. Exatamente um <h1> por página.
  5. <title> com até 65 caracteres e <meta name="description"> com até 160.
  6. Todo <img> tem alt (vazio vale, para imagem decorativa).
  7. Selo das imagens: img/ai-* precisa da etiqueta "Ilustração IA" e img/real-* da etiqueta
     "Foto real" no mesmo bloco (heurística abaixo).
  8. JSON-LD (<script type="application/ld+json">) é JSON válido.
  9. Com INDEXAR=1, nenhuma página além da 404 tem noindex, e o robots.txt não bloqueia o site.
 10. sitemap.xml, robots.txt e llms.txt só apontam para páginas e âncoras que existem;
     o sitemap não lista a 404.
 11. Variáveis do build: com SITE_URL definida, o canonical da Home é ela; com GTM_ID definida,
     toda página carrega o GTM.
 12. Na pasta publicada (qualquer pasta sem build.py): não há build.py, llms.src.txt nem logo_paths.svg.

Heurística do selo (item 7). As etiquetas são texto visível (span/figcaption com "Ilustração IA" ou
"Foto real"), não o alt. Para cada imagem, o verificador sobe pelos ancestrais, do pai para cima, e em
cada um conta quantas imagens daquele tipo e quantas etiquetas existem dentro dele. A imagem passa no
primeiro ancestral em que há pelo menos uma etiqueta para cada imagem. A subida para no primeiro
"bloco": as tags figure, article, section, li, dialog, aside, header, footer, main e body, ou as classes
.tile, .pc, .card, .card-img, .pd-img e .studio-stage. Assim a etiqueta pode ser filha da figure ou
irmã do wrapper da imagem (.tile-img, .pc-img, .studio-3d), mas não pode vir de outro cartão nem da
nota do rodapé. Um <picture> conta como uma imagem, e imagens irmãs no mesmo wrapper (o par
antes/depois de .pc-img, que ocupa um quadro só) também. Limite: se um bloco tem duas imagens IA em
quadros diferentes e duas etiquetas, mas as duas ficam junto da mesma imagem, a heurística não percebe.
Imagem IA usada só pelo CSS ou pelo JS vira aviso, para conferir à mão.
"""
import argparse
import json
import os
import posixpath
import re
import sys
from html.parser import HTMLParser
from urllib.parse import unquote, urlsplit

RAIZ_REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

TITULO_MAX = 65
DESCRICAO_MAX = 160
SELOS = (('ai', 'Ilustração IA'), ('real', 'Foto real'))
NAO_PUBLICAR = ('build.py', 'llms.src.txt', 'logo_paths.svg')
PAGINA_SEM_INDEX = '404.html'

VAZIAS = {'area', 'base', 'br', 'col', 'embed', 'hr', 'img', 'input', 'link', 'meta', 'param',
          'source', 'track', 'wbr'}
BLOCO_TAGS = {'figure', 'article', 'section', 'li', 'dialog', 'aside', 'header', 'footer', 'main',
              'body', 'html', '#documento'}
BLOCO_CLASSES = {'tile', 'pc', 'card', 'card-img', 'pd-img', 'studio-stage'}
ESQUEMAS_IGNORADOS = ('mailto:', 'tel:', 'sms:', 'javascript:', 'data:', 'blob:', 'about:')
ATRIBUTOS_LINK = {'a': 'href', 'area': 'href', 'link': 'href', 'form': 'action', 'use': 'href'}
ATRIBUTOS_ARQUIVO = ('src', 'poster', 'data-src')
ATRIBUTOS_SRCSET = ('srcset', 'imagesrcset', 'data-srcset')
METAS_ARQUIVO = ('og:image', 'og:image:secure_url', 'twitter:image', 'og:url')
REFS_ID = ('for', 'aria-labelledby', 'aria-describedby', 'aria-controls', 'aria-owns', 'list', 'form')
RE_CSS_URL = re.compile(r'url\(\s*([\'"]?)([^\'")]+)\1\s*\)|@import\s+([\'"])([^\'"]+)\3')
RE_JS_CAMINHO = re.compile(r'([\'"`])((?:\./)?(?:img|js|css|fonts)/[A-Za-z0-9_.\-/]+\.[A-Za-z0-9]{2,5})\1')


# ---------- árvore HTML mínima ----------

class No:
    __slots__ = ('tag', 'attrs', 'pai', 'filhos', 'linha')

    def __init__(self, tag, attrs, pai, linha):
        self.tag, self.attrs, self.pai, self.filhos, self.linha = tag, attrs, pai, [], linha

    def classes(self):
        return set((self.attrs.get('class') or '').split())

    def nome(self):
        c = '.'.join(sorted(self.classes()))
        return self.tag + ('.' + c if c else '')

    def descendentes(self):
        for f in self.filhos:
            if isinstance(f, No):
                yield f
                yield from f.descendentes()


class Arvore(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.raiz = No('#documento', {}, None, 0)
        self.atual = self.raiz
        self.nos = []

    def _novo(self, tag, attrs):
        d = {}
        for k, v in attrs:
            d.setdefault(k, '' if v is None else v)
        no = No(tag, d, self.atual, self.getpos()[0])
        self.atual.filhos.append(no)
        self.nos.append(no)
        return no

    def handle_starttag(self, tag, attrs):
        no = self._novo(tag, attrs)
        if tag not in VAZIAS:
            self.atual = no

    def handle_startendtag(self, tag, attrs):
        self._novo(tag, attrs)

    def handle_endtag(self, tag):
        n = self.atual
        while n is not None and n.tag != tag:
            n = n.pai
        if n is not None and n.pai is not None:
            self.atual = n.pai

    def handle_data(self, data):
        self.atual.filhos.append(data)


def texto(no, visivel=True):
    partes = []

    def rec(n):
        for f in n.filhos:
            if isinstance(f, str):
                partes.append(f)
            elif not visivel or f.tag not in ('script', 'style', 'template'):
                rec(f)
    rec(no)
    return ' '.join(''.join(partes).replace('\xa0', ' ').split())


# ---------- verificador ----------

class Verificador:
    def __init__(self, pasta):
        self.pasta = pasta
        self.fonte = os.path.exists(os.path.join(pasta, 'build.py'))
        self.problemas = []  # (nivel, arquivo, linha, mensagem)
        self.contagem = {'links': 0, 'arquivos': 0, 'âncoras': 0, 'imagens com selo': 0, 'JSON-LD': 0}
        self.indexar = os.environ.get('INDEXAR', '').strip()
        self.gtm = os.environ.get('GTM_ID', '').strip()
        site_env = os.environ.get('SITE_URL', '').strip()
        self.site_env = site_env.rstrip('/') + '/' if site_env else ''
        self.paginas = {}  # nome -> Arvore
        self.ids = {}      # nome -> set de ids

    def erro(self, arq, linha, msg):
        self.problemas.append(('ERRO', arq, linha, msg))

    def aviso(self, arq, linha, msg):
        self.problemas.append(('AVISO', arq, linha, msg))

    # --- carga ---
    def carregar(self):
        nomes = sorted(f for f in os.listdir(self.pasta) if f.endswith('.html'))
        for nome in nomes:
            a = Arvore()
            with open(os.path.join(self.pasta, nome), encoding='utf-8') as fh:
                a.feed(fh.read())
            a.close()
            self.paginas[nome] = a
            self.ids[nome] = {n.attrs['id'] for n in a.nos if n.attrs.get('id')}
        partes = []
        for raiz, dirs, arquivos in os.walk(self.pasta):
            rel = os.path.relpath(raiz, self.pasta).replace(os.sep, '/')
            if rel == 'js/vendor' or rel.startswith('js/vendor/'):
                continue
            for f in arquivos:
                if f.endswith('.js'):
                    with open(os.path.join(raiz, f), encoding='utf-8') as fh:
                        partes.append(fh.read())
        self.js_texto = '\n'.join(partes)
        self.site = self.site_env or self._canonical('index.html')
        self.site_path = urlsplit(self.site).path if self.site else ''

    def _canonical(self, nome):
        a = self.paginas.get(nome)
        if not a:
            return ''
        for n in a.nos:
            if n.tag == 'link' and 'canonical' in (n.attrs.get('rel') or '').split():
                h = (n.attrs.get('href') or '').strip()
                return h.rstrip('/') + '/' if h else ''
        return ''

    # --- resolução de endereços ---
    def resolver(self, ref, base_dir, doc_base):
        """Devolve (tipo, caminho_local, fragmento). tipo: local, externo, ignorado, vazio, raiz, fora."""
        ref = (ref or '').strip()
        if not ref:
            return 'vazio', None, None
        low = ref.lower()
        if low.startswith(ESQUEMAS_IGNORADOS):
            return 'ignorado', None, None
        if low.startswith('//'):
            ref, low = 'https:' + ref, 'https:' + low
        sp = urlsplit(ref)
        if sp.scheme:
            if sp.scheme in ('http', 'https') and self.site and (ref.startswith(self.site) or ref + '/' == self.site):
                sp = urlsplit(ref[len(self.site):] if ref.startswith(self.site) else '')
                base_dir, doc_base = '', 'index.html'
            else:
                return 'externo', ref, None
        caminho, frag = unquote(sp.path), unquote(sp.fragment)
        if caminho.startswith('/'):
            if self.site_path and self.site_path != '/' and caminho.startswith(self.site_path):
                caminho = caminho[len(self.site_path):]
            elif self.site_path in ('', '/'):
                caminho = caminho[1:]
            else:
                return 'raiz', ref, None
            base_dir = ''
            if not caminho:
                return 'local', 'index.html', frag
        if not caminho:
            return 'local', doc_base, frag
        final = posixpath.normpath(posixpath.join(base_dir, caminho))
        if final.startswith('..'):
            return 'fora', ref, None
        if final == '.' or caminho.endswith('/'):
            final = posixpath.join('' if final == '.' else final, 'index.html')
        return 'local', final, frag

    def existe(self, caminho):
        return os.path.isfile(os.path.join(self.pasta, *caminho.split('/')))

    def conferir_ref(self, arq, linha, ref, base_dir, doc_base, tipo_ref, ancora=True):
        tipo, caminho, frag = self.resolver(ref, base_dir, doc_base)
        if tipo in ('externo', 'ignorado'):
            return None
        if tipo == 'vazio':
            self.aviso(arq, linha, 'link vazio' if tipo_ref == 'link' else 'referência de arquivo vazia')
            return None
        if tipo == 'raiz':
            self.erro(arq, linha, f'{tipo_ref} começa com "/" e sai do site no GitHub Pages: {ref}')
            return None
        if tipo == 'fora':
            self.erro(arq, linha, f'{tipo_ref} sai da pasta do site: {ref}')
            return None
        self.contagem['links' if tipo_ref == 'link' else 'arquivos'] += 1
        if not self.existe(caminho):
            self.erro(arq, linha, (f'link quebrado: {ref}' if tipo_ref == 'link' else f'arquivo não existe: {ref}'))
            return caminho
        if ancora and frag and caminho.endswith('.html'):
            self.contagem['âncoras'] += 1
            ids = self.ids.get(caminho)
            if ids is not None and frag not in ids and frag != 'top':
                self.erro(arq, linha, f'âncora #{frag} não existe em {caminho}: {ref}')
        return caminho

    # --- por página ---
    def verificar_pagina(self, nome, arv):
        nos = arv.nos
        base_dir, doc_base = posixpath.dirname(nome), nome
        bases = [n for n in nos if n.tag == 'base' and n.attrs.get('href')]
        if bases:
            t, c, _ = self.resolver(bases[0].attrs['href'], base_dir, nome)
            if t == 'local':
                base_dir, doc_base = posixpath.dirname(c), c
            elif t == 'externo':
                self.erro(nome, bases[0].linha, f'<base href> fora do SITE ({self.site}): {bases[0].attrs["href"]}')
        if doc_base != nome:
            for n in (n for n in nos if len(n.attrs.get('href') or '') > 1 and n.attrs['href'].startswith('#')):
                self.aviso(nome, n.linha, f'com <base href>, {n.tag} href="{n.attrs["href"]}" aponta para '
                                          f'{doc_base}{n.attrs["href"]}, não para esta página')

        # links e arquivos
        for n in nos:
            at = ATRIBUTOS_LINK.get(n.tag)
            if at and at in n.attrs:
                rel = (n.attrs.get('rel') or '').split()
                if n.tag == 'link' and set(rel) & {'preconnect', 'dns-prefetch'}:
                    continue
                tipo_ref = 'link' if n.tag in ('a', 'area', 'form') or 'canonical' in rel or 'alternate' in rel else 'arquivo'
                self.conferir_ref(nome, n.linha, n.attrs[at], base_dir, doc_base, tipo_ref)
            if n.tag == 'use' and 'xlink:href' in n.attrs:
                self.conferir_ref(nome, n.linha, n.attrs['xlink:href'], base_dir, doc_base, 'arquivo')
            for at in ATRIBUTOS_ARQUIVO:
                if at in n.attrs and n.tag not in ('a',):
                    self.conferir_ref(nome, n.linha, n.attrs[at], base_dir, doc_base, 'arquivo', ancora=False)
            for at in ATRIBUTOS_SRCSET:
                for cand in (n.attrs.get(at) or '').split(','):
                    url = cand.strip().split(' ')[0] if cand.strip() else ''
                    if url:
                        self.conferir_ref(nome, n.linha, url, base_dir, doc_base, 'arquivo', ancora=False)
            if n.tag == 'meta' and (n.attrs.get('property') or n.attrs.get('name')) in METAS_ARQUIVO:
                c = n.attrs.get('content') or ''
                t = 'link' if (n.attrs.get('property') == 'og:url') else 'arquivo'
                if c and self.resolver(c, base_dir, doc_base)[0] == 'externo':
                    self.erro(nome, n.linha, f'{n.attrs.get("property") or n.attrs.get("name")} fora do SITE ({self.site}): {c}')
                else:
                    self.conferir_ref(nome, n.linha, c, base_dir, doc_base, t)
            if 'style' in n.attrs:
                self.conferir_css(nome, n.attrs['style'], base_dir, doc_base, n.linha)
            if n.tag == 'style':
                self.conferir_css(nome, texto(n, visivel=False), base_dir, doc_base, n.linha)
            if n.tag == 'script' and 'src' not in n.attrs and (n.attrs.get('type') or '') != 'application/ld+json':
                self.conferir_js(nome, texto(n, visivel=False), n.linha)

        # canonical
        canon = [n for n in nos if n.tag == 'link' and 'canonical' in (n.attrs.get('rel') or '').split()]
        if len(canon) != 1:
            self.erro(nome, 0, f'{len(canon)} <link rel="canonical"> (esperado 1)')
        else:
            t, c, _ = self.resolver(canon[0].attrs.get('href'), base_dir, doc_base)
            if t == 'externo' and self.site:
                self.erro(nome, canon[0].linha, f'canonical fora do SITE ({self.site}): {canon[0].attrs.get("href")}')
            elif t == 'local' and c != nome:
                self.erro(nome, canon[0].linha, f'canonical aponta para outra página ({c}): {canon[0].attrs.get("href")}')

        # IDs
        vistos = {}
        for n in nos:
            i = n.attrs.get('id')
            if i is None:
                continue
            if not i.strip():
                self.erro(nome, n.linha, f'id vazio em <{n.tag}>')
            elif i in vistos:
                self.erro(nome, n.linha, f'id duplicado "{i}" (já usado na linha {vistos[i]})')
            else:
                vistos[i] = n.linha
        ids = self.ids[nome]
        for n in nos:
            for at in REFS_ID:
                if at == 'for' and n.tag not in ('label', 'output'):
                    continue
                if at == 'form' and n.tag not in ('button', 'input', 'select', 'textarea', 'fieldset', 'output', 'object'):
                    continue
                if at == 'list' and n.tag != 'input':
                    continue
                for alvo in (n.attrs.get(at) or '').split():
                    # um id escrito entre aspas num .js é criado pelo script (ex.: o título do diálogo de projeto)
                    if alvo not in ids and not re.search(r'[\'"`]' + re.escape(alvo) + r'[\'"`]', self.js_texto):
                        self.erro(nome, n.linha, f'{at}="{alvo}" aponta para um id que não existe')

        # h1, título, descrição
        h1 = [n for n in nos if n.tag == 'h1']
        if len(h1) != 1:
            self.erro(nome, h1[1].linha if len(h1) > 1 else 0, f'{len(h1)} <h1> na página (esperado 1)')
        titulos = [n for n in nos if n.tag == 'title']
        if len(titulos) != 1:
            self.erro(nome, 0, f'{len(titulos)} <title> na página (esperado 1)')
        else:
            t = texto(titulos[0], visivel=False)
            if not t:
                self.erro(nome, titulos[0].linha, '<title> vazio')
            elif len(t) > TITULO_MAX:
                self.erro(nome, titulos[0].linha, f'<title> com {len(t)} caracteres (máximo {TITULO_MAX}): "{t}"')
        desc = [n for n in nos if n.tag == 'meta' and (n.attrs.get('name') or '').lower() == 'description']
        if len(desc) != 1:
            self.erro(nome, 0, f'{len(desc)} <meta name="description"> (esperado 1)')
        else:
            d = ' '.join((desc[0].attrs.get('content') or '').split())
            if not d:
                self.erro(nome, desc[0].linha, 'meta description vazia')
            elif len(d) > DESCRICAO_MAX:
                self.erro(nome, desc[0].linha, f'meta description com {len(d)} caracteres (máximo {DESCRICAO_MAX})')

        # alt e selos
        for n in nos:
            if n.tag == 'img' and 'alt' not in n.attrs:
                self.erro(nome, n.linha, f'<img> sem alt: {n.attrs.get("src", "")}')
        self.conferir_selos(nome, arv, base_dir, doc_base)

        # JSON-LD
        for n in nos:
            if n.tag == 'script' and (n.attrs.get('type') or '').strip().lower() == 'application/ld+json':
                self.contagem['JSON-LD'] += 1
                try:
                    json.loads(''.join(f for f in n.filhos if isinstance(f, str)))
                except ValueError as e:
                    self.erro(nome, n.linha, f'JSON-LD inválido: {e}')

        # noindex e GTM
        robots = ' '.join((n.attrs.get('content') or '').lower() for n in nos if n.tag == 'meta'
                          and (n.attrs.get('name') or '').lower() in ('robots', 'googlebot'))
        if self.indexar == '1' and nome != PAGINA_SEM_INDEX and 'noindex' in robots:
            self.erro(nome, 0, 'INDEXAR=1, mas a página tem noindex')
        if self.gtm:
            html = ''.join(texto(n, visivel=False) for n in nos if n.tag == 'script')
            if self.gtm not in html:
                self.erro(nome, 0, f'GTM_ID={self.gtm} definido, mas a página não carrega o GTM')

    def tipo_imagem(self, no, base_dir, doc_base):
        urls = [no.attrs.get('src') or '']
        for at in ATRIBUTOS_SRCSET:
            urls += [c.strip().split(' ')[0] for c in (no.attrs.get(at) or '').split(',') if c.strip()]
        if no.tag == 'img' and no.pai is not None and no.pai.tag == 'picture':
            for irmao in no.pai.filhos:
                if isinstance(irmao, No) and irmao.tag == 'source':
                    urls += [c.strip().split(' ')[0] for c in (irmao.attrs.get('srcset') or '').split(',') if c.strip()]
        for u in urls:
            t, c, _ = self.resolver(u, base_dir, doc_base)
            if t == 'local':
                b = posixpath.basename(c)
                for prefixo, _rotulo in SELOS:
                    if b.startswith(prefixo + '-') and posixpath.dirname(c).split('/')[-1] == 'img':
                        return prefixo
        return None

    def conferir_selos(self, nome, arv, base_dir, doc_base):
        imagens = {}
        for n in arv.nos:
            if n.tag == 'img':
                t = self.tipo_imagem(n, base_dir, doc_base)
                if t:
                    imagens[id(n)] = (n, t)
        rotulos = dict(SELOS)
        for n, t in imagens.values():
            rot = rotulos[t]
            anc, ok, bloco = n.pai, False, None
            while anc is not None:
                # imagens irmãs no mesmo wrapper ocupam o mesmo quadro (antes/depois): contam como uma
                n_img = len({id(d.pai) for d in anc.descendentes() if id(d) in imagens and imagens[id(d)][1] == t})
                if texto(anc).count(rot) >= n_img:
                    ok = True
                    break
                if anc.tag in BLOCO_TAGS or anc.classes() & BLOCO_CLASSES:
                    bloco = anc
                    break
                anc = anc.pai
            src = n.attrs.get('src') or (n.attrs.get('srcset') or '').split(' ')[0]
            if ok:
                self.contagem['imagens com selo'] += 1
            else:
                onde = bloco.nome() if bloco is not None else 'documento'
                self.erro(nome, n.linha, f'imagem {"IA" if t == "ai" else "real"} sem a etiqueta "{rot}" no bloco {onde}: {src}')
        # imagem de compartilhamento: o WhatsApp e o LinkedIn não mostram etiqueta
        for n in arv.nos:
            if n.tag == 'meta' and (n.attrs.get('property') or n.attrs.get('name')) in ('og:image', 'twitter:image'):
                tp, c, _ = self.resolver(n.attrs.get('content'), base_dir, doc_base)
                if tp == 'local' and posixpath.basename(c).startswith('ai-'):
                    self.aviso(nome, n.linha, f'imagem de compartilhamento é ilustração IA e sai sem a etiqueta: {c}')

    # --- CSS e JS ---
    def conferir_css(self, arq, css, base_dir, doc_base, linha=None):
        for m in RE_CSS_URL.finditer(css):
            url = (m.group(2) or m.group(4) or '').strip()
            if not url or url.startswith('#'):
                continue
            ln = linha or css.count('\n', 0, m.start()) + 1
            c = self.conferir_ref(arq, ln, url, base_dir, doc_base, 'arquivo', ancora=False)
            if c and posixpath.basename(c).startswith('ai-'):
                self.aviso(arq, ln, f'ilustração IA usada pelo CSS: confira a etiqueta à mão ({url})')

    def conferir_js(self, arq, js, linha=None):
        for m in RE_JS_CAMINHO.finditer(js):
            ln = linha or js.count('\n', 0, m.start()) + 1
            # caminhos nos .js são relativos à página (raiz do site), não ao arquivo .js
            c = self.conferir_ref(arq, ln, m.group(2), '', 'index.html', 'arquivo', ancora=False)
            if c and posixpath.basename(c).startswith('ai-'):
                self.aviso(arq, ln, f'ilustração IA usada pelo JS: confira a etiqueta à mão ({m.group(2)})')

    def verificar_estaticos(self):
        for raiz, dirs, arquivos in os.walk(self.pasta):
            dirs[:] = sorted(d for d in dirs if not d.startswith(('.', '__')))
            rel = os.path.relpath(raiz, self.pasta).replace(os.sep, '/')
            rel = '' if rel == '.' else rel
            for f in sorted(arquivos):
                caminho = posixpath.join(rel, f)
                if f.endswith('.css'):
                    with open(os.path.join(raiz, f), encoding='utf-8') as fh:
                        self.conferir_css(caminho, fh.read(), rel, caminho)
                elif f.endswith('.js') and not (rel == 'js/vendor' or rel.startswith('js/vendor/')):
                    with open(os.path.join(raiz, f), encoding='utf-8') as fh:
                        self.conferir_js(caminho, fh.read())

    # --- sitemap, robots, llms ---
    def verificar_buscadores(self):
        sm = os.path.join(self.pasta, 'sitemap.xml')
        if not os.path.exists(sm):
            self.erro('sitemap.xml', 0, 'arquivo não existe')
        else:
            with open(sm, encoding='utf-8') as fh:
                xml = fh.read()
            for m in re.finditer(r'<loc>\s*([^<\s]+)\s*</loc>', xml):
                url = m.group(1)
                linha = xml.count('\n', 0, m.start()) + 1
                t, c, _ = self.resolver(url, '', 'index.html')
                if t != 'local':
                    self.erro('sitemap.xml', linha, f'URL fora do SITE ({self.site}): {url}')
                elif not self.existe(c):
                    self.erro('sitemap.xml', linha, f'página não existe: {url}')
                elif c == PAGINA_SEM_INDEX:
                    self.erro('sitemap.xml', linha, 'o sitemap não deve listar a 404')
        rb = os.path.join(self.pasta, 'robots.txt')
        if not os.path.exists(rb):
            self.erro('robots.txt', 0, 'arquivo não existe')
        else:
            with open(rb, encoding='utf-8') as fh:
                linhas = fh.read().splitlines()
            for i, l in enumerate(linhas, 1):
                k, _, v = l.partition(':')
                if k.strip().lower() == 'sitemap':
                    t, c, _ = self.resolver(v.strip(), '', 'index.html')
                    if t != 'local' or not self.existe(c):
                        self.erro('robots.txt', i, f'Sitemap aponta para fora do site ou para arquivo que não existe: {v.strip()}')
                if self.indexar == '1' and k.strip().lower() == 'disallow' and v.strip() == '/':
                    self.erro('robots.txt', i, 'INDEXAR=1, mas o robots.txt bloqueia o site inteiro')
        ll = os.path.join(self.pasta, 'llms.txt')
        if not os.path.exists(ll):
            self.erro('llms.txt', 0, 'arquivo não existe')
        elif self.site:
            with open(ll, encoding='utf-8') as fh:
                txt = fh.read()
            for m in re.finditer(re.escape(self.site) + r'[^\s)\]>"\'`]*', txt):
                linha = txt.count('\n', 0, m.start()) + 1
                self.conferir_ref('llms.txt', linha, m.group(0).rstrip('.,;:'), '', 'index.html', 'link')
            if '{SITE}' in txt:
                self.erro('llms.txt', 0, 'sobrou {SITE} sem trocar')

    def verificar_variaveis(self):
        if self.indexar not in ('', '0', '1'):
            self.aviso('(variáveis)', 0, f'INDEXAR="{self.indexar}" não liga a indexação: use 1')
        if self.gtm and not re.fullmatch(r'GTM-[A-Z0-9]+', self.gtm):
            self.aviso('(variáveis)', 0, f'GTM_ID="{self.gtm}" não tem o formato GTM-XXXXXXX')
        if self.site_env:
            canon = self._canonical('index.html')
            if canon and canon != self.site_env:
                self.erro('index.html', 0, f'SITE_URL={self.site_env}, mas o canonical da Home é {canon} (o build usou outra SITE_URL?)')
            if not self.site_env.startswith('https://'):
                self.aviso('(variáveis)', 0, f'SITE_URL não começa com https://: {self.site_env}')
        if not self.fonte:
            for f in NAO_PUBLICAR:
                if os.path.exists(os.path.join(self.pasta, f)):
                    self.erro(f, 0, 'não deveria estar na pasta publicada')

    # --- execução ---
    def rodar(self):
        self.carregar()
        if not self.paginas:
            return None
        if not self.site:
            self.erro('index.html', 0, 'sem SITE_URL e sem canonical na Home: não dá para conferir endereços absolutos')
        self.verificar_variaveis()
        for nome, arv in self.paginas.items():
            self.verificar_pagina(nome, arv)
        self.verificar_estaticos()
        self.verificar_buscadores()
        return self.problemas


def main():
    ap = argparse.ArgumentParser(description='Confere o HTML gerado do site Smart Pix (links, arquivos, IDs, '
                                             'h1, título, descrição, alt, selos de imagem, JSON-LD, noindex).')
    ap.add_argument('pasta', nargs='?', default=os.path.join(RAIZ_REPO, 'site'),
                    help='pasta com os .html (padrão: site/; use _site para a pasta publicada)')
    args = ap.parse_args()
    pasta = os.path.abspath(args.pasta)
    if not os.path.isdir(pasta):
        print(f'Pasta não encontrada: {pasta}', file=sys.stderr)
        return 2
    v = Verificador(pasta)
    problemas = v.rodar()
    if problemas is None:
        print(f'Nenhum .html em {pasta}', file=sys.stderr)
        return 2
    rel = os.path.relpath(pasta, os.getcwd())
    rel = pasta if rel.startswith('..') else rel
    ind = 'INDEXAR=1' if v.indexar == '1' else 'INDEXAR desligado (piloto com noindex)'
    print(f'Verificando {rel}/ · {len(v.paginas)} páginas ({", ".join(v.paginas)})')
    print(f'SITE {v.site or "(desconhecido)"} · {ind} · GTM {v.gtm or "desligado"}')
    print()
    ordem = {'ERRO': 0, 'AVISO': 1}
    por_arquivo = {}
    vistos = set()
    for p in problemas:
        if p in vistos:
            continue
        vistos.add(p)
        por_arquivo.setdefault(p[1], []).append(p)
    for arq in sorted(por_arquivo):
        print(arq)
        for nivel, _, linha, msg in sorted(por_arquivo[arq], key=lambda p: (p[2], ordem[p[0]], p[3])):
            onde = f'linha {linha}' if linha else '—'
            print(f'  {nivel:<5}  {onde:<10}  {msg}')
        print()
    n_erros = sum(1 for p in vistos if p[0] == 'ERRO')
    n_avisos = len(vistos) - n_erros
    c = v.contagem
    print('Conferidos: ' + ', '.join(f'{c[k]} {k}' for k in c) + '.')
    if n_erros:
        print(f'Resultado: {n_erros} erro(s) e {n_avisos} aviso(s).')
        return 1
    print(f'Resultado: nenhum erro' + (f', {n_avisos} aviso(s).' if n_avisos else '.'))
    return 0


if __name__ == '__main__':
    sys.exit(main())
