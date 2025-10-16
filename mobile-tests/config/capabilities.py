import os
from pathlib import Path
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

class AppiumCapabilities:

    # Paths
    BASE_DIR = Path(__file__).parent.parent.parent
    APP_PATH = BASE_DIR / os.getenv("APK_PATH", "mobile-tests/app/VitaQA.apk")
    
    @classmethod
    def get_android_capabilities(cls):

        capabilities = {
            # Configuración básica de Appium
            "platformName": "Android",
            "automationName": "UiAutomator2",
            
            # Dispositivo desde .env
            "platformVersion": os.getenv("ANDROID_PLATFORM_VERSION", "15"),
            "deviceName": os.getenv("ANDROID_DEVICE_NAME", "Android"),
            "udid": os.getenv("ANDROID_UDID"),
            
            # APP CONFIGURATION - VITA WALLET
            "app": str(cls.APP_PATH),

            # Package y Activity desde .env
            "appPackage": os.getenv("APP_PACKAGE", "com.vita_wallet"),
            "appActivity": os.getenv("APP_ACTIVITY", "com.vita_wallet.MainActivity"),
            
            # REINSTALAR EN CADA EJECUCIÓN
            "noReset": False,
            "fullReset": True,
            "autoGrantPermissions": True,

            # Timeouts desde .env
            "newCommandTimeout": int(os.getenv("NEW_COMMAND_TIMEOUT", "300")),
            "androidInstallTimeout": int(os.getenv("ANDROID_INSTALL_TIMEOUT", "300000")),
            
            # Configuraciones adicionales
            "unicodeKeyboard": True,
            "resetKeyboard": True,
            "autoWebview": False,
            
            # Performance
            "skipDeviceInitialization": False,
            "ignoreHiddenApiPolicyError": True,

            # Forzar reinstalación de helper apps de Appium
            # Esto reinstala io.appium.settings y io.appium.uiautomator2.server
            "skipServerInstallation": False,
            "skipUnlock": True,
            "allowInvisibleElements": True,
        }
        
        return capabilities
    
    @staticmethod
    def get_appium_server_url():
        return os.getenv("APPIUM_SERVER_URL", "http://127.0.0.1:4723")
    
    @classmethod
    def validate_app_exists(cls):
        if not cls.APP_PATH.exists():
            raise FileNotFoundError(
                f"❌ APK no encontrado en: {cls.APP_PATH}\n"
                f"Por favor, coloca el archivo VitaQA.apk en la carpeta 'mobile-tests/app/'"
            )
        return True


class VitaWalletConfig:

    # Credenciales desde .env
    QA_USER_EMAIL = os.getenv("QA_USER_EMAIL")
    QA_USER_PASSWORD = os.getenv("QA_USER_PASSWORD")
    QA_BASE_URL = os.getenv("QA_BASE_URL", "https://qa.vitawallet.io/")

    # Datos de prueba desde .env
    DEFAULT_EXCHANGE_AMOUNT = int(os.getenv("DEFAULT_EXCHANGE_AMOUNT", "1000"))
    FROM_CURRENCY = os.getenv("FROM_CURRENCY", "ARS")
    TO_CURRENCY = os.getenv("TO_CURRENCY", "USDT")

    # Timeouts desde .env
    LOGIN_TIMEOUT = int(os.getenv("LOGIN_TIMEOUT", "20"))
    EXCHANGE_TIMEOUT = int(os.getenv("EXCHANGE_TIMEOUT", "30"))
    TRANSACTION_TIMEOUT = int(os.getenv("TRANSACTION_TIMEOUT", "60"))
    
    @staticmethod
    def get_test_data():
        return {
            "email": VitaWalletConfig.QA_USER_EMAIL,
            "password": VitaWalletConfig.QA_USER_PASSWORD,
            "amount": VitaWalletConfig.DEFAULT_EXCHANGE_AMOUNT,
            "from_currency": VitaWalletConfig.FROM_CURRENCY,
            "to_currency": VitaWalletConfig.TO_CURRENCY
        }