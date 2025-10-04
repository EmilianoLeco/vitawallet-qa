# Ejecución con Docker

Esta guía explica cómo ejecutar los tests usando Docker, eliminando la necesidad de instalar Python, Node.js y Appium localmente.

---

## Prerequisitos

- **Docker Desktop** instalado y corriendo
  - Windows: https://www.docker.com/products/docker-desktop/
  - Linux/Mac: https://docs.docker.com/get-docker/
- **Docker Compose** (incluido en Docker Desktop)
- Archivo `.env` configurado (copiar de `.env.example`)

---

## Ventajas de usar Docker

✅ **Ambiente consistente** - Mismo entorno en cualquier máquina
✅ **Sin instalaciones** - No necesitas Python, Node.js, Appium localmente
✅ **Aislamiento** - No contamina tu sistema con dependencias
✅ **CI/CD Ready** - Fácil integración en pipelines
✅ **Reproducibilidad** - Resultados idénticos en cualquier máquina

---

## Estructura Docker

```
qa-automation-vitawallet/
├── docker/
│   ├── Dockerfile.api-tests       # Imagen para API tests
│   └── Dockerfile.mobile-tests    # Imagen para Mobile tests
├── docker-compose.yml             # Orquestación de servicios
├── .dockerignore                  # Archivos a ignorar
├── run-docker-tests.bat           # Script Windows
└── run-docker-tests.sh            # Script Linux/Mac
```

---

## Servicios Disponibles

### 1. **api-tests**
Ejecuta API tests con Pytest

```bash
docker-compose run --rm api-tests
```

### 2. **newman-tests**
Ejecuta API tests con Newman

```bash
docker-compose run --rm newman-tests
```

### 3. **appium**
Servidor Appium para mobile tests

```bash
docker-compose up -d appium
```

### 4. **mobile-tests**
Ejecuta mobile tests (requiere Appium corriendo)

```bash
docker-compose run --rm mobile-tests
```

---

## Ejecución Rápida

### Opción 1: Script Interactivo (Recomendado)

**Windows:**
```bash
run-docker-tests.bat
```

**Linux/Mac:**
```bash
./run-docker-tests.sh
```

**Menú disponible:**
```
1. Ejecutar API Tests (Pytest)
2. Ejecutar API Tests (Newman)
3. Ejecutar Mobile Tests
4. Iniciar Appium Server
5. Ver logs de Appium
6. Detener todos los contenedores
7. Limpiar imagenes y contenedores
8. Salir
```

### Opción 2: Comandos Directos

**API Tests con Pytest:**
```bash
docker-compose run --rm api-tests
```

**API Tests con Newman:**
```bash
docker-compose run --rm newman-tests
```

**Mobile Tests:**
```bash
# 1. Iniciar Appium
docker-compose up -d appium

# 2. Ejecutar tests (espera 10 segundos a que Appium esté listo)
docker-compose run --rm mobile-tests

# 3. Ver logs de Appium (opcional)
docker-compose logs -f appium

# 4. Detener Appium
docker-compose down
```

---

## Reportes

Los reportes se generan en la carpeta `reports/` de tu máquina local:

| Test | Ubicación |
|------|-----------|
| API Pytest | `reports/pytest/api_report.html` |
| API Newman | `reports/newman/newman_report.html` |
| Mobile | `reports/mobile/mobile_report.html` |

---

## Configuración para Mobile Tests

### 1. Crear archivo `.env`

```bash
# Windows
copy .env.example .env

# Linux/Mac
cp .env.example .env
```

### 2. Editar `.env` con tus credenciales

```bash
# Credenciales
QA_USER_EMAIL=tu_email@vitawallet.io
QA_USER_PASSWORD=tu_contraseña

# Dispositivo (si usas dispositivo real)
ANDROID_UDID=tu_device_udid
ANDROID_DEVICE_NAME=tu_device_name
```

### 3. Conectar dispositivo USB (Opcional)

**Linux/Mac:**
El `docker-compose.yml` ya monta `/dev/bus/usb` para usar dispositivos reales.

**Windows:**
Docker Desktop para Windows tiene limitaciones con USB. Opciones:
- Usar emulador Android en el host
- Usar WSL2 con soporte USB
- Ejecutar Appium en el host (no en Docker) y conectar desde el contenedor

---

## Comandos Útiles

### Build de imágenes
```bash
# Build todas las imágenes
docker-compose build

# Build imagen específica
docker-compose build api-tests
docker-compose build mobile-tests
```

### Ver logs
```bash
# Logs de todos los servicios
docker-compose logs

# Logs de servicio específico
docker-compose logs appium
docker-compose logs -f mobile-tests  # modo follow
```

### Detener servicios
```bash
# Detener todos
docker-compose down

# Detener y eliminar volúmenes
docker-compose down -v
```

### Limpiar
```bash
# Eliminar contenedores, imágenes sin usar
docker system prune -f

# Eliminar TODO (incluyendo imágenes del proyecto)
docker-compose down --rmi all -v
```

### Ejecutar comandos personalizados
```bash
# Ejecutar pytest con opciones específicas
docker-compose run --rm api-tests pytest api-tests/pytest/test_petstore_api.py::test_create_pet -v

# Bash en el contenedor (debug)
docker-compose run --rm api-tests bash
```

---

## Troubleshooting

### Error: "Cannot connect to Docker daemon" / "El sistema no puede encontrar el archivo especificado"

**Causa:** Docker Desktop no está corriendo.

**Solución Windows:**
1. Buscar "Docker Desktop" en el menú Inicio
2. Iniciar Docker Desktop
3. Esperar a que el ícono aparezca en la bandeja del sistema (system tray)
4. Cuando el ícono deje de parpadear, Docker está listo
5. Verificar: `docker --version` y `docker ps`

**Solución Linux:**
```bash
# Iniciar servicio Docker
sudo systemctl start docker

# Verificar estado
sudo systemctl status docker

# Habilitar inicio automático
sudo systemctl enable docker
```

**Solución Mac:**
1. Abrir Docker Desktop desde Applications
2. Esperar a que aparezca el ícono en la barra superior
3. Verificar: `docker --version` y `docker ps`

### Error: "Appium server not responding"
```bash
# Ver logs de Appium
docker-compose logs appium

# Reiniciar Appium
docker-compose restart appium

# Verificar que está corriendo
curl http://localhost:4723/status
```

### Mobile tests fallan con "No devices connected"
```bash
# Opción 1: Verificar dispositivo USB (Linux/Mac)
adb devices

# Opción 2: Usar emulador en el host
# Configurar APPIUM_SERVER_URL=http://host.docker.internal:4723 en .env
# Ejecutar Appium en el host en lugar de Docker
```

### Reportes no se generan
```bash
# Verificar que la carpeta reports/ existe y tiene permisos
mkdir -p reports/pytest reports/newman reports/mobile

# Linux/Mac: dar permisos
chmod -R 777 reports/
```

### Build muy lento
```bash
# Usar caché de Docker
docker-compose build --parallel

# Limpiar caché viejo
docker builder prune
```

---

## CI/CD Integration

### GitHub Actions

Crear `.github/workflows/docker-tests.yml`:

```yaml
name: QA Tests con Docker

on: [push, pull_request]

jobs:
  api-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Run API Tests (Pytest)
        run: docker-compose run --rm api-tests

      - name: Upload Reports
        uses: actions/upload-artifact@v3
        with:
          name: api-reports
          path: reports/

  newman-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Run API Tests (Newman)
        run: docker-compose run --rm newman-tests

      - name: Upload Reports
        uses: actions/upload-artifact@v3
        with:
          name: newman-reports
          path: reports/
```

### Jenkins

```groovy
pipeline {
    agent any
    stages {
        stage('API Tests - Pytest') {
            steps {
                sh 'docker-compose run --rm api-tests'
            }
        }
        stage('API Tests - Newman') {
            steps {
                sh 'docker-compose run --rm newman-tests'
            }
        }
    }
    post {
        always {
            publishHTML([
                reportDir: 'reports',
                reportFiles: '**/*.html',
                reportName: 'QA Reports'
            ])
        }
    }
}
```

---

## Comparación: Local vs Docker

| Aspecto | Instalación Local | Docker |
|---------|-------------------|--------|
| **Setup inicial** | Instalar Python, Node.js, Appium | Instalar solo Docker |
| **Tiempo de setup** | 30-60 minutos | 5 minutos |
| **Consistencia** | Varía según SO/versiones | Idéntico siempre |
| **Aislamiento** | Contamina sistema | Totalmente aislado |
| **CI/CD** | Configuración compleja | Plug & play |
| **Velocidad ejecución** | Más rápida | Ligeramente más lenta |
| **Debugging** | Más fácil | Requiere conocer Docker |

---

## Siguientes Pasos

1. ✅ Clonar el repositorio
2. ✅ Instalar Docker Desktop
3. ✅ Copiar `.env.example` a `.env` y configurar
4. ✅ Ejecutar `run-docker-tests.bat` (Windows) o `./run-docker-tests.sh` (Linux/Mac)
5. ✅ Ver reportes en `reports/`

---

## Soporte

Si encuentras problemas:
1. Revisa la sección Troubleshooting
2. Verifica logs: `docker-compose logs`
3. Abre un issue en GitHub: https://github.com/EmilianoLeco/vitawallet-qa/issues
