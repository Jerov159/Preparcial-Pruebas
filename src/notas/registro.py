"""Servicio de aplicacion que orquesta el registro y consulta de notas."""

from __future__ import annotations

from notas.errores import NotaDuplicadaError, SinNotasError
from notas.modelo import Nota


class RegistroNotas:
    """Coleccion de notas de un estudiante.

    Expone las operaciones que el dominio necesita: registrar una nota nueva
    (REQ-1) y calcular el promedio actual (REQ-3). El control de duplicados
    (REQ-4) se anade en una iteracion posterior siguiendo TDD.
    """

    def __init__(self) -> None:
        self._notas: list[Nota] = []

    def registrar(self, *, materia: str, semestre: str, valor: float) -> Nota:
        """Crea una ``Nota`` y la agrega al registro.

        Reglas combinadas:
            - REQ-1: la validacion de rango y tipo la realiza ``Nota``.
            - REQ-4: no se permite duplicar (materia, semestre); si ya existe
              una nota para esa combinacion se lanza ``NotaDuplicadaError`` y
              el estado del registro no cambia.
        """
        if self._existe_duplicado(materia, semestre):
            raise NotaDuplicadaError(
                f"Ya existe una nota registrada para la materia '{materia}' "
                f"en el semestre '{semestre}'."
            )
        nota = Nota(materia=materia, semestre=semestre, valor=valor)
        self._notas.append(nota)
        return nota

    def _existe_duplicado(self, materia: str, semestre: str) -> bool:
        return any(
            n.materia == materia and n.semestre == semestre for n in self._notas
        )

    def promedio(self) -> float:
        """REQ-3: promedio aritmetico de las notas registradas."""
        if not self._notas:
            raise SinNotasError(
                "No se puede calcular el promedio: no hay notas registradas."
            )
        return sum(nota.valor for nota in self._notas) / len(self._notas)

    @property
    def notas(self) -> tuple[Nota, ...]:
        """Vista inmutable de las notas registradas (utilidad para tests/BDD)."""
        return tuple(self._notas)
