# Notas Academicas - Preparcial de Pruebas de Software

Modulo de registro de notas academicas construido con un enfoque dirigido por
pruebas (TDD) y desarrollo dirigido por comportamiento (BDD).

## Requerimientos

- **REQ-1**: Registrar una nota entre `0.0` y `5.0` para una materia.
- **REQ-2**: Determinar si una nota aprueba o reprueba (`aprueba si nota >= 3.0`).
- **REQ-3**: Calcular el promedio de todas las notas de un estudiante.
- **REQ-4**: No permitir dos notas para la misma materia en el mismo semestre.

## Stack

- Python `>=3.10`
- Gestor de paquetes: `uv`
- Pruebas unitarias: `pytest`
- Pruebas BDD: `pytest-bdd`
- Cobertura: `pytest-cov`
- CI: GitHub Actions

## Estructura del proyecto

```
.
|-- .github/workflows/ci.yml      # Pipeline de CI
|-- docs/test-design.md           # Particiones, valores limite y casos
|-- src/notas/                    # Codigo de produccion
|   |-- modelo.py                 # Dataclasses (Nota)
|   |-- errores.py                # Excepciones de dominio
|   `-- registro.py               # RegistroNotas (logica principal)
|-- tests/
|   |-- unit/                     # Tests unitarios (pytest)
|   `-- bdd/                      # Tests BDD (pytest-bdd)
|       |-- features/             # Archivos .feature en Gherkin
|       `-- test_steps.py         # Step definitions
|-- pyproject.toml
`-- README.md
```

## Como ejecutar

Instalar dependencias en un entorno virtual gestionado por `uv`:

```powershell
uv sync
```

Ejecutar todos los tests (unitarios + BDD) con reporte de cobertura:

```powershell
uv run pytest --cov=src/notas --cov-report=term-missing
```

Ejecutar solo los tests unitarios:

```powershell
uv run pytest tests/unit
```

Ejecutar solo los tests BDD:

```powershell
uv run pytest tests/bdd
```

Ejecutar solo los smoke tests (escenarios criticos rapidos):

```powershell
uv run pytest -m smoke
```

## Flujo de trabajo TDD

Cada requerimiento se implemento siguiendo el ciclo **Red - Green - Refactor**:

1. **RED**: se escribe el test antes que cualquier codigo de produccion. El test
   debe fallar (rojo).
2. **GREEN**: se escribe el codigo minimo necesario para que el test pase
   (verde). Nada mas.
3. **REFACTOR**: se mejora el codigo sin alterar el comportamiento ni romper los
   tests existentes.

El historial de commits refleja explicitamente cada fase con prefijos
`test:`, `feat:` y `refactor:`.
