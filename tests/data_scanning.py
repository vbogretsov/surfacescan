INFRA = (
    [
        {
            "vm_id": "ssh-1",
            "name": "ssh-1",
            "tags": ["ssh"],
        },
        {
            "vm_id": "ssh-2",
            "name": "ssh-2",
            "tags": ["ssh"]
        },
        {
            "vm_id": "lb-1",
            "name": "lb-1",
            "tags": ["lb"]
        },
        {
            "vm_id": "master-1",
            "name": "master-1",
            "tags": ["masters"],
        },
        {
            "vm_id": "master-2",
            "name": "master-2",
            "tags": ["masters"],
        },
        {
            "vm_id": "master-3",
            "name": "master-3",
            "tags": ["masters"],
        },
        {
            "vm_id": "node-1",
            "name": "node-1",
            "tags": ["nodes"],
        },
        {
            "vm_id": "node-2",
            "name": "node-2",
            "tags": ["nodes"],
        },
        {
            "vm_id": "node-3",
            "name": "node-3",
            "tags": ["nodes"],
        },
        {
            "vm_id": "node-4",
            "name": "node-4",
            "tags": ["nodes"],
        },
        {
            "vm_id": "postgres",
            "name": "postgres",
            "tags": ["db"],
        },
        {
            "vm_id": "redis",
            "name": "redis",
            "tags": ["cache"],
        },
    ],
    [
        {
            "fw_id": "ssh-lb",
            "source_tag": "ssh",
            "dest_tag": "lb",
        },
        {
            "fw_id": "ssh-masters",
            "source_tag": "ssh",
            "dest_tag": "masters",
        },
        {
            "fw_id": "ssh-nodes",
            "source_tag": "ssh",
            "dest_tag": "nodes",
        },
        {
            "fw_id": "lb-nodes",
            "source_tag": "lb",
            "dest_tag": "nodes",
        },
        {
            "fw_id": "nodes-db",
            "source_tag": "nodes",
            "dest_tag": "db",
        },
        {
            "fw_id": "nodes-cache",
            "source_tag": "nodes",
            "dest_tag": "cache",
        },
        {
            "fw_id": "nodes-cache",
            "source_tag": "nodes",
            "dest_tag": "nodes",
        },
        {
            "fw_id": "nodes-cache",
            "source_tag": "masters",
            "dest_tag": "masters",
        },
        {
            "fw_id": "nodes-masters",
            "source_tag": "nodes",
            "dest_tag": "masters",
        },
    ],
)

CYCLED = (
    [
        {
            "vm_id": "a-1",
            "name": "a-1",
            "tags": ["a"],
        },
        {
            "vm_id": "b-1",
            "name": "b-1",
            "tags": ["b"],
        },
        {
            "vm_id": "c-1",
            "name": "c-1",
            "tags": ["c"],
        },
    ],
    [
        {
            "fw_id": "a-b",
            "source_tag": "a",
            "dest_tag": "b",
        },
        {
            "fw_id": "b-c",
            "source_tag": "b",
            "dest_tag": "c",
        },
        {
            "fw_id": "c-a",
            "source_tag": "c",
            "dest_tag": "a",
        },
    ]
)


SCAN_CASES = [
    # empty case
    (
        [
        ],
        [
        ],
        "vm",
        (None, False)
    ),
    # empty surface
    (
        [
            {
                "vm_id": "vm-a211de",
                "name": "jira_server",
                "tags": ["ci", "dev"]
            },
            {
                "vm_id": "vm-c7bac01a07",
                "name": "bastion",
                "tags": ["ssh", "dev"]
            }
        ],
        [],
        "vm-a211de",
        ([], True),
    ),
    # case from doc
    (
        [
            {
                "vm_id": "vm-a211de",
                "name": "jira_server",
                "tags": ["ci", "dev"]
            },
            {
                "vm_id": "vm-c7bac01a07",
                "name": "bastion",
                "tags": ["ssh", "dev"]
            }
        ],
        [
            {
                "fw_id": "fw-82af742",
                "source_tag": "ssh",
                "dest_tag": "dev"
            }
        ],
        "vm-a211de",
        (["vm-c7bac01a07"], True),
    ),
    # ignore myself
    (
        [
            {
                "vm_id": "vm-a211de",
                "name": "jira_server",
                "tags": ["ci", "dev", "ssh"]
            },
            {
                "vm_id": "vm-c7bac01a07",
                "name": "bastion",
                "tags": ["ssh", "dev"]
            }
        ],
        [
            {
                "fw_id": "fw-82af742",
                "source_tag": "ssh",
                "dest_tag": "dev"
            }
        ],
        "vm-a211de",
        (["vm-c7bac01a07"], True),
    ),
    # transitive case
    (
        [
            {
                "vm_id": "vm-a211de",
                "name": "jira_server",
                "tags": ["ci", "dev"]
            },
            {
                "vm_id": "vm-c7bac01a07",
                "name": "bastion",
                "tags": ["ssh"]
            },
            {
                "vm_id": "vm-b4eed1",
                "name": "db",
                "tags": ["db"]
            }
        ],
        [
            {
                "fw_id": "fw-82af742",
                "source_tag": "ssh",
                "dest_tag": "dev"
            },
            {
                "fw_id": "fw-82af744",
                "source_tag": "dev",
                "dest_tag": "db"
            }
        ],
        "vm-b4eed1",
        (["vm-c7bac01a07", "vm-a211de"], True),
    ),
    # isolated vm
    (
        [
            {
                "vm_id": "vm-a211de",
                "name": "jira_server",
                "tags": ["ci", "dev"]
            },
            {
                "vm_id": "vm-c7bac01a07",
                "name": "bastion",
                "tags": ["ssh"]
            },
            {
                "vm_id": "vm-b4eed1",
                "name": "db",
                "tags": ["db"]
            },
            {
                "vm_id": "vm-b4ee22",
                "name": "cache",
                "tags": ["cache"]
            },
        ],
        [
            {
                "fw_id": "fw-82af742",
                "source_tag": "ssh",
                "dest_tag": "dev"
            },
            {
                "fw_id": "fw-82af744",
                "source_tag": "dev",
                "dest_tag": "db"
            }
        ],
        "vm-b4ee22",
        ([], True),
    ),
    (
        *INFRA,
        "postgres",
        (
            [
                "ssh-1",
                "ssh-2",
                "lb-1",
                "node-1",
                "node-2",
                "node-3",
                "node-4",
            ],
            True,
        )
    ),
    (
        *INFRA,
        "node-3",
        (
            [
                "ssh-1",
                "ssh-2",
                "lb-1",
                "node-1",
                "node-2",
                "node-4",
            ],
            True,
        )
    ),
    (
        *INFRA,
        "master-1",
        (
            [
                "ssh-1",
                "ssh-2",
                "lb-1",
                "master-2",
                "master-3",
                "node-1",
                "node-2",
                "node-3",
                "node-4",
            ],
            True,
        )
    ),
    (
        *INFRA,
        "lb-1",
        (
            [
                "ssh-1",
                "ssh-2",
            ],
            True,
        )
    ),
    (
        *INFRA,
        "ssh-1",
        ([], True),
    ),
    (
        *CYCLED,
        "a-1",
        (["b-1", "c-1"], True)
    )
]

VM_COUNT_CASES = [
    (
        [],
        0,
    ),
    (
        [
            INFRA[0][0],
            INFRA[0][1],
            INFRA[0][2],
        ],
        3
    ),
    (
        INFRA[0],
        len(INFRA[0]),
    )
]
