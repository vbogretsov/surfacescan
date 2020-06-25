import argparse
import json
import random

import faker


DESCRIPTION = """
Generates test data for surfacescan application to run performance tests
"""

parser = argparse.ArgumentParser(
    "gendata",
    description=DESCRIPTION,
)

parser.add_argument(
    "--nodes",
    default=100,
    type=int,
    help="desired number of nodes",
)

parser.add_argument(
    "--tags",
    default=50,
    type=int,
    help="desired number of tags",
)

parser.add_argument(
    "--rules",
    default=50,
    type=int,
    help="desired number of rules"
)

parser.add_argument(
    "--out",
    default="data.json",
    help="output file path",
)


def main():
    args = parser.parse_args()
    rng = faker.Faker()
    tags = [rng.pystr(min_chars=2, max_chars=5) for i in range(args.tags)]
    vms = [
        {
            "vm_id": rng.pystr_format(),
            "name": rng.word(),
            "tags": [random.choice(tags) for i in range(rng.pyint(0, 5))],
        } for i in range(args.nodes)
    ]
    fw_rules = [
        {
            "fw_id": rng.pystr_format(),
            "source_tag": random.choice(tags),
            "dest_tag": random.choice(tags),
        } for i in range(args.rules)
    ]
    with open(args.out, "w") as fd:
        json.dump({"vms": vms, "fw_rules": fw_rules}, fd)
