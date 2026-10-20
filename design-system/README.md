# Sistema de design Smart Pix

Referência da marca Smart Pix Impressão Digital para o site e demais materiais. A versão navegável, com prévias ao vivo, fica no Claude (Sistema de design → Smart Pix).

**Como usar:** carregue `tokens.css` e depois `components/bundle.css`; use as classes `sp-` descritas em `components/<Componente>/README.md`. Cada pasta de componente tem um `preview.html` que abre direto no navegador.

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
- Números concretos no lugar de adjetivos: "até 5 m sem emenda", "4,7 no Google", "frota própria". Nada de "o melhor", "líder" ou "incrível".
- Sem emoji. Símbolos só funcionais: ★ ao lado da nota do Google, × entre medidas ("5,0 × 3,0 m"), vírgula decimal.
- Rótulos de seção (`kicker`) sempre em minúsculas: "impressão digital · cenografia · instalação".
- Nunca prometa prazo, preço ou condição que a empresa não confirmou.

## Cor

- `lime` (#bde000) é a cor da marca: o selo, as ações e os grandes momentos de marca. Use em botões principais (`sp-btn--fill`), na faixa de provas (`sp-proof`) e no destaque de títulos sobre `stage`.
- Texto sobre `lime` é sempre `on-lime` (preto). Nunca branco.
- `lime` nunca é texto sobre `surface` ou `surface-alt` (contraste 1,5:1). Nesses fundos, o verde de texto é `lime-ink`.
- `stage` (preto) é o fundo das seções de impacto, igual nos dois temas. Sobre ele: texto `on-stage`, apoio `on-stage-muted`, destaque `lime`.
- As páginas alternam seções `stage` e `surface` / `surface-alt`. Não use mais de uma seção inteira em `lime` por página.
- `graphite` (#4d4d4d) é o cinza do "smart" no logo: use como cor de marca (preenchimentos, a palavra "smart" na assinatura), não como cor de texto corrido.
- `print-cyan`, `print-magenta` e `print-yellow` formam o degradê de impressão (CMY + `lime`). Só para ilustrar material impresso (lonas, pisos, prévias em escala), nunca em interface ou texto.
- `warn` / `warn-soft` para avisos de prazo; `danger` para erros de formulário. Avisos sempre têm texto, nunca só cor.

## Tipografia

- Títulos em `display` (Poppins 600, a mesma família geométrica do "smart" do logo), com espaçamento negativo: `hero` 64 px na abertura, `headline` 56 px, `section` 40 px, `title` 28 px, `subtitle` 21 px.
- No celular (até 734 px): `hero` vai a 40 px, `headline` a 36 px, `section` a 30 px, `title` a 24 px, `subtitle` a 19 px.
- Texto em `body` (Inter): `lead` 21 px para subtítulos, `body` 17 px, `small` 14 px, `caption` 12 px. Botões em `button`.
- O `kicker` (Poppins 400, 14 px, espaçamento .24em, minúsculas) imita o "impressão digital" do selo. Vem sempre antes de um título, precedido pelo traço do X.
- Destaque de palavra-chave: sobre `stage`, a palavra em `lime`; sobre `surface`, `sp-mark` (marca-texto `lime` atrás da palavra). Um destaque por título, no máximo.
- Números de medida e preço com algarismos tabulares (`font-variant-numeric: tabular-nums`).

## Marca e motivos

- O logo é o selo redondo (`assets/Logos/smartpix-selo.svg`). Use inteiro, sem recolorir, sem contorno, sem girar e sem cortar. Tamanho mínimo: 28 px de diâmetro na tela.
- O selo funciona sobre qualquer fundo, porque traz o próprio círculo `lime`. Deixe ao redor um respiro de pelo menos um quarto do diâmetro.
- Na barra de navegação, a assinatura é o selo + "smart" + "PIX" (`sp-navbrand`): "smart" em Poppins 600, "PIX" em Poppins 700.
- O **traço do X** (o braço branco do X do logo, inclinado cerca de 31°) é o motivo gráfico da marca. Aparece antes do `kicker`, nos itens da faixa de provas e nos avisos (`assets/Motivos/smartpix-traco.svg` ou a forma em CSS do `sp-kicker`). Não use outro ícone como marcador.
- Sem respingos de tinta, texturas ou degradês decorativos na interface.

## Imagem

- Fotos reais de trabalhos entregues vêm primeiro. Quando a foto é real, diga: etiqueta "Foto real" (`sp-tag`).
- Ilustração gerada por IA só para mostrar equipamento ou material genérico (impressora, rolo de lona, amostras), sempre com a etiqueta "Ilustração IA" e o texto alternativo começando por "Ilustração gerada por IA:". Nunca apresente ilustração como trabalho entregue.
- Fotos ocupam o bloco inteiro (`object-fit: cover`), com degradê de `stage` no topo para o texto ficar legível.
- Marcas de clientes só aparecem com autorização e como referência de projeto.

## Layout

- A gramática é a de blocos grandes, no estilo Apple: abertura de tela cheia, blocos 2 × 2 de `tile-height` (580 px) com `space-3` (12 px) entre eles, cantos retos (`radius-none`).
- Conteúdo centralizado em até 1080 px; laterais de `space-4` (16 px) no celular.
- Seções com `space-9` (88 px) de respiro vertical no computador e `space-8` (64 px) no celular.
- Painéis e formulários usam `radius-xl`; cartões de opção `radius-md`; fotos em carrossel `radius-lg`; campos e seletores `radius-sm`; botões `radius-pill`.
- Sombra só para o que flutua: `shadow-panel` no resumo do pedido e `shadow-lift` no cartão em foco. Separações são feitas com `line`.
- Todo alvo de toque tem pelo menos `touch-target` (44 px).

## Movimento

- Movimento discreto e com função: o conteúdo sobe 32 px ao entrar na tela (1 s, `cubic-bezier(.2,.7,.2,1)`), cartões inclinam até 10° com o cursor, peças 3D giram sob o dedo.
- Tudo respeita `prefers-reduced-motion`: sem deslocamento, sem 3D animado, com uma imagem parada no lugar.
- O conteúdo nunca depende da animação para aparecer.

## Ícones

- Ícones de traço, desenhados à mão numa grade de 32 × 32, traço de 1,6 a 1,7 px, pontas e cantos arredondados, sem preenchimento. Cor `ink` em fundo claro e `lime` dentro de uma caixa `stage` (`sp-seg`).
- Não há biblioteca de ícones da marca; desenhe no mesmo estilo e mantenha o conjunto pequeno.
- Sem emoji como ícone.

## Acessibilidade

- Texto com contraste mínimo de 4,5:1 nos dois temas; cada token de texto diz em quais fundos pode ser usado.
- Foco do teclado: contorno sólido de 3 px em `focus-ring`, afastado 3 px do elemento. Sobre `stage`, o contorno é `lime`.
- Formulários dizem o que falta em texto ("Falta o produto e seu nome para montar o pedido."), não só com cor.

## Componentes

Os componentes são classes CSS em `components/bundle.css`, com prefixo `sp-`. Carregue `tokens.css` e depois `bundle.css`; as fontes vêm do Google Fonts pelo próprio `bundle.css`. Envolva seções escuras em `sp-stage` para os componentes trocarem para a versão sobre preto.
