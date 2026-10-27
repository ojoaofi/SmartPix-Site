# Site Smart Pix

Site institucional da Smart Pix Impressão Digital (Atibaia, SP): impressão digital em grande formato, cenografia e instalação.

## Estrutura

- `site/`: o site publicado (5 páginas estáticas: início, soluções, cenografia e agências, projetos, orçamento).
  - `build.py`: gera os 5 `.html` a partir dos dados e modelos. **Edite aqui, não nos `.html`.**
  - `css/site.css`: estilos (padrão minimalista apple.com).
  - `js/`: `site.js` (molas, menu, barra que muda de tom, galerias), `studio.js` (estúdio 3D), `problems.js` (galeria de problemas), `quote.js` (orçamento em 2 etapas → WhatsApp/e-mail), `projects.js` (filtros e detalhe dos projetos).
  - `img/`, `fonts/`: imagens (ilustrações IA marcadas + fotos reais) e fontes locais.
  - `robots.txt`, `sitemap.xml`, `llms.txt`: SEO e buscadores de IA.
- `design-system/`: sistema de design da marca (cores, tipografia, componentes, logo).

## Rodar localmente

```bash
cd site
python3 build.py          # gera os .html
python3 -m http.server 8000
# abra http://localhost:8000
```

## Pendências para confirmar com a Smart Pix

- Equipe de instalação própria (o site afirma; só a frota própria está confirmada).
- Cidades atendidas para entrega e instalação.
- Entrega sem a identificação da Smart Pix para clientes de agências.
- Prazo médio de resposta e de produção; montagem à noite ou em fim de semana.
- Telefone fixo (11) 2427-3880 e Instagram @smartpixoficial.
- Fotos reais de qualidade para substituir as ilustrações de IA.
