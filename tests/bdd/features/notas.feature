# language: en
Feature: Registro de notas academicas
  Como estudiante del sistema academico
  Quiero registrar las notas de mis materias por semestre
  Para conocer mi rendimiento y saber si apruebo o repruebo cada curso

  Background:
    Given un registro de notas vacio

  @smoke @critical
  Scenario: Registrar una nota valida en el rango permitido
    When registro la materia "Calculo" en el semestre "2025-1" con nota 4.0
    Then el registro contiene 1 notas
    And la nota registrada para "Calculo" en "2025-1" es 4.0

  @critical
  Scenario Outline: Rechazar notas fuera del rango [0.0, 5.0]
    When intento registrar la materia "Calculo" en el semestre "2025-1" con nota <valor>
    Then el sistema lanza el error "NotaFueraDeRangoError"
    And el registro contiene 0 notas

    Examples:
      | valor |
      | -0.01 |
      | -1.5  |
      |  5.01 |
      |  7.2  |

  @regression
  Scenario Outline: Aprobacion segun la nota registrada
    When registro la materia "Calculo" en el semestre "2025-1" con nota <valor>
    Then la nota registrada para "Calculo" en "2025-1" tiene aprobacion <aprueba>

    Examples:
      | valor | aprueba |
      | 2.99  | False   |
      | 3.0   | True    |
      | 3.01  | True    |
      | 4.5   | True    |

  @critical
  Scenario: Calcular el promedio de tres notas validas
    When registro la materia "Calculo" en el semestre "2025-1" con nota 3.0
    And registro la materia "Fisica" en el semestre "2025-1" con nota 4.0
    And registro la materia "Algebra" en el semestre "2025-1" con nota 5.0
    Then el promedio del estudiante es 4.0

  @regression
  Scenario: Consultar el promedio sin notas lanza un error
    When consulto el promedio del estudiante
    Then el sistema lanza el error "SinNotasError"

  @critical @regression
  Scenario: No se permite registrar dos veces la misma materia en el mismo semestre
    Given existe una nota de 4.0 en la materia "Calculo" del semestre "2025-1"
    When intento registrar la materia "Calculo" en el semestre "2025-1" con nota 3.5
    Then el sistema lanza el error "NotaDuplicadaError"
    And el mensaje de error menciona "Calculo" y "2025-1"
    And el registro contiene 1 notas

  @regression
  Scenario: La misma materia en distinto semestre se acepta
    Given existe una nota de 4.0 en la materia "Calculo" del semestre "2025-1"
    When registro la materia "Calculo" en el semestre "2025-2" con nota 3.5
    Then el registro contiene 2 notas
