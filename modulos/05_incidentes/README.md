# Módulo 5 — Diagnóstico de incidentes

## Escenario
La API devuelve 500 en `GET /orders/99` (el pedido no existe). El instructor genera tráfico:
```bash
curl -i http://<ip>:8080/orders/99
```

## Ejercicio
1. `/logs 15` — localizar `KeyError: 99` en CloudWatch (`/ecs/ccd-orders-api`).
2. Pedir *«Diagnostica con el skill incident-triage»*: debe cruzar logs, estado de ECS y último despliegue del pipeline.
3. Aprobar el fix propuesto: devolver 404 con mensaje claro, agregar `tests/test_api.py::test_get_order_missing`.
4. `git push` → pipeline → verificar con `curl -i .../orders/99` (404) y `/logs`.

## Variantes
- Romper la configuración (p. ej. puerto de contenedor incorrecto en `infra/base.yml`) y diagnosticar tareas que no estabilizan con `aws ecs describe-services` (eventos).
- Imagen inexistente en ECR → tarea en bucle de reinicios.
