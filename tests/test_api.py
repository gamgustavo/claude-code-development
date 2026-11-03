import copy
import os
import sys

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from app.main import ORDERS, app  # noqa: E402

client = app.test_client()
_INITIAL_ORDERS = copy.deepcopy(ORDERS)


@pytest.fixture(autouse=True)
def reset_orders():
    """ORDERS es estado global: se restaura tras cada test para aislarlos."""
    yield
    ORDERS.clear()
    ORDERS.update(copy.deepcopy(_INITIAL_ORDERS))


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


def test_create_order_valid():
    r = client.post("/orders", json={"customer": "Umbrella", "total_amt": 99.9})
    assert r.status_code == 201
    body = r.get_json()
    assert body == {"id": 4, "customer": "Umbrella", "total_amt": 99.9, "status": "PENDING"}
    assert client.get("/orders/4").get_json()["customer"] == "Umbrella"
    assert len(client.get("/orders").get_json()) == 4


@pytest.mark.parametrize(
    "payload",
    [
        {"total_amt": 10},
        {"customer": "", "total_amt": 10},
        {"customer": "   ", "total_amt": 10},
        {"customer": 123, "total_amt": 10},
        {"customer": "Umbrella"},
        {"customer": "Umbrella", "total_amt": -5},
        {"customer": "Umbrella", "total_amt": 0},
        {"customer": "Umbrella", "total_amt": "10"},
        {"customer": "Umbrella", "total_amt": True},
    ],
)
def test_create_order_invalid(payload):
    r = client.post("/orders", json=payload)
    assert r.status_code == 400
    assert "error" in r.get_json()
    assert len(ORDERS) == 3


@pytest.mark.parametrize("raw", ["no es json", "[1, 2]"])
def test_create_order_not_json_object(raw):
    r = client.post("/orders", data=raw, content_type="application/json")
    assert r.status_code == 400
    assert r.get_json()["error"] == "JSON invalido"
