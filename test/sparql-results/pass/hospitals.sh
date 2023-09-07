#!/bin/bash

set -euf -o pipefail
set -x

curl --get 'https://query.wikidata.org/sparql' \
	--data-urlencode 'query@-' \
	--data-urlencode 'format=json' <<EOF >hospitals.json
SELECT DISTINCT * WHERE {
  ?item wdt:P31/wdt:P279* wd:Q16917;
        wdt:P625 ?geo.
}
EOF
