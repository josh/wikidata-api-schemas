#!/usr/bin/env python3

import json
from pathlib import Path
from textwrap import indent

# Script Dependencies:
#     jsonschema==4.19.0
#     referencing==0.30.2
import referencing.retrieval
from jsonschema import Draft202012Validator
from referencing import Registry


@referencing.retrieval.to_cached_resource()
def retrieve_from_filesystem(uri: str) -> str:
    return Path(uri).read_text()


tests = []
for schema_path in Path(".").glob("test/**/test.schema.json"):
    for instance_path in schema_path.parent.glob("pass/*.json"):
        tests.append((schema_path, instance_path))
    for instance_path in schema_path.parent.glob("fail/*.json"):
        tests.append((schema_path, instance_path))

registry = Registry(retrieve=retrieve_from_filesystem)

exitstatus = 0

print(f"1..{len(tests)}")
for tp_id, (schema_path, instance_path) in enumerate(tests, start=1):
    json_data = instance_path.read_bytes()
    instance = json.loads(json_data)

    type = instance_path.parent.name
    schema = {"$ref": str(schema_path)}
    validator = Draft202012Validator(schema, registry=registry)
    errors = list(validator.iter_errors(instance))

    if (type == "pass" and len(errors) == 0) or (type == "fail" and len(errors) > 0):
        print(f"ok {tp_id} - {schema_path} {instance_path}")
    else:
        exitstatus += 1
        print(f"not ok {tp_id} - {schema_path} {instance_path}")
        for error in errors:
            print(indent(str(error), "    "))

exit(exitstatus)
