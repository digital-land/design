#!/bin/sh
# Download legislation.gov.uk XML for each instrument in content/legislation into var/cache/legislation
mkdir -p var/cache/legislation
for f in content/legislation/*.md; do
  s=$(basename "$f" .md)
  ref=$(sed -n 's/^reference: //p' "$f" | head -1)
  [ -s "var/cache/legislation/$s.xml" ] && continue
  echo "$s $ref"
done | xargs -P4 -L1 sh -c 'curl -sfL "https://www.legislation.gov.uk/$1/data.xml" -o "var/cache/legislation/$0.xml" || { echo "FAIL $1" >&2; rm -f "var/cache/legislation/$0.xml"; }'
