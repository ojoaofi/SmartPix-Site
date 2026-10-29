# Pesquisa de mercado e conversão: Smart Pix

**Data:** 29/10/2026. **Escopo:** como o comprador B2B escolhe gráfica de grande formato e produção para cenografia no Brasil, o que os sites do setor mostram, palavras-chave e metadados das 5 páginas, textos propostos, FAQ e Google Meu Negócio.

**Método e limites.** Cerca de 28 buscas na web (pt-BR, foco em São Paulo e interior). O WebFetch estava bloqueado no ambiente (não abriu `mckinsey.com.br` nem `support.google.com`), então tudo vem dos resumos das buscas. A leitura dos sites concorrentes se baseia nesses resumos, não numa revisão página a página. Não houve acesso a volume de busca (Planejador de Palavras-chave ou Search Console): as prioridades de palavra-chave são qualitativas e precisam ser validadas depois do `INDEXAR=1`. Os textos "atuais" citados são os do `site/build.py` em 29/10/2026, que outros agentes estão editando ao mesmo tempo.

Regra usada em todo o documento: só fatos confirmados (CLAUDE.md). Tudo que depende de dado não confirmado aparece como **Pendência** com o dado que falta.

---

## 1. Resumo

1. **"5 m sem emenda" não é exclusivo.** Pelo menos uma gráfica da capital paulista anuncia lona em peça única de até 5 m de largura. Outra anuncia 3,20 m. O 5 m continua sendo prova forte (licitações públicas ainda aceitam lona grande com emenda soldada e backdrop de 10 × 1 m montado com 3 lonas), mas não sustenta a venda sozinho. O diferencial defensável é a **combinação**: lona, tecido, piso, ACM, PVC, adesivo e 3D **num pedido só**, com **frota própria** e a cerca de 65 km de São Paulo.
2. **O comprador principal está perto e cresce.** Em 2025 a capital teve 1.511 eventos B2B de grande porte (+22% sobre 2024) e mais de 250 feiras; a cidade concentra cerca de 70% desse mercado no país (Ubrafe/SPTuris). Cenografia e montadoras são a página de maior valor do site.
3. **O risco do montador é o pavilhão, não a impressão.** Os regulamentos de montagem têm janelas fixas (por exemplo, 8h às 20h; circulação vedada depois das 18h30; caminhões de montadora só depois das 13h no primeiro dia de desmontagem). Os bombeiros e as organizadoras pedem que tecidos e acabamentos tenham laudo ou certificado de retardância de chamas. Uma montadora concorrente já anuncia esses laudos. O site da Smart Pix não fala disso. **Pendência:** a Smart Pix fornece ficha técnica ou laudo do fabricante do material?
4. **O comprador quer decidir antes de falar com alguém.** 61% dos compradores B2B preferem comprar sem vendedor (Gartner, 2025; 67% na edição de 2026), e 69% veem diferença entre o que o site diz e o que o vendedor diz. O site precisa responder prazo, preço, regras do pavilhão e sigilo **antes** do WhatsApp.
5. **Velocidade fecha.** Empresas que respondem um lead em até 1 hora têm cerca de 7 vezes mais chance de qualificá-lo (HBR, 2011). No Brasil, 75% dos vendedores preferem o WhatsApp para o primeiro contato (RD Station, 2025). O site já entrega a mensagem pronta no WhatsApp. Falta **publicar o prazo de resposta**. **Pendência:** prazo médio de resposta.
6. **"Smart Floor" não é buscado.** Ninguém pesquisa o nome de um produto que não conhece. Todo título e metadado precisa do termo genérico ao lado: **piso impresso**. Use "piso adesivado" só se o Smart Floor for de fato um adesivo de piso. **Pendência:** o Smart Floor é manta vinílica impressa ou adesivo laminado?
7. **Instalação ainda aparece como oferta.** Os textos de reserva do `inst()` (usados quando `instalacao_propria=False`) ainda dizem "A gente instala", "a instalação entra no mesmo pedido" e "Montagem no local". O CTA final diz "A gente produz e instala". Só a frota está confirmada. Até a Smart Pix confirmar se oferece instalação, própria ou com parceiro, o padrão seguro é o que o site já usa em Vitrines: **"sob consulta"**.
8. **O Google Meu Negócio é o maior canal local que falta.** A categoria principal e a consistência do nome, endereço e telefone pesam mais que qualquer texto do site para "gráfica Atibaia" e "gráfica perto de mim".

---

## 2. Como o comprador escolhe

### Cenografia e montadoras de estande (maior valor, pedido recorrente)

| Critério | O que o comprador quer ver | Como o site da Smart Pix está | Ação |
|---|---|---|---|
| Cumprir a data e a janela de montagem | Prazo de produção, data e hora de entrega no pavilhão | "Prazo confirmado no orçamento" (correto, sem promessa) | Publicar prazo de resposta e prazo típico por tipo de peça. **Pendência:** prazos |
| Peça sem emenda na medida do projeto | Largura máxima por material | Só a lona (5 m) | **Pendência:** largura máxima de tecido, adesivo e piso |
| Cor igual entre substratos | Lona, tecido e adesivo da mesma produção; prova de cor | Card "A cor muda de uma peça para outra" | Manter. **Pendência:** a Smart Pix faz prova de cor ou amostra física? |
| Um fornecedor para tudo | Lona, tecido, piso, rígidos, 3D | Bem coberto ("Um pedido só") | Dar mais destaque: é o diferencial real (item 1 do Resumo) |
| Documentos do pavilhão | Laudo de retardância de chamas do tecido e da lona; ficha técnica | Ausente | Pôr no checklist "O que mandar" e no FAQ. **Pendência:** laudos |
| Entrega no pavilhão | Frota, horário de doca, credenciamento | "Entrega no pavilhão com frota própria" | **Pendência:** entrega à noite ou no fim de semana; cidades e pavilhões atendidos |
| Montagem ou só entrega | Opção clara | Texto ainda promete montagem | Trocar por "Montagem sob consulta". **Pendência:** instalação (própria ou parceira); trabalho em altura (NR-35) |
| Atendimento técnico rápido | Alguém que entenda arquivo, escala e sangria pelo WhatsApp | Mensagem pronta, sem prazo de resposta | **Pendência:** especificação de arquivo (formato, escala, resolução, perfil de cor) |
| Preço comparável | Concorrência com o mesmo briefing | Formulário estruturado (bom para isso) | FAQ "Como é calculado o preço" |

### Agências e produtoras

1. **Sigilo.** A produção terceirizada não pode aparecer para o cliente final. O site diz "identificação da entrega conversada no orçamento": correto, mas fraco. **Pendência:** entrega sem a identificação da Smart Pix. Com confirmação, o texto vira "Entrega sem a nossa marca".
2. **Um contato só**, do arquivo à entrega. O site já diz "Um responsável do pedido à entrega".
3. **Prova para mostrar ao cliente:** foto real da peça, amostra de material. **Pendência:** fotos e amostras.
4. **Faturamento:** nota para a agência ou para o cliente final. **Pendência:** como a Smart Pix fatura.

### Empresas (eventos, lojas, fachada, frota)

1. **Atende a minha cidade? Instala?** **Pendências:** cidades atendidas e instalação.
2. **Dura quanto tempo na rua?** **Pendência:** durabilidade por material (o site só pode dizer que indica o material pelo uso).
3. **Fachada:** quem cuida da regra da prefeitura? Na capital, a Lei Cidade Limpa limita o anúncio indicativo (por exemplo, até 10 m² por anúncio em imóvel de testada pequena), e a prefeitura dobrou as multas em 2025. **Pendência:** a Smart Pix orienta ou cuida da licença?
4. **Frota:** quanto tempo o veículo fica parado; a remoção danifica a pintura? **Pendências:** tempo de aplicação; aplicação própria.
5. **Rede de lojas:** a mesma campanha igual em todas. O site já cobre isso bem.

---

## 3. O que os melhores sites fazem (anonimizados)

| Site | O que mostra bem | O que falta |
|---|---|---|
| Gráfica A, SP capital | Especificação no topo: lona em peça única de até 5 m. Aplicações listadas (palco, empena, feira, tapume, fachada). Backdrop em tecido ou lona. Atende montadoras | Prazo de resposta, como pedir, sigilo para agência |
| Gráfica B, SP capital | Números técnicos: largura sem emenda de 3,20 m, resolução 1440 dpi, materiais | Diferencial além da máquina |
| Montadora C, SP zona norte | Documentos de pavilhão: ART e laudo de retardância de chamas para tecidos. Tecido tensionado. Entrega antecipada com prazo em horas | Não é gráfica: terceiriza parte da impressão |
| Gráfica D, SP capital | Atendimento 24h (urgência como posicionamento) | Detalhe técnico |
| Gráfica E, SP capital | Tempo de mercado (mais de 35 anos) como prova | Público B2B de eventos |
| Cenografia F, SP | Projeto 3D, impressão e aplicação no mesmo fornecedor; atendimento nacional | Preço e prazo |
| Fornecedor G, displays, SP | Guia longo B2B por produto (conteúdo que ranqueia) | Orçamento rápido |
| Gráfica H, SP | Artigo "onde fazer impressão em lona para eventos em SP" (capta a busca local informacional) | Página de produto fraca |
| Gráfica I, SP capital | Página por produto + cidade ("lonas em grandes formatos SP") | Prova real |

**Padrão do setor.** Os sites vendem a máquina (largura, dpi) ou o tempo de casa. Quase nenhum dos que apareceram mostra: (1) prazo de resposta com número; (2) como pedir, em passos, e o que mandar; (3) sigilo explícito para agência; (4) um formulário que vira mensagem pronta; (5) foto real com escala (a lona de 5 m inteira); (6) a combinação de materiais num pedido, escrita como benefício.

**Onde a Smart Pix já ganha:** itens 2, 4 e 6. **Onde pode ganhar com dado confirmado:** itens 1, 3 e 5, mais os laudos do pavilhão, que hoje só uma montadora anuncia.

---

## 4. Palavras-chave e metadados por página

Prioridade qualitativa: **A** = intenção de compra clara e aderente ao que a Smart Pix vende; **B** = apoio. Validar volume e posição no Search Console 30 dias depois do `INDEXAR=1`.

### Termos por página

| Página | Primárias (A) | Secundárias (B) |
|---|---|---|
| Início | gráfica Atibaia; gráfica de grande formato Atibaia; comunicação visual Atibaia; impressão digital Atibaia | impressão em lona Atibaia; impressão UV grande formato; gráfica perto de São Paulo |
| Soluções | lona sem emenda; backdrop em lona; letra-caixa em ACM; fachada em ACM; envelopamento de frota; piso impresso para eventos | painel de lona para palco; lona backlight; letra-caixa acrílico; adesivo de vitrine; material de PDV; adesivação de veículos; plotagem de frota; impressão 3D para cenografia; impressão em tecido; PVC expandido |
| Cenografia e agências | gráfica para montadoras; impressão para estandes; produção gráfica para cenografia; gráfica para agências; gráfica terceirizada | impressão para feiras e eventos; gráfica para eventos São Paulo; gráfica white label; piso para estande |
| Aplicações (projetos) | comunicação visual para feiras; backdrop para evento corporativo; cenografia para eventos | vitrine adesivada; envelopamento de vans; piso para palco |
| Orçamento | orçamento de lona; orçamento de backdrop; orçamento de letra-caixa; orçamento de envelopamento de frota | preço de lona impressa por m² (a página explica do que o preço depende, sem tabela) |

**Busca local.** O endereço confirmado é Atibaia: só Atibaia entra nos metadados agora. Bragança Paulista (25 km), Jundiaí (cerca de 60 km), Campinas (65 a 79 km, conforme a fonte) e Grande SP entram **depois** de a Smart Pix confirmar as cidades atendidas (**pendência**). Quando entrarem: uma seção única "Onde entregamos" com as cidades confirmadas e a mesma lista na área de serviço do Google Meu Negócio. Evite páginas finas por cidade, que o Google trata como páginas de entrada (*doorway*).

**Regras aplicadas.** Title até 60 caracteres e description até 155, com termo de busca primeiro e marca no fim. Uma descrição diferente por página. Nenhuma lista de palavras-chave solta. O Google ignora a description quando ela é só uma lista de termos.

### Metadados propostos (contados)

| Página | Title (caracteres) | Meta description (caracteres) |
|---|---|---|
| Início | Gráfica de grande formato em Atibaia, SP \| Smart Pix (52) | Impressão UV LED em Atibaia, perto de São Paulo: lona até 5 m sem emenda, piso impresso, estandes, letras-caixa e frota. Orçamento pelo WhatsApp. (145) |
| Soluções | Lona sem emenda, piso impresso e letra-caixa \| Smart Pix (56) | Lona e backdrop até 5 m sem emenda, piso impresso, estandes, letras-caixa em ACM, vitrines, envelopamento de frota e impressão 3D. Em Atibaia, SP. (146) |
| Cenografia e agências | Gráfica para montadoras, cenografia e agências \| Smart Pix (58) | Produção gráfica de estandes e palcos: lona até 5 m sem emenda, tecido, piso, ACM, PVC e 3D num pedido só. Entrega no pavilhão com frota própria. (145) |
| Aplicações | Aplicações: estandes, palcos, vitrines e frota \| Smart Pix (58) | Estandes, palcos, pisos, vitrines, fachadas e frota: veja onde a Smart Pix entra no seu projeto e peça orçamento de um parecido. Atibaia, SP. (141) |
| Orçamento | Orçamento de lona, estande e letra-caixa \| Smart Pix (52) | Peça orçamento de lona, piso, estande, letra-caixa ou envelopamento. Informe medidas, data e local e envie pelo WhatsApp ou e-mail. Seg a sex, 8h às 18h. (153) |

Atuais em 29/10: Início "Smart Pix | Impressão digital e cenografia em Atibaia, SP" (57); Soluções 62 caracteres (passa do limite); Cenografia "Produção gráfica para cenografia e montadoras | Smart Pix" (57, sem "agências" nem "gráfica"); Aplicações e Orçamento ok, mas sem "estandes" e com "Smart Pix Atibaia" repetindo a marca.

---

## 5. Textos propostos por página

Voz: títulos curtos com ponto final, frases curtas, "você", sem ponto de exclamação, sem emoji, sem superlativo. Formato: **bloco › texto atual → texto novo**. Onde a Smart Pix ainda vai confirmar instalação, o texto novo vale para `CONFIRMADO['instalacao_propria']=False` (o texto "sim" do `inst()` continua como está).

### Global
- Menu › "Problemas" → **"Como resolvemos"** (v9 D10).
- `cta_end` › passo 3 "A gente produz e instala" → **"A gente produz e entrega"** (a linha de apoio "Impressão em Atibaia, entrega com frota própria." fica).
- `cta_end` › passo 2, só depois de confirmar o prazo: "Pelo WhatsApp ou por e-mail, de segunda a sexta, das 8h às 18h." → "Em até X horas úteis, pelo WhatsApp ou por e-mail." **Pendência:** X.
- Padrão para instalação enquanto não houver confirmação: **"Montagem sob consulta"** ou **"Instalação sob consulta"**, igual ao que Vitrines já usa.

### Início
- Hero › nota "Para eventos, cenografia e empresas. Em Atibaia, SP." → **"Para cenografia, agências e empresas. Em Atibaia, a 65 km de São Paulo."** A ordem segue o valor de cada público e o menu. Os 65 km são distância pública (IBGE e rota rodoviária), não dado da empresa; se preferir, use "perto de São Paulo".
- Bloco XL Smart Floor › linha "O chão também comunica." → **"Piso impresso. O chão também comunica."** Sem isso, quem chega não sabe o que é Smart Floor.
- Para quem › Empresas "…com um fornecedor só, do arquivo à instalação." → **"…com um fornecedor só, do arquivo à entrega."**
- Quem somos › passo 04 "Entrega e instalação" / "A frota própria leva até o local, e a instalação entra no mesmo pedido." → **"Entrega"** / **"A frota própria leva até o local. Montagem sob consulta."**
- Problemas › card `instalacao`: o título "A gráfica entrega, mas não instala" pressupõe instalação própria. Trocar o card inteiro:
  - título → **"A entrega depende de terceiros"**
  - problema → **"A gráfica despacha por transportadora, e o material chega ao pavilhão sem hora certa, no meio da janela de montagem."**
  - solução → **"Frota própria: o material sai do nosso galpão direto para o local."**
  - curto (`SHORT`) "A gente leva e monta." → **"Do galpão direto para o local."**
- FAQ › "Vocês fazem a instalação?" → resposta "Sim. A entrega é com frota própria e a instalação pode entrar no mesmo pedido…" → **"A entrega é com frota própria. Se precisar de montagem, informe o local e a janela no orçamento, e a gente confirma."**
- FAQ › "Onde vocês atendem?" → resposta **"A produção fica em Atibaia, a 65 km de São Paulo. Informe a cidade e o local no orçamento."**
- FAQ › "Posso pedir só a impressão, sem instalação?" → resposta **"Sim. No orçamento, escolha "Só a produção" para a sua equipe montar."**
- FAQ › acrescentar as 4 perguntas da seção 6.

### Soluções
- Lona › bullet 4 "Entrega com frota própria e montagem no mesmo pedido" → **"Entrega com frota própria"**.
- Smart Floor › kicker "Smart Floor" → **"Smart Floor · piso impresso"**. Bullet 4 "Instalação no mesmo pedido" → **"Instalação sob consulta"**.
- Cenografia › bullet 4 "Montagem no local, se você precisar" → **"Montagem sob consulta"**.
- Letras-caixa › bullet 3 "Produção própria e instalação no mesmo pedido" → **"Produção própria. Instalação sob consulta"**.
- Frota › linha "Envelopamento de carros, vans e caminhões, da impressão à aplicação." → **"Envelopamento e adesivação de carros, vans e caminhões."** Isso acrescenta o termo buscado sem afirmar a aplicação. Bullet "Impressão e aplicação num pedido só" → **"Aplicação sob consulta"**. **Pendência:** aplicação própria.

### Cenografia e agências
- Topo › linha de apoio "Para quem projeta e monta estandes, palcos e ativações e precisa de uma produção gráfica que respeite a janela do pavilhão." → **"Lona, tecido, piso, ACM, PVC e peças 3D para estandes, palcos e ativações. Num pedido só, entregue no pavilhão."**
- Por que terceirizar › lead "…Por isso, a mesma empresa produz, entrega e instala." → **"…Por isso, a mesma empresa produz e entrega, com frota própria."**
- Cartões › "Montagem ou só entrega" / "A gente instala, ou entrega para a sua equipe montar." → **"Pronto para a sua equipe"** / **"O material chega pronto para montar. Montagem sob consulta."**
- Cartões › "Perto de São Paulo" → **"A 65 km de São Paulo"** (texto de apoio igual). Opcional.
- Passos › 04 "Entrega ou montagem" / "No pavilhão, com a nossa frota. A montagem entra no pedido, se você quiser." → **"Entrega"** / **"No pavilhão, com a nossa frota. Montagem sob consulta."**
- Agências › acrescentar à lista: **"Lona, tecido, piso, ACM, PVC, adesivo e 3D num pedido só"**. Com a pendência de sigilo confirmada: "Identificação da entrega conversada no orçamento" → "Entrega sem a nossa marca".
- O que mandar › acrescentar **"Regras do pavilhão: horário de entrega e documentos do material"**. Trocar "Se precisa de instalação" → **"Se precisa de montagem"**.
- Novo bloco curto de dúvidas antes do fechamento, com 4 perguntas: prazo, regras do pavilhão, só algumas peças, identificação da entrega. O montador decide nesta página; hoje o FAQ fica só na Home.

### Aplicações
- Card `montagem` › título "Montagem no local" → **"Entrega no local"**; linha → **"Do nosso galpão direto para o local, com frota própria."**; bullets → **"Frota própria"**, **"Eventos, lojas e fachadas"**, **"Montagem sob consulta"**.
- Card `corporativo` › bullet "Montagem na janela do evento" → **"Entrega com frota própria"**.
- Card `frota` › bullet "Impressão e aplicação próprias" → **"Aplicação sob consulta"**.
- Assim que houver 3 casos reais sem cliente (segmento, medida, prazo): um bloco "Casos" no topo. **Pendência:** casos.

### Orçamento
- Detalhes › placeholder "Ex.: dois backdrops, piso para o palco e montagem na véspera do evento" → **"Ex.: dois backdrops e piso para o palco. Horário de entrega do pavilhão e documentos que ele pede."**
- "Como nos conheceu?" › acrescentar **"Google Maps"** (mede o Google Meu Negócio).
- Contatos › o telefone fixo só aparece com `CONFIRMADO['telefone_fixo']=True` (já previsto no build).

---

## 6. FAQ propostas e objeções

### Objeções que o FAQ precisa responder antes do primeiro contato

| # | Objeção | Dá para responder hoje? | Dado que falta |
|---|---|---|---|
| 1 | "Dá tempo para a minha data?" | Sim, como processo (o prazo é confirmado no orçamento) | Prazo de resposta e de produção |
| 2 | "Quanto custa? Tem pedido mínimo?" | Sim, sobre do que o preço depende | Pedido mínimo, se houver |
| 3 | "O material passa nas regras do pavilhão?" | Sim, como processo | Laudo ou ficha técnica de retardância de chamas |
| 4 | "Vocês fazem o estande inteiro ou só peças?" | Sim (parte gráfica completa ou só peças) | Se a Smart Pix faz estrutura (marcenaria, metal) |
| 5 | "Vocês montam?" | Só "sob consulta" | Instalação própria ou parceira; NR-35 |
| 6 | "Entregam na minha cidade? À noite? No fim de semana?" | Só "informe no orçamento" | Cidades; horários |
| 7 | "Meu cliente vai ver a sua marca?" | Parcial ("conversada no orçamento") | Entrega sem identificação |
| 8 | "Em que formato mando a arte?" | Parcial (canal: WhatsApp ou e-mail) | Formato, escala, resolução, perfil de cor |
| 9 | "A cor vai sair igual?" | Parcial (mesma produção) | Prova de cor ou amostra |
| 10 | "Como é a nota e o pagamento?" | Não | Faturamento, sinal, prazo de pagamento |
| 11 | "Quanto dura na rua?" | Parcial (indicamos pelo uso) | Durabilidade por material |
| 12 | "Vocês cuidam da licença da fachada?" | Não | Se orienta ou cuida da licença |

### Perguntas novas (prontas, só com fatos confirmados)

1. **Qual é o prazo?**
   Depende do tamanho do pedido e da data. Informe a data do evento ou da entrega no orçamento: o prazo é confirmado antes de você fechar.
2. **Quanto custa?**
   O valor depende da medida, do material, da quantidade, do acabamento e do local de entrega. Informe esses dados no orçamento, e a gente responde com o preço.
3. **O material atende às regras do pavilhão?**
   Cada pavilhão tem as suas regras. Mande o manual do expositor ou a lista de exigências junto com o pedido, e a gente confirma no orçamento.
   (Quando a Smart Pix confirmar os laudos, a resposta passa a ser afirmativa.)
4. **Vocês fazem o estande inteiro ou só algumas peças?**
   Os dois. A gente produz a parte gráfica completa (lona, tecido, piso, ACM, PVC, adesivo e peças em impressão 3D) ou só as peças de que você precisa.

Reserva (conhecimento de material, sem afirmação sobre a empresa):

5. **Qual a diferença entre lona e lona backlight?**
   A lona backlight é feita para receber luz por trás, em painéis iluminados. A lona comum é para peças sem luz interna. Na dúvida, conte o uso da peça.

---

## 7. Google Meu Negócio (Perfil da Empresa no Google)

Pré-requisito: resolver a pendência do telefone fixo (v9 C2), porque nome, endereço e telefone precisam ser iguais no perfil, no rodapé e no JSON-LD.

| Campo | O que preencher |
|---|---|
| Nome | **Smart Pix Impressão Digital**, exatamente como no site. Sem "Gráfica Atibaia" nem slogan: palavra-chave no nome viola as diretrizes e pode suspender o perfil |
| Categoria principal | **Gráfica**. É a que casa com "gráfica Atibaia" e "gráfica perto de mim". Alternativa, se o editor mostrar: **Serviço de impressão digital** |
| Categorias adicionais (poucas, só as que descrevem o negócio) | **Serviço de impressão digital**; **Loja de placas e letreiros** ou o rótulo equivalente para *sign shop* (letras-caixa, fachadas); **Serviço de envelopamento de veículos** (rótulo visto num perfil ativo em SP); **Serviço de impressão 3D**. Os rótulos exatos em pt-BR precisam ser conferidos no editor do perfil, que é a lista oficial. Não use categoria de montadora de estandes: a Smart Pix produz a parte gráfica (**pendência:** se faz estrutura) |
| Endereço | Av. São Paulo, 111, Alvinópolis, Atibaia, SP (visível; o galpão recebe a verificação) |
| Área de serviço | Só depois de confirmar as cidades atendidas (**pendência**) |
| Horário | Seg a sex, 8h às 18h. Atualizar nos feriados |
| Telefone principal | (11) 91010-1324. Fixo só depois da confirmação |
| Site | URL do site com UTM: `?utm_source=google&utm_medium=organic&utm_campaign=perfil-google`, para separar no GA4 o que vem do perfil |
| Serviços | Os 7 do site, cada um com uma linha: Lona e backdrop até 5 m sem emenda; Smart Floor, piso vinílico impresso; Cenografia e estandes (parte gráfica); Letras-caixa e fachadas em ACM e acrílico; Vitrines e PDV; Envelopamento de frota; Impressão 3D |
| Descrição (até 750 caracteres) | Texto pronto abaixo |
| Fotos | Só fotos reais: fachada, galpão, impressora UV LED, lona de 5 m estendida, Smart Floor instalado, van. Sem marca de cliente e sem ilustração IA: o perfil é prova, não vitrine |
| Avaliações | Pedir a todo cliente depois da entrega, com o link direto de avaliação (WhatsApp, resposta rápida pronta). Responder todas. Não oferecer nada em troca, porque o Google proíbe incentivo |
| Atualizações | Uma por mês com foto real de um trabalho (sem marca de cliente) |
| Mensagens | O chat do Google foi descontinuado em 2024. O contato vai pelo WhatsApp do botão e do site |
| Site ↔ perfil | Depois de criar o perfil, apontar "Como chegar" (Orçamento) e o `hasMap` do JSON-LD para o link do perfil |

**Descrição pronta (661 caracteres):**

> A Smart Pix Impressão Digital produz comunicação visual em grande formato no próprio galpão, em Atibaia, SP. Imprime em UV LED lona e backdrop de até 5 m de largura sem emenda, piso vinílico impresso (Smart Floor), peças para cenografia e estandes, letras-caixa e fachadas em ACM e acrílico, adesivos de vitrine e PDV, envelopamento de frota e impressão 3D. Materiais: lona, lona backlight, tecido, ACM, PVC expandido, adesivo vinil e piso vinílico. Atende empresas de cenografia e montadoras, agências e produtoras, e empresas. Entrega com frota própria. Orçamento pelo WhatsApp (11) 91010-1324 ou por atendimento@smartpix.com.br, de segunda a sexta, das 8h às 18h.

**O que pesa no ranking local** (consenso de guias de SEO; o Google não publica os pesos): relevância (categoria principal, serviços, descrição), distância (endereço) e proeminência (avaliações, links, citações). A categoria principal é um dos fatores de maior peso.

---

## 8. Pendências para a Smart Pix (acréscimos às do v8 e do v9)

1. A Smart Pix oferece instalação? Com equipe própria ou parceira? Faz trabalho em altura (NR-35)? Aplica o envelopamento?
2. Prazo médio de resposta ao orçamento; prazo típico por tipo de peça; atende urgência?
3. Laudo ou ficha técnica de retardância de chamas dos materiais (lona, tecido, piso).
4. Largura máxima sem emenda de tecido, adesivo e piso.
5. O Smart Floor é manta vinílica impressa ou adesivo de piso laminado? (Define se o site pode usar "piso adesivado".)
6. Entrega sem a identificação da Smart Pix para agências; faturamento para a agência ou para o cliente final.
7. Cidades e pavilhões atendidos; entrega à noite ou no fim de semana.
8. Especificação de arquivo: formato, escala, resolução, sangria, perfil de cor.
9. Prova de cor ou amostra física; pedido mínimo; forma de pagamento.
10. A Smart Pix faz estrutura (marcenaria, metal) ou só a parte gráfica?
11. Fachada: orienta ou cuida da licença municipal?
12. Três casos reais sem cliente (segmento, medida, prazo) e fotos com escala (lona de 5 m inteira).

---

## 9. Fontes

Os sites de concorrentes (Gráficas A a I, Montadora C, Cenografia F, Fornecedor G) foram consultados pela busca em 29/10/2026. As URLs foram omitidas de propósito, pela regra de não citar concorrentes.

**Comportamento do comprador B2B**
- Gartner, 61% preferem compra sem vendedor; 69% veem diferença entre site e vendedor (jun. 2025): https://www.gartner.com/en/newsroom/press-releases/2025-06-25-gartner-sales-survey-finds-61-percent-of-b2b-buyers-prefer-a-rep-free-buying-experience
- Gartner, 67% (mar. 2026), cobertura: https://www.digitalcommerce360.com/2026/03/17/gartner-b2b-buyers-rep-free-purchasing-ai-reshapes-sales/
- HBR, "The Short Life of Online Sales Leads" (2011), resposta em até 1 hora e cerca de 7× mais qualificação: https://hbr.org/2011/03/the-short-life-of-online-sales-leads (citado por resumos secundários, como https://ainora.lt/blog/lead-response-time-statistics-every-study-2026)
- WhatsApp nas vendas no Brasil (RD Station 2025: 75% dos vendedores preferem o WhatsApp no primeiro contato): https://viniensina.com.br/whatsapp-vendas-brasil-2026/
- Agendor, uso do WhatsApp com empresas: https://www.agendor.com.br/blog/?p=54534
- Escolha de fornecedor para feiras (normas da feira, metodologia): https://www.ohub.com.br/mkt/feiras-e-estandes
- Concorrência com o mesmo briefing: https://gironews.com/opinioes/estrategias-de-marketing-para-feiras-de-negocios-57507/
- Calibração de cor como critério: https://mercadohoje.uai.com.br/2026/07/15/7-decisoes-de-comunicacao-visual-que-sustentam-a-marca/
- Prazo recomendado para a gráfica antes da feira (3 a 4 semanas): https://wavecnct.com/pt/blog/como-se-preparar-para-uma-feira-de-negocios-checklist-completo-para-sua-equipe-2026

**Mercado de eventos**
- Ubrafe/SPTuris, 1.511 eventos B2B de grande porte em SP em 2025 (+22%), R$ 14 bilhões: https://propmark.com.br/mercado/eventos-b2b-crescem-22-em-sao-paulo-e-movimentam-r-14-bilhoes-em-2025/
- Recorde de eventos em SP em 2025, mais de 250 feiras: https://mercadoeconsumo.com.br/20/02/2026/eventos/sao-paulo-bate-recorde-de-eventos-de-grande-porte-em-2025/

**Pavilhão: janelas, ART e laudos**
- Regulamento de montagem e cronograma de congresso em SP, 2026 (atendimento ao expositor das 8h às 20h): https://transparencia.cfo.org.br/wp-content/uploads/2025/11/REGULAMENTO-DE-MONTAGEM-E-CRONOGRAMA.pdf
- Regulamento de feira 2026 (caminhões de montadora a partir das 13h na desmontagem): https://tecnoshowcomigo.com.br/assets/pdf/regulamento-tecnoshow-2026.pdf
- Manual de feira (circulação vedada após 18h30): https://www.tecnoshowcomigo.com.br/_files/ugd/f3cf5f_6078b387ec3d41e1b9fe893bf56529b6.pdf
- Manual do expositor, ART ou RRT obrigatória no estande: https://nortenordeste.conasems.org.br/wp-content/uploads/2023/08/MANUAL-DO-EXPOSITOR_CONGRESSO.pdf
- Laudo antichamas para eventos e estandes (documentos exigidos): https://www.docparaeventos.com.br/post/laudo-antichamas-para-eventos-laudo-de-ignifuga%C3%A7%C3%A3o-para-stand-atestado-de-inabilidade-ou-retardant
- Tratamento antichamas de tecidos para aprovação de organizadora: https://antichamas.tensarte.com.br/

**Emenda e especificação em compras públicas**
- TRE-SP: lona de 18 × 3,5 m aceita com emenda soldada: https://www.tre-sp.jus.br/transparencia-e-prestacao-de-contas/licitacoes/aquisicao-contratacao-direta-covid-19/dispensas-de-licitacao-2020-1/termo-de-referencia-dlf-066-2020
- Memorial descritivo com backdrop de 10 × 1 m em 3 lonas: https://www.memorialdoimigrante.org.br/uploads/portal/gestao/compras_e_contratacoes/arquivos/descritivo-impressoes-cv-28fi-01-11-2023-21-35.docx
- TRE-GO 2026, especificação de backdrop em lona: https://www.tre-go.jus.br/transparencia-e-prestacao-de-contas/licitacoes-e-contratos/pregoes-eletronicos/arquivos/tre-go-pe-90014-2026-edital-etp-srp-aquisicao-banners-backdrops
- Laminação em vinil para piso de evento: https://ferax.com.br/?p=13927
- Guia de impressão digital (limites da tinta UV em material flexível): https://multimedia.3m.com/mws/media/1625265O/whitepaper-5-a-guide-to-digital-printing-portugese.pdf

**SEO e Google Meu Negócio**
- Google Search Central, snippets e meta description: https://developers.google.com/search/docs/advanced/appearance/snippet
- Google, como escolher a categoria: https://support.google.com/business/answer/7249669?hl=pt-br
- Diretrizes do perfil (nome sem palavra-chave): https://pt.semrush.com/blog/google-meu-negocio/ e https://www.seo.com/pt/blog/how-to-create-google-business-profile/
- Método de categoria para gráficas: https://thestacc.com/blog/print-shop-gbp-categories/
- Fatores de ranking local (relevância, distância, proeminência): https://collingmedia.com/?p=7740 e https://pushleads.com/google-business-profile/google-business-profile-mastery/

**Fachada e localização**
- Lei Cidade Limpa (Lei 14.223/2006): https://www.prefeitura.sp.gov.br/cidade/upload/lei_14_223_1254941069.pdf
- Prefeitura de SP, multas dobradas em 2025: https://prefeitura.sp.gov.br/web/subprefeituras/w/prefeitura-de-s%C3%A3o-paulo-dobra-n%C3%BAmero-de-multas-da-lei-cidade-limpa-nos-primeiros-sete-meses-de-2025
- IBGE, Atibaia (cerca de 65 km da capital): https://biblioteca.ibge.gov.br/visualizacao/dtb/saopaulo/atibaia.pdf
- Rota Atibaia–Bragança Paulista (25 km): https://www.emsampa.com.br/rotas_rodoviarias_IV/atibaia_braganca.htm
