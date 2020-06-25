import atomiclong


class Tracker:
    """Request statistics tracker.
    """

    def __init__(self):
        self.count = atomiclong.AtomicLong(0)
        self.duration = atomiclong.AtomicLong(0)

    def track(self, duration: float):
        """Accumulates request duration info.
        """
        self.count += 1
        # NOTE: we assume overwlow will not occur because a service for a
        # particulaar environment will not have quite long uptimes, at least
        # becase cloud environment usually can change during the time.
        self.duration += int(duration * 1000)

    def get_stat(self) -> dict:
        """Gets statistics accumulated from the process startup.
        """
        count = self.count.value
        duration = self.duration.value
        return {
            "request_count": count,
            "average_request_time": count and duration / count or 0,
        }
