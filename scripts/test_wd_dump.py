#!/usr/bin/env python3
# usage: python3 scripts/test_wd_dump.py latest-*.json.gz

import gzip
import io
import json
import multiprocessing as mp
import sys
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path
from typing import Iterator

# Script Dependencies:
#     jsonschema==4.19.0
#     referencing==0.30.2
#     tqdm==4.66.1
import referencing.retrieval
from jsonschema import Draft202012Validator
from referencing import Registry
from tqdm import tqdm


@referencing.retrieval.to_cached_resource()
def retrieve_from_filesystem(uri: str) -> str:
    return Path(uri).read_text()


registry = Registry(retrieve=retrieve_from_filesystem)
item_validator = Draft202012Validator(
    {"$ref": "./item.schema.json"},
    registry=registry,
)
property_validator = Draft202012Validator(
    {"$ref": "./property.schema.json"},
    registry=registry,
)
lexeme_validator = Draft202012Validator(
    {"$ref": "./lexeme.schema.json"},
    registry=registry,
)


def validate_data(instance: dict) -> None:
    if instance["type"] == "item":
        validator = item_validator
    elif instance["type"] == "property":
        validator = property_validator
    elif instance["type"] == "lexeme":
        validator = lexeme_validator
    else:
        raise ValueError(f"Unknown type: {instance['type']}")

    errors = list(validator.iter_errors(instance))
    if len(errors) > 0:
        tqdm.write(str(instance))
        for error in errors:
            tqdm.write(str(error))
        raise errors[0]


def parse_gz_jsonl(filename: Path, position: int) -> Iterator[dict]:
    pbar = tqdm(
        desc=filename.name,
        total=filename.stat().st_size,
        leave=True,
        unit="B",
        unit_scale=True,
        unit_divisor=1024,
        position=position,
    )

    with gzip.open(filename, mode="rb") as file:
        assert isinstance(file.fileobj, io.BufferedReader)
        assert next(file) == b"[\n"
        for line in file:
            pbar.update(file.fileobj.tell() - pbar.n)
            yield json.loads(line.rstrip(b",\n"))
            if line.endswith(b"}\n"):
                break
        assert next(file) == b"]\n"

    pbar.close()


def worker(filename: str) -> None:
    worker_id = mp.current_process()._identity[0] - 1
    for obj in parse_gz_jsonl(Path(filename), worker_id):
        validate_data(obj)


def main() -> None:
    worker_count = mp.cpu_count()
    tqdm_lock = mp.RLock()
    with ProcessPoolExecutor(
        max_workers=worker_count,
        initializer=tqdm.set_lock,
        initargs=(tqdm_lock,),
    ) as pool:
        for filename in sys.argv[1:]:
            pool.submit(worker, filename)


if __name__ == "__main__":
    main()
