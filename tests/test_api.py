import http


def test_stats_returns_zero_if_there_was_no_requests(app):
    resp = app.get("/stats")
    assert resp.status_code == http.HTTPStatus.OK
    data = resp.json()
    assert data["vm_count"] > 0
    assert data["request_count"] == 0
    assert data["average_request_time"] == 0


def test_stats_increments_requests_count(app):
    c1 = app.get("/stats").json()["request_count"]
    c2 = app.get("/stats").json()["request_count"]
    assert c2 - c1 == 1


def test_scan_with_invalid_vm_id_returns_404(app):
    resp = app.get("/attack", params={"vm_id": "xxx"})
    assert resp.status_code == http.HTTPStatus.NOT_FOUND


def test_scan_isolated_vm_returns_empty_list(app):
    resp = app.get("/attack", params={"vm_id": "vm-8d2d12765"})
    assert resp.status_code == http.HTTPStatus.OK
    assert resp.json() == []


def test_scan_connected_vm_returns_not_empty_list(app):
    resp = app.get("/attack", params={"vm_id": "vm-a211de"})
    assert resp.status_code == http.HTTPStatus.OK
    data = resp.json()
    data.sort()
    assert data == [
        "vm-0c1791",
        "vm-2987241",
        "vm-2ba4d2f87",
        "vm-575c4a",
        "vm-59574582",
        "vm-5f3ad2b",
        "vm-7d1ff7af47",
        "vm-864a94f",
        "vm-9ea3998",
        "vm-a3660c",
        "vm-a3ed2eed23",
        "vm-ab51cba10",
        "vm-ae24e37f8a",
        "vm-b35b501",
        "vm-b462c04",
        "vm-b8e6c350",
        "vm-c1e6285f",
        "vm-c7bac01a07",
        "vm-cf1f8621",
        "vm-d9e0825",
        "vm-e30d5fa49a",
        "vm-ec02d5c153",
        "vm-f00923",
    ]
