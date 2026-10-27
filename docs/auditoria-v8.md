# Auditoria do site Smart Pix: v7.1 → v8

**Escopo:** as 5 páginas do site (`site/`), avaliadas por três lentes:

1. Design no padrão Apple: movimento, materiais, tipografia e hierarquia.
2. Estratégia de vendas B2B: conversão, objeções e caminho até o pedido.
3. O segmento da Smart Pix: cenografia e montadoras, agências e produtoras, e empresas.

Status de cada item: **Aplicado** (já está na v8) ou **Pendente**. Um item fica pendente quando depende de informação ou material que só a Smart Pix tem.

## Resumo

A v7.1 já resolvia o essencial:
- abre com a marca;
- tem visual Apple;
- tem orçamento estruturado pelo WhatsApp.

O que faltava era **vender para o cliente principal** e **tirar atrito do pedido**:
- a empresa de cenografia ou agência não tinha entrada própria na home;
- o caminho "como peço" não aparecia;
- no celular, o botão de envio sumia durante o formulário;
- o site apontava para um domínio que a empresa ainda não usa.

A v8 corrige isso sem adicionar ruído visual.

O maior ganho que ainda falta não é de código. É ter **fotos reais e alguns números confirmados**; a lista do que fotografar está no fim deste documento.

## 1. Design no padrão Apple

| # | Achado | Princípio | Ação | Status |
|---|---|---|---|---|
| A1 | O título principal era só "Smart Pix"; a frase "Impressão digital em grande formato" ficava fora do título. | Clareza: o mais importante tem que ser o mais óbvio. | O título passa a ser "Smart Pix · Impressão digital em grande formato.", com o mesmo visual. | Aplicado |
| A2 | O 3D (cerca de 150 KB) carregava assim que a página abria, mesmo para quem não descia até o estúdio. | Resposta: nada que não seja essencial no caminho de quem chega. | O 3D só carrega quando o estúdio está perto de aparecer na tela ou quando a pessoa toca no campo da marca. | Aplicado |
| A3 | A imagem principal e a fonte do título não eram carregadas primeiro. | Resposta. | A imagem principal e as fontes 400 e 700 passam a carregar antes do resto. | Aplicado |
| A4 | As seções apareciam sem nenhuma transição. | Ofício: movimento natural, nunca enfeite. | Os títulos e cartões sobem 1,5 rem com fade ao entrar na tela. Tudo é desligado com "reduzir movimento". | Aplicado |
| A5 | Na página Soluções, a barra de navegação local não tinha a ação principal. A Apple sempre põe "Comprar" na barra local. | Familiaridade. | Botão "Pedir orçamento" fixo à direita da barra (no computador). | Aplicado |
| A6 | O degradê da barra de atalhos de Soluções apagava também o botão. | Ofício. | O degradê agora vale só para a lista de atalhos. | Aplicado |
| A7 | No estúdio 3D, o botão dizia sempre "Orçar este estande". | Feedback: confirmar o que a pessoa fez. | Depois de digitar, o botão vira "Orçar o estande Aurora" (com a marca digitada). | Aplicado |
| A8 | No celular, o envio do orçamento ficava no fim da página, longe do polegar. | Flexibilidade: celular é toque rápido. | Uma barra translúcida com "Enviar pelo WhatsApp" acompanha o formulário. Ela some quando o resumo do pedido aparece na tela. | Aplicado |
| A9 | Não havia página de erro (404). | Orientação: nunca deixar a pessoa perdida. | Página 404 com links para o início e para o orçamento. | Aplicado |
| A10 | Os efeitos de "antes e depois" antigos continuavam no código, sem uso. | Propósito: decidir o que não construir. | Código removido. | Aplicado |

## 2. Estratégia de vendas

| # | Achado | Por que importa | Ação | Status |
|---|---|---|---|---|
| V1 | O cliente principal (cenografia e agências) não tinha um bloco na grade da home. "Materiais" ocupava esse lugar. | Em B2B, o comprador recorrente precisa se reconhecer em segundos. | O bloco "Para cenografia e agências" substitui "Materiais" na home. "Materiais" continua em Soluções. | Aplicado |
| V2 | O topo da home falava com todos, mas não abria um caminho para o parceiro. | Separar o público logo no começo aumenta a conversão. | Link discreto no topo: "É de cenografia ou agência? Conheça a parceria". | Aplicado |
| V3 | "Como eu peço?" não tinha resposta visível. | Tirar a incerteza do primeiro contato diminui o abandono. | Os 3 passos ("Conte o projeto", "Receba o orçamento", "A gente produz e instala") aparecem no fim da home e de Projetos, junto com o horário de atendimento. | Aplicado |
| V4 | A página Projetos terminava sem nenhum chamado para orçar. | Toda página precisa terminar numa ação. | Fechamento "Tem um projeto parecido?" com os 3 passos. | Aplicado |
| V5 | A página Cenografia só tinha o formulário como saída. | Montadoras preferem falar direto pelo WhatsApp. | Botão "Mandar pelo WhatsApp" ao lado de "Montar o pedido". | Aplicado |
| V6 | Cada solução aparecia sozinha. | Vender junto (lona com piso, letra-caixa com vitrine) aumenta o valor do pedido. | Linha "Combina com…" em cada solução. | Aplicado |
| V7 | O FAQ não respondia a três dúvidas comuns antes de pedir. | Responder a objeção antes de ela virar pergunta. | Novas perguntas: "Só a impressão, sem instalação?", "Como envio a arte?" e "Vocês ajudam a escolher o material?". As respostas usam só fatos que o site já afirma. | Aplicado |
| V8 | Não há prazo médio de resposta nem de produção. | É o primeiro critério de quem trabalha com data de montagem. | Não publicamos sem a confirmação da Smart Pix. | Pendente |
| V9 | Não há prova social: casos, números, avaliações. | Sem marcas de clientes, a prova precisa ser número, foto real e avaliação. | Ver as pendências abaixo. | Pendente |
| V10 | Os eventos de medição já estão no código, mas não há conta conectada. | Sem medir, não dá para saber de onde vêm os pedidos. | Basta configurar `GTM_ID` no build, e o Google Tag Manager entra em todas as páginas. | Pendente (ID) |

## 3. Busca, publicação e técnica

| # | Achado | Ação | Status |
|---|---|---|---|
| T1 | O canonical e o sitemap apontavam para `smartpix.com.br`, um domínio que a empresa ainda não usa. | O endereço passa a ser configurável (`SITE_URL`). Hoje aponta para o GitHub Pages. | Aplicado |
| T2 | Um piloto com textos ainda não aprovados não deve aparecer no Google. | `noindex` em todas as páginas até `INDEXAR=1`. | Aplicado |
| T3 | `sitemap.xml`, `robots.txt` e `llms.txt` eram escritos à mão. | Passam a ser gerados no build a partir de `SITE_URL`. | Aplicado |
| T4 | A página Soluções não tinha dados estruturados dos serviços. | Catálogo de serviços (`OfferCatalog`) em Soluções. | Aplicado |
| T5 | O perfil no Google (Google Meu Negócio) ainda não existe ou não está ligado ao site. | Criar ou atualizar o perfil com o mesmo nome, endereço e telefone do site. | Pendente |

## Pendências para a Smart Pix

**Informações (sem elas o site não pode afirmar):**
1. Prazo médio de resposta ao orçamento e prazo padrão de produção.
2. Se a equipe de instalação é própria. O site afirma isso, mas só a frota própria está confirmada.
3. Cidades atendidas para entrega e instalação.
4. Entrega sem a identificação da Smart Pix para clientes de agências.
5. Montagem à noite ou em fim de semana.
6. Ano de fundação e outros números verdadeiros: largura máxima por material, área do galpão, quantidade de máquinas.
7. Telefone fixo (11) 2427-3880 e Instagram @smartpixoficial.
8. Domínio do site e ID do Google Tag Manager.
9. Link das avaliações no Google, se houver.

**Fotos e vídeos para produzir.** Nenhum quadro pode mostrar marca de cliente, e quem aparecer precisa autorizar o uso da imagem.
1. Galpão em plano aberto, com as impressoras ligadas e luz natural.
2. Close da impressora UV LED imprimindo (para a abertura do site).
3. Uma lona de 5 m saindo da máquina ou estendida inteira, sem emenda.
4. Equipe instalando num pavilhão ou numa loja, de costas ou com autorização.
5. Van da Smart Pix carregada, com a marca visível.
6. Amostras de material lado a lado: lona, tecido, ACM, adesivo e piso.
7. Fachada da empresa.
8. Vídeo vertical de 10 a 15 segundos com a lona saindo da impressora, para o site e o Instagram.
9. Dois ou três casos sem citar o cliente: segmento, tamanho e prazo.

## Fora do site (vendas)

- **WhatsApp Business:** respostas rápidas para as perguntas do FAQ, etiquetas por perfil (cenografia, agência, empresa) e catálogo com as soluções.
- **Velocidade:** a mensagem do site já chega organizada (perfil, peças, medidas, data e local). Responder no mesmo dia, dentro do horário, é o que mais converte.
- **Acompanhamento:** retomar o orçamento enviado em 2 dias úteis se não houver resposta.
- **Indicação:** perguntar a todo cliente de cenografia se ele indicaria um colega. No B2B, indicação costuma ser um dos canais mais fortes para parceiros novos.
