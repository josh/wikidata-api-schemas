#!/bin/bash

set -euf -o pipefail
set -x

curl --get 'https://query.wikidata.org/sparql' \
	--data-urlencode 'query@-' \
	--data-urlencode 'format=json' <<EOF >datatype-demonstration.json
SELECT ?prop ?value WHERE {
  wd:Q115569934 ?prop ?value.
  _:b0 wikibase:directClaim ?prop.
}
EOF
