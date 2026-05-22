"""Tests para REQ-2: aprobacion (>= 3.0) o reprobacion (< 3.0).

Cubre:
    - Particion de aprobados (>= 3.0).
    - Particion de reprobados (< 3.0).
    - Valores limite alrededor de 3.0 (BVA: 2.99, 3.0, 3.01).

Casos del documento de diseno asociados: TC04, TC05, TC06.
"""

from __future__ import annotations

import pytest

from notas.modelo import Nota


class TestParticionAprueba:
    """REQ-2: notas >= 3.0 aprueban."""

    @pytest.mark.parametrize("valor", [3.0, 3.5, 4.0, 5.0])
    def test_nota_mayor_o_igual_a_tres_aprueba(self, valor: float) -> None:
        assert Nota(materia="Calculo", semestre="2025-1", valor=valor).aprueba() is True


class TestParticionReprueba:
    """REQ-2: notas < 3.0 reprueban."""

    @pytest.mark.parametrize("valor", [0.0, 1.5, 2.0, 2.5])
    def test_nota_menor_a_tres_reprueba(self, valor: float) -> None:
        assert Nota(materia="Calculo", semestre="2025-1", valor=valor).aprueba() is False


class TestValoresLimiteAprobacion:
    """REQ-2: BVA en el umbral 3.0 con delta=0.01."""

    def test_nota_justo_debajo_del_umbral_reprueba(self) -> None:
        assert Nota(materia="Calculo", semestre="2025-1", valor=2.99).aprueba() is False

    def test_nota_exactamente_en_el_umbral_aprueba(self) -> None:
        # 3.0 es el umbral inclusivo: aprueba.
        assert Nota(materia="Calculo", semestre="2025-1", valor=3.0).aprueba() is True

    def test_nota_justo_arriba_del_umbral_aprueba(self) -> None:
        assert Nota(materia="Calculo", semestre="2025-1", valor=3.01).aprueba() is True
