import json
import random
import locust


def readvms(path):
    with open(path, "r") as fd:
        return [i["vm_id"] for i in json.load(fd)["vms"]]


VMS = readvms("data/big.json")


class User(locust.HttpUser):
    authorization = None
    wait_time = locust.between(0, 0)

    @locust.task(100)
    def attack(self):
        self.client.get(
            "/attack",
            params={"vm_id": random.choice(VMS)},
            name="/attack",
        )

    @ locust.task(10)
    def stats(self):
        self.client.get("/stats")
