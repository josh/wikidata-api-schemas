#!/bin/bash

set -euf -o pipefail
set -x

curl 'https://www.wikidata.org/wiki/Special:EntityData/L9.json' >L9.json
