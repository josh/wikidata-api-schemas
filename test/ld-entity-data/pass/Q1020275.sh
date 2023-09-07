#!/bin/bash

set -euf -o pipefail
set -x

curl 'https://www.wikidata.org/wiki/Special:EntityData/Q1020275.json' >Q1020275.json
