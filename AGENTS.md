# Laboratorio 03 — Django: Orquestación de Agentes (OpenCode)

## Propósito

Este repositorio implementa el **Laboratorio 03** de Aplicaciones Empresariales (cuarto ciclo) mediante una **arquitectura de agentes de OpenCode**. Un agente **orquestador** (`django-capataz`) desglosa el trabajo en un checklist de **12 pasos**, delega la ejecución **secuencial** a **subagentes especializados**, y aplica **puertas de validación** estrictas antes de avanzar.

La fuente de verdad de los requisitos del laboratorio es el subagente/registro `lab` (`.opencode/agents/lab.md`). Ningún agente puede inventar requisitos fuera de ese registro.

## Arquitectura y flujo

```
Usuario ──> django-capataz (orquestador, primary)
              │ 1. Lee las especificaciones (lab)
              │ 2. Desglosa el checklist de 12 pasos
              │ 3. Delega UN paso a la vez (ejecución secuencial)
              │ 4. Exige verificación (django-revisor) por etapa
              │ 5. Ordena commits (django-github) y evidencia (django-entregable)
              │
              ├─ django-arquitecto    → estructura del proyecto
              ├─ django-modelador     → ORM / modelos / migraciones / inspección BD
              ├─ django-administrador → admin.py, superusuario, datos de prueba
              ├─ django-vistas        → vistas, forms, formsets, URLs
              ├─ django-templatero    → UI/UX y plantillas HTML
              ├─ django-revisor       → QA, refactor, verificación estricta
              ├─ django-github        → control de versiones / commits
              └─ django-entregable    → EVIDENCIA.md
```

## Directorio de agentes y herramientas

La asignación de herramientas a cada agente está codificada en la cabecera (`permission`) de cada archivo de `.opencode/agents/`. Matriz de referencia:

| Agente | Modo | Rol | Herramientas principales | Herramientas denegadas |
| --- | --- | --- | --- | --- |
| `django-capataz` | primary | Orquestador | task, todowrite, read, glob, grep, question | edit, bash (solo `git status/log/branch/remote`), web |
| `django-arquitecto` | subagent | Estructura del proyecto | read, edit, glob, grep, list, bash | task, web |
| `django-modelador` | subagent | Modelos ORM y migraciones | read, edit, glob, grep, list, bash | task, web |
| `django-vistas` | subagent | Vistas, formularios, URLs | read, edit, glob, grep, list, bash | task, web |
| `django-templatero` | subagent | UI/UX y plantillas | read, edit, glob, grep, list, bash | task, web |
| `django-administrador` | subagent | admin.py, superuser, seed | read, edit, glob, grep, list, bash | task, web |
| `django-revisor` | subagent | QA / refactor / verificación | read, edit, glob, grep, list, bash, question | task, web |
| `django-github` | subagent | Control de versiones | read, glob, grep, list, bash (`git*`) | edit, task, bash (no git), web |
| `django-entregable` | subagent | Documento `EVIDENCIA.md` | read, edit, glob, grep, list, bash (solo salidas/lectura) | task, web |
| `lab` | subagent | Registro de especificaciones | read, glob, grep, list | edit, bash, task, web |

Nota: `task` denegado en todos los subagentes impide delegación anidada (profundidad máxima = 1). Con esto el flujo es siempre orquestado por el capataz.

## Checklist de 12 pasos

| # | Paso | Agente responsable | Puerta de validación |
| --- | --- | --- | --- |
| 1 | Estructura del proyecto (virtualenv, `src/`, `config/`, `requirements.txt`, `.gitignore`) | django-arquitecto | venv activa + `manage.py check` sin errores |
| 2 | Modelos `Exam`, `Question`, `Choice` + clase `Meta` | django-modelador | revisión del modelo (revisor) |
| 3 | Migraciones iniciales e inspección de BD | django-modelador | tablas presentes en `sqlite3` |
| 4 | Registro en `admin.py` | django-administrador | `manage.py check` + panel admin responde |
| 5 | Superusuario y datos de prueba (seed) | django-administrador | conteo de registros en el shell de Django |
| 6 | Vistas (listar, crear, detalle, editar, eliminar) | django-vistas | cada URL responde con HTTP 200/302 |
| 7 | Formularios + Formset (validación opción correcta única) | django-vistas | prueba de validación positiva y negativa |
| 8 | URLs / routing | django-vistas | `resolve()` de todas las rutas |
| 9 | Plantillas UI (base, listado, detalle) | django-templatero | renderizado sin errores en navegador/CLI |
| 10 | Refactor + migración adicional (campo `puntaje`) | django-revisor | `makemigrations --check --dry-run` limpio |
| 11 | Verificación estricta (`check`, tests, inspección BD) | django-revisor | suite de verificación completa en verde |
| 12 | Control de versiones + `EVIDENCIA.md` | django-github / django-entregable | commits por etapa + evidencia revisada |

## Protocolo de orquestación

1. El capataz lee el registro de especificaciones (`lab`) y crea el checklist con `todowrite`.
2. Ejecuta los pasos **en orden secuencial**: un solo subagente activo a la vez, con contexto mínimo (spec, archivos afectados, entregable esperado).
3. Tras cada paso, invoca a `django-revisor` como **puerta de calidad**. Si la verificación falla, el paso regresa al agente responsable con el reporte de errores; no se avanza mientras no esté en verde.
4. `django-github` crea un commit incremental al cierre de cada etapa aprobada.
5. Al completar los pasos 1-11, `django-entregable` redacta `EVIDENCIA.md` (justificación de tipos de campo, capturas simuladas/logs, casos de prueba) y el capataz solicita la revisión final al revisor.
6. Ante bloqueos o decisiones ambiguas, el capataz escala al usuario con la herramienta `question` — los subagentes nunca deciden requisitos por sí mismos.

## Reglas de interfaz entre agentes

- **Un solo agente activo**: el capataz jamás lanza dos subagentes en paralelo; la ejecución es estrictamente secuencial.
- **Contexto mínimo explícito**: cada delegación incluye el requisito (del registro `lab`), los archivos en los que trabajar y el criterio de aceptación esperado.
- **Definición de "hecho"**: una tarea está hecha solo cuando (a) existe código en disco, (b) pasa la verificación del revisor y (c) el capataz lo marca como completado en el checklist.
- **Comunicación**: cada subagente responde con un reporte corto: qué hizo, archivos modificados, comandos/validaciones ejecutadas y salidas relevantes.
- **No saltos de paso**: ningún subagente puede modificar archivos fuera de su alcance; si lo necesita, lo reporta al capataz para que delegue al agente adecuado.

## Puertas de calidad

- `python manage.py check` limpio en cada etapa.
- `python manage.py makemigrations --check --dry-run` (sin migraciones pendientes) tras los pasos de modelos.
- Inspección real de la BD con `sqlite3` (tablas, columnas y `PRAGMA table_info`).
- Validación negativa del formulario: no puede existir más de una opción correcta por pregunta.
- Los commits son atómicos por tema y no incluyen secretos, `.venv/` ni artefactos.

## Convenciones de control de versiones

- Mensajes de commit convencionales y en español descriptivo: `feat(models): agrega modelos Exam, Question, Choice`, `fix(forms): valida única opción correcta`, `docs: agrega EVIDENCIA.md`.
- No `push` automático: solo commits/ramas locales salvo aprobación explícita del usuario.
- No se versionan secretos, configuraciones con `apiKey`, `.venv/`, `__pycache__/` ni base de datos local.

## Glosario del laboratorio

- `Exam` — examen/encuesta (cabecera).
- `Question` — pregunta perteneciente a un `Exam`; define el tipo (texto, opción múltiple, etc.).
- `Choice` — opción de respuesta asociada a una `Question`; exactamente una es correcta.
- `puntaje` — campo adicional solicitado en verificación (migración extra supervisada por el revisor).
- **EVIDENCIA.md** — documento final que justifica 3 tipos de campo por modelo, complementado con capturas simuladas/logs y casos de prueba.