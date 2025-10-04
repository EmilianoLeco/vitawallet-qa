from appium.webdriver.common.appiumby import AppiumBy
from pages.base_page import BasePage

class LoginPage(BasePage):
    """Page Object para la pantalla de Login - VITA WALLET"""
    
    # ==================== PANTALLA DE BIENVENIDA/ONBOARDING ====================
    WELCOME_LOGIN_BUTTON = (AppiumBy.ACCESSIBILITY_ID, "Iniciar sesión")
    WELCOME_LOGIN_BUTTON_XPATH = (AppiumBy.XPATH, '//android.view.ViewGroup[@content-desc="Iniciar sesión"]')
    WELCOME_LOGIN_BUTTON_UIAUTOMATOR = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().description("Iniciar sesión")')
    
    REGISTER_BUTTON = (AppiumBy.ACCESSIBILITY_ID, "Registrarme gratis")
    REGISTER_BUTTON_XPATH = (AppiumBy.XPATH, '//android.view.ViewGroup[@content-desc="Registrarme gratis"]')
    
    # ==================== PANTALLA DE FORMULARIO LOGIN ====================
    EMAIL_INPUT = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().className("android.widget.EditText").instance(0)')
    PASSWORD_INPUT = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().className("android.widget.EditText").instance(1)')
    
    EMAIL_LABEL = (AppiumBy.XPATH, '//android.widget.TextView[@text="Correo electrónico"]')
    PASSWORD_LABEL = (AppiumBy.XPATH, '//android.widget.TextView[@text="Contraseña"]')
    LOGIN_TITLE = (AppiumBy.XPATH, '//android.widget.TextView[@text="Iniciar sesión"]')
        
    SUBMIT_BUTTON = (AppiumBy.ACCESSIBILITY_ID, "Ingresar")
    SUBMIT_BUTTON_XPATH = (AppiumBy.XPATH, '//android.view.ViewGroup[@content-desc="Ingresar"]')
        
    FORGOT_PASSWORD_LINK = (AppiumBy.XPATH, '//*[@text="He olvidado mi contraseña"]')
    
    # ==================== POPUP POST-LOGIN ====================
    # Popup "Recibir y Recargar ahora son Depositar"
    POPUP_ENTENDIDO_BUTTON = (AppiumBy.ACCESSIBILITY_ID, "Entendido")
    POPUP_ENTENDIDO_XPATH = (AppiumBy.XPATH, '//android.view.ViewGroup[@content-desc="Entendido"]')
    POPUP_ENTENDIDO_UIAUTOMATOR = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().description("Entendido")')
    POPUP_ENTENDIDO_TEXT = (AppiumBy.XPATH, '//android.widget.TextView[@text="Entendido"]')
    
    # ==================== VALIDACIONES ====================
    HOME_INDICATOR = (AppiumBy.XPATH, "//*[contains(@text, 'Inicio') or contains(@text, 'Home') or contains(@content-desc, 'Inicio')]")
    ERROR_MESSAGE = (AppiumBy.XPATH, "//*[contains(@text, 'Error') or contains(@text, 'incorrecto') or contains(@text, 'inválido')]")
        
    # ==================== COACH MARKS / BANNERS EN HOME ====================
    X1_VIEWGROUP_INSTANCE = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().className("android.view.ViewGroup").instance(52)')
    X1_XPATH = (AppiumBy.XPATH, '//android.widget.FrameLayout[@resource-id="android:id/content"]/android.widget.FrameLayout/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup[2]/android.widget.FrameLayout/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup[1]/android.view.ViewGroup/android.widget.FrameLayout/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup[6]/android.view.ViewGroup[2]')

    X2_DESC_INSTANCE = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().description("cerrar").instance(1)')
    X2_XPATH = (AppiumBy.XPATH, '(//android.view.ViewGroup[@content-desc="cerrar"])[2]')

    X3_A11Y = (AppiumBy.ACCESSIBILITY_ID, "cerrar")
    X3_UIA  = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().description("cerrar")')
    X3_XPATH = (AppiumBy.XPATH, '//android.view.ViewGroup[@content-desc="cerrar"]')

    X4_A11Y = (AppiumBy.ACCESSIBILITY_ID, "g")
    X4_UIA  = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().description("g")')
    X4_XPATH = (AppiumBy.XPATH, '//android.view.ViewGroup[@content-desc="g"]')
    
    
    def __init__(self, driver):
        super().__init__(driver)
    
    def dismiss_home_banners(self):
        """
       Cierra las 4 vistas tipo banner/coach mark en Home tocando la 'X' de cada una.
       Usa exactamente los localizadores provistos, en orden.
        """
        self.logger.info("Cerrando banners en Home (4 pasos)")
        sequences = [
            [self.X1_VIEWGROUP_INSTANCE, self.X1_XPATH],
            [self.X2_DESC_INSTANCE, self.X2_XPATH],
            [self.X3_A11Y, self.X3_UIA, self.X3_XPATH],
            [self.X4_A11Y, self.X4_UIA, self.X4_XPATH],
        ]

        closed = 0
        for i, locs in enumerate(sequences, start=1):
            clicked = False
            for loc in locs:
                try:
                    if self.is_element_visible(loc, timeout=2):
                        self.find_element(loc).click()
                        self.wait_for_seconds(0.3)
                        self.logger.info(f"Banner {i} cerrado ({loc})")
                        closed += 1
                        clicked = True
                        break
                except Exception:
                    continue
            if not clicked:
                self.logger.info(f"Banner {i} no estaba presente (o ya estaba cerrado)")
        if closed:
            self.take_screenshot("home_banners_closed")
        return closed == len(sequences)

    def dismiss_popup_if_present(self):
        """Cerrar popup 'Entendido' si aparece después del login"""
        try:
            self.logger.info("Verificando si hay popup post-login...")
            
            # Esperar a que el popup aparezca
            self.wait_for_seconds(5)
            self.take_screenshot("popup_check")
            
            # Estrategia 1: Accessibility ID (ViewGroup con content-desc)
            try:
                if self.is_element_visible(self.POPUP_ENTENDIDO_BUTTON, timeout=3):
                    self.logger.info("Popup detectado - Método 1 (accessibility id)")
                    element = self.find_element(self.POPUP_ENTENDIDO_BUTTON)
                    element.click()
                    self.wait_for_seconds(2)
                    self.take_screenshot("popup_dismissed_success")
                    self.logger.info("Popup cerrado exitosamente")
                    return True
            except Exception as e:
                self.logger.info(f"Método 1 falló: {str(e)[:100]}")
            
            # Estrategia 2: XPath con ViewGroup
            try:
                if self.is_element_visible(self.POPUP_ENTENDIDO_XPATH, timeout=2):
                    self.logger.info("Popup detectado - Método 2 (xpath viewgroup)")
                    element = self.find_element(self.POPUP_ENTENDIDO_XPATH)
                    element.click()
                    self.wait_for_seconds(2)
                    self.take_screenshot("popup_dismissed_success")
                    self.logger.info("Popup cerrado exitosamente")
                    return True
            except Exception as e:
                self.logger.info(f"Método 2 falló: {str(e)[:100]}")
            
            # Estrategia 3: XPath con TextView hijo
            try:
                if self.is_element_visible(self.POPUP_ENTENDIDO_TEXT, timeout=2):
                    self.logger.info("Popup detectado - Método 3 (xpath textview)")
                    element = self.find_element(self.POPUP_ENTENDIDO_TEXT)
                    element.click()
                    self.wait_for_seconds(2)
                    self.take_screenshot("popup_dismissed_success")
                    self.logger.info("Popup cerrado exitosamente")
                    return True
            except Exception as e:
                self.logger.info(f"Método 3 falló: {str(e)[:100]}")
            
            # Estrategia 4: UiAutomator con description
            try:
                if self.is_element_visible(self.POPUP_ENTENDIDO_UIAUTOMATOR, timeout=2):
                    self.logger.info("Popup detectado - Método 4 (uiautomator)")
                    element = self.find_element(self.POPUP_ENTENDIDO_UIAUTOMATOR)
                    element.click()
                    self.wait_for_seconds(2)
                    self.take_screenshot("popup_dismissed_success")
                    self.logger.info("Popup cerrado exitosamente")
                    return True
            except Exception as e:
                self.logger.info(f"Método 4 falló: {str(e)[:100]}")
            
            # Estrategia 5: Tap por coordenadas (último recurso)
            try:
                self.logger.info("Intentando cerrar popup por coordenadas...")
                screen_size = self.driver.get_window_size()
                x = screen_size['width'] // 2
                y = int(screen_size['height'] * 0.68)

                self.driver.tap([(x, y)])
                self.wait_for_seconds(2)
                self.take_screenshot("popup_dismissed_coordinates")
                self.logger.info("Popup cerrado por coordenadas")
                return True
            except Exception as e:
                self.logger.info(f"Método 5 falló: {str(e)[:100]}")

            self.logger.warning("No se detectó popup o ya estaba cerrado")
            return False

        except Exception as e:
            self.logger.error(f"Error crítico al cerrar popup: {e}")
            self.take_screenshot("error_popup_critical")
            return False

    def click_welcome_login_button(self):
        """PASO 1: Click en 'Iniciar sesión' desde pantalla de bienvenida"""
        try:
            self.logger.info("PASO 1: Navegando desde pantalla de bienvenida")
            self.wait_for_seconds(3)
            self.take_screenshot("00_welcome_screen")

            self.click_element(self.WELCOME_LOGIN_BUTTON, timeout=10)
            self.wait_for_seconds(2)

            self.logger.info("Navegación al formulario de login exitosa")
            self.take_screenshot("00b_login_form_loaded")
            return True

        except Exception as e:
            self.logger.error(f"Error navegando desde bienvenida: {e}")
            self.take_screenshot("error_welcome_navigation")

            try:
                self.logger.info("Intentando con xpath...")
                self.click_element(self.WELCOME_LOGIN_BUTTON_XPATH, timeout=5)
                self.wait_for_seconds(2)
                return True
            except:
                try:
                    self.logger.info("⚠️ Intentando con UiAutomator...")
                    self.click_element(self.WELCOME_LOGIN_BUTTON_UIAUTOMATOR, timeout=5)
                    self.wait_for_seconds(2)
                    return True
                except:
                    raise Exception(f"No se pudo navegar al formulario de login: {e}")
    
    def enter_email(self, email):
        """PASO 2: Ingresar email en el formulario"""
        try:
            self.logger.info(f"PASO 2: Ingresando email: {email}")
            self.wait_for_seconds(1)

            self.click_element(self.EMAIL_INPUT, timeout=10)
            self.wait_for_seconds(1)

            self.send_keys(self.EMAIL_INPUT, email, clear_first=True)
            self.hide_keyboard()

            self.logger.info("Email ingresado correctamente")
            return True

        except Exception as e:
            self.logger.error(f"Error ingresando email: {e}")
            self.take_screenshot("error_enter_email")
            raise
    
    def enter_password(self, password):
        """PASO 3: Ingresar contraseña en el formulario"""
        try:
            self.logger.info("PASO 3: Ingresando contraseña")
            self.wait_for_seconds(1)

            self.click_element(self.PASSWORD_INPUT, timeout=10)
            self.wait_for_seconds(1)

            self.send_keys(self.PASSWORD_INPUT, password, clear_first=True)
            self.hide_keyboard()

            self.logger.info("Contraseña ingresada correctamente")
            return True

        except Exception as e:
            self.logger.error(f"Error ingresando contraseña: {e}")
            self.take_screenshot("error_enter_password")
            raise
    
    def click_submit_button(self):
        """PASO 4: Click en botón 'Ingresar' para hacer submit del formulario"""
        try:
            self.logger.info("PASO 4: Click en botón 'Ingresar'")

            self.click_element(self.SUBMIT_BUTTON, timeout=10)
            self.wait_for_seconds(3)

            self.logger.info("Submit exitoso")
            return True

        except Exception as e:
            self.logger.error(f"Error haciendo submit: {e}")
            self.take_screenshot("error_submit_button")

            try:
                self.logger.info("Intentando con xpath...")
                self.click_element(self.SUBMIT_BUTTON_XPATH, timeout=5)
                self.wait_for_seconds(3)
                return True
            except:
                raise Exception(f"No se pudo hacer click en botón Ingresar: {e}")
    
    def login(self, email, password):
        """Flujo completo de login desde pantalla de bienvenida hasta home"""
        self.logger.info("=" * 70)
        self.logger.info("INICIANDO LOGIN COMPLETO")
        self.logger.info(f"Usuario: {email}")
        self.logger.info("=" * 70)
        
        try:
            # PASO 1: Navegar desde bienvenida al formulario
            self.click_welcome_login_button()
            
            # PASO 2: Ingresar email
            self.wait_for_seconds(1)
            self.take_screenshot("01_before_email")
            self.enter_email(email)
            self.take_screenshot("02_email_entered")
            
            # PASO 3: Ingresar contraseña
            self.enter_password(password)
            self.take_screenshot("03_password_entered")
            
            # PASO 4: Click en Ingresar
            self.click_submit_button()
            self.take_screenshot("04_after_submit")
            
            # PASO 5: Esperar que cargue el home
            self.wait_for_seconds(5)
            self.take_screenshot("05_login_completed")
            
            self.logger.info("=" * 70)
            self.logger.info("PROCESO DE LOGIN COMPLETADO")
            self.logger.info("=" * 70)
            return True

        except Exception as e:
            self.logger.error("=" * 70)
            self.logger.error(f"ERROR DURANTE EL LOGIN: {e}")
            self.logger.error("=" * 70)
            self.take_screenshot("error_login_process")
            raise
    
    def is_login_successful(self):
        """Verificar si el login fue exitoso"""
        try:
            self.logger.info("Verificando si login fue exitoso...")
            self.wait_for_seconds(3)

            is_home = self.is_element_visible(self.HOME_INDICATOR, timeout=10)

            if is_home:
                self.logger.info("Login exitoso - Home screen visible")
                self.take_screenshot("login_success_confirmed")
                return True
            else:
                self.logger.error("Login falló - Home screen no visible")
                self.take_screenshot("login_failed_no_home")
                return False

        except Exception as e:
            self.logger.error(f"Error verificando login: {e}")
            self.take_screenshot("error_verify_login")
            return False
    
    def is_error_displayed(self):
        """Verificar si hay mensaje de error en pantalla"""
        try:
            return self.is_element_visible(self.ERROR_MESSAGE, timeout=5)
        except:
            return False
    
    def wait_for_home_screen(self, timeout=15):
        """Esperar a que aparezca la pantalla principal (home)"""
        try:

            # IMPORTANTE: Cerrar popup si aparece
            self.dismiss_popup_if_present()

            self.logger.info("Esperando que cargue el home screen...")

            self.wait_for_seconds(3)

            self.find_element(self.HOME_INDICATOR, timeout=timeout)

            # Cerrar los 4 banners con 'X'
            self.dismiss_home_banners()

            self.logger.info("Home screen cargado exitosamente")
            self.take_screenshot("home_screen_loaded")


            return True

        except Exception as e:
            self.logger.error(f"Timeout esperando home screen: {e}")
            self.take_screenshot("error_home_timeout")
            return False