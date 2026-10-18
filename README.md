# GuardianQuake — Backend API (FastAPI + MySQL)

API REST para las funcionalidades **complementarias** de GuardianQuake:
cuentas de usuario, respaldo de historial de eventos, contenido educativo
y gestión de la suscripción Pro.

## ⚠️ Alcance importante

La detección sísmica en sí (RF01–RF07: leer el acelerómetro, distinguir
la onda P, activar/desactivar vigilancia, alertar, mostrar estado en
tiempo real) ocurre **100% en el dispositivo, sin internet** (RNF01).
Esta API **no participa en esa detección** — solo da soporte a las
funciones que sí tiene sentido llevar a la nube:

| RF/RNF | Función | ¿Vive en la API? |
|---|---|---|
| RF01–RF05, RF07 | Detección y alerta en tiempo real | ❌ 100% en el dispositivo |
| RF06 | Sismograma en tiempo real (sensibilidad fija, no configurable) | ❌ 100% en el dispositivo |
| RF08 | Historial de eventos | ✅ respaldo en la nube |
| RF09 | Contenido educativo | ✅ servido desde la API |
| RF10 | Versión gratuita / Pro | ✅ control de suscripción |

## 1. Arquitectura

```
guardianquake_backend/
├── app/
│   ├── main.py                 # Punto de entrada FastAPI, registra routers
│   ├── database.py             # Engine, sesión SQLAlchemy
│   ├── security.py             # Hash de password (bcrypt) y JWT
│   ├── models/
│   │   └── models.py           # Modelos SQLAlchemy (una clase por tabla)
│   ├── schemas/
│   │   └── schemas.py          # Esquemas Pydantic (request/response)
│   ├── crud/                   # Lógica de negocio (equivalente a "controladores")
│   │   ├── usuarios.py
│   │   ├── dispositivos.py
│   │   ├── eventos.py
│   │   ├── contenido.py
│   │   ├── suscripcion.py
│   │   └── contactos.py
│   └── routers/                 # Endpoints HTTP (uno por recurso)
│       ├── usuarios.py
│       ├── dispositivos.py
│       ├── eventos.py
│       ├── contenido.py
│       ├── suscripcion.py
│       └── contactos.py
├── database/
│   └── schema.sql               # DDL + datos semilla (MySQL)
├── config.py                    # Variables de entorno (DB, JWT)
└── requirements.txt
```

**Flujo de una petición:** `Router` recibe el HTTP → valida el body con
un esquema `Pydantic` → delega en la función de `crud/` correspondiente →
esa función usa los `models/` (SQLAlchemy) para leer/escribir en MySQL →
FastAPI serializa la respuesta con el esquema de salida.

## 2. Modelo de datos (MySQL)

| Tabla | Descripción |
|---|---|
| `usuarios` | Cuenta (correo, password_hash, tipo_cuenta FREE/PRO) |
| `dispositivos` | Modelo/fabricante registrado, para calibración (RNF04) |
| `eventos_sismicos` | Respaldo del historial detectado localmente (RF08) |
| `contenido_educativo` | Artículos que la app consulta/actualiza (RF09) |
| `suscripciones` | Historial de compras/estado de la versión Pro (RF10) |
| `contactos_emergencia` | Contactos para notificación automática (función Pro) |

Ver el DDL completo en `database/schema.sql`.

## 3. Endpoints implementados

**Usuarios / autenticación**
| Método | Endpoint | Descripción |
|---|---|---|
| POST | `/api/usuarios/registro` | Crear cuenta (201) |
| POST | `/api/usuarios/login` | Login (OAuth2 form), devuelve JWT (200) |
| GET | `/api/usuarios/me` | Perfil del usuario autenticado (200) |

**Dispositivos**
| Método | Endpoint | Descripción |
|---|---|---|
| POST | `/api/dispositivos` | Registrar modelo/fabricante (201) |
| GET | `/api/dispositivos/{id}/calibracion` | Sensibilidad recomendada (200) |

**Eventos sísmicos (historial)**
| Método | Endpoint | Descripción |
|---|---|---|
| POST | `/api/eventos` | Respaldar un evento detectado localmente (201) |
| GET | `/api/eventos?desde=&hasta=` | Listar historial del usuario (200) |
| GET | `/api/eventos/{id}` | Detalle de un evento (200) |

**Contenido educativo**
| Método | Endpoint | Descripción |
|---|---|---|
| GET | `/api/contenido-educativo` | Listar artículos (200) |
| GET | `/api/contenido-educativo/{id}` | Detalle de un artículo (200) |

**Suscripción Pro**
| Método | Endpoint | Descripción |
|---|---|---|
| GET | `/api/suscripcion/estado` | Consultar si el usuario tiene Pro (200) |
| POST | `/api/suscripcion/verificar-compra` | Validar transacción y activar Pro (201) |
| POST | `/api/suscripcion/cancelar` | Cancelar Pro (200) |

**Contactos de emergencia**
| Método | Endpoint | Descripción |
|---|---|---|
| GET | `/api/contactos-emergencia` | Listar contactos (200) |
| POST | `/api/contactos-emergencia` | Agregar contacto (201) |
| DELETE | `/api/contactos-emergencia/{id}` | Eliminar contacto (204) |

Todos los endpoints (excepto registro, login, calibración y contenido
educativo, que son públicos) requieren el header:
```
Authorization: Bearer <token>
```

## 4. Documentación interactiva (Swagger / ReDoc)

FastAPI genera la documentación automáticamente, sin dependencias extra:

- **Swagger UI:** `http://localhost:8000/docs`
- **ReDoc:** `http://localhost:8000/redoc`
- **OpenAPI JSON:** `http://localhost:8000/openapi.json`

## 5. Despliegue en servidor local

### Requisitos
- Python 3.10+
- MySQL 8 o MariaDB 10.x

### Paso a paso

```bash
# 1. Instalar MariaDB (si no la tienes)
sudo apt-get update
sudo apt-get install -y mariadb-server mariadb-client
sudo service mariadb start

# 2. Crear usuario y base de datos
sudo mysql -u root -e "
  CREATE USER IF NOT EXISTS 'guardian_user'@'127.0.0.1' IDENTIFIED BY 'guardian_pass';
  CREATE USER IF NOT EXISTS 'guardian_user'@'localhost' IDENTIFIED BY 'guardian_pass';
  GRANT ALL PRIVILEGES ON guardianquake_db.* TO 'guardian_user'@'127.0.0.1';
  GRANT ALL PRIVILEGES ON guardianquake_db.* TO 'guardian_user'@'localhost';
  FLUSH PRIVILEGES;
"

# 3. Cargar el modelo de datos y los datos semilla
sudo mysql -u root < database/schema.sql

# 4. Crear entorno virtual e instalar dependencias
python3 -m venv venv
source venv/bin/activate          # Windows: venv\Scripts\activate
pip install -r requirements.txt

# 5. (Opcional) variables de entorno si usas otras credenciales
export DB_USER=guardian_user
export DB_PASSWORD=guardian_pass
export DB_HOST=127.0.0.1
export DB_PORT=3306
export DB_NAME=guardianquake_db
export JWT_SECRET_KEY=cambia-esto-en-produccion

# 6. Levantar el servidor
uvicorn app.main:app --host 0.0.0.0 --port 8001 --reload
# API disponible en http://localhost:8001
# Documentacion en http://localhost:8001/docs
```

### Ejemplo de flujo completo (curl)

```bash
# Registro
curl -X POST http://localhost:8000/api/usuarios/registro \
  -H "Content-Type: application/json" \
  -d '{"correo":"demo@guardianquake.com","password":"secreto123"}'

# Login (nota: es un formulario, no JSON)
curl -X POST http://localhost:8001/api/usuarios/login \
  -d "username=demo@guardianquake.com&password=secreto123"
# -> {"access_token": "...", "token_type": "bearer"}

# Usar el token en cualquier endpoint protegido
curl http://localhost:8001/api/usuarios/me \
  -H "Authorization: Bearer <access_token>"
```

Este backend fue probado en un entorno local (MariaDB 10.11 + FastAPI
0.115 + Uvicorn), ejecutando los 16 endpoints exitosamente con los
códigos de estado esperados (200/201/204), incluyendo el flujo completo:
registro → login → registrar dispositivo → consultar calibración →
configurar sensibilidad → registrar y listar eventos → consultar
contenido educativo → activar y consultar suscripción Pro → gestionar
contactos de emergencia.

## 6. Notas de diseño

- **Autenticación:** JWT con `python-jose`, contraseñas con `bcrypt`
  directo (sin `passlib`, que tiene un bug de compatibilidad conocido
  con versiones recientes de `bcrypt`).
- **Suscripción Pro (RF10):** `verificar-compra` valida que el
  `id_transaccion` de Google Play no se haya usado antes (evita
  duplicar la activación con el mismo recibo) y actualiza
  `tipo_cuenta` del usuario a `PRO`.
- **Sensibilidad fija (RF06):** la app ya NO permite configurar el
  nivel de sensibilidad — siempre opera al máximo, para priorizar no
  perder ninguna alerta real sobre reducir falsos positivos. Por eso
  no existe ningún endpoint de configuración en esta API; el campo
  `sensibilidad_usada` en `eventos_sismicos` siempre se recibe en 10,
  y se conserva solo como registro histórico/de auditoría.
- **Historial (RF08):** los endpoints de eventos filtran siempre por
  el usuario autenticado — un usuario no puede ver el historial de otro.
