#!/bin/bash

set -euf -o pipefail
set -x

curl 'https://www.wikidata.org/w/api.php?action=query&meta=wbcontentlanguages&wbclcontext=monolingualtext&wbclprop=code&format=json' |
	jq '.query.wbcontentlanguages | keys | map({"value": {"language": ., "text": "foo"}, "type": "monolingualtext"})' >wbcontentlanguages.json
