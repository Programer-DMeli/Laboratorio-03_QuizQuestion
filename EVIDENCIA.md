# EVIDENCIA — Laboratorio 03: Django Quiz (Orquestación de Agentes)

## 1. Información general

| Campo | Detalle |
| --- | --- |
| **Laboratorio** | Lab03 — Django: Orquestación de Agentes (OpenCode) |
| **Aplicación** | `quiz` (Examenes / Preguntas / Opciones) |
| **Stack** | Python 3.14 · Django 5.2.17 · SQLite |
| **Ubicación** | `/home/meli_dev/cuarto_ciclo/Aplicaciones_empresariales/Lab03` |
| **Entregable** | Este documento (`EVIDENCIA.md`) en la raíz del proyecto |

### Estructura de carpetas

```
Lab03/
├── .venv/                      # Entorno virtual (no versionado)
├── .opencode/agents/           # Agentes y registro de especificaciones (lab)
├── requirements.txt            # Django==5.2.17
├── EVIDENCIA.md                # ← Este entregable
└── src/
    ├── manage.py
    ├── db.sqlite3              # Base de datos local (no versionada)
    ├── config/                 # settings.py, urls.py, asgi.py, wsgi.py
    └── quiz/                   # Aplicación de dominio
        ├── models.py           # Exam, Question, Choice
        ├── forms.py            # ExamForm, QuestionForm, ChoiceFormSet
        ├── views.py            # listar, crear, detalle, editar, eliminar
        ├── urls.py             # Rutas del namespace `quiz`
        ├── admin.py            # Registro del modelo
        ├── tests.py            # 5 tests (vistas + formset)
        ├── migrations/         # 0001_initial, 0002_question_puntaje
        ├── management/commands/seed.py
        └── templates/quiz/     # base.html, exam_list, exam_detail, question_form
```

---

## 2. Justificación de tipos de campo

Los modelos se definen en `src/quiz/models.py`. Se justifica el tipo de campo elegido
para **cada atributo** (más de los 3 mínimos exigidos por modelo).

### 2.1 Modelo `Exam` (cabecera del examen)

| Atributo | Tipo de campo | Justificación técnica |
| --- | --- | --- |
| `title` | `CharField(max_length=200)` | Título corto e identificador visible del examen. Se acota a 200 caracteres porque son cadenas acotadas (nombres/etiquetas) y no contenido extenso; en SQLite se materializa como `varchar(200)` según `PRAGMA`, sin costo de texto largo. |
| `description` | `TextField` | Descripción libre y potencialmente extensa (resumen del examen). No tiene límite de longitud en el esquema; en SQLite se materializa como `TEXT`, evitando truncamientos que un `CharField` corto provocaría. |
| `created_at` | `DateTimeField(auto_now_add=True)` | Fecha de creación que solo debe fijarse al insertar el registro y no cambiar con cada `save()`. `auto_now_add` delega el timestamp a Django y garantiza inmutabilidad temporal; en `PRAGMA` se ve como `datetime`. |

### 2.2 Modelo `Question` (pregunta de un `Exam`)

| Atributo | Tipo de campo | Justificación técnica |
| --- | --- | --- |
| `text` | `TextField` | Enunciado de la pregunta: texto libre cuyo largo es impredecible (puede ser largo). `TEXT` en SQLite sin límite; es el tipo correcto frente a un `CharField` con tope arbitrario. |
| `exam` | `ForeignKey(Exam, on_delete=CASCADE, related_name='questions')` | Relación N:1 (muchas preguntas → un examen). La FK garantiza integridad referencial y el índice `quiz_question_exam_id` creado en migración optimiza el acceso por examen. |
| `puntaje` | `PositiveIntegerField(default=0)` | Puntaje aritmético entero que no puede ser negativo. El tipo unsigned + `CHECK (puntaje >= 0)` (verificado en el SQL emitido por la migración 0002) lo impone a nivel de BD. `default=0` da un valor seguro ante alta directa. (Ver sección 5.) |
| `created_at` | `DateTimeField(auto_now_add=True)` | Momento de creación de la pregunta, inmutable desde el insert. Es un `datetime` de SQLite; permite ordenar el listado (`ordering = ['exam', 'created_at']`). |

### 2.3 Modelo `Choice` (opción de respuesta)

| Atributo | Tipo de campo | Justificación técnica |
| --- | --- | --- |
| `text` | `CharField(max_length=255)` | Texto breve de la opción (p. ej. "Perro"). Acotado a 255 porque las opciones son cortas; en `PRAGMA` se materializa como `varchar(255)`, más compacto que `TEXT`. |
| `question` | `ForeignKey(Question, on_delete=CASCADE, related_name='choices')` | Relación N:1 (muchas opciones → una pregunta). Garantiza que cada opción pertenece a una pregunta existente y permite acceder desde la pregunta vía `question.choices`. |
| `is_correct` | `BooleanField(default=False)` | Flag binario que indica si la opción es la correcta. Un `bool` de SQLite (`0`/`1`) es el tipo mínimo y exacto para cardinalidad de verdad; `default=False` evita opciones "correctas" accidentales al crearlas sin marcar. |

### 2.4 Relaciones y `on_delete`

Las dos relaciones forman la jerarquía del dominio `Exam → Question → Choice`:

- `Question.exam` y `Choice.question` son **claves foráneas** (N:1); se materializan en la BD como `exam_id`/`question_id` (`bigint` según `PRAGMA`).
- `on_delete=CASCADE`: si se elimina un `Exam`, se eliminan en cascada sus preguntas y opciones (evita huérfanos e integridad rota). Es la semántica correcta porque las opciones/preguntas no tienen significado sin su cabecera.
- `related_name='questions'` / `related_name='choices'`: habilita acceso reverso idiomático `exam.questions.all()` y `question.choices.all()`, y es lo que usa la vista de detalle y las plantillas para listar preguntas y opciones de cada examen.

---

## 3. Capturas / logs reales

Todas las salidas se ejecutaron con el venv del proyecto
(`/home/meli_dev/cuarto_ciclo/Aplicaciones_empresariales/Lab03/.venv/bin/python`) desde
`src/`. Ninguna es simulada.

### 3.1 `python manage.py check`

```text
$ .venv/bin/python manage.py check
System check identified no issues (0 silenced).
```

### 3.2 `python manage.py makemigrations --check --dry-run`

```text
$ .venv/bin/python manage.py makemigrations --check --dry-run
No changes detected
```

No hay migraciones pendientes: el esquema coincide con lo declarado en los modelos.

### 3.3 `python manage.py sqlmigrate quiz 0002`

```text
$ .venv/bin/python manage.py sqlmigrate quiz 0002
BEGIN;
--
-- Add field puntaje to question
--
CREATE TABLE "new__quiz_question" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "puntaje" integer unsigned NOT NULL CHECK ("puntaje" >= 0), "text" text NOT NULL, "created_at" datetime NOT NULL, "exam_id" bigint NOT NULL REFERENCES "quiz_exam" ("id") DEFERRABLE INITIALLY DEFERRED);
INSERT INTO "new__quiz_question" ("id", "text", "created_at", "exam_id", "puntaje") SELECT "id", "text", "created_at", "exam_id", 0 FROM "quiz_question";
DROP TABLE "quiz_question";
ALTER TABLE "new__quiz_question" RENAME TO "quiz_question";
CREATE INDEX "quiz_question_exam_id_963bb8ea" ON "quiz_question" ("exam_id");
COMMIT;
```

El SQL emitido confirma el `CHECK ("puntaje" >= 0)` a nivel de base de datos, la
recreación de la tabla con los valores existentes y el índice de la FK.

### 3.4 Inspección real de la BD (PRAGMA)

Nota: la herramienta CLI `sqlite3` no está instalada en el entorno, por lo que la
inspección se hizo con `PRAGMA table_info` a través de la conexión de Django a la misma
BD `db.sqlite3` (evidencia equivalente y real).

```text
$ python manage.py shell -c "<inspección PRAGMA>"
TABLES: auth_group, auth_group_permissions, auth_permission, auth_user, auth_user_groups, auth_user_user_permissions, django_admin_log, django_content_type, django_migrations, django_session, quiz_choice, quiz_exam, quiz_question, sqlite_sequence
--- quiz_exam ---
(0, 'id', 'INTEGER', 1, None, 1)
(1, 'title', 'varchar(200)', 1, None, 0)
(2, 'description', 'TEXT', 1, None, 0)
(3, 'created_at', 'datetime', 1, None, 0)
--- quiz_question ---
(0, 'id', 'INTEGER', 1, None, 1)
(1, 'text', 'TEXT', 1, None, 0)
(2, 'created_at', 'datetime', 1, None, 0)
(3, 'exam_id', 'bigint', 1, None, 0)
(4, 'puntaje', 'integer unsigned', 1, None, 0)
--- quiz_choice ---
(0, 'id', 'INTEGER', 1, None, 1)
(1, 'text', 'varchar(255)', 1, None, 0)
(2, 'is_correct', 'bool', 1, None, 0)
(3, 'question_id', 'bigint', 1, None, 0)
```

Las tres tablas del dominio existen con las columnas esperadas.

### 3.5 Conteos del seed

El seed (`manage.py seed`) es idempotente: crea el examen "Sonido de los animales" con
2 preguntas y 8 opciones (4 por pregunta). Verificación con `manage.py shell -c`:

```text
$ python manage.py shell -c "from quiz.models import Question; ..."
seed questions: 2 | corrects: 2
¿Qué animal dice 'guau'?
¿Qué animal dice 'miau'?
```

Detalle por atributos del seed (opciones con su bandera `is_correct`):

```text
Q2: "¿Qué animal dice 'guau'?" puntaje=0 correctas=1
Q3: "¿Qué animal dice 'miau'?" puntaje=0 correctas=1
- C3: 'Perro' (correcta=True)      - C4: 'Gato' (correcta=False)
- C5: 'Pato' (correcta=False)      - C6: 'Vaca' (correcta=False)
- C7: 'Gato' (correcta=True)       - C8: 'Perro' (correcta=False)
- C9: 'Pájaro' (correcta=False)    - C10: 'Caballo' (correcta=False)
```

Cada pregunta tiene **exactamente una** opción correcta (regla de negocio del lab).

> Nota de trazabilidad: en la BD además existen 3 exámenes con título "T" (ids 4–6),
> creados durante la verificación funcional manual de la vista de alta. Los conteos
> globales de la tabla son `Exam=4, Question=2, Choice=8`; el seed aporta el examen
> "Sonido de los animales" (id=3) con sus 2 preguntas / 8 opciones.

### 3.6 `python manage.py test quiz -v 2`

```text
$ python manage.py test quiz -v 2
Creating test database for alias 'default' ('file:memorydb_default?mode=memory&cache=shared')...
Found 5 test(s).
Operations to perform:
  Synchronize unmigrated apps: messages, staticfiles
  Apply all migrations: admin, auth, contenttypes, quiz, sessions
Synchronizing apps without migrations:
  Creating tables...
    Running deferred SQL...
Running migrations:
  Applying contenttypes.0001_initial... OK
  Applying auth.0001_initial... OK
  Applying admin.0001_initial... OK
  Applying admin.0002_logentry_remove_auto_add... OK
  Applying admin.0003_logentry_add_action_flag_choices... OK
  Applying contenttypes.0002_remove_content_type_name... OK
  Applying auth.0002_alter_permission_name_max_length... OK
  Applying auth.0003_alter_user_email_max_length... OK
  Applying auth.0004_alter_user_username_opts... OK
  Applying auth.0005_alter_user_last_login_null... OK
  Applying auth.0006_require_contenttypes_0002... OK
  Applying auth.0007_alter_validators_add_error_messages... OK
  Applying auth.0008_alter_user_username_opts... OK
  Applying auth.0009_alter_user_last_name_max_length... OK
  Applying auth.0010_alter_group_name_max_length... OK
  Applying auth.0011_update_proxy_permissions... OK
  Applying auth.0012_alter_user_first_name_max_length... OK
  Applying quiz.0001_initial... OK
  Applying quiz.0002_question_puntaje... OK
  Applying sessions.0001_initial...test_exam_detail_200 (quiz.tests.ExamViewTests.test_exam_detail_200) ... ok
test_exam_list_200 (quiz.tests.ExamViewTests.test_exam_list_200) ... ok
test_question_create_invalid_two_correct (quiz.tests.ExamViewTests.test_question_create_invalid_two_correct) ... ok
test_question_create_invalid_zero_correct (quiz.tests.ExamViewTests.test_question_create_invalid_zero_correct) ... ok
test_question_create_valid (quiz.tests.ExamViewTests.test_question_create_valid) ... ok

----------------------------------------------------------------------
Ran 5 tests in 0.119s

OK

Destroying test database for alias 'default' ('file:memorydb_default?mode=memory&cache=shared')...
 OK
System check identified no issues (0 silenced).
```

Suite en verde: **5/5 OK**.

---

## 4. Casos de prueba

Los 5 casos están en `src/quiz/tests.py` (`ExamViewTests`).

| Caso | Qué valida | Resultado esperado | Resultado real |
| --- | --- | --- | --- |
| `test_exam_list_200` | GET a `quiz:exam_list` responde HTTP 200 | `200` | `ok` |
| `test_exam_detail_200` | GET a `quiz:exam_detail` responde HTTP 200 | `200` | `ok` |
| `test_question_create_valid` | Alta válida con **1 sola** opción correcta y `puntaje=10` → redirección al detalle del examen | `302` + 1 Question + 2 Choices + 1 correcta | `ok` |
| `test_question_create_invalid_two_correct` | Alta inválida con **2** opciones correctas → formset inválido, no persiste nada | `200`, `is_valid()==False`, non_form_errors, 0 registros | `ok` |
| `test_question_create_invalid_zero_correct` | Alta inválida con **0** opciones correctas → formset inválido, no persiste nada | `200`, `is_valid()==False`, non_form_errors, 0 registros | `ok` |

### Validación de "exactamente una opción correcta"

Se implementa en `src/quiz/forms.py` en `BaseChoiceFormSet.clean()`: conta las opciones
con `is_correct=True` (omitiendo formas eliminadas o vacías) y, si el total `!= 1`,
lanza `ValidationError("Cada pregunta debe tener exactamente una opción correcta ...")`
con código `invalid_correct_choices`. El error aparece como *non-form error* del formset,
por lo que la vista redirige en el caso válido (`302`) y re-renderiza el formulario con
el error en el caso inválido (`200`). La prueba negativa cubre tanto el fallo por exceso
(2 correctas) como por defecto (0 correctas).

---

## 5. Decisión de diseño del campo `puntaje`

- **Tipo:** `PositiveIntegerField(default=0)` (`src/quiz/models.py:26`).
- **Justificación:** los puntajes por pregunta son enteros no negativos (no tiene sentido
  restar en la encuesta base del lab). `PositiveIntegerField` lo expresa en el ORM y, en
  SQLite, Django lo materializa como `integer unsigned` con `CHECK (puntaje >= 0)`, tal
  como se comprueba en el SQL de la migración 0002 (sección 3.3): la restricción queda
  **impuesta por la base de datos**, no solo por la capa de aplicación.
- **Migración adicional:** `0002_question_puntaje` añade el campo poblándolo con `0` para
  los registros existentes (recreación de tabla con `SELECT ... , 0`), conservando los ids
  y la FK. `default=0` asegura que futuros inserts sin puntaje explícito no rompan la
  integridad.
- **Verificación:** `makemigrations --check --dry-run` → `No changes detected`, lo que
  confirma que la migración adicional está consolidada y el modelo no tiene drift.