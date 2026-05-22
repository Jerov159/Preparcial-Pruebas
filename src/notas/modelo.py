"""Entidades del dominio de notas academicas."""

from __future__ import annotations

import math
from dataclasses import dataclass

from notas.errores import NotaFueraDeRangoError, TipoDeNotaInvalidoError

NOTA_MINIMA: float = 0.0
NOTA_MAXIMA: float = 5.0
UMBRAL_APROBACION: float = 3.0


@dataclass(frozen=True)
class Nota:
    """Una nota academica registrada para una (materia, semestre).

    Invariantes:
        - ``valor`` debe ser numerico (no bool, no string, no None).
        - ``valor`` debe pertenecer al intervalo cerrado ``[0.0, 5.0]``.
        - ``valor`` no puede ser NaN ni infinito.
    """

    materia: str
    semestre: str
    valor: float

    def __post_init__(self) -> None:
        _validar_tipo(self.valor)
        _validar_rango(self.valor)

    def aprueba(self) -> bool:
        """REQ-2: la nota aprueba si es mayor o igual a ``UMBRAL_APROBACION``."""
        return self.valor >= UMBRAL_APROBACION


def _validar_tipo(valor: object) -> None:
    if isinstance(valor, bool):
        raise TipoDeNotaInvalidoError(
            f"El valor de la nota no puede ser booleano: {valor!r}"
        )
    if not isinstance(valor, (int, float)):
        raise TipoDeNotaInvalidoError(
            "El valor de la nota debe ser numerico (int o float); "
            f"se recibio {type(valor).__name__}: {valor!r}"
        )


def _validar_rango(valor: float) -> None:
    if math.isnan(valor) or math.isinf(valor):
        raise NotaFueraDeRangoError(
            f"El valor de la nota no admite NaN ni infinitos: {valor!r}"
        )
    if not NOTA_MINIMA <= valor <= NOTA_MAXIMA:
        raise NotaFueraDeRangoError(
            f"La nota debe estar entre {NOTA_MINIMA} y {NOTA_MAXIMA}; "
            f"se recibio {valor}"
        )
