# Módulo 6 — MCP, GitHub y búsqueda

## MCP
Model Context Protocol conecta Claude con herramientas externas. Ejemplos con GitHub:
```bash
claude mcp add --transport http github https://api.githubcopilot.com/mcp/ --header "Authorization: Bearer <TOKEN>"
claude mcp list
```
El token lo configura el participante (nunca se pega en el chat ni se guarda en el repo). Para compartir con el equipo se usa `.mcp.json` en el repo, sin secretos (variables de entorno).

## Ejercicios
1. Con MCP de GitHub: *«Lista los PR abiertos y resume los cambios de cada uno»*.
2. Crear un issue desde Claude y enlazarlo al PR del módulo 3.
3. Búsqueda en codebase: *«¿Dónde se define el nombre del cluster y quién lo usa?»* (Grep/Glob: `infra/`, `scripts/`, `.claude/commands/`).
4. Búsqueda web: pedir la documentación vigente de CodeConnections y compararla con `infra/pipeline.yml`.

## Gobierno
Los servidores MCP aprobados se listan en el repo; todo lo demás requiere revisión del instructor.
