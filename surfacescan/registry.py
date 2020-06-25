from surfacescan import scanning
from surfacescan import tracking


_tracker = None
_scanner = None


def set_tracker(tracker: tracking.Tracker) -> None:
    global _tracker
    _tracker = tracker


def get_tracker() -> tracking.Tracker:
    return _tracker


def set_scanner(scanner: scanning.Scanner) -> None:
    global _scanner
    _scanner = scanner


def get_scanner() -> scanning.Scanner:
    return _scanner
