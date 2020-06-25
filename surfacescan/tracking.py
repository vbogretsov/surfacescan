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
