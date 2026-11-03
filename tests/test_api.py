import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from app.main import app  # noqa: E402

client = app.test_client()


def test_health():
    r = client.get("/health")
    assert r.status_code == 200
    assert r.get_json()["status"] == "ok"


def test_list_orders():
    r = client.get("/orders")
    assert r.status_code == 200
    assert len(r.get_json()) == 3


def test_get_order_existing():
    assert client.get("/orders/1").get_json()["customer"] == "ACME"
