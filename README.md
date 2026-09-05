##  El Reparto de Agentes (Roles y Especialidades)

Cada subagente tiene un rol muy claro dentro del sistema para evitar "ruido" en la comunicación y garantizar código de nivel profesional:

| Agente | Rol | Especialidad |
| :--- | :--- | :--- |
| 🤠 **`Django-Capataz`** | Orquestador / Tech Lead | Lee la metodología, asigna tareas y supervisa la entrega de cada fase. |
| 🏗️ **`django-arquitecto`** | Arquitectura y Entorno | Configura carpetas (`src/`, `config/`), entorno virtual y `requirements.txt`. |
| 🗄️ **`django-modelador`** | Ingeniero de Datos | Diseña los modelos `Exam`, `Question`, `Choice`, maneja la clase `Meta` y migraciones. |
| ⚙️ **`django-vistas`** | Lógica de Negocio | Desarrolla las vistas, formularios, formsets y la regla de opción correcta única. |
| 🎨 **`django-templatero`** | Diseñador UI/UX | Construye plantillas HTML hermosas, modernas y responsivas con componentes UI. |
| 🛡️ **`django-administrador`** | Superusuario y Admin | Registra paneles en `admin.py` y genera datos iniciales de prueba. |
| 🔍 **`django-revisor`** | Auditor QA | Realiza refactorizaciones, cambios de campos (`puntaje`) y control de calidad. |
| 🐙 **`django-github`** | Control de Versiones | Controla los commits y el estado del repositorio Git. |
| 📝 **`django-entregable`** | Documentación | Genera el informe final `EVIDENCIA.md` con justificaciones y pruebas. |

---

## 💡 ¿Por qué es Vital Delegar Tareas a Subagentes?

Delegar no es solo por orden, es la clave para que la Inteligencia Artificial no cometa errores en proyectos grandes:

* 🎯 **Enfoque de Dominio (Domain Isolation):** El agente de diseño no necesita saber cómo funciona SQL, y el agente de datos no necesita saber sobre diseño de interfaces. Cada uno tiene instrucciones perfeccionadas para su área.
* 🧠 **Uso Eficiente de Memoria (Context Overhead):** Al dividir el trabajo, los chats son más cortos y enfocados. Esto evita que la IA empiece a olvidar instrucciones o inventar código.
* 🛡️ **Seguridad y Aislamiento:** Un fallo en la interfaz gráfica no altera la estructura de la base de datos ni elimina tus archivos de configuración.
* 🕵️ **Trazabilidad Inmediata:** Si un formulario falla, sabemos exactamente a qué subagente pedirle cuentas (`django-vistas`) sin revisar todo el proyecto.

---

## 🚀 Paso a Paso para Orquestar tus Agentes

Sigue estas sencillas instrucciones para arrancar tu equipo de desarrollo virtual dentro de **Open Code**:

### Paso 1: Inicialización del Equipo
Copia el prompt de configuración de agentes e inyéctalo en Open Code. Esto creará la carpeta `.opencode/agents/` con los perfiles (`.md`) de cada subagente y la configuración global `opencode.json`.

### Paso 2: Selección del Capataz
En la barra inferior de Open Code, cambia tu agente activo a **`Django-Capataz`**.

### Paso 3: Inyección de la Metodología
Envia la lista de las 12 tareas del proyecto al Capataz. Él tomará el control y empezará a llamar a sus colaboradores en secuencia lógica:
1. Llamará a `@django-github` para iniciar el repo.
2. Pasará el control a `@django-arquitecto` para la estructura.
3. Le pedirá a `@django-modelador` que cree la base de datos.
4. Y así sucesivamente hasta completar el 100% del checklist.

---

## ⚡ Opciones Avanzadas de Orquestación (Pro Level)

Para llevar este modelo a producción o proyectos de gran escala, se pueden aplicar técnicas avanzadas:

* 🔄 **Autocorrección (Self-Healing Loops):** Si la consola arroja un error al ejecutar `python manage.py migrate`, el Capataz captura la falla y se la reenvía inmediatamente al `django-modelador` para que la corrija de forma autónoma.
* 🔀 **Ejecución Paralela (DAGs):** Tareas independientes (como redactar documentación y diseñar componentes CSS de la interfaz) son ejecutadas en paralelo por distintos subagentes para ahorrar tiempo.
* 🛑 **Verificación Estricta (QA Gates):** Ningún paso se da por finalizado hasta que el subagente de auditoría (`django-revisor`) pase una suite de pruebas automatizadas.

---

## 🎖️ Recomendaciones de Nivel Senior

> 1. **Mantén el Contexto Delgado:** Evita enviarle todo el código del proyecto al Agente Capataz; él solo debe leer estados, resúmenes e instrucciones de coordinación.
> 2. **Sistemas de Entrega Claros:** Define reglas estrictas para la entrega entre agentes. *Ejemplo: "El modelador debe entregar el código con migraciones probadas antes de pasarlo al agente de vistas"*.
> 3. **Bloqueo de Archivos Sensibles:** Restringe el acceso de escritura de los subagentes a archivos críticos como `settings.py` para prevenir cambios no autorizados.

---
