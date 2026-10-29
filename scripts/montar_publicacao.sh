#!/usr/bin/env bash
# Monta a pasta publicada a partir de site/. Usada pelo workflow do GitHub Pages e pela verificação,
# para que a lista do que vai ao ar exista num lugar só.
# Uso (na raiz do repositório, depois de python3 site/build.py):
#   bash scripts/montar_publicacao.sh [destino]    # padrão: _site
# Publica: todas as páginas site/*.html (a 404 inclusive), css/, js/ (com js/vendor/), img/, fonts/,
# robots.txt, sitemap.xml e llms.txt. Fica de fora: build.py, llms.src.txt, logo_paths.svg.
set -euo pipefail
cd "$(dirname "$0")/.."

destino="${1:-_site}"
case "$destino" in
  "" | "/" | "." | ".." | site | site/ | scripts | scripts/)
    echo "Destino recusado: '$destino'" >&2
    exit 2 ;;
esac

rm -rf "$destino"
mkdir -p "$destino"
cp site/*.html "$destino"/
cp -R site/css site/js site/img site/fonts "$destino"/
cp site/robots.txt site/sitemap.xml site/llms.txt "$destino"/
touch "$destino/.nojekyll"

echo "Pasta publicada em $destino: $(ls "$destino"/*.html | wc -l | tr -d ' ') páginas, $(find "$destino" -type f | wc -l | tr -d ' ') arquivos."
