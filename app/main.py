"""API de pedidos del curso Claude Code: de la terminal al pipeline CI/CD en AWS."""
import logging
import os
import sys

from flask import Flask, jsonify, request

from app.validation import validate_order

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
    """Endpoint de salud (GET /health), usado por el HEALTHCHECK de Docker.

    Parámetros: ninguno.

    Devuelve:
        JSON ``{"status": "ok", "version": <APP_VERSION o "dev">}``.

    Códigos HTTP:
        200: el servicio está en pie.
    """
    return jsonify(status="ok", version=os.environ.get("APP_VERSION", "dev"))


@app.get("/orders")
def list_orders():
    """Lista todos los pedidos (GET /orders).

    Parámetros: ninguno.

    Devuelve:
        Lista JSON con los pedidos almacenados en ``ORDERS``.

    Códigos HTTP:
        200: siempre, aunque la lista esté vacía.
    """
    log.info("list_orders count=%d", len(ORDERS))
    return jsonify(list(ORDERS.values()))


@app.post("/orders")
def create_order():
    """Crea un pedido nuevo (POST /orders).

    Parámetros:
        Cuerpo JSON con ``customer`` (texto no vacío) y ``total_amt``
        (número finito mayor que 0). Se valida con ``validate_order``.

    Devuelve:
        El pedido creado con ``id`` autoincremental, ``customer`` sin espacios
        sobrantes, ``total_amt`` y ``status`` "PENDING"; o ``{"error": <mensaje>}``
        si el payload es inválido.

    Códigos HTTP:
        201: pedido creado.
        400: JSON inválido o campos que no cumplen la validación.
    """
    data = request.get_json(silent=True)
    error = validate_order(data)
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
    """Obtiene un pedido por su id (GET /orders/<order_id>).

    Parámetros:
        order_id: identificador entero del pedido, tomado de la ruta.

    Devuelve:
        El pedido como JSON, o ``{"error": "pedido no encontrado"}`` si no existe.

    Códigos HTTP:
        200: pedido encontrado.
        404: no existe un pedido con ese id.
    """
    order = ORDERS.get(order_id)
    if order is None:
        log.warning("get_order not_found id=%d", order_id)
        return jsonify(error="pedido no encontrado"), 404
    log.info("get_order id=%d", order_id)
    return jsonify(order)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", "8080")))
