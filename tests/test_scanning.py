import pytest

from surfacescan import scanning
from tests import data_scanning


@pytest.mark.parametrize("vms,fw_rules,vm_id,output", data_scanning.SCAN_CASES)
def test_scan(vms, fw_rules, vm_id, output):
    scanner = scanning.Scanner(vms, fw_rules)
    actual = scanner.scan(vm_id)

    actual[0] and actual[0].sort()
    output[0] and output[0].sort()

    assert output == actual


@pytest.mark.parametrize("vms,expected", data_scanning.VM_COUNT_CASES)
def test_vm_count(vms, expected):
    scanner = scanning.Scanner(vms, [])
    assert scanner.vm_count == expected
