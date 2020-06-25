import collections
import glob
import itertools
import json
import logging
import os
import typing

import networkx

from surfacescan import settings


LOG = logging.getLogger(__name__)


VMs = typing.Sequence[typing.Dict[str, typing.Any]]
FwRules = typing.Sequence[typing.Dict[str, str]]


class Scanner:
    """Attack surface scanner.
    """

    def __init__(self, vms: VMs = (), fw_rules: FwRules = ()) -> None:
        self.graph = networkx.DiGraph()
        self.vm2tag = {}
        self.tag2vm = collections.defaultdict(list)

        for vm in vms:
            vm_id = vm["vm_id"]
            tags = vm["tags"]

            self.vm2tag[vm_id] = tags

            for tag in tags:
                if tag not in self.graph:
                    self.graph.add_node(tag)
                self.tag2vm[tag].append(vm_id)

        for rule in fw_rules:
            self.graph.add_edge(rule["dest_tag"], rule["source_tag"])

    def scan(self, vm_id: str) -> typing.Tuple[typing.List[str], bool]:
        """Finds attack surface for the given vm.

        The second return value is the boolean flag which indicates whether a
        vm with the id provided was found.
        """
        tags = self.vm2tag.get(vm_id, None)
        if tags is None:
            return None, False

        tag_surface = set()
        for tag in tags:
            tag_surface |= networkx.descendants(self.graph, tag)
            if self.graph.has_edge(tag, tag):
                tag_surface.add(tag)

        cache = set()

        vm_surface = []
        for tag in tag_surface:
            for vm in self.tag2vm[tag]:
                if vm not in cache and vm != vm_id:
                    vm_surface.append(vm)
                    cache.add(vm)

        return vm_surface, True

    @property
    def vm_count(self) -> int:
        """Gets total count of VMs.
        """
        return len(self.vm2tag)


def load_data(dir: str) -> typing.Tuple[VMs, FwRules]:
    """Load environment data from directory provided in settings.
    """
    LOG.info("Reading data files from directory %s", settings.current.datadir)

    vms = []
    fw_rules = []

    for f in glob.glob(os.path.join(dir, "*.json")):
        LOG.info("reading data file %s", f)
        with open(f) as fd:
            data = json.load(fd)
            vms.append(data["vms"])
            fw_rules.append(data["fw_rules"])

    return itertools.chain(*vms), itertools.chain(*fw_rules)
