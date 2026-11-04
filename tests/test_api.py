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


def test_get_order_not_found():
    r = client.get("/orders/100")
    assert r.status_code == 404
    assert "error" in r.get_json()


def test_get_order_80_not_found():
    r = client.get("/orders/80")
    assert r.status_code == 404
    assert r.get_json()["error"] == "pedido no encontrado"


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


@pytest.mark.parametrize("literal", ["NaN", "Infinity", "-Infinity"])
def test_create_order_non_finite_total(literal):
    raw = '{"customer": "Umbrella", "total_amt": %s}' % literal
    r = client.post("/orders", data=raw, content_type="application/json")
    assert r.status_code == 400
    assert "error" in r.get_json()
    assert len(ORDERS) == 3


@pytest.mark.parametrize(
    "raw_total",
    ["null", "[]", "[10]", "{}", '{"v": 10}', '""', '"abc"', "-0.0", "-0", "-1e-9", "-1e308", "1e400", "-1e400"],
)
def test_create_order_total_amt_edge_invalid(raw_total):
    """Tipos inesperados, cero negativo, negativos mínimos y overflow a infinito se rechazan."""
    raw = '{"customer": "Umbrella", "total_amt": %s}' % raw_total
    r = client.post("/orders", data=raw, content_type="application/json")
    assert r.status_code == 400
    assert r.get_json()["error"] == "total_amt debe ser un numero mayor que 0"
    assert len(ORDERS) == 3


@pytest.mark.parametrize(
    "raw_total, esperado",
    [
        ("0.01", 0.01),
        ("5e-324", 5e-324),  # menor float positivo
        ("1", 1),
        ("1.0", 1.0),
        ("1e308", 1e308),  # cerca del máximo float
        ("1000000000000", 1000000000000),
    ],
)
def test_create_order_total_amt_edge_valid(raw_total, esperado):
    """Valores positivos extremos pero finitos se aceptan y se guardan tal cual."""
    raw = '{"customer": "Umbrella", "total_amt": %s}' % raw_total
    r = client.post("/orders", data=raw, content_type="application/json")
    assert r.status_code == 201
    assert r.get_json()["total_amt"] == esperado
    assert ORDERS[4]["total_amt"] == esperado


def test_create_order_missing_total_amt_message():
    r = client.post("/orders", json={"customer": "Umbrella"})
    assert r.status_code == 400
    assert r.get_json()["error"] == "total_amt debe ser un numero mayor que 0"


@pytest.mark.parametrize("raw", ["no es json", "[1, 2]"])
def test_create_order_not_json_object(raw):
    r = client.post("/orders", data=raw, content_type="application/json")
    assert r.status_code == 400
    assert r.get_json()["error"] == "JSON invalido"
