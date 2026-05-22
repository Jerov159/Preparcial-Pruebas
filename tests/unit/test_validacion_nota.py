"""Tests para REQ-1: Registrar una nota entre 0.0 y 5.0 para una materia.

Cubre:
    - Particiones de equivalencia (validas, invalidas, tipo invalido, especiales).
    - Analisis de valores limite en 0.0 y 5.0 (delta=0.01).

Casos del documento de diseno asociados: TC01, TC02, TC03.
"""

from __future__ import annotations

import math

import pytest

from notas.errores import NotaFueraDeRangoError, TipoDeNotaInvalidoError
from notas.modelo import Nota


class TestParticionesDeRango:
    """REQ-1: la nota debe estar entre 0.0 y 5.0 (inclusivo)."""

    def test_nota_valida_interior_se_crea_con_su_valor(self):
        nota = Nota(materia="Calculo", semestre="2025-1", valor=3.5)
        assert nota.valor == 3.5

    def test_nota_menor_a_cero_lanza_nota_fuera_de_rango(self):
        with pytest.raises(NotaFueraDeRangoError):
            Nota(materia="Calculo", semestre="2025-1", valor=-1.5)

    def test_nota_mayor_a_cinco_lanza_nota_fuera_de_rango(self):
        with pytest.raises(NotaFueraDeRangoError):
            Nota(materia="Calculo", semestre="2025-1", valor=7.2)


class TestValidacionDeTipo:
    """REQ-1: solo se aceptan tipos numericos (int o float)."""

    @pytest.mark.parametrize(
        "valor_invalido",
        ["cinco", None, [3.5], {"valor": 3.5}, (3.5,)],
    )
    def test_tipo_no_numerico_lanza_tipo_de_nota_invalido(self, valor_invalido):
        with pytest.raises(TipoDeNotaInvalidoError):
            Nota(materia="Calculo", semestre="2025-1", valor=valor_invalido)

    def test_boolean_es_rechazado_aunque_python_lo_considere_int(self):
        # bool es subclase de int en Python; el dominio NO acepta True/False.
        with pytest.raises(TipoDeNotaInvalidoError):
            Nota(materia="Calculo", semestre="2025-1", valor=True)


class TestValoresLimite:
    """REQ-1: BVA en 0.0 y 5.0 con delta=0.01."""

    @pytest.mark.parametrize("valor", [0.0, 0.01, 4.99, 5.0])
    def test_valores_en_o_dentro_del_limite_son_validos(self, valor):
        nota = Nota(materia="Calculo", semestre="2025-1", valor=valor)
        assert nota.valor == valor

    @pytest.mark.parametrize("valor", [-0.01, 5.01])
    def test_valores_apenas_fuera_del_limite_son_rechazados(self, valor):
        with pytest.raises(NotaFueraDeRangoError):
            Nota(materia="Calculo", semestre="2025-1", valor=valor)


class TestValoresEspeciales:
    """REQ-1: NaN y los infinitos no son notas validas."""

    @pytest.mark.parametrize("valor", [math.nan, math.inf, -math.inf])
    def test_nan_e_infinitos_son_rechazados(self, valor):
        with pytest.raises(NotaFueraDeRangoError):
            Nota(materia="Calculo", semestre="2025-1", valor=valor)
