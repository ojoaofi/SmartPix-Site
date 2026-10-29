# Site Smart Pix

Site institucional da Smart Pix Impressão Digital (Atibaia, SP): impressão digital em grande formato, cenografia e instalação. Hoje é um piloto no GitHub Pages, fora do Google até o lançamento (ver o checklist abaixo).

## Estrutura

- `site/`: o site. São 7 páginas estáticas: início (`index.html`), soluções (`solucoes.html`), cenografia e agências (`cenografia.html`), aplicações (`projetos.html`), orçamento (`orcamento.html`), privacidade (`privacidade.html`) e a página de erro (`404.html`).
  - `build.py`: gera as páginas, o `sitemap.xml`, o `robots.txt` e o `llms.txt` (a partir de `llms.src.txt`). **Edite aqui, nunca nos `.html`.** Dados em `PRODUCTS`, `PROBLEMS`, `PROJECTS`, `FAQ`, `XL` e `GRID`; o que depende de confirmação da Smart Pix fica em `CONFIRMADO` (ver Pendências).
  - `css/site.css`: estilos (padrão minimalista apple.com).
  - `js/`: `site.js` (molas, menu, barra que muda de tom, galerias), `studio.js` (estúdio 3D), `problems.js` (galeria de problemas), `quote.js` (orçamento em 2 etapas → WhatsApp/e-mail), `projects.js` (filtros e detalhe das aplicações).
  - `js/vendor/three.min.js`: three.js r128 servido pelo próprio site, sem depender do CDN. Só carrega quando o estúdio 3D se aproxima da tela; sem WebGL, o estúdio mostra a versão 2D.
  - `img/`: imagens WebP (ilustrações de IA com a etiqueta "Ilustração IA", fotos reais com "Foto real"), `og.jpg` (imagem de compartilhamento) e logos. `fonts/`: Inter e Poppins locais.
  - `logo_paths.svg`: vetor do logo que o build embute nas páginas. Não é publicado, assim como `build.py` e `llms.src.txt`.
- `scripts/`
  - `verificar_site.py`: confere o HTML gerado (só biblioteca padrão do Python).
  - `montar_publicacao.sh`: monta a pasta publicada `_site/` a partir de `site/`. É a lista única do que vai ao ar: todas as páginas `site/*.html` (a 404 inclusive), `css/`, `js/` (com `js/vendor/`), `img/`, `fonts/`, `robots.txt`, `sitemap.xml` e `llms.txt`.
- `.github/workflows/`
  - `pages.yml` (**Publicar site no GitHub Pages**): em push na `main` que mexa em `site/` ou `scripts/`, ou à mão. Gera as páginas com as Variables do repositório, monta `_site`, verifica e publica.
  - `verificar.yml` (**Verificar site**): em todo push e pull request. Gera as páginas sem variáveis, confere se os arquivos commitados batem com o `build.py` e roda o verificador em `site/` e na pasta que seria publicada.
- `design-system/`: sistema da marca (cores, tipografia, componentes, logo) para impressos, redes e apresentações. A seção "No site" do README dele diz o que muda no site.
- `docs/`: auditorias. A mais recente é [`docs/auditoria-v9.md`](docs/auditoria-v9.md).

## Rodar localmente

```bash
python3 site/build.py                   # gera as páginas
python3 scripts/verificar_site.py       # confere o HTML gerado
cd site && python3 -m http.server 8000  # abra http://localhost:8000
```

Confira no navegador em 1440 px e em 390 px: sem rolagem horizontal, alvos de toque com pelo menos 44 px e nenhum erro no console. Antes do commit, rode o build sem variáveis: os `.html` do repositório são sempre os do padrão.

## Verificação automática

`scripts/verificar_site.py` confere, em cada `.html` de `site/` (ou da pasta passada, ex.: `_site`):

- links internos e âncoras (`#id`) existem; todo arquivo referenciado existe (imagens e `srcset`, CSS, JS, fontes, ícones, `og:image`, `url()` do CSS e caminhos escritos nos `.js`); nenhum caminho começa com `/` (no GitHub Pages ele sairia do site);
- IDs duplicados (`data-id` não conta) e `for`/`aria-*` que apontam para um id que não existe;
- exatamente um `<h1>`; `<title>` com até 65 caracteres; meta description com até 160;
- todo `<img>` tem `alt` (vazio vale para imagem decorativa);
- toda imagem `img/ai-*` está num bloco com a etiqueta "Ilustração IA", e toda `img/real-*` num bloco com "Foto real". O verificador sobe do pai da imagem até o primeiro bloco (`figure`, `article`, `section`, `.tile`, `.pc`, `.card`, `.card-img`, `.pd-img`, `.studio-stage`…) e exige uma etiqueta por imagem; a regra completa está no topo do script;
- JSON-LD válido; `sitemap.xml`, `robots.txt` e `llms.txt` só apontam para páginas e âncoras que existem;
- com `INDEXAR=1`, nenhuma página além da 404 tem `noindex`; com `SITE_URL`, o canonical da Home é ela; com `GTM_ID`, toda página tem o GTM;
- na pasta publicada, não há `build.py`, `llms.src.txt` nem `logo_paths.svg`.

Erro sai com código 1 e derruba o workflow. Aviso só aparece na saída.

## Configuração do build

| Variável | Para quê | Padrão (vazia = não definida) |
|---|---|---|
| `SITE_URL` | endereço público (canonical, sitemap, Open Graph, JSON-LD, `llms.txt`) | `https://ojoaofi.github.io/SmartPix-Site/` |
| `INDEXAR` | `1` libera o Google; qualquer outro valor deixa todas as páginas com `noindex` | desligado (piloto) |
| `GTM_ID` | Google Tag Manager (`GTM-XXXXXXX`); os eventos de clique e de orçamento já vão para o `dataLayer` | vazio (sem GTM) |

**No GitHub:** Settings → Secrets and variables → Actions → aba **Variables** → **New repository variable**. Crie `SITE_URL`, `INDEXAR` e `GTM_ID` ali (são Variables, não Secrets: nenhuma é segredo, todas aparecem no HTML). Mudar uma Variable não publica nada sozinho: depois, vá em Actions → Publicar site no GitHub Pages → **Run workflow**. Se a variável não pegar, o passo "Verificar pasta publicada" falha antes de publicar.

**Local:** `SITE_URL=https://www.dominio.com.br/ INDEXAR=1 GTM_ID=GTM-XXXX python3 site/build.py`. Serve para testar; não faça commit desse resultado (o workflow "Verificar site" compara os arquivos commitados com o build sem variáveis).

## Checklist de lançamento

Na ordem:

- [ ] **Textos aprovados pela Smart Pix**, com nome e e-mail de quem aprovou, e as pendências do `CONFIRMADO` resolvidas (ver abaixo).
- [ ] **Domínio próprio no GitHub Pages:** Settings → Pages → Custom domain. No DNS, `CNAME` do `www` para `ojoaofi.github.io` e, para o domínio sem `www`, os registros `A`/`AAAA` do GitHub Pages. Marcar **Enforce HTTPS**. Verificar o domínio na conta (Settings da conta → Pages → Add a domain) para nenhum outro repositório usá-lo. O endereço `github.io` passa a redirecionar para o domínio.
- [ ] **`SITE_URL`** = o domínio, com `https://` e barra no fim (ex.: `https://www.smartpix.com.br/`).
- [ ] **`INDEXAR=1`**, só depois dos textos aprovados.
- [ ] **GTM:** criar o contêiner do Google Tag Manager com o GA4 e informar o `GTM_ID`. Antes de ligar, a Smart Pix revisa a política de privacidade (`privacidade.html`) e o aviso de cookies (LGPD); depois de publicar, conferir que o GTM só carrega após o aceite.
- [ ] **Publicar de novo** (Run workflow) e conferir no endereço novo: canonical, `robots.txt`, `sitemap.xml` e a 404 (abrir um endereço que não existe).
- [ ] **Google Search Console:** propriedade do domínio (verificação por DNS) e envio do `sitemap.xml`, **só depois do `INDEXAR=1`** (antes, o Search Console acusa "URL enviada marcada como noindex").
- [ ] **Google Meu Negócio** (Perfil da Empresa no Google) com o mesmo nome, endereço e telefone do site: Smart Pix Impressão Digital, Av. São Paulo, 111, Alvinópolis, Atibaia/SP, WhatsApp (11) 91010-1324 (o fixo só se confirmado). Site = o domínio novo.
- [ ] **Teste num iPhone e num Android reais:** menu, barra translúcida, estúdio 3D, detalhe das aplicações, teclado no formulário e o orçamento até abrir o WhatsApp.

## Pendências para confirmar com a Smart Pix

O `build.py` tem o dicionário `CONFIRMADO = {'instalacao_propria': False, 'telefone_fixo': False, 'instagram': False}`. Enquanto um item estiver `False`, o site não afirma aquilo: usa um texto que não depende da confirmação e tira o dado do rodapé, do orçamento, do JSON-LD e do `llms.txt`. Quando a Smart Pix confirmar, basta trocar para `True`, rodar `python3 site/build.py` e fazer commit.

- Equipe de instalação própria (`instalacao_propria`). Hoje só a frota própria está confirmada.
- Telefone fixo (11) 2427-3880 (`telefone_fixo`) e Instagram @smartpixoficial (`instagram`).
- Cidades atendidas para entrega e instalação.
- Entrega sem a identificação da Smart Pix para clientes de agências.
- Prazo médio de resposta ao orçamento e de produção; montagem à noite ou em fim de semana.
- Fotos reais em boa resolução, sem marca de cliente e sem precisar borrar nada, para substituir as ilustrações de IA, a capa de Cenografia e o `og.jpg`.
- Ano de fundação (confere no cartão CNPJ) e números do galpão e das máquinas (área, quantidade, largura máxima por material).
- Link das avaliações no Google (depende do perfil no Google Meu Negócio).
- Nome e e-mail de quem aprova os textos antes do `INDEXAR=1`.
