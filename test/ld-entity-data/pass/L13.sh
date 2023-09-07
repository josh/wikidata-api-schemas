#!/bin/bash

set -euf -o pipefail
set -x

curl 'https://www.wikidata.org/wiki/Special:EntityData/L13.json' >L13.json
