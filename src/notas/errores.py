"""Excepciones de dominio del modulo de notas academicas.

Cada excepcion modela una violacion concreta de los requerimientos. Tener
errores nombrados (en lugar de ``ValueError`` generico) hace que los tests
y los step definitions BDD puedan distinguir el motivo de la falla con
precision.
"""

from __future__ import annotations


class ErrorDeDominio(Exception):
    """Excepcion base del dominio de notas."""


class NotaFueraDeRangoError(ErrorDeDominio):
    """REQ-1: la nota debe estar en el intervalo [0.0, 5.0]."""


class TipoDeNotaInvalidoError(ErrorDeDominio):
    """REQ-1: el valor de la nota debe ser numerico (int o float real)."""
