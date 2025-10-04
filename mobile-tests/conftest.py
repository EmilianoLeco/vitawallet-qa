# mobile-tests/conftest.py
import pytest
import logging
import os
from pathlib import Path
from datetime import datetime
from appium import webdriver
from appium.options.android import UiAutomator2Options

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