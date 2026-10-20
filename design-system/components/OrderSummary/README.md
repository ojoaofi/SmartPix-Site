# OrderSummary

Resumo vivo do pedido, ao lado do configurador: itens, área total em m², aviso e o envio pelo WhatsApp.

`<aside class="sp-summary">` com `.sp-sum`: título `<h3>`, uma `<dl>` com os itens escolhidos, `.sp-total` (rótulo e valor), avisos `sp-notice` e o botão `sp-btn--fill sp-btn--block`.

- Fixo ao rolar (`position: sticky`) no computador; no fluxo, depois do formulário, no celular.
- Os valores vêm do formulário; mostre "—" no que ainda não foi respondido.
- Nunca mostre preço sem tabela confirmada pela empresa.
