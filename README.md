
# INTRODUCCIÓN To-Do Tasks API

API REST para una buena gestión de tareas grupales o personales, construida principalmente con **Flask**, **Flask-RESTFUL**,**SQLALCHEMY** y autenticación mediante **JWT**. Cada usuario puede registrarse, iniciar sesion y administrar únicamente sus propias tareas.
---

## TECNOLOGIAS USADAS
|    **TECNOLOGÍA**    |   ** EMPLEAMIENTO **               |
| Flask                |  Micro Framework Web               |
| Flask-RESTFUL        |  Estructura de recursos/endpoints  |
| Flask-SQLAlchemy     |  ORM para la Base de Datos         |
| Flask Migrate        |  Migraciones (Alembic)             |
| Flask-JWT-Extended   |  Autenticación con JWT             |
| Pydantic             |  Validación de Datos               |
| PostgreSQL           |  Base de Datos                     |
| Bcrypt               |  Hasheo de contraseñas             |

---

## CARACTERISTICAS

- Registro e inicio de sesión de usuarios con contraseñas totalmente hasheadas (uso de `bcrypt`)
- Autenticación mediante **JSON Web Tokens** (uso de `Flash-JWT-Extended`)
- CRUD completo de tareas (CREAR, VER, EDITAR Y ELIMINAR)
- Marcado de tareas como completadas o pendientes
- Validación de datos de ingresados con **Pydantic**
- Aislamiento de datos: Cada usuario solo puede ver y modificar lo suyo
- Migraciones de base de datos haciendo uso de **Flask-Migrate** (Alembic)

---

## ESTRUCTURA DEL PROYECTO

```
proyecto/
├── app/
│   ├── __init__.py          # Inicialización de Flask, DB, JWT, migraciones
│   ├── router.py            # Registro de rutas (endpoints)
│   ├── models/
│   │   ├── user_model.py
│   │   └── task_model.py
│   ├── schemas/
│   │   ├── auth_schema.py
│   │   ├── user_schema.py
│   │   ├── show_user_schema.py
│   │   └── task_schema.py
│   ├── services/
│   │   ├── user_service.py
│   │   └── task_service.py
│   ├── resources/
│   │   ├── auth_resource.py
│   │   ├── user_resource.py
│   │   └── task_resource.py
│   └── utils/
│       └── helpers.py       # hash_password, verify_password
├── config.py
├── db.py
├── run.py
└── requirements.txt
```
---

## COPIA DEL PROYECTO

1. Clona el repositorio y entra en la carpeta del proyecto en VS CODE
2. Activa el entorno virtual
```bash
source entorno_virtual/Scripts/activate
```

3. Instala las dependencias:

```bash
pip install -r requirements.txt
```

4. Crea un archivo **.env** en la raíz (app) con tus variables de entorno

```env
DATABASE_URL=postgresql://usuario:password@localhost:5432/todo_db
JWT_SECRET_KEY=tu_clave_secreta
```

5. Aplica migraciones:
```bash
flask db init
flask db migrate -m "create users and tasks tables"
flask db upgrade
```
6. Levanta tu servidor:

```bash
python run.py
```

El servidor estará inicializandose en: `http://127.0.0.1:5000`. :D

---

## AUTENTICACIÓN

La API utiliza JWT de Flask. Despues de iniciar sesión, recibirás un `access token`que debe enviarse en el header `Authorization` de cada endpoint protegido:

```
Authorization: Bearer <access_token>
```

**NOTA**: TODOS LOS ENDPOINTS MENOS EL `REGISTER` REQUIEREN EL USO DEL `BEARER TOKEN` AL INICIAR SESIÓN.

---

## ENDPOINTS 

Puedes usar Bruno o Postman para la lectura de los endpoints :D

### REGISTRAR USUARIO
```
POST /api/v1/auth/register
```

**Body:**
```json
{
  "name": "John",
  "last_name": "Doe",
  "email": "johndoe@example.com",
  "password": "12345678"
}
```
**Respuesta `201`:**
```json
{
  "id": 1,
  "name": "Juan",
  "last_name": "Pérez",
  "email": "juan@example.com",
  "is_active": true,
  "created_at": "2026-07-06T10:00:00",
  "updated_at": "2026-07-06T10:00:00"
}
```

**NOTA:** `400` SIGNIFICA QUE EL EMAIL YA EXISTE O LOS DATOS SON INVÁLIDOS

---

#### INICIAR SESIÓN
```
POST /api/v1/auth/login
```

**Body:**
```json
{
  "email": "johndoe@example.com",
  "password": "12345678"
}
```

**Respuesta `200`:**
```json
{
  "access": "eyJhbGciOiJIUzI1NiIs...", 
  "refresh": "eyJhbGciOiJIUzI1NiIs..."
}
```

**NOTA:** `4O4` SIGNIFICA QUE EL USUARIO NO SE HA ENCONTRADO O QUE LA CONTRASEÑA O EMAIL SON INCORRECTOS

---

### USUARIOS

### CÓMO VER USUARIOS Y SUS TAREAS
```
GET /api/v1/users/<user_id>
```
**NOTA** ANTES DE USAR ESTE ENDPOINT DEBES USAR TU BEARER TOKEN, PUEDES VOLVER A LEER LA GUÍA PARA ENTENDER CÓMO

**Respuesta `200`:**
```json
{
  "id": 1,
  "name": "John",
  "last_name": "Doe",
  "email": "Johndoe@example.com",
  "is_active": true,
  "created_at": "2026-07-06T10:00:00",
  "updated_at": "2026-07-06T10:00:00",
  "tasks": [
    {
      "id": 1,
      "title": "Presentar mi proyecto de Tecsup",
      "description": "Entrega el 6 de julio a las 7 de la noche",
      "is_completed": false,
      "priority": "high",
      "due_date": "2026-07-15T18:00:00",
      "created_at": "2026-07-06T11:00:00"
    }
  ]
}
```

**NOTAS:** `403` SIGNIFICA QUE EL USUARIO NO ESTÁ AUTORIZADO(No puedes ver la tarea de otro usuario), `404` USUARIO NO ENCONTRADO

---

#### EDITAR EL USUARIO
```
PUT /api/v1/users/<user_id>
```

**Body:**
```json
{
  "name": "John",
  "last_name": "Doe",
  "email": "Johndoe@example.com"
}
```
**Respuesta `200`:** datos actualizados del usuario.

**Errores:** `400` (datos inválidos) · `403` (no autorizado) · `404` (no encontrado)

---

#### BORRAR EL USUARIO
```
DELETE /api/v1/users/<user_id>
```

**Respuesta `200`:**
```json
{
  "message": "User deleted successfully"
}
```

**Errores:** `403` (no autorizado) · `404` (no encontrado)

---

### TASK

#### CREAR TAREA
```
POST /api/v1/tasks
```

**Body:**
```json
{
  "title": "Terminar API",
  "description": "Completar el README",
  "priority": "high",
  "due_date": "2026-07-15T18:00:00"
}
```

**Respuesta `201`:**
```json
{
  "id": 1,
  "title": "Terminar API",
  "description": "Completar el README",
  "is_completed": false,
  "priority": "high",
  "due_date": "2026-07-15 18:00:00",
  "created_at": "2026-07-06 11:00:00",
  "updated_at": "2026-07-06 11:00:00"
}
```

**Errores:** `400` (datos inválidos)

---

#### LISTAR LAS TAREAS
```
GET /api/v1/tasks/usuario
```

**Respuesta `200`:** lista de tareas del usuario autenticado.
```json
[
  {
    "id": 1,
    "title": "Terminar API",
    "is_completed": false,
    "priority": "high",
    "due_date": "2026-07-15 18:00:00",
    "..."
  }
]
```

---

#### VER UNA TAREA
```
GET /api/v1/tasks/<task_id>
```

**Respuesta `200`:** datos de la tarea.

**Errores:** `404` (no encontrada o no pertenece al usuario)

---

#### EDITAR LA TAREA
```
PUT /api/v1/tasks/<task_id>
```

**Body:** igual que crear tarea.

**Respuesta `200`:** tarea actualizada.

**Errores:** `400` (datos inválidos) · `404` (no encontrada)

---

#### ELIMINAR LA TAREA
```
DELETE /api/v1/tasks/<task_id>
```

**Respuesta `200`:**
```json
{
  "message": "Task was successfully deleted"
}
```

**Errores:** `404` (no encontrada)

---

#### MARCAR COMO COMPLETADA O PENDIENTE
```
PATCH /api/v1/tasks/<task_id>/complete
```

Alterna el valor de `is_completed`(True o False).

**Respuesta `200`:** tarea con el nuevo estado.

**Errores:** `404` (no encontrada)

---

## REGLAS DE LA API

- Un usuario **solo** puede ver, editar o eliminar su propia cuenta.
- Un usuario **solo** puede ver, editar, eliminar o completar sus propias tareas.
- `priority` acepta únicamente: `low`, `medium`, `high`.
- El campo `password` nunca se expone en las respuestas de la API.

---

## CÓMO PROBAR

Se recomienda usar [Bruno](https://www.usebruno.com/) o Postman:

1. `POST /auth/register` → crea tu usuario
2. `POST /auth/login` → copia el `access` token
3. Configura el header `Authorization: Bearer <token>` en el resto de requests
4. Prueba crear, listar, editar y completar tareas
5. Verifica en `GET /users/<id>` que las tareas aparezcan anidadas

---
