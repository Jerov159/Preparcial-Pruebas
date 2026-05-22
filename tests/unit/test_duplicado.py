"""Tests para REQ-4: no permitir dos notas para la misma (materia, semestre).

Cubre:
    - Registro inicial sin duplicados (positivo).
    - Intento de duplicado (negativo) lanza error claro con datos.
    - Misma materia en distinto semestre se permite (borde).
    - Diferente materia en el mismo semestre se permite.
    - El estado del registro no cambia cuando se rechaza un duplicado.

Casos del documento de diseno asociados: TC10, TC11, TC12.
"""

from __future__ import annotations

import pytest

from notas.errores import NotaDuplicadaError
from notas.registro import RegistroNotas


class TestRegistroSinDuplicados:
    """REQ-4: primera nota para (materia, semestre) siempre se acepta."""

    def test_registrar_primera_nota_de_materia_y_semestre_funciona(self) -> None:
        registro = RegistroNotas()
        nota = registro.registrar(materia="Calculo", semestre="2025-1", valor=4.0)

        assert nota.valor == 4.0
        assert len(registro.notas) == 1


class TestRechazoDeDuplicado:
    """REQ-4: segundo intento sobre (materia, semestre) debe fallar."""

    def test_registrar_misma_materia_y_semestre_lanza_nota_duplicada(self) -> None:
        registro = RegistroNotas()
        registro.registrar(materia="Calculo", semestre="2025-1", valor=4.0)

        with pytest.raises(NotaDuplicadaError):
            registro.registrar(materia="Calculo", semestre="2025-1", valor=3.5)

    def test_mensaje_de_error_incluye_materia_y_semestre(self) -> None:
        registro = RegistroNotas()
        registro.registrar(materia="Calculo", semestre="2025-1", valor=4.0)

        with pytest.raises(NotaDuplicadaError) as info:
            registro.registrar(materia="Calculo", semestre="2025-1", valor=3.5)

        mensaje = str(info.value)
        assert "Calculo" in mensaje
        assert "2025-1" in mensaje

    def test_duplicado_rechazado_no_modifica_el_registro(self) -> None:
        registro = RegistroNotas()
        registro.registrar(materia="Calculo", semestre="2025-1", valor=4.0)

        with pytest.raises(NotaDuplicadaError):
            registro.registrar(materia="Calculo", semestre="2025-1", valor=3.5)

        assert len(registro.notas) == 1
        assert registro.notas[0].valor == 4.0


class TestCasosPermitidos:
    """REQ-4: misma materia distinto semestre, o distinta materia mismo semestre."""

    def test_misma_materia_en_distinto_semestre_se_permite(self) -> None:
        registro = RegistroNotas()
        registro.registrar(materia="Calculo", semestre="2025-1", valor=4.0)
        registro.registrar(materia="Calculo", semestre="2025-2", valor=3.5)

        assert len(registro.notas) == 2

    def test_distinta_materia_en_mismo_semestre_se_permite(self) -> None:
        registro = RegistroNotas()
        registro.registrar(materia="Calculo", semestre="2025-1", valor=4.0)
        registro.registrar(materia="Fisica", semestre="2025-1", valor=3.5)

        assert len(registro.notas) == 2
