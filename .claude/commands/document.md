---
description: Documenta un archivo Python (docstrings) sin cambiar la lógica y verifica con pytest
argument-hint: <archivo, por ejemplo app/main.py>
allowed-tools: Read, Grep, Edit, Bash(python -m pytest:*), Bash(git diff:*)
---

Documenta el archivo `$ARGUMENTS` (si no se indica, usa `app/main.py`).

1. Lee el archivo y los tests relacionados en `tests/`.
2. Agrega un docstring en español a cada función y clase: qué hace, parámetros, qué devuelve y qué códigos HTTP responde (si es un endpoint).
3. No cambies la lógica: solo docstrings y comentarios. No renombres nada.
4. Ejecuta `python -m pytest -q` y reporta el resultado.
5. Muestra `git diff --stat` y confirma que solo cambiaron líneas de documentación.
