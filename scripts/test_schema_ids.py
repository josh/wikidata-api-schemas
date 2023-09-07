#!/usr/bin/env python3

import json
from pathlib import Path

http_base_uri = "https://josh.github.io/wikidata-api-schemas"

tests = list(Path(".").glob("**/*.schema.json"))
exitstatus = 0

print(f"1..{len(tests)}")
for tp_id, schema_path in enumerate(tests, start=1):
    json_data = schema_path.read_bytes()
    schema = json.loads(json_data)

    if "$id" not in schema:
        print(f"not ok {tp_id} - {schema_path}")
        continue

    actual_id = schema["$id"]
    expected_id = f"{http_base_uri}/{schema_path}"

    if actual_id != expected_id:
        exitstatus += 1
        print(f"not ok {tp_id} - {schema_path}")
        continue

    print(f"ok {tp_id} - {schema_path}")

exit(exitstatus)
