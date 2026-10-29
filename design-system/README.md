# Sistema de design Smart Pix

Referência da marca Smart Pix Impressão Digital para impressos, redes sociais, apresentações e protótipos. O site segue a mesma marca, com as adaptações da seção "No site" logo abaixo. A versão navegável, com prévias ao vivo, fica no Claude (Sistema de design → Smart Pix).

## No site

O site (`site/`) segue a direção aprovada pelo cliente, no padrão apple.com (ver `CLAUDE.md` na raiz). Ele **não** carrega `tokens.css` nem `components/bundle.css`: tem o próprio `site/css/site.css`, que é a fonte da verdade para o site. Valem para o site, sem mudança, a voz e o texto (menos o `kicker` em minúsculas), a cor da marca e as regras de contraste, o logo e a assinatura da barra, os ícones, as etiquetas "Foto real" e "Ilustração IA" e os alvos de toque de 44 px. O que muda:

| Assunto | Neste sistema (impressos, redes, apresentações) | No site |
| --- | --- | --- |
| Família tipográfica | Títulos em Poppins 600, textos em Inter | Uma família só para títulos e textos: a fonte do sistema (SF Pro nos aparelhos Apple), com Inter como reserva (arquivos locais em `site/fonts/`). Poppins só no logotipo ("smartPIX" da barra) e nas artes do estúdio 3D |
| Títulos | 600, tamanhos fixos (64/56/40/28/21 px) | 700, tamanhos fluidos com `clamp()` (o maior título da Home chega a 120 px), espaçamento negativo por tamanho; escala em `site.css` |
| `kicker` | Poppins 400, 14 px, minúsculas espaçadas, depois do traço do X | Rótulo de 21 px, peso 600, cinza, na fonte do sistema, sem traço do X e sem forçar minúsculas |
| Verde-limão | Botões principais, faixa de provas, destaque de palavra em título | Só no logo e nos botões principais (e no rótulo curto "Com a Smart Pix" sobre preto, nos cartões de problema). Sem faixa lima e sem marca-texto |
| Fundos | Alterna `stage` (preto) e `surface` em temas claro e escuro | Branco e `#f5f5f7`; preto só onde a imagem pede. Sem tema escuro automático |
| Cantos | Blocos retos; painéis 24 px, cartões 16 px, carrossel 20 px, campos 14 px | Blocos de tela cheia e mosaico de produtos retos (como apple.com). Cartões, painéis, fotos, formulário e diálogo com 28 px (`--r3`); campos, avisos e seletor de quantidade com 12 px (`--r1`); botões e etiquetas em pílula |
| Sombras | `shadow-panel` e `shadow-lift` | Só no que flutua: resumo do pedido, detalhe de projeto e uma sombra leve nos cartões do trilho de problemas |
| Foco | Contorno de 3 px em `focus-ring` (lima sobre preto) | Contorno azul de 2 px (`#0071e3`; `#2997ff` sobre preto), afastado 3 px |
| Movimento | Sobe 32 px em 1 s; cartões inclinam até 10° com o cursor | Molas com amortecimento e resposta, interrompíveis; entrada com fade curto (classe `rise`, nunca em bloco de tela cheia); sem inclinação com o cursor. Respeita `prefers-reduced-motion`, `prefers-reduced-transparency` e `prefers-contrast` |
| Ilustração IA | Só equipamento ou material genérico | Também mostra tipos de projeto (palco, estande, fachada) enquanto faltam fotos reais, sempre com a etiqueta "Ilustração IA" e o alt começando por "Ilustração gerada por IA:". Nunca apresentada como trabalho entregue |
| Marcas de clientes | Com autorização, como referência de projeto | Nenhuma marca de cliente ou de terceiros (texto, imagem, alt, JSON-LD), nem com autorização. As fotos de `assets/Fotos/` que mostram marca de cliente não vão para o site |
| Fontes | Google Fonts, pelo `bundle.css` | Arquivos locais (`site/fonts/`), sem Google Fonts |

## Como usar

Carregue `tokens.css` e depois `components/bundle.css`; use as classes `sp-` descritas em `components/<Componente>/README.md`. Cada pasta de componente tem um `preview.html` que abre direto no navegador.

| Arquivo | O que é |
| --- | --- |
| `tokens.json` | Cores (tema claro e escuro), tipografia, espaçamentos, raios, tamanhos e sombras |
| `tokens.css` | Os mesmos tokens como variáveis CSS, gerados a partir de `tokens.json` |
| `components/bundle.css` | Componentes em CSS, prefixo `sp-` |
| `assets/` | Logo em vetor e original, traço do X e fotos reais de projetos |

A Smart Pix é uma gráfica digital de Atibaia, SP, especializada em impressão UV LED de grande formato, cenografia e instalação para eventos, lojas e marcas. O sistema tira tudo do próprio logo: o selo lima, o "smart" em grafite, o "PIX" em preto com o braço branco do X, e o "impressão digital" em minúsculas espaçadas. A promessa da marca é **Sua marca em tamanho real.**

## Voz e texto

- Fale direto com o cliente, de "você", em frases curtas. Português do Brasil, sem gíria e sem ponto de exclamação.
- Títulos curtos e com ponto final: "O chão também fala.", "Do arquivo ao palco.", "Monte seu orçamento."
- Botões começam com verbo e dizem o que acontece: "Montar orçamento", "Orçar Smart Floor", "Enviar pedido pelo WhatsApp". Nunca "Clique aqui" ou "Saiba mais" sozinho.
- Números concretos no lugar de adjetivos, só os confirmados pela Smart Pix: "até 5 m sem emenda", "UV LED", "frota própria". Nada de "o melhor", "líder" ou "incrível". Número sem confirmação (nota no Google, ano de fundação, prazo) fica fora até a empresa confirmar.
- Sem emoji. Símbolos só funcionais: ★ ao lado da nota do Google (quando houver nota real), × entre medidas ("5,0 × 3,0 m"), vírgula decimal.
- Fora do site, rótulos de seção (`kicker`) sempre em minúsculas: "impressão digital · cenografia · instalação". No site, o rótulo segue a grafia normal ("Estúdio 3D").
- Nunca prometa prazo, preço ou condição que a empresa não confirmou.

## Cor

- `lime` (#bde000) é a cor da marca: o selo, as ações e os grandes momentos de marca. Use em botões principais (`sp-btn--fill`), na faixa de provas (`sp-proof`) e no destaque de títulos sobre `stage`. No site, só no logo e nos botões principais.
- Texto sobre `lime` é sempre `on-lime` (preto). Nunca branco.
- `lime` nunca é texto sobre `surface` ou `surface-alt` (contraste 1,5:1). Nesses fundos, o verde de texto é `lime-ink`.
- `stage` (preto) é o fundo das seções de impacto, igual nos dois temas. Sobre ele: texto `on-stage`, apoio `on-stage-muted`, destaque `lime`.
- As páginas alternam seções `stage` e `surface` / `surface-alt`. Não use mais de uma seção inteira em `lime` por página.
- `graphite` (#4d4d4d) é o cinza do "smart" no logo: use como cor de marca (preenchimentos, a palavra "smart" na assinatura), não como cor de texto corrido.
- `print-cyan`, `print-magenta` e `print-yellow` formam o degradê de impressão (CMY + `lime`). Só para ilustrar material impresso (lonas, pisos, prévias em escala), nunca em interface ou texto.
- `warn` / `warn-soft` para avisos de prazo; `danger` para erros de formulário. Avisos sempre têm texto, nunca só cor.

## Tipografia

- Fora do site, títulos em `display` (Poppins 600, a mesma família geométrica do "smart" do logo), com espaçamento negativo: `hero` 64 px na abertura, `headline` 56 px, `section` 40 px, `title` 28 px, `subtitle` 21 px.
- No celular (até 734 px): `hero` vai a 40 px, `headline` a 36 px, `section` a 30 px, `title` a 24 px, `subtitle` a 19 px.
- Texto em `body` (Inter): `lead` 21 px para subtítulos, `body` 17 px, `small` 14 px, `caption` 12 px. Botões em `button`.
- O `kicker` (Poppins 400, 14 px, espaçamento .24em, minúsculas) imita o "impressão digital" do selo. Vem sempre antes de um título, precedido pelo traço do X.
- No site, títulos e textos usam a fonte do sistema com Inter de reserva, e Poppins fica só no logotipo e nas artes do estúdio 3D (ver "No site").
- Destaque de palavra-chave: sobre `stage`, a palavra em `lime`; sobre `surface`, `sp-mark` (marca-texto `lime` atrás da palavra). Um destaque por título, no máximo.
- Números de medida e preço com algarismos tabulares (`font-variant-numeric: tabular-nums`).

## Marca e motivos

- O logo é o selo redondo (`assets/Logos/smartpix-selo.svg`). Use inteiro, sem recolorir, sem contorno, sem girar e sem cortar. Tamanho mínimo: 28 px de diâmetro na tela.
- O selo funciona sobre qualquer fundo, porque traz o próprio círculo `lime`. Deixe ao redor um respiro de pelo menos um quarto do diâmetro.
- Na barra de navegação, a assinatura é o selo + "smart" + "PIX" (`sp-navbrand`): "smart" em Poppins 600, "PIX" em Poppins 700.
- O **traço do X** (o braço branco do X do logo, inclinado cerca de 31°) é o motivo gráfico da marca. Aparece antes do `kicker`, nos itens da faixa de provas e nos avisos (`assets/Motivos/smartpix-traco.svg` ou a forma em CSS do `sp-kicker`). Não use outro ícone como marcador. O site não usa o traço do X.
- Sem respingos de tinta, texturas ou degradês decorativos na interface.

## Imagem

- Fotos reais de trabalhos entregues vêm primeiro. Quando a foto é real, diga: etiqueta "Foto real" (`sp-tag`).
- Ilustração gerada por IA só para mostrar equipamento ou material genérico (impressora, rolo de lona, amostras; no site, também tipos de projeto enquanto faltam fotos reais), sempre com a etiqueta "Ilustração IA" e o texto alternativo começando por "Ilustração gerada por IA:". Nunca apresente ilustração como trabalho entregue.
- Fotos ocupam o bloco inteiro (`object-fit: cover`), com degradê de `stage` no topo para o texto ficar legível.
- Fora do site, marcas de clientes só aparecem com autorização e como referência de projeto. No site, nenhuma marca de cliente ou de terceiros, em texto, imagem, alt ou JSON-LD.

## Layout

- A gramática é a de blocos grandes, no estilo Apple: abertura de tela cheia, blocos 2 × 2 de `tile-height` (580 px) com `space-3` (12 px) entre eles, cantos retos (`radius-none`).
- Conteúdo centralizado em até 1080 px; laterais de `space-4` (16 px) no celular. No site, as larguras e laterais são `--max`, `--wide` e `--gutter` de `site.css`.
- Seções com `space-9` (88 px) de respiro vertical no computador e `space-8` (64 px) no celular. No site, o respiro é `--s9` de `site.css`.
- Painéis e formulários usam `radius-xl`; cartões de opção `radius-md`; fotos em carrossel `radius-lg`; campos e seletores `radius-sm`; botões `radius-pill`. No site, só dois raios além da pílula: 28 px para cartões, painéis, fotos e diálogo, e 12 px para campos e avisos.
- Sombra só para o que flutua: `shadow-panel` no resumo do pedido e `shadow-lift` no cartão em foco. Separações são feitas com `line`. No site, também no detalhe de projeto e, leve, nos cartões do trilho de problemas.
- Todo alvo de toque tem pelo menos `touch-target` (44 px).

## Movimento

- Movimento discreto e com função. Em protótipos e peças animadas: o conteúdo sobe 32 px ao entrar na tela (1 s, `cubic-bezier(.2,.7,.2,1)`), cartões inclinam até 10° com o cursor, peças 3D giram sob o dedo.
- No site: molas com amortecimento e resposta, interrompíveis (menu, detalhe de projeto, trilho de problemas, giro do estúdio 3D); entrada curta com fade (`rise`), nunca em bloco de tela cheia; sem inclinação com o cursor.
- Tudo respeita `prefers-reduced-motion`: sem deslocamento, sem 3D animado, com uma imagem parada no lugar. O site respeita também `prefers-reduced-transparency` e `prefers-contrast`.
- O conteúdo nunca depende da animação para aparecer.

## Ícones

- Ícones de traço, desenhados à mão numa grade de 32 × 32, traço de 1,6 a 1,7 px, pontas e cantos arredondados, sem preenchimento. Cor `ink` em fundo claro e `lime` dentro de uma caixa `stage` (`sp-seg`).
- Não há biblioteca de ícones da marca; desenhe no mesmo estilo e mantenha o conjunto pequeno.
- Sem emoji como ícone.

## Acessibilidade

- Texto com contraste mínimo de 4,5:1 nos dois temas; cada token de texto diz em quais fundos pode ser usado.
- Foco do teclado: contorno sólido de 3 px em `focus-ring`, afastado 3 px do elemento. Sobre `stage`, o contorno é `lime`. No site, o contorno é azul, de 2 px (`#0071e3`; `#2997ff` sobre preto), afastado 3 px.
- Formulários dizem o que falta em texto ("Falta o produto e seu nome para montar o pedido."), não só com cor.

## Componentes

Os componentes são classes CSS em `components/bundle.css`, com prefixo `sp-`. Carregue `tokens.css` e depois `bundle.css`; as fontes vêm do Google Fonts pelo próprio `bundle.css`. Envolva seções escuras em `sp-stage` para os componentes trocarem para a versão sobre preto. O site não usa estes componentes nem o Google Fonts: tem classes próprias em `site/css/site.css` e fontes locais.
