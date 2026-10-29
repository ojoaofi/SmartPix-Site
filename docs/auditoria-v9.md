# Auditoria completa do site Smart Pix (v9)

**Commit auditado:** `123ea78` (v9, ilustrações IA novas). **Data:** 29/10/2026.
**Escopo:** as 5 páginas + 404, o build, o CSS/JS, as imagens, o workflow de publicação e a documentação. Lentes: design (padrão Apple), movimento e interação, desempenho, acessibilidade, SEO e publicação, conteúdo e confiança, código e processo.

## Como medi

- Build local (`python3 site/build.py`): os `.html` commitados estão em dia com o `build.py`.
- Chromium (Playwright) em 320, 390, 768, 1024, 1440, 1920 e 2560 px: rolagem horizontal, alvos de toque, console, rede, CLS, capturas de tela de todas as páginas.
- Lighthouse 12 (celular simulado = 4G lento + CPU 4× mais lenta; e desktop) nas 5 páginas.
- axe-core 4.10 (WCAG 2.2 AA + boas práticas) nas 5 páginas, em desktop e celular.
- Fluxos reais: menu, cartões de problema, detalhe de projeto, orçamento em 2 etapas (mensagem do WhatsApp), estúdio 3D (digitar, cor, arrastar, visões), teclado (Tab), `prefers-reduced-motion`.

**Limites:** o site publicado (github.io) e o CDN do three.js estavam bloqueados no ambiente; testei o build local e o 3D com uma cópia local do three.js r128. O servidor local não usa gzip (no GitHub Pages os números de transferência caem uns 70% nos textos). Só testei Chromium: falta conferir num iPhone e num Android reais (`backdrop-filter`, `dialog`, barra de endereço, teclado).

## Resumo

**A parte técnica está muito boa.** A parte que ainda segura o site é **conteúdo e prova**: duas informações publicadas sem confirmação e fotos reais fracas. Depois vêm cerca de dez defeitos visuais pequenos e fáceis de corrigir.

| Medida | Resultado |
|---|---|
| Lighthouse desempenho | Celular: 91 (Home), 97–98 (demais). Desktop: 100 (Home, a única medida) |
| Lighthouse acessibilidade / boas práticas | 100 / 100 em todas as páginas |
| Lighthouse SEO | 66–69, só por causa do `noindex` do piloto (intencional) |
| axe-core | 0 violações em 10 combinações página × tela |
| CLS | 0,000 em todas as páginas |
| LCP | Desktop 0,6 s · celular simulado 2,3–2,7 s |
| Peso da Home | 548 KB (desktop) / 405 KB (celular), sem gzip. HTML + CSS + JS somam ~95 KB (~30 KB com gzip) |
| Rolagem horizontal | Nenhuma de 390 a 2560 px. **Há em 320 px** (item D7) |
| Erros de console | Nenhum, fora o CDN bloqueado do ambiente |
| Alvos de toque no celular | Todos ≥ 44 px (o botão "Orçamento" da barra tem 24 px visíveis e 44 px de área de toque) |

## O que já está no nível Apple (manter)

- Abertura com a marca, frases curtas, muito respiro, blocos de produto em tela cheia, verde-limão só no logo e nos botões principais.
- Molas com amortecimento e resposta (`Spring`), interrompíveis: menu, detalhe de projeto (cresce a partir do cartão e volta para ele), rotação do 3D (amortecimento 0,8 e resposta 0,4, os valores da Apple).
- Arrasto 1:1 com `setPointerCapture`, projeção de momento até o ponto mais próximo, elástico nas bordas (trilho de problemas, estúdio 3D, folha de projeto no celular).
- Feedback no toque (`:active` imediato), barra com material translúcido que muda de tom conforme o que passa por baixo, linha de borda só depois da rolagem.
- `prefers-reduced-motion`, `prefers-reduced-transparency`, `prefers-contrast` e `forced-colors` tratados. Com "reduzir movimento", 0 elementos ficam escondidos.
- Foco visível em toda a ordem de Tab, link "Pular para o conteúdo", `inert` nos fundos do menu.
- Formulário: rascunho guardado na sessão, validação com mensagem, resumo vivo, barra de envio no celular, mensagem do WhatsApp bem montada (perfil, produtos, medida, m², data, local, instalação, arte).
- Imagens: WebP com `srcset`, `width`/`height` (CLS 0), LCP com `fetchpriority` e preload, três.js só carrega perto do estúdio, versão 2D quando não há WebGL.

## Achados

Gravidade: **Crítico** (regra do projeto quebrada ou risco ao negócio) · **Alto** · **Médio** · **Baixo**.
Esforço: **5 min**, **1 h** ou **Smart Pix** (depende de informação ou material que só a empresa tem).

### 1. Conteúdo e confiança

| # | Grav. | Achado | Ação | Esforço |
|---|---|---|---|---|
| C1 | Crítico | **"Equipe de instalação própria" é afirmada como fato** na Home (hero, FAQ, "Quem somos"), em Soluções, em Projetos, no JSON-LD e no `llms.txt`. O `CLAUDE.md` e o README dizem que só a **frota própria** está confirmada. | Confirmar com seu pai. Até lá, trocar por "Frota própria para entrega. Instalação: consulte" (e ajustar o JSON-LD e o `llms.src.txt`). | 15 min + confirmação |
| C2 | Crítico | **Telefone fixo (11) 2427-3880 e Instagram estão publicados** (rodapé de todas as páginas, Orçamento com botão "Copiar número", JSON-LD, `llms.txt`), mas o README os lista como **pendência de confirmação**. Número errado numa página de orçamento custa lead. | Confirmar ou remover dos três lugares. | 10 min + confirmação |
| C3 | Alto | **A melhor foto real tem uma faixa borrada** atravessando a lona (parece ocultar marca de cliente), é um quadro de vídeo (1440 px, compressão visível) e aparece em três lugares: capa de Cenografia, "Quem somos" e a imagem de compartilhamento (`og.jpg`, o que aparece no WhatsApp e no LinkedIn). A segunda foto ("impressora UV", 1000 × 460 px, 14 KB) está visivelmente pixelada. | Nova sessão de fotos (lista no v8, itens de 1 a 9). No curto prazo: recortar a faixa borrada fora e refazer o `og.jpg`. | Smart Pix |
| C4 | Alto | **Prova real só aparece no fim da Home.** Acima da dobra e nos blocos de produto tudo é ilustração IA: 18 das 20 imagens, só 10 ilustrações diferentes (o estande aparece 4 vezes, o palco 2). Para cenografia e agências, uma foto real vale mais que qualquer ilustração. | Subir a foto real do galpão para logo depois dos 4 destaques; reduzir a repetição de imagens na Home. | 30 min |
| C5 | Médio | **A página "Projetos" não tem nenhum projeto:** são 9 "tipos de projeto" ilustrados por IA. O nome promete portfólio. | Renomear para "O que produzimos" até haver 3 casos reais (segmento, tamanho, prazo, sem cliente), ou pôr 1 foto real por tipo. | 5 min / Smart Pix |
| C6 | Médio | **Promessa de prazo:** "Prazo de produção alinhado à data do evento/da montagem" (Cenografia ×2, Projetos). A regra do projeto é não prometer prazo sem confirmação. | Trocar por "Você informa a data. O prazo é confirmado no orçamento." | 5 min |
| C7 | Médio | **Sem política de privacidade (LGPD).** O formulário coleta nome e empresa, e quando o `GTM_ID` entrar haverá rastreamento. | Página curta de privacidade + aviso de cookies quando ligar o GTM (Consent Mode). | 1 h |
| C8 | Baixo | **Ilustração IA sem selo** por alguns instantes: a imagem de reserva do estúdio (`ai-booth`) aparece sem a etiqueta até o 3D carregar. No modo 2D (sem WebGL, economia de dados ou CDN fora), o texto ainda promete "e gire" e lista balcão, totem e letra-caixa, mas só aparece a lona. | Pôr a etiqueta na imagem de reserva; no modo 2D, trocar o texto por "Digite o nome e escolha a cor". | 15 min |

### 2. Design visual

| # | Grav. | Achado | Ação | Esforço |
|---|---|---|---|---|
| D1 | Alto | **Barra cinza sobre a abertura preta.** No topo da Home (desktop e celular) a barra translúcida escura fica sobre o fundo branco do `body` e renderiza **cinza #454545**, formando uma tarja acima do hero preto. A direção aprovada é abrir com a marca, e a Apple usa barra preta sobre hero preto. | Fundo preto sob a barra enquanto a página está no topo (por exemplo `html{background:#000}` na Home, ou `--edge:0` com fundo opaco `#000`). | 10 min |
| D2 | Médio | **Texto de apoio descentralizado** nos fechamentos ("Qual é o seu próximo projeto?", "Tem um projeto parecido?", "Não achou o que procura?"): o título é centralizado, mas o parágrafo fica à esquerda (`.lead` só ganha `margin-inline:auto` dentro de `.sec-head.center`). | `.center .lead{margin-inline:auto}`. | 5 min |
| D3 | Médio | **Seta dupla** em "Como chegar › ›" no Orçamento: o texto já traz "›" e `.link::after` põe outra. | Tirar o "›" do texto em `build.py`. | 5 min |
| D4 | Médio | **Subnav de Soluções no celular:** o botão "Pedir orçamento" aparece (a regra `.subnav-cta{display:none}` perde para `.subnav a{display:inline-flex}`), ocupa ~40% da barra de atalhos e duplica o botão "Orçamento" que está logo acima. | Aumentar a especificidade: `.subnav a.subnav-cta{display:none}` no `@media (max-width:734px)`. | 5 min |
| D5 | Médio | **Estúdio 3D no celular:** o seletor Lateral / 3/4 / Frente cobre o topo do estande (a letra-caixa fica cortada). | Pôr o seletor abaixo do palco, ou afastar a câmera / aumentar a altura do palco no celular. | 30 min |
| D6 | Baixo | **Link "É de cenografia ou agência? Conheça a parceria ›"** quebra em duas linhas no celular e a seta fica solta à direita (`inline-flex` + `::after`). | Deixar o link como `display:inline` com a seta colada ao fim do texto. | 5 min |
| D7 | Médio | **A 320 px (iPhone SE, Androids pequenos) a barra do topo passa 16 px da tela** em todas as páginas e o botão de menu fica cortado. | Abaixo de 360 px, esconder o ícone do WhatsApp da barra (o menu já tem) ou reduzir os espaços. | 10 min |
| D8 | Médio | **Imagens de tela cheia sobem só até 1536 px.** Em 1920 px o hero é ampliado 1,25× e fica macio; em telas Retina (muito comum entre agências e produtoras), 2×. A foto real da fábrica (1440 × 1440) é cortada em 16:8, então só ~720 px de altura úteis. | Acrescentar uma variante de ~2400 px às imagens de largura total (hero + 2 blocos grandes), via `srcset` (só baixa quem tem tela grande, +~100 KB). Para a foto real, usar o original, não o quadro de vídeo. | 1 h |
| D9 | Baixo | **Texto pequeno:** links da barra e do rodapé a 12 px, etiquetas a 12 px, legendas a 13 px. A Apple usa 12 px na barra, mas o público aqui está em desktops Windows (fonte Inter, não SF Pro) e vê pior. | Links da barra desktop a 13–14 px. | 5 min |
| D10 | Baixo | **O item "Problemas" no menu principal** é vago e soa negativo. | "Como resolvemos". | 5 min |
| D11 | Baixo | `design-system/README.md` está desatualizado em relação ao site aprovado: fala em títulos em Poppins, cantos retos e sem sombras; o site usa Inter/SF, cantos de 28 px e sombras no resumo do pedido. | Atualizar o README ou marcar como "histórico". | 15 min |

### 3. Movimento e interação (lente Apple)

| # | Grav. | Achado | Ação | Esforço |
|---|---|---|---|---|
| M1 | Médio | **A entrada dos blocos (`.rise`) dura 1 s** (fade + subida de 1,5 rem) e só dispara com 8% do bloco na tela. Em rolagem rápida o conteúdo chega vazio e demora a aparecer: o oposto de "resposta primeiro". | Encurtar para 0,5–0,6 s, subida de ~0,75 rem e gatilho em 0%. | 5 min |

O restante do movimento já segue os princípios (ver "O que já está no nível Apple"). Não encontrei transição CSS usada em gesto contínuo, nem animação que trave a entrada.

### 4. Desempenho

| # | Grav. | Achado | Ação | Esforço |
|---|---|---|---|---|
| P1 | Médio | **`studio.js` sonda o WebGL no carregamento** (`getContext('webgl')`, linha 77) em toda visita à Home, mesmo de quem não rola até o estúdio: ~200 ms de tarefa longa no celular simulado, e deixa um contexto WebGL órfão. | Mover a sonda para dentro de `soon()` (só quando o estúdio chegar perto). | 15 min |
| P2 | Baixo | **`site.js` (`edge()`) mede todas as faixas no carregamento** (`getBoundingClientRect` em loop): ~75 ms de reflow forçado no celular simulado (única recomendação de desempenho do Lighthouse além das imagens). | Usar um `IntersectionObserver` para a faixa sob a barra, ou só medir depois da 1ª rolagem. | 30 min |
| P3 | Médio | **three.js r128 vem do cdnjs sem integridade (SRI) e sem cópia local.** Se o CDN cair, vira o modo 2D (funciona, mas empobrece). É uma biblioteca de 2021. | Servir de `js/vendor/three.min.js` (mesmo domínio, mesmo cache) ou, no mínimo, `integrity` + `crossorigin`. | 30 min |
| P4 | Baixo | **Projetos:** o 1º cartão tem `loading="lazy"` e está acima da dobra no celular (Lighthouse "descoberta do LCP"). | Primeiro cartão `eager` + `fetchpriority="high"`. | 5 min |
| P5 | Baixo | **WebP recomprimível:** economia estimada de ~48 KB (`ai-facade-800` −20 KB, `ai-printer-800` −19 KB, `ai-vitrine-800` −10 KB). | Recomprimir a qualidade ~72. Compensa o item D8. | 15 min |
| P6 | Baixo | **Cache:** o GitHub Pages fixa 10 minutos e os arquivos não têm hash no nome. | Se o domínio próprio ficar atrás da Cloudflare: cache longo + nomes com hash. Hoje não vale a pena. | — |
| P7 | Baixo | **Código morto:** Manifesto e "dock" em `site.js` e `quote.js` (não há `#dock` nem `.manifesto` no HTML), fonte Inter 500 declarada e nunca usada, campos `before` e `kind` de `PROBLEMS` sem uso, variável `big` em `img()`. | Remover. | 15 min |

### 5. Acessibilidade

Sem violações no axe-core e Lighthouse 100. Dois ajustes finos:

| # | Grav. | Achado | Ação | Esforço |
|---|---|---|---|---|
| A1 | Baixo | O link da marca tem `aria-label="Smart Pix Impressão Digital, página inicial"`, mas o texto visível é "smartPIX". Quem usa comando de voz ("clicar smartPIX") não acerta (Lighthouse: *label-content-name-mismatch*, WCAG 2.5.3). | `aria-label="smartPIX, página inicial"`. | 5 min |
| A2 | Baixo | O `<h1>` da Home junta dois `<span>` de bloco sem espaço ("Smart Pix" + "Impressão digital…"): o `textContent` (que alguns leitores e rastreadores usam) vira "Smart PixImpressão". | Espaço entre os spans (ou `<br>` oculto). | 5 min |

### 6. SEO e publicação

| # | Grav. | Achado | Ação | Esforço |
|---|---|---|---|---|
| S1 | Alto | **A página 404 nunca é publicada:** o workflow do Pages copia só 5 `.html` para `_site` e `404.html` não está na lista. O item A9 do v8 está "Aplicado" só no repositório. (A 404 usa `<base href>` absoluto, então também não carrega CSS fora do endereço publicado: só dá para testá-la depois de publicar.) | Incluir `site/404.html` no `cp` de `.github/workflows/pages.yml`. | 5 min |
| S2 | Alto (no lançamento) | **O workflow roda `build.py` sem `SITE_URL`, `INDEXAR` nem `GTM_ID`.** Mesmo com domínio próprio, o site sairia `noindex` e com canonical do github.io. | Passar as três variáveis (Variables do repositório) e criar um checklist de lançamento: domínio, `INDEXAR=1`, GTM, Search Console. | 15 min |
| S3 | Médio | **O sitemap lista páginas `noindex`** (o Search Console avisa "URL enviada marcada como noindex"). | Só enviar o sitemap quando ligar `INDEXAR=1`. | — |
| S4 | Baixo | A meta description da Home tem 172 caracteres (o Google corta em ~155). | Encurtar. | 5 min |
| S5 | Médio | **Google Meu Negócio ainda não existe** (pendência T5 do v8). É o maior canal local da empresa. | Criar o perfil com o mesmo nome, endereço e telefone do site (só depois de resolver C2). | Smart Pix |
| S6 | Baixo | JSON-LD `LocalBusiness` sem `geo`; `areaServed` só diz Atibaia (cidades atendidas é pendência). FAQ com rich result restrito pelo Google a sites de governo e saúde (inofensivo, serve para buscadores de IA). | Acrescentar `geo` (coordenadas do endereço). Não inventar `priceRange`. | 10 min |

### 7. Conversão (vendas)

| # | Grav. | Achado | Ação | Esforço |
|---|---|---|---|---|
| V1 | Alto | **Falta prazo de resposta ao orçamento e de produção** (pendência V8 do v8): é o primeiro critério de quem tem data de montagem. | Uma linha "Respondemos em até X horas úteis" assim que a Smart Pix confirmar. | Smart Pix |
| V2 | Médio | **Sem prova social:** nenhum número, avaliação ou ano de fundação. | Pedir ao seu pai: ano de fundação (confere no cartão CNPJ), largura máxima por material, área do galpão, quantidade de máquinas, nota no Google. | Smart Pix |
| V3 | Médio | **O pedido sai pelo WhatsApp ou e-mail do cliente: sem GTM, a Smart Pix não sabe de onde vêm os pedidos.** Os eventos (`generate_lead`, `whatsapp_click`, etc.) já existem no `dataLayer`. | Criar o GTM + GA4 e informar o `GTM_ID`; só depois, avisar de cookies (C7). | 1 h |

### 8. Código e processo

| # | Grav. | Achado | Ação | Esforço |
|---|---|---|---|---|
| E1 | Médio | **Nenhuma verificação automática:** nada confere se os `.html` commitados estão em dia com o `build.py`, nem se há link quebrado ou arquivo faltando no `_site` (foi assim que o 404 escapou, S1). | Job de CI: `python3 site/build.py && git diff --exit-code`, mais um verificador de links internos e de lista do `cp`. | 1 h |
| E2 | Baixo | README diz "5 páginas" (são 6, com a 404); o `auditoria-v8.md` não reflete o v9. | Atualizar. | 10 min |

## Ordem sugerida

1. **Com seu pai (hoje):** C1, C2, V1 e V2. Sem isso o site não pode ser aprovado nem indexado.
2. **Uma tarde de ajustes:** D1, D2, D3, D4, D6, D7, D10, A1, A2, C6, M1, S1, P4 (todos de 5 a 15 min, em `build.py` e `site.css`).
3. **Meio dia:** P1, P2, P3, C8, D5, S2, E1.
4. **Material novo:** fotos reais (C3, C4, C5) e variante de 2400 px das imagens grandes (D8, P5).
5. **Lançamento:** domínio, `SITE_URL` + `INDEXAR=1`, GTM + aviso de cookies + política de privacidade (C7, V3), Google Meu Negócio (S5), teste num iPhone e num Android reais.

## Pendências para a Smart Pix (acréscimos ao v8)

- Confirmar se há **equipe de instalação própria** (C1) e o **telefone fixo e o Instagram** (C2).
- Fotos reais em boa resolução, sem marca de cliente e sem precisar borrar nada (C3).
- Prazo médio de resposta e de produção (V1); ano de fundação, números do galpão e das máquinas, link das avaliações no Google (V2).
- Nome e e-mail da pessoa que vai aprovar os textos antes do `INDEXAR=1`.

## Status depois do v10

Gravidade e números de item como acima. **Aplicado** = está no site; **Pendente** = depende da Smart Pix ou de material novo.

| Item | Status | Como ficou |
|---|---|---|
| C1 | Aplicado (aguarda confirmação) | `CONFIRMADO['instalacao_propria'] = False` no `build.py`: o site diz "montagem sob consulta", o cartão "Montagem no local" sai de Aplicações e o problema "a gráfica não instala" vira "a entrega depende de terceiros". Com `True`, os textos fortes voltam. |
| C2 | Aplicado (aguarda confirmação) | Telefone fixo e Instagram saem do rodapé, do Orçamento, do JSON-LD e do `llms.txt` até serem confirmados (`telefone_fixo`, `instagram`). |
| C3 | Aplicado em parte | Novo recorte do galpão sem a faixa borrada (faixa da Home, capa de Cenografia, "Quem somos") e `og.jpg` refeito. A foto borrada da impressora saiu. Fotos novas continuam pendentes. |
| C4 | Aplicado | Faixa "Produção própria." com foto real logo depois da abertura; foto real do Smart Floor em "Quem somos" e em Aplicações; cartões de problema com versões "antes", o que reduz a repetição. |
| C5 | Aplicado | "Projetos" virou "Aplicações" (mesma URL) e o cartão de pisos usa a foto real. |
| C6 | Aplicado | "O prazo é confirmado no orçamento." |
| C7 | Aplicado | Página `privacidade.html`; com `GTM_ID`, aviso de cookies e Tag Manager só depois do aceite. |
| C8 | Aplicado | Selo na imagem de reserva do estúdio; texto do modo 2D sem "gire". |
| D1–D7, D9–D11 | Aplicado | Home sob a barra translúcida; textos centralizados; seta dupla e seta solta corrigidas; subnav sem o botão no celular; seletor do 3D sem cobrir o estande; 320 px sem rolagem; barra a 13 px; "Como resolvemos"; `design-system/README.md` com a seção "No site". |
| D8 | Pendente | Não há fonte maior que 1536 px; a geração no Canva funciona, mas o download em alta resolução é bloqueado neste ambiente. |
| M1 | Aplicado | Entrada em 0,6 s, subida menor, gatilho ao entrar na tela. |
| P1–P3, P7 | Aplicado | Sonda do WebGL só perto do estúdio; barra sem reflow forçado; three.js servido de `js/vendor/`; código morto removido. |
| P4, P5 | Aplicado | 1º cartão de Aplicações sem lazy; WebP de 800 px recomprimidos. |
| P6 | Não aplicado | O GitHub Pages fixa o cache; reavaliar com domínio próprio. |
| A1, A2 | Aplicado | Nome do link da marca começa pelo texto visível; espaço no `<h1>`. |
| S1, S2, S4 | Aplicado | 404 publicada (com endereços absolutos); variáveis do build vindas das Variables do GitHub; descrições ≤ 155 caracteres (textos da pesquisa de mercado). |
| S3 | Documentado | No checklist de lançamento do README. |
| S5, V1, V2 | Pendente | Google Meu Negócio, prazo de resposta, números e avaliações: dependem da Smart Pix (ver `docs/pesquisa-mercado.md`, seção 8). |
| S6 | Não aplicado | `geo` exige coordenadas confirmadas. |
| V3 | Aplicado em parte | "Google Maps" em "Como nos conheceu?"; a medição espera o `GTM_ID`. |
| E1, E2 | Aplicado | `scripts/verificar_site.py` + `verificar.yml`; README atualizado. |
