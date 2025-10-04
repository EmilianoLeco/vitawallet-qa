# mobile-tests/tests/test_crypto_exchange.py
import pytest
import logging
from appium import webdriver
from appium.options.android import UiAutomator2Options
import sys
import os
import time

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from pages.login_page import LoginPage
from pages.crypto_page import CryptoPage
from config.capabilities import AppiumCapabilities, VitaWalletConfig

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('reports/mobile_tests.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)


class TestCryptoExchange:
    """Suite de tests para intercambio cripto - VITA WALLET"""
    
    @pytest.fixture(scope="function")
    def driver(self):
        """Fixture para inicializar driver de Appium"""
        logger.info("=" * 70)
        logger.info("Iniciando Appium Driver")
        logger.info("=" * 70)
        
        AppiumCapabilities.validate_app_exists()
        
        capabilities = AppiumCapabilities.get_android_capabilities()
        server_url = AppiumCapabilities.get_appium_server_url()
        
        options = UiAutomator2Options()
        options.load_capabilities(capabilities)
        
        logger.info(f"Dispositivo: {capabilities['deviceName']}")
        logger.info(f"Android: {capabilities['platformVersion']}")
        logger.info("Instalando app (30-60 segundos)...")
        
        driver = webdriver.Remote(server_url, options=options)
        driver.implicitly_wait(10)
        
        logger.info("App instalada y abierta")

        yield driver

        logger.info("Cerrando driver...")
        driver.quit()
        logger.info("=" * 70)
    
    @pytest.fixture(scope="function")
    def login_page(self, driver):
        """Fixture para LoginPage"""
        return LoginPage(driver)
    
    @pytest.fixture(scope="function")
    def crypto_page(self, driver):
        """Fixture para CryptoPage"""
        return CryptoPage(driver)
    
    @pytest.fixture(scope="function")
    def test_data(self):
        """Fixture para datos de prueba"""
        return VitaWalletConfig.get_test_data()
    
    def test_complete_crypto_exchange_flow(self, login_page, crypto_page, test_data):
        """
        TEST PRINCIPAL: Flujo completo de intercambio ARS → USDT
        
        Este es el test que cumple con los requisitos de la prueba técnica:
        1. Login en la aplicación
        2. Navegar a sección Cripto
        3. Seleccionar intercambio
        4. Configurar ARS → USDT
        5. Ingresar monto (1000 ARS)
        6. Confirmar transacción
        7. Validar éxito
        """
        logger.info("=" * 70)
        logger.info("TEST: Flujo completo ARS -> USDT")
        logger.info("=" * 70)
        
        # PASO 1: Login
        logger.info("\nPASO 1: LOGIN")
        login_page.login(test_data["email"], test_data["password"])

        # Validar login exitoso
        assert login_page.wait_for_home_screen(timeout=20), "Login falló"
        logger.info("PASO 1 COMPLETADO: Login exitoso\n")

        # PASO 2-7: Realizar intercambio completo
        logger.info("PASO 2-7: INTERCAMBIO CRIPTO")
        exchange_success = crypto_page.perform_exchange(
            from_currency=test_data["from_currency"],
            to_currency=test_data["to_currency"],
            amount=test_data["amount"]
        )
        
        # Validación final
        assert exchange_success, "El intercambio no fue exitoso"
        time.sleep(3)
        # validar Historial y abrir el último intercambio
        assert crypto_page.wait_for_history_title()
        assert crypto_page.open_first_history_item()

        logger.info("\n" + "=" * 70)
        logger.info("TEST COMPLETADO EXITOSAMENTE")
        logger.info("Intercambio ARS -> USDT realizado")
        logger.info("=" * 70)
        time.sleep(3)
    
    def test_negative_min_amount_validation(self, login_page, crypto_page, test_data):
        """
        Test negativo: Validar error con monto menor a 1000 ARS
        """
        logger.info("=" * 70)
        logger.info("TEST NEGATIVO: Monto menor al mínimo")
        logger.info("=" * 70)

        # Login
        logger.info("\nPASO 1: LOGIN")
        login_page.login(test_data["email"], test_data["password"])
        assert login_page.wait_for_home_screen(timeout=20), "Login falló"
        logger.info("Login exitoso\n")

        # Test negativo - monto menor a 1000 ARS
        logger.info("PASO 2: VALIDAR MONTO MÍNIMO")
        has_error = crypto_page.test_min_amount_validation(amount=500)

        assert has_error, "Debería mostrar error para monto < 1000 ARS"

        logger.info("\n" + "=" * 70)
        logger.info("TEST NEGATIVO COMPLETADO")
        logger.info("Error de monto mínimo validado correctamente")
        logger.info("=" * 70)
        
    @pytest.mark.smoke
    def test_smoke_navigation_to_crypto(self, login_page, crypto_page, test_data):
        """
        Smoke test: Solo verificar navegación hasta sección cripto
        """
        logger.info("SMOKE TEST: Navegación a Cripto")

        # Login
        login_page.login(test_data["email"], test_data["password"])
        assert login_page.is_login_successful()

        # Navegar a cripto
        success = crypto_page.navigate_to_crypto_section()
        assert success, "No se pudo navegar a Cripto"

        # Verificar que estamos en la pantalla correcta
        assert crypto_page.verify_intercambiar_screen(), "Pantalla Intercambiar no cargó"

        logger.info("SMOKE TEST PASSED")


# Para ejecutar desde línea de comandos:
# pytest mobile-tests/tests/test_crypto_exchange.py -v -s
# pytest mobile-tests/tests/test_crypto_exchange.py::TestCryptoExchange::test_complete_crypto_exchange_flow -v -s
# pytest mobile-tests/tests/test_crypto_exchange.py -m smoke -v -s