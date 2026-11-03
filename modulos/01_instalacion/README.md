# Módulo 1 — Instalación y configuración

**Objetivo:** tener Claude Code funcionando en el sistema del participante.

## Pasos
```bash
node --version                               # Node.js 18+
npm install -g @anthropic-ai/claude-code
claude --version
```
- **macOS:** `brew install node` y luego el comando npm.
- **Ubuntu/Debian:** `sudo apt install -y nodejs npm` (o NodeSource para 18+) y el comando npm.
- **Windows con WSL:** `wsl --install -d Ubuntu`, abrir Ubuntu e instalar como en Debian; trabajar dentro del sistema de archivos de WSL.

## Ejercicio
1. Abrir `claude` en la carpeta del repo y ejecutar `/check-env`.
2. Ejecutar `/init` en una carpeta vacía y comparar con el `CLAUDE.md` de este repo.
3. Discusión: ¿qué reglas pondría su equipo en `CLAUDE.md`?

**Resultado esperado:** tabla ✅ con Python, Git, Docker, AWS CLI y cuenta `471112715746`.
