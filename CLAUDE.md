# Smart Pix site — notas para o Claude Code

Site estático (HTML/CSS/JS puro, sem framework) da Smart Pix Impressão Digital, Atibaia/SP. Público: empresas de cenografia/montadoras, agências/produtoras e empresas.

## Como trabalhar
- O HTML é gerado: edite `site/build.py` (dados em `PRODUCTS`, `PROBLEMS`, `PROJECTS`, `FAQ`, `XL`, `GRID`; páginas em `page_*`) e rode `python3 site/build.py`. Nunca edite os `.html` à mão.
- Teste servindo `site/` (`python3 -m http.server`) e confira desktop (1440px) e celular (390px): sem rolagem horizontal, alvos de toque ≥ 44px, sem erros no console.
- Three.js r128 é servido pelo próprio site (`js/vendor/three.min.js`) e só carrega quando o estúdio se aproxima da tela; sem WebGL, com economia de dados ou se o 3D falhar, há uma versão 2D (só a lona).
- `SITE_URL`, `INDEXAR` e `GTM_ID` são variáveis do build (ver README); vazias valem como não definidas. O build também gera `sitemap.xml`, `robots.txt` e `llms.txt` (fonte: `llms.src.txt`, com marcadores como `{CONTATOS}` e `{INST_*}`).
- `CONFIRMADO` no topo do `build.py` decide o que o site pode afirmar (instalação própria, telefone fixo, Instagram). Texto novo que dependa de um desses itens passa por `inst(sim, nao)` ou pelo dicionário; sem confirmação, o padrão é "sob consulta".
- Imagens opcionais (fotos reais recortadas, versões "antes" dos problemas) entram só se o arquivo existir em `img/`; o build lê as medidas do próprio `.webp`.
- Home e Aplicações (`projetos.html`) terminam em `cta_end()` (3 passos + orçamento + WhatsApp). Elementos com a classe `rise` entram com fade; não usar em blocos de tela cheia.
- Com `GTM_ID`, o Tag Manager só carrega depois do aceite no aviso de cookies; a página `privacidade.html` explica o que o site faz com os dados.
- Antes de publicar: `python3 site/build.py && python3 scripts/verificar_site.py`. O CI (`verificar.yml`) falha se os `.html` commitados não baterem com o build sem variáveis. Pasta nova de arquivos em `site/` precisa entrar em `scripts/montar_publicacao.sh` (é a lista do que vai ao ar).

## Direção visual (aprovada pelo cliente)
- Padrão apple.com: abre com a marca (logo + "Smart Pix"), blocos de produto em tela cheia, muito respiro, frases curtas.
- Uma família tipográfica (sistema/SF Pro, Inter como reserva); Poppins só no logotipo e nas artes do estúdio.
- Verde-limão `#bde000` só no logo e nos botões principais. Fundo branco/#f5f5f7; preto só onde a imagem pede.
- Movimento com molas (damping/response), interrompível; respeitar `prefers-reduced-motion`, `prefers-reduced-transparency` e `prefers-contrast`.

## Regras de conteúdo (não negociáveis)
- Nenhuma marca de cliente ou de terceiros (texto, imagem, alt, JSON-LD).
- Não inventar números, clientes, prazos, certificações ou garantias. Dado faltando vira pendência no README.
- Toda imagem gerada por IA leva o selo "Ilustração IA"; fotos reais levam "Foto real".
- Fatos confirmados: Av. São Paulo, 111, Alvinópolis, Atibaia/SP; CNPJ 05.801.627/0001-65; WhatsApp (11) 91010-1324; atendimento@smartpix.com.br; seg–sex 8h–18h; lona até 5 m sem emenda; UV LED; frota própria.
