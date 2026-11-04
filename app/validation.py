"""Validación de pedidos de la API."""
import math


def validate_order(data):
    """Devuelve un mensaje de error si el payload es inválido, o None si es correcto."""
    if not isinstance(data, dict):
        return "JSON invalido"
    customer = data.get("customer")
    if not isinstance(customer, str) or not customer.strip():
        return "customer debe ser un texto no vacio"
    total = data.get("total_amt")
    if (
        isinstance(total, bool)
        or not isinstance(total, (int, float))
        or not math.isfinite(total)
        or total <= 0
    ):
        return "total_amt debe ser un numero mayor que 0"
    return None
