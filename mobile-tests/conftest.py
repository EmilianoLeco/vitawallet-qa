# mobile-tests/conftest.py
import pytest
import logging
import os
from pathlib import Path
from datetime import datetime
from appium import webdriver
from appium.options.android import UiAutomator2Options
from dotenv import load_dotenv

# CARGAR VARIABLES DE ENTORNO AL INICIO
# Buscar el archivo .env en el directorio raíz del proyecto
BASE_DIR = Path(__file__).parent.parent
env_path = BASE_DIR / ".env"

if env_path.exists():
    load_dotenv(dotenv_path=env_path)
    print(f"[OK] Variables de entorno cargadas desde: {env_path}")

    # Validar variables críticas
    critical_vars = {
        'ANDROID_DEVICE_NAME': os.getenv('ANDROID_DEVICE_NAME'),
        'ANDROID_UDID': os.getenv('ANDROID_UDID'),
        'ANDROID_PLATFORM_VERSION': os.getenv('ANDROID_PLATFORM_VERSION'),
        'QA_USER_EMAIL': os.getenv('QA_USER_EMAIL'),
        'QA_USER_PASSWORD': os.getenv('QA_USER_PASSWORD')
    }

    print("\nVariables criticas cargadas:")
    for var_name, var_value in critical_vars.items():
        status = "[OK]" if var_value else "[FAIL]"
        display_value = var_value if var_name != 'QA_USER_PASSWORD' else "***" if var_value else None
        print(f"  {status} {var_name} = {display_value}")

    missing_vars = [k for k, v in critical_vars.items() if not v]
    if missing_vars:
        print(f"\n[WARNING] Variables faltantes en .env: {', '.join(missing_vars)}")
else:
    print(f"[ERROR] No se encontro el archivo .env en: {env_path}")
    print("Crea el archivo .env en la raiz del proyecto con las variables necesarias")

def pytest_configure(config):
    """Configuración inicial de pytest para mobile tests"""
    # Crear directorios necesarios
    directories = [
        "reports",
        "reports/screenshots",
        "reports/logs",
        "reports/mobile"
    ]
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
    
    # Configurar markers
    config.addinivalue_line("markers", "smoke: Smoke tests")
    config.addinivalue_line("markers", "regression: Regression tests")
    config.addinivalue_line("markers", "mobile: Mobile tests")

def pytest_runtest_setup(item):
    """Ejecutar antes de cada test"""
    logger = logging.getLogger(__name__)
    logger.info("=" * 80)
    logger.info(f"Iniciando test: {item.name}")
    logger.info("=" * 80)

def pytest_runtest_teardown(item, nextitem):
    """Ejecutar después de cada test"""
    logger = logging.getLogger(__name__)
    logger.info("=" * 80)
    logger.info(f"Test finalizado: {item.name}")
    logger.info("=" * 80)

@pytest.fixture(scope="session", autouse=True)
def test_session_setup():
    """Setup que se ejecuta una vez por sesión de tests"""
    logger = logging.getLogger(__name__)
    logger.info("Iniciando sesión de tests mobile")
    logger.info(f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    yield

    logger.info("Finalizando sesión de tests mobile")