# QA Automation - Vita Wallet Technical Test

Proyecto de automatización de pruebas para API (Petstore) y Mobile (Vita Wallet Android).

**Autor:** Emiliano Lecoña
**Fecha:** Octubre 2025
**Repositorio:** https://github.com/EmilianoLeco/vitawallet-qa

> 🐳 **NUEVO:** Ahora disponible con Docker! Ver [DOCKER.md](DOCKER.md) para ejecutar sin instalaciones.

---

## Descripción

Este proyecto contiene la automatización completa de pruebas de API Petstore y pruebas mobile para la aplicación Vita Wallet.

**API Tests:**
- 20 casos de prueba automatizados
- Cobertura completa de operaciones CRUD (POST, GET, PUT, DELETE)
- Implementación dual: Python/Pytest + Postman/Newman
- Casos positivos y negativos

**Mobile Tests:**
- Flujo completo de intercambio cripto ARS → USDT
- Framework: Appium + Python
- Patrón Page Object Model (POM)

---

## Estructura del Proyecto

```
qa-automation-vitawallet/
├── api-tests/
│   ├── postman/
│   │   └── Petstore_Collection.json
│   └── pytest/
│       ├── test_petstore_api.py
│       └── conftest.py
├── mobile-tests/
│   ├── tests/
│   │   └── test_crypto_exchange.py
│   ├── pages/
│   │   ├── base_page.py
│   │   ├── login_page.py
│   │   └── crypto_page.py
│   └── config/
│       └── capabilities.py
├── reports/
│   ├── pytest/
│   ├── newman/
│   └── mobile/
├── requirements.txt        # Dependencias Python
├── package.json           # Dependencias Node.js (Newman, Appium)
├── pytest.ini
├── run_api_pytest.bat     # Script para ejecutar API tests con Pytest
├── run_api_newman.bat     # Script para ejecutar API tests con Newman
└── run_mobile_tests.bat   # Script interactivo para Mobile tests
```

---

## Prerequisitos

### Opción 1: Instalación Local (Tradicional)
- Python 3.8 o superior
- Node.js 14+ y npm
- Git
- Appium 2.x (solo para mobile tests)
- Android SDK (solo para mobile tests)

### Opción 2: Con Docker (Recomendado) 🐳
- Docker Desktop
- Git
- Archivo `.env` configurado

> **Nota:** Para ejecución con Docker, ver [DOCKER.md](DOCKER.md)

---

## Instalación

> 🐳 **¿Prefieres usar Docker?** Salta a [DOCKER.md](DOCKER.md) para instalación y ejecución simplificada.

### Instalación Local

#### 1. Clonar el repositorio
```bash
git clone https://github.com/EmilianoLeco/vitawallet-qa.git
cd vitawallet-qa
```

#### 2. Instalar dependencias de Node.js
```bash
# Instalar Newman, Appium y dependencias
npm install

# Instalar driver de Appium para Android
npx appium driver install uiautomator2
```

#### 3. Configurar entorno Python
```bash
# Crear entorno virtual
python -m venv venv

# Activar entorno virtual
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt
```

#### 4. Configurar variables de entorno (Mobile Tests)
```bash
# Copiar el archivo de ejemplo
copy .env.example .env

# Editar .env con tus credenciales y configuración de dispositivo
# - Credenciales de QA
# - UDID de tu dispositivo Android
# - Versión de Android
# - etc.
```

**Nota:** El archivo `.env` contiene información sensible y NO debe subirse al repositorio.

---

## Ejecución de Tests

### Scripts BAT Disponibles

#### 1. `run_api_pytest.bat` - API Tests con Pytest
**Descripción:** Ejecuta los 20 casos de prueba de la API Petstore usando Pytest.

**Características:**
- ✅ Activa automáticamente el entorno virtual
- ✅ Genera reporte HTML con timestamp
- ✅ Abre el reporte automáticamente en el navegador
- ✅ Muestra resultados en consola con formato verbose

**Uso:**
```bash
# Doble clic en el archivo o ejecutar desde cmd:
run_api_pytest.bat
```

**Reporte generado:** `reports/pytest/api_report_[timestamp].html`

---

#### 2. `run_api_newman.bat` - API Tests con Newman
**Descripción:** Ejecuta la colección de Postman usando Newman (CLI).

**Características:**
- ✅ Verifica que Newman esté instalado
- ✅ Genera reporte HTML con tema oscuro
- ✅ Genera reporte JSON adicional
- ✅ Abre el reporte automáticamente en el navegador
- ✅ Delay de 500ms entre requests

**Uso:**
```bash
# Doble clic en el archivo o ejecutar desde cmd:
run_api_newman.bat
```

**Reportes generados:**
- HTML: `reports/newman/newman_report_[timestamp].html`
- JSON: `reports/newman/newman_report_[timestamp].json`

---

#### 3. `run_mobile_tests.bat` - Mobile Tests Interactivo
**Descripción:** Menú interactivo para ejecutar tests mobile de Vita Wallet.

**Características:**
- ✅ Valida que el entorno virtual esté activado
- ✅ Verifica que Appium Server esté corriendo (puerto 4723)
- ✅ Menú con 5 opciones de ejecución
- ✅ Genera reporte HTML automáticamente
- ✅ Pregunta si deseas abrir el reporte al finalizar

**Opciones del menú:**
1. **Ejecutar flujo completo de Crypto Exchange** - Test completo ARS → USDT
2. **Ejecutar todos los tests de Crypto Exchange** - Todos los tests del archivo
3. **Ejecutar todos los tests de mobile-tests** - Suite completa
4. **Ejecutar test específico** - Ingresar ruta manualmente
5. **Salir**

**Uso:**
```bash
# Antes de ejecutar:
# 1. Activar entorno virtual
venv\Scripts\activate

# 2. Iniciar Appium Server (en otra terminal)
appium

# 3. Ejecutar el script
run_mobile_tests.bat
```

**Reporte generado:** `reports/mobile/mobile_report_[timestamp].html`

---

### Prerequisitos para Mobile Tests

**Antes de ejecutar `run_mobile_tests.bat` asegúrate de:**

1. **Entorno virtual activado:**
```bash
venv\Scripts\activate
```

2. **Appium Server corriendo:**
```bash
# En otra terminal:
appium
# Debe mostrar: [Appium] Welcome to Appium v2.x.x
```

3. **Dispositivo conectado o emulador corriendo:**
```bash
adb devices
# Debe mostrar al menos un dispositivo
```

---

### Ejecución Manual (Alternativa)

Si prefieres ejecutar manualmente sin los scripts BAT:

**API Tests - Pytest:**
```bash
venv\Scripts\activate
python -m pytest api-tests/pytest/ -v --html=reports/pytest/api_report.html --self-contained-html
```

**API Tests - Newman:**
```bash
newman run api-tests/postman/Petstore_Collection.json -r htmlextra --reporter-htmlextra-export reports/newman/report.html
```

**Mobile Tests:**
```bash
venv\Scripts\activate
pytest mobile-tests/tests/test_crypto_exchange.py::TestCryptoExchange::test_complete_crypto_exchange_flow -v -s --html=reports/report.html --self-contained-html
```

---

## Casos de Prueba

### API Tests - Petstore (20 casos)

#### Pet Endpoints (13 casos)
| Método | Tipo | Descripción |
|--------|------|-------------|
| POST | Positivo | Crear mascota con datos válidos |
| POST | Negativo | Crear mascota con datos inválidos |
| POST | Negativo | Crear mascota sin body |
| GET | Positivo | Obtener mascota por ID |
| GET | Negativo | Buscar mascota inexistente |
| GET | Negativo | ID con formato inválido |
| GET | Positivo | Buscar mascotas por status |
| PUT | Positivo | Actualizar mascota existente |
| PUT | Negativo | Actualizar mascota inexistente |
| PUT | Negativo | Actualizar con datos inválidos |
| DELETE | Positivo | Eliminar mascota existente |
| DELETE | Negativo | Eliminar mascota inexistente |
| DELETE | Negativo | Eliminar con ID inválido |

#### Store Endpoints (7 casos)
| Método | Tipo | Descripción |
|--------|------|-------------|
| POST | Positivo | Crear orden válida |
| POST | Negativo | Crear orden inválida |
| GET | Positivo | Obtener orden por ID |
| GET | Negativo | Orden inexistente |
| GET | Positivo | Obtener inventario |
| DELETE | Positivo | Eliminar orden |
| DELETE | Negativo | Eliminar orden inexistente |

**Cobertura:** 100% de operaciones CRUD  
**Success Rate:** 20/20 tests pasando

### Mobile Tests - Vita Wallet

**Flujo principal:** Login → Navegación Cripto → Intercambio ARS → USDT

**Configuración:**
Las credenciales y configuración del dispositivo se obtienen del archivo `.env` (no incluido en el repositorio por seguridad).
Ver `.env.example` para conocer las variables requeridas.

---

## Reportes

Todos los scripts BAT generan reportes HTML automáticamente:

| Script | Ubicación del Reporte | Formato |
|--------|----------------------|---------|
| `run_api_pytest.bat` | `reports/pytest/api_report_[timestamp].html` | HTML (self-contained) |
| `run_api_newman.bat` | `reports/newman/newman_report_[timestamp].html` | HTML + JSON |
| `run_mobile_tests.bat` | `reports/mobile/mobile_report_[timestamp].html` | HTML (self-contained) |

**Características de los reportes:**
- ✅ Se abren automáticamente en el navegador al finalizar
- ✅ Incluyen resultados detallados de cada test
- ✅ Muestran tiempo de ejecución
- ✅ Screenshots en caso de fallos (mobile tests)
- ✅ Formato HTML responsive y profesional

---

## Buenas Prácticas Implementadas

### Código
- ✅ Page Object Model (POM) para mobile tests
- ✅ Fixtures de pytest para setup/teardown
- ✅ Separación de responsabilidades (tests, pages, config)
- ✅ Tests independientes y reutilizables
- ✅ Cleanup automático de datos
- ✅ Logging detallado
- ✅ Screenshots en caso de fallos

### Automatización
- ✅ Scripts BAT para Windows con validaciones pre-ejecución
- ✅ Generación automática de reportes HTML con timestamps
- ✅ Apertura automática de reportes en navegador
- ✅ Menú interactivo para mobile tests
- ✅ Validación de entorno virtual y servicios (Appium)

---

## Configuración

### Variables de entorno

**API Tests:** No requieren variables de entorno.

**Mobile Tests:** Utilizan archivo `.env` para credenciales y configuración del dispositivo.

**Archivo `.env.example`** (incluido en el repositorio):
```bash
# Credenciales de QA
QA_USER_EMAIL=tu_email@vitawallet.io
QA_USER_PASSWORD=tu_contraseña

# Configuración del Dispositivo Android
ANDROID_PLATFORM_VERSION=15
ANDROID_DEVICE_NAME=TU_DEVICE_NAME
ANDROID_UDID=TU_DEVICE_UDID

# URLs
QA_BASE_URL=https://qa.vitawallet.io/
APPIUM_SERVER_URL=http://127.0.0.1:4723

# Configuración de la App
APP_PACKAGE=com.vita_wallet
APP_ACTIVITY=com.vita_wallet.MainActivity
APK_PATH=mobile-tests/app/VitaQA.apk

# Datos de prueba
DEFAULT_EXCHANGE_AMOUNT=1000
FROM_CURRENCY=ARS
TO_CURRENCY=USDT
```

**Pasos para configurar:**
1. Copiar `.env.example` a `.env`
2. Editar `.env` con tus credenciales y configuración de dispositivo
3. El archivo `.env` está en `.gitignore` y NO se sube al repositorio

---

## Troubleshooting

### Scripts BAT

**`run_api_pytest.bat` - Error: "No se encuentra el entorno virtual"**
```bash
# Crear entorno virtual primero:
python -m venv venv
pip install -r requirements.txt
```

**`run_api_newman.bat` - Error: "Newman no esta instalado"**
```bash
# Instalar dependencias desde package.json:
npm install
```

**`run_mobile_tests.bat` - Error: "El entorno virtual no esta activado"**
```bash
# Activar antes de ejecutar el script:
venv\Scripts\activate
# Luego ejecutar:
run_mobile_tests.bat
```

**`run_mobile_tests.bat` - Error: "Appium Server no esta corriendo"**
```bash
# En otra terminal:
appium
# Debe mostrar: [Appium] Welcome to Appium v2.x.x
```

**Error: "curl no reconocido" (al validar Appium)**
- Instalar curl o usar PowerShell en lugar de CMD
- Alternativamente, comentar la validación de Appium en el BAT

### Mobile Tests

**Error: "No devices connected"**
```bash
adb devices
# Si no aparece ninguno, reiniciar adb:
adb kill-server
adb start-server
```

**Error: "App not found"**
- Verificar que el APK esté en la ruta correcta
- Revisar configuración en `mobile-tests/config/capabilities.py`

---

## Tecnologías Utilizadas

### Python
- **Testing:** Pytest 7.4.3, Appium-Python-Client 3.1.0
- **API:** Requests 2.31.0
- **Reporting:** pytest-html 4.1.1
- **Automation:** Selenium 4.15.2

### Node.js
- **CLI Testing:** Newman 6.1.0
- **Reporting:** newman-reporter-htmlextra 1.23.0
- **Mobile Automation:** Appium 2.11.0

### Tools
- Postman (Collections)
- Android SDK & ADB

---

## API Base URL

**Petstore API:** https://petstore.swagger.io/v2  
**Documentación:** https://petstore.swagger.io/


**Tiempo de ejecución:**
- API Tests (Pytest): ~30 segundos
- API Tests (Newman): ~30 segundos
- Mobile Tests: ~2-3 minutos
