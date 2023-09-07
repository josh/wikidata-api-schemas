#!/bin/bash

set -euf -o pipefail
set -x

curl --get 'https://query.wikidata.org/sparql' \
	--data-urlencode 'query@-' \
	--data-urlencode 'format=json' <<EOF >catpics.json
SELECT ?item ?itemLabel ?pic WHERE {
  ?item wdt:P31 wd:Q146;
    wdt:P18 ?pic.
  SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }
}
EOF
