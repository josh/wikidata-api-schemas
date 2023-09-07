#!/bin/bash
# usage: splitjson.sh latest-all.json.gz latest-{}.json.gz 10
#
# Script Dependencies:
#   brew install pv

set -euf -o pipefail

gzcat_() {
	name="$(basename "$1")"
	pv --cursor --buffer-size 1024 --name "$name" "$1" | gzcat
}

gzip_() {
	name="$(basename "$1")"
	gzip | pv --cursor --buffer-size 1024 --name "$name" >"$1"
}

PYSCRIPT=$(
	cat <<'PYTHON'
from itertools import cycle
from sys import argv, stdin

stdin.buffer.readline()

files = [open(fn, "wb") for fn in argv[1:]]

for line, f in zip(stdin.buffer, files):
    f.write(b"[\n")
    f.write(line[:-2])

for line, f in zip(stdin.buffer, cycle(files)):
    f.write(b",\n")
    if line[-2] == 44:
        f.write(line[:-2])
    else:
        f.write(line[:-1])
        break

for f in files:
    f.write(b"\n]\n")
    f.close()
PYTHON
)

splitjson_py() {
	python3 -c "$PYSCRIPT" "$@"
}

splitjson_cmd() {
	printf 'splitjson_py'
	for i in $(seq 1 "$2"); do
		fn="${1/\{\}/$i}"
		printf ' >(gzip_ "%s")' "$fn"
	done
	printf '\n'
}

splitjson() {
	eval "$(splitjson_cmd "$@")"
}

gzcat_ "$1" | splitjson "$2" "$3"
