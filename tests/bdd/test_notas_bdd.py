"""Step definitions BDD conectadas al codigo de produccion del modulo de notas.

Las escenarios viven en ``features/notas.feature``. Aqui registramos las
funciones de Given/When/Then que traducen cada paso en lenguaje natural a
llamadas concretas sobre ``RegistroNotas``.
"""

from __future__ import annotations

from typing import Any

import pytest
from pytest_bdd import given, parsers, scenarios, then, when

from notas.registro import RegistroNotas

scenarios("features/notas.feature")


@pytest.fixture
def contexto() -> dict[str, Any]:
    """Estado compartido entre los pasos de un mismo escenario."""
    return {"registro": RegistroNotas(), "ultimo_error": None}


# ----------------------------- GIVEN ----------------------------------------


@given("un registro de notas vacio")
def _registro_vacio(contexto: dict[str, Any]) -> None:
    contexto["registro"] = RegistroNotas()
    contexto["ultimo_error"] = None


@given(
    parsers.parse(
        'existe una nota de {valor:g} en la materia "{materia}" '
        'del semestre "{semestre}"'
    )
)
def _precondicion_nota(
    contexto: dict[str, Any], materia: str, semestre: str, valor: float
) -> None:
    contexto["registro"].registrar(
        materia=materia, semestre=semestre, valor=valor
    )


# ----------------------------- WHEN -----------------------------------------


@when(
    parsers.parse(
        'registro la materia "{materia}" en el semestre "{semestre}" '
        "con nota {valor:g}"
    )
)
def _registrar(
    contexto: dict[str, Any], materia: str, semestre: str, valor: float
) -> None:
    contexto["registro"].registrar(
        materia=materia, semestre=semestre, valor=valor
    )


@when(
    parsers.parse(
        'intento registrar la materia "{materia}" en el semestre "{semestre}" '
        "con nota {valor:g}"
    )
)
def _intentar_registrar(
    contexto: dict[str, Any], materia: str, semestre: str, valor: float
) -> None:
    try:
        contexto["registro"].registrar(
            materia=materia, semestre=semestre, valor=valor
        )
    except Exception as exc:  # noqa: BLE001 - capturamos para validar el error
        contexto["ultimo_error"] = exc


@when("consulto el promedio del estudiante")
def _consultar_promedio(contexto: dict[str, Any]) -> None:
    try:
        contexto["resultado"] = contexto["registro"].promedio()
    except Exception as exc:  # noqa: BLE001
        contexto["ultimo_error"] = exc


# ----------------------------- THEN -----------------------------------------


@then(parsers.parse("el registro contiene {cantidad:d} notas"))
def _verificar_cantidad(contexto: dict[str, Any], cantidad: int) -> None:
    assert len(contexto["registro"].notas) == cantidad


@then(
    parsers.parse(
        'la nota registrada para "{materia}" en "{semestre}" es {valor:g}'
    )
)
def _verificar_valor_nota(
    contexto: dict[str, Any], materia: str, semestre: str, valor: float
) -> None:
    encontrada = _buscar_nota(contexto, materia, semestre)
    assert encontrada is not None, "No se encontro la nota esperada."
    assert encontrada.valor == pytest.approx(valor)


@then(
    parsers.parse(
        'la nota registrada para "{materia}" en "{semestre}" tiene '
        "aprobacion {aprueba}"
    )
)
def _verificar_aprobacion(
    contexto: dict[str, Any], materia: str, semestre: str, aprueba: str
) -> None:
    encontrada = _buscar_nota(contexto, materia, semestre)
    assert encontrada is not None
    esperado = aprueba.strip().lower() == "true"
    assert encontrada.aprueba() is esperado


@then(parsers.parse("el promedio del estudiante es {valor:g}"))
def _verificar_promedio(contexto: dict[str, Any], valor: float) -> None:
    assert contexto["registro"].promedio() == pytest.approx(valor)


@then(parsers.parse('el sistema lanza el error "{nombre_error}"'))
def _verificar_error(contexto: dict[str, Any], nombre_error: str) -> None:
    assert contexto["ultimo_error"] is not None, (
        "Se esperaba un error pero no se capturo ninguno."
    )
    assert type(contexto["ultimo_error"]).__name__ == nombre_error, (
        f"Se esperaba {nombre_error} pero se obtuvo "
        f"{type(contexto['ultimo_error']).__name__}"
    )


@then(parsers.parse('el mensaje de error menciona "{a}" y "{b}"'))
def _verificar_mensaje_error(contexto: dict[str, Any], a: str, b: str) -> None:
    mensaje = str(contexto["ultimo_error"])
    assert a in mensaje, f"El mensaje no contiene '{a}': {mensaje!r}"
    assert b in mensaje, f"El mensaje no contiene '{b}': {mensaje!r}"


# ----------------------------- helpers --------------------------------------


def _buscar_nota(contexto: dict[str, Any], materia: str, semestre: str):
    return next(
        (
            n
            for n in contexto["registro"].notas
            if n.materia == materia and n.semestre == semestre
        ),
        None,
    )
