import fastapi
import pkg_resources

from surfacescan import api
from surfacescan import middleware
from surfacescan import registry
from surfacescan import scanning
from surfacescan import settings
from surfacescan import tracking


def create_scanner():
    vms, fw_rules = scanning.load_data(settings.current.datadir)
    scanner = scanning.Scanner(vms, fw_rules)
    registry.set_scanner(scanner)


def create_app() -> fastapi.FastAPI:
    pkg = pkg_resources.get_distribution(__package__)
    app = fastapi.FastAPI(
        title=__package__,
        version=pkg.version,
        on_startup=(create_scanner,),
    )

    tracker = tracking.Tracker()
    registry.set_tracker(tracker)

    app.add_middleware(middleware.RequestStats, track=tracker.track)
    app.include_router(api.router)

    return app


app = create_app()
