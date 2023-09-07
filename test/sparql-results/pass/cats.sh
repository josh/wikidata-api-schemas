#!/bin/bash

set -euf -o pipefail
set -x

curl --get 'https://query.wikidata.org/sparql' \
	--data-urlencode 'query@-' \
	--data-urlencode 'format=json' <<EOF >cats.json
SELECT ?item ?itemLabel WHERE {
  ?item wdt:P31 wd:Q146.
  SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }
}
EOF
