# mobile-tests/tests/test_login_only.py
import pytest
import logging
from appium import webdriver
from appium.options.android import UiAutomator2Options
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from pages.login_page import LoginPage
from config.capabilities import AppiumCapabilities, VitaWalletConfig

logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)


class TestLogin:
    """Tests solo de Login - BÁSICOS"""
    
    @pytest.fixture(scope="function")
    def driver(self):
        AppiumCapabilities.validate_app_exists()
        capabilities = AppiumCapabilities.get_android_capabilities()
        server_url = AppiumCapabilities.get_appium_server_url()
        
        options = UiAutomator2Options()
        options.load_capabilities(capabilities)
        
        driver = webdriver.Remote(server_url, options=options)
        driver.implicitly_wait(10)
        
        yield driver
        
        driver.quit()
    
    def test_login_successful(self, driver):
        """Test: Login exitoso"""
        logger.info("TEST: Login exitoso")

        login_page = LoginPage(driver)
        test_data = VitaWalletConfig.get_test_data()

        login_page.login(test_data["email"], test_data["password"])
        success = login_page.wait_for_home_screen(timeout=20)

        assert success, "Login falló"
        logger.info("LOGIN EXITOSO")

    def test_login_invalid_credentials(self, driver):
        """Test negativo: Credenciales inválidas"""
        logger.info("TEST: Login con credenciales inválidas")

        login_page = LoginPage(driver)

        login_page.login("invalid@email.com", "wrongpassword")

        # No debería llegar al home
        success = login_page.is_login_successful()
        assert not success, "Login no debería ser exitoso con credenciales inválidas"

        logger.info("Error de login manejado correctamente")