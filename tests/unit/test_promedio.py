"""Tests para REQ-3: calcular el promedio de las notas de un estudiante.

Cubre:
    - Promedio con varias notas validas.
    - Promedio con una unica nota.
    - Promedio sin notas: error de dominio.

Casos del documento de diseno asociados: TC07, TC08, TC09.
"""

from __future__ import annotations

import pytest

from notas.errores import SinNotasError
from notas.registro import RegistroNotas


class TestPromedioConNotas:
    """REQ-3: el promedio es la suma de notas dividida por la cantidad."""

    def test_promedio_de_tres_notas_es_correcto(self) -> None:
        registro = RegistroNotas()
        registro.registrar(materia="Calculo", semestre="2025-1", valor=3.0)
        registro.registrar(materia="Fisica", semestre="2025-1", valor=4.0)
        registro.registrar(materia="Algebra", semestre="2025-1", valor=5.0)

        assert registro.promedio() == pytest.approx(4.0)

    def test_promedio_de_una_sola_nota_es_esa_nota(self) -> None:
        registro = RegistroNotas()
        registro.registrar(materia="Calculo", semestre="2025-1", valor=3.5)

        assert registro.promedio() == pytest.approx(3.5)

    def test_promedio_maneja_decimales_sin_errores_de_redondeo(self) -> None:
        registro = RegistroNotas()
        registro.registrar(materia="Calculo", semestre="2025-1", valor=3.3)
        registro.registrar(materia="Fisica", semestre="2025-1", valor=4.7)

        assert registro.promedio() == pytest.approx(4.0)


class TestPromedioSinNotas:
    """REQ-3: si no hay notas, el promedio no esta definido."""

    def test_promedio_sin_notas_lanza_sin_notas_error(self) -> None:
        registro = RegistroNotas()
        with pytest.raises(SinNotasError):
            registro.promedio()
