#!/bin/bash

set -euf -o pipefail
set -x

curl 'https://www.wikidata.org/wiki/Special:EntityData/L2.json' >L2.json
