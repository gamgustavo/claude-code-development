"""API de pedidos del curso Claude Code: de la terminal al pipeline CI/CD en AWS."""
import logging
import os
import sys

from flask import Flask, jsonify, request

logging.basicConfig(
    stream=sys.stdout,
    level=os.environ.get("LOG_LEVEL", "INFO"),
    format='{"ts":"%(asctime)s","level":"%(levelname)s","msg":"%(message)s"}',
)
log = logging.getLogger("orders-api")

app = Flask(__name__)

ORDERS = {
    1: {"id": 1, "customer": "ACME", "total_amt": 120.50, "status": "PAID"},
    2: {"id": 2, "customer": "Globex", "total_amt": 75.00, "status": "PENDING"},
    3: {"id": 3, "customer": "Initech", "total_amt": 310.25, "status": "SHIPPED"},
}


@app.get("/health")
def health():
    return jsonify(status="ok", version=os.environ.get("APP_VERSION", "dev"))


@app.get("/orders")
def list_orders():
    log.info("list_orders count=%d", len(ORDERS))
    return jsonify(list(ORDERS.values()))


def _validate_order(data):
    """Devuelve un mensaje de error si el payload es inválido, o None si es correcto."""
    if not isinstance(data, dict):
        return "JSON invalido"
    customer = data.get("customer")
    if not isinstance(customer, str) or not customer.strip():
        return "customer debe ser un texto no vacio"
    total = data.get("total_amt")
    if isinstance(total, bool) or not isinstance(total, (int, float)) or total <= 0:
        return "total_amt debe ser un numero mayor que 0"
    return None


@app.post("/orders")
def create_order():
    data = request.get_json(silent=True)
    error = _validate_order(data)
    if error:
        log.warning("create_order invalid error=%s", error)
        return jsonify(error=error), 400
    order_id = max(ORDERS, default=0) + 1
    order = {
        "id": order_id,
        "customer": data["customer"].strip(),
        "total_amt": data["total_amt"],
        "status": "PENDING",
    }
    ORDERS[order_id] = order
    log.info("create_order id=%d", order_id)
    return jsonify(order), 201


@app.get("/orders/<int:order_id>")
def get_order(order_id: int):
    # Ejercicio del módulo 5 (incidentes): este endpoint falla con 500 si el pedido no existe.
    order = ORDERS[order_id]
    log.info("get_order id=%d", order_id)
    return jsonify(order)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", "8080")))
