#!/bin/bash

set -euf -o pipefail
set -x

curl 'https://www.wikidata.org/wiki/Special:EntityData/Q18445392.json' >Q18445392.json
