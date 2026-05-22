# Diseno de Pruebas - Modulo de Notas Academicas

Este documento contiene el analisis de pruebas exigido por el preparcial:
particiones de equivalencia, analisis de valores limite, preguntas al Product
Owner y los 12 casos de prueba minimos (3 por requerimiento).

---

## 1. Particiones de equivalencia

### REQ-1: nota entre 0.0 y 5.0

| #  | Particion                              | Rango                | Valor rep. | Resultado esperado                      |
|----|----------------------------------------|----------------------|------------|------------------------------------------|
| P1 | Nota valida (interior)                 | `[0.0, 5.0]`         | `3.5`      | Registrar la nota correctamente          |
| P2 | Nota invalida por debajo               | `(-inf, 0.0)`        | `-1.5`     | Lanzar `NotaFueraDeRangoError`           |
| P3 | Nota invalida por encima               | `(5.0, +inf)`        | `7.2`      | Lanzar `NotaFueraDeRangoError`           |
| P4 | Tipo de dato invalido (no numerico)    | `str`, `None`, `list`| `"cinco"`  | Lanzar `TipoDeNotaInvalidoError`         |
| P5 | Valor especial (NaN, +inf, -inf)       | `nan`, `inf`         | `nan`      | Lanzar `NotaFueraDeRangoError`           |

> Nota sobre notacion: se usa `[ ]` para incluir el extremo y `( )` para
> excluirlo. Como `0.0` y `5.0` SI son notas validas (limite inclusivo), la
> particion valida usa corchetes.

### REQ-2: aprueba si nota >= 3.0 (asume nota ya valida en [0.0, 5.0])

| #  | Particion                | Rango               | Valor rep. | Resultado esperado |
|----|--------------------------|---------------------|------------|---------------------|
| P1 | Reprobada                | `[0.0, 3.0)`        | `2.0`      | `False`             |
| P2 | Aprobada                 | `[3.0, 5.0]`        | `4.0`      | `True`              |

### REQ-3: promedio de notas

| #  | Particion                                | Caracteristica                | Ejemplo                | Resultado esperado |
|----|------------------------------------------|-------------------------------|------------------------|--------------------|
| P1 | Estudiante con multiples notas validas   | n >= 2                        | `[3.0, 4.0, 5.0]`      | `4.0`              |
| P2 | Estudiante con una unica nota            | n == 1                        | `[3.5]`                | `3.5`              |
| P3 | Estudiante sin notas registradas         | n == 0                        | `[]`                   | Lanzar `SinNotasError` |

### REQ-4: no permitir duplicados por (materia, semestre)

| #  | Particion                                              | Estado previo                                  | Accion              | Resultado esperado |
|----|--------------------------------------------------------|------------------------------------------------|---------------------|---------------------|
| P1 | Primer registro (materia, semestre) nuevo              | Sin registros previos                          | Registrar           | OK                  |
| P2 | Segundo registro misma materia y mismo semestre        | Ya existe nota para (M, S)                     | Registrar           | Lanzar `NotaDuplicadaError` |
| P3 | Misma materia pero diferente semestre                  | Ya existe nota para (M, 2025-1)                | Registrar (M, 2025-2)| OK                 |
| P4 | Diferente materia mismo semestre                       | Ya existe nota para (Calculo, S)               | Registrar (Fisica, S)| OK                 |

---

## 2. Analisis de valores limite (Boundary Value Analysis)

La regla aplicada es: para cada limite L, se evaluan tres valores -> `L - delta`,
`L`, `L + delta`. Para flotantes usamos `delta = 0.01`.

### REQ-1: rango `[0.0, 5.0]`

| Valor   | Dentro / fuera del rango | Resultado esperado |
|---------|--------------------------|---------------------|
| `-0.01` | Fuera (justo debajo)     | Error `NotaFueraDeRango` |
| `0.0`   | Dentro (limite inferior) | Registrar           |
| `0.01`  | Dentro (justo arriba)    | Registrar           |
| `4.99`  | Dentro (justo abajo)     | Registrar           |
| `5.0`   | Dentro (limite superior) | Registrar           |
| `5.01`  | Fuera (justo arriba)     | Error `NotaFueraDeRango` |

### REQ-2: umbral de aprobacion `3.0`

| Valor   | Resultado esperado |
|---------|---------------------|
| `2.99`  | `False` (reprueba) |
| `3.0`   | `True` (aprueba, limite inclusivo) |
| `3.01`  | `True` (aprueba) |

---

## 3. Preguntas al Product Owner (REQ-4)

Cuando un requerimiento dice "no permitir duplicados", siempre quedan
ambiguedades. Las preguntas siguientes impactan directamente el diseno de
pruebas y la modelacion del dominio:

1. **Que identifica una nota de manera unica?**
   - Posibilidad A: `(estudiante, materia, semestre)`
   - Posibilidad B: `(materia, semestre)` global
   - **Impacto en pruebas**: define si necesito modelar al estudiante o no, y si
     un mismo curso dictado a dos estudiantes distintos en el mismo semestre se
     considera duplicado o no.

2. **Como representamos el semestre?**
   - Formato `"2025-1"`, `"2025-S1"`, `int(20251)`, dataclass con anio y periodo.
   - **Impacto en pruebas**: define la equivalencia entre valores (por ejemplo
     `"2025-1"` y `"2025-I"` no son iguales como string, pero pueden ser el
     mismo semestre conceptual). Sin esto, no se que comparar.

3. **Que tipo de error debe recibir el usuario al intentar duplicar?**
   - Una excepcion tecnica con stacktrace, o un mensaje amable con datos del
     registro existente (`"Ya tienes una nota de 3.8 en Calculo 2025-1"`).
   - **Impacto en pruebas**: define el contrato del mensaje de error que se
     valida en los asserts.

> Preguntas propuestas por el estudiante (autoevaluacion): el usuario
> puede agregar aqui dos preguntas adicionales como ejercicio.

---

## 4. Casos de prueba (12 minimos: 3 por requerimiento)

Formato estandar: `ID | Requerimiento | Descripcion | Precondicion | Datos |
Pasos | Resultado esperado | Tipo`.

### Criterios para el tipo (Positivo / Negativo / Borde)

- **Positivo**: ejercita un valor del interior de una particion VALIDA y
  espera que el sistema acepte la operacion.
- **Negativo**: ejercita un valor del interior de una particion INVALIDA y
  espera que el sistema rechace la operacion (excepcion).
- **Borde**: ejercita exactamente un valor limite (`L`, `L - delta`,
  `L + delta`), sin importar si el resultado es exito o error.

### REQ-1: validacion de nota

| ID   | Req  | Descripcion                          | Precondicion        | Datos             | Pasos                                    | Resultado esperado                        | Tipo     |
|------|------|--------------------------------------|---------------------|-------------------|------------------------------------------|--------------------------------------------|----------|
| TC01 | REQ-1| Registrar nota valida interior       | Sistema inicializado| `nota=3.5`        | `registrar(materia, semestre, 3.5)`      | Nota registrada                            | Positivo |
| TC02 | REQ-1| Rechazar nota negativa               | Sistema inicializado| `nota=-1.5`       | `registrar(materia, semestre, -1.5)`     | Lanza `NotaFueraDeRangoError`              | Negativo |
| TC03 | REQ-1| Aceptar nota en limite inferior 0.0  | Sistema inicializado| `nota=0.0`        | `registrar(materia, semestre, 0.0)`      | Nota registrada                            | Borde    |

### REQ-2: aprobacion / reprobacion

| ID   | Req  | Descripcion                                  | Precondicion              | Datos       | Pasos                  | Resultado esperado | Tipo     |
|------|------|----------------------------------------------|---------------------------|-------------|------------------------|--------------------|----------|
| TC04 | REQ-2| Nota 4.0 debe aprobar                        | Sistema con nota 4.0      | `nota=4.0`  | `aprueba(nota)`        | `True`             | Positivo |
| TC05 | REQ-2| Nota 2.0 debe reprobar                       | Sistema con nota 2.0      | `nota=2.0`  | `aprueba(nota)`        | `False`            | Negativo |
| TC06 | REQ-2| Nota exactamente 3.0 debe aprobar (borde)    | Sistema con nota 3.0      | `nota=3.0`  | `aprueba(nota)`        | `True`             | Borde    |

### REQ-3: promedio

| ID   | Req  | Descripcion                                  | Precondicion                           | Datos                  | Pasos              | Resultado esperado     | Tipo     |
|------|------|----------------------------------------------|----------------------------------------|------------------------|--------------------|------------------------|----------|
| TC07 | REQ-3| Promedio de varias notas                     | Estudiante con 3, 4, 5                 | `[3.0, 4.0, 5.0]`     | `promedio()`       | `4.0`                  | Positivo |
| TC08 | REQ-3| Promedio con una sola nota                   | Estudiante con [3.5]                   | `[3.5]`                | `promedio()`       | `3.5`                  | Borde    |
| TC09 | REQ-3| Promedio sin notas debe fallar               | Estudiante sin notas                   | `[]`                   | `promedio()`       | Lanza `SinNotasError`  | Negativo |

### REQ-4: no permitir duplicados

| ID   | Req  | Descripcion                                                    | Precondicion                                           | Datos                                                       | Pasos                                                      | Resultado esperado                        | Tipo     |
|------|------|----------------------------------------------------------------|--------------------------------------------------------|-------------------------------------------------------------|------------------------------------------------------------|--------------------------------------------|----------|
| TC10 | REQ-4| Registro de materia nueva                                      | Sistema vacio                                          | `materia="Calculo"`, `semestre="2025-1"`, `nota=4.0`        | `registrar(...)`                                           | Nota registrada                            | Positivo |
| TC11 | REQ-4| Duplicado mismo (materia, semestre) lanza error                | Ya existe nota en `Calculo 2025-1`                    | Segundo intento con `Calculo, 2025-1, 3.5`                  | `registrar(...)`                                           | Lanza `NotaDuplicadaError`                 | Negativo |
| TC12 | REQ-4| Misma materia en distinto semestre se acepta                   | Existe nota en `Calculo 2025-1`                       | `Calculo, 2025-2, 4.2`                                      | `registrar(...)`                                           | Nota registrada                            | Borde    |
