import http

import fastapi

from surfacescan import registry
from surfacescan import scanning
from surfacescan import tracking


router = fastapi.APIRouter()


@router.get("/attack")
def attack(
    vm_id: str,
    scanner: scanning.Scanner = fastapi.Depends(registry.get_scanner),
):
    """Gets the list of the virtual machine ids that can potentially attack it.
    """
    surface, found = scanner.scan(vm_id)
    if not found:
        raise fastapi.HTTPException(status_code=http.HTTPStatus.NOT_FOUND)
    return surface


@router.get("/stats")
def stats(
    scanner: scanning.Scanner = fastapi.Depends(registry.get_scanner),
    tracker: tracking.Tracker = fastapi.Depends(registry.get_tracker),
):
    """Gets the service statistics accumulated from the process startup.
    """
    return {
        "vm_count": scanner.vm_count,
        **tracker.get_stat(),
    }
