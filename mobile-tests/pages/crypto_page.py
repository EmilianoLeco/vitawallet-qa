from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.base_page import BasePage


class CryptoPage(BasePage):
    """Page Object para la pantalla de Intercambio Cripto - VITA WALLET"""

    # ==================== HOME / NAV ====================
    CRYPTO_TAB = (AppiumBy.ACCESSIBILITY_ID, "Cripto")
    CRYPTO_TAB_XPATH = (AppiumBy.XPATH, '//android.view.ViewGroup[@content-desc="Cripto"]')
    CRYPTO_TAB_UIAUTOMATOR = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().description("Cripto")')

    # ==================== INTERCAMBIAR ====================
    INTERCAMBIAR_TITLE = (AppiumBy.XPATH, '//android.widget.TextView[@text="Intercambiar"]')
    INTERCAMBIAR_TITLE_UIAUTOMATOR = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Intercambiar")')

    # (Botones/íconos para abrir pickers; mantenemos tus locators y agregamos alternativas)
    FROM_CURRENCY_DROPDOWN = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().className("android.widget.ImageView").instance(6)')
    FROM_CURRENCY_DROPDOWN_XPATH = (AppiumBy.XPATH, '//android.widget.ScrollView/android.view.ViewGroup/android.view.ViewGroup[6]/android.widget.ImageView[2]')

    TO_CURRENCY_DROPDOWN = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().className("android.widget.ImageView").instance(10)')
    TO_CURRENCY_DROPDOWN_XPATH = (AppiumBy.XPATH, '//android.widget.ScrollView/android.view.ViewGroup/android.view.ViewGroup[10]/android.widget.ImageView[2]')

    # Contenedores comunes del modal/lista
    LIST_CONTAINER = (AppiumBy.XPATH, "//*[contains(@class,'RecyclerView') or contains(@class,'ListView')]")
    MODAL_HEADER  = (AppiumBy.XPATH, "//*[contains(@text,'Seleccionar') or contains(@text,'Elige') or contains(@content-desc,'Seleccionar')]")

    # ==================== INPUT MONTO ====================
    AMOUNT_INPUT = (AppiumBy.XPATH, '//android.widget.EditText[@text="0"]')
    AMOUNT_INPUT_UIAUTOMATOR = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("0")')
    AMOUNT_INPUT_EDITTEXT = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().className("android.widget.EditText").instance(0)')

    ERROR_MIN_AMOUNT = (AppiumBy.XPATH, '//android.widget.TextView[@text="Monto mínimo: 1.000 ARS"]')
    ERROR_MIN_AMOUNT_UIAUTOMATOR = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Monto mínimo: 1.000 ARS")')

    # ==================== CONTINUAR ====================
    CONTINUE_BUTTON = (AppiumBy.ACCESSIBILITY_ID, "Continuar")
    CONTINUE_BUTTON_XPATH = (AppiumBy.XPATH, '//android.view.ViewGroup[@content-desc="Continuar"]')
    CONTINUE_BUTTON_TEXT = (AppiumBy.XPATH, '//*[@text="Continuar" or .="Continuar"]')

    # ==================== VALIDACIONES ====================
    SUCCESS_MESSAGE = (AppiumBy.XPATH, "//*[contains(@text, 'exitoso') or contains(@text, 'éxito') or contains(@text, 'Éxito')]")

    # ==================== CONFIRMACIÓN ====================
    SUMMARY_TITLE = (AppiumBy.XPATH, '//*[@text="Resumen de la transacción" or contains(@text,"Resumen")]')

    # content-desc dinámico: "Confirmar , 00:50" (varía por el contador)
    CONFIRM_BUTTON_DESC_CONTAINS = (AppiumBy.XPATH, '//*[@content-desc and contains(@content-desc,"Confirmar")]')

    # TextView hijo con posible espacio al final: "Confirmar "
    CONFIRM_BUTTON_TEXT_EXACT = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Confirmar ")')

    # Fallback sin espacio por si cambia: "Confirmar"
    CONFIRM_BUTTON_TEXT_TRIM = (AppiumBy.XPATH, '//*[@text="Confirmar" or .="Confirmar"]')

    # ==================== ÉXITO & VOLVER AL INICIO ====================
    SUCCESS_TITLE_EXACT = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("¡Intercambio exitoso!")')
    SUCCESS_TITLE_XPATH = (AppiumBy.XPATH, '//android.widget.TextView[@text="¡Intercambio exitoso!"]')

    GO_HOME_A11Y = (AppiumBy.ACCESSIBILITY_ID, "Ir al inicio")
    GO_HOME_XPATH = (AppiumBy.XPATH, '//*[@content-desc="Ir al inicio"]')

    # ==================== HOME / HISTORIAL ====================
    HISTORY_TITLE = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Historial")')
    # primer item de la lista dentro del ScrollView cuyo content-desc empieza con "Intercambio"
    FIRST_HISTORY_ITEM = (
       AppiumBy.XPATH,
        '(//android.widget.ScrollView//android.view.ViewGroup[contains(@content-desc,"Intercambio")])[1]'
    )


    # Reuso un indicador simple de Home (idéntico criterio que en LoginPage)
    HOME_INDICATOR_SIMPLE = (AppiumBy.XPATH, "//*[contains(@text,'Inicio') or contains(@content-desc,'Inicio')]")

    # ==================== COACH MARKS / BANNERS EN HOME ====================
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
        self._wait = WebDriverWait(self.driver, 12)

    def dismiss_home_banners(self):
        """
       Cierra las 4 vistas tipo banner/coach mark en Home tocando la 'X' de cada una.
       Usa exactamente los localizadores provistos, en orden.
        """
        self.logger.info(" Cerrando banners en Home (4 pasos)")
        sequences = [
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
                        self.logger.info(f" Banner {i} cerrado ({loc})")
                        closed += 1
                        clicked = True
                        break
                except Exception:
                    continue
            if not clicked:
                self.logger.info(f" Banner {i} no estaba presente (o ya estaba cerrado)")
        if closed:
            self.take_screenshot("home_banners_closed")
        return closed == len(sequences)

    # ----------------- helpers internos -----------------
    def _click_any(self, locators, timeout=6, after_wait=0.2):
        last_exc = None
        for loc in locators:
            try:
                el = WebDriverWait(self.driver, timeout).until(EC.element_to_be_clickable(loc))
                el.click()
                if after_wait:
                    self.wait_for_seconds(after_wait)
                return True
            except Exception as e:
                last_exc = e
        if last_exc:
            self.logger.debug(f"_click_any falló: {str(last_exc)[:200]}")
        return False

    def _open_picker_and_wait(self, which="from", timeout=8):
        """Abre el picker 'Desde' o 'Para' y espera que la lista inline esté visible."""
        self.logger.info(f" Abriendo picker: {which}")
        btns = (
            [self.FROM_CURRENCY_DROPDOWN, self.FROM_CURRENCY_DROPDOWN_XPATH]
            if which == "from"
            else [self.TO_CURRENCY_DROPDOWN, self.TO_CURRENCY_DROPDOWN_XPATH]
        )
        if not self._click_any(btns, timeout=timeout, after_wait=0.2):
            self.take_screenshot(f"{which}_picker_open_error")
            raise Exception(f"No se pudo abrir picker {which}")

        # 👇 la lista es un ScrollView con items ViewGroup (no hay modal)
        try:
           WebDriverWait(self.driver, timeout).until(
               EC.any_of(
                   EC.presence_of_element_located((AppiumBy.CLASS_NAME, "android.widget.ScrollView")),
                   EC.presence_of_element_located((AppiumBy.XPATH, '//*[@content-desc and contains(@content-desc,", - ")]')),
                   EC.presence_of_element_located((AppiumBy.XPATH, '//*[contains(@text,"ARS") or contains(@text,"USDT")]')),
                )
            )
        except Exception:
            # Último intento: un pequeño scroll para forzar layout
            self._scroll_text_into_view_android("ARS")
        self.take_screenshot(f"{which}_picker_open")
        return True

    def _scroll_text_into_view_android(self, text, instance=0):
        """Trae a vista un item por texto exacto o parcial con UiScrollable."""
        try:
            ui = (
                f'new UiScrollable(new UiSelector().scrollable(true).instance({instance}))'
                f'.scrollTextIntoView("{text}")'
            )
            self.driver.find_element(AppiumBy.ANDROID_UIAUTOMATOR, ui)
            return True
        except Exception:
            try:
                ui = (
                    f'new UiScrollable(new UiSelector().scrollable(true).instance({instance}))'
                    f'.scrollIntoView(new UiSelector().textContains("{text}"))'
                )
                self.driver.find_element(AppiumBy.ANDROID_UIAUTOMATOR, ui)
                return True
            except Exception as e:
                self.logger.debug(f"UiScrollable no encontró '{text}': {e}")
                return False

    def _select_currency_by_code(self, code: str, timeout=10):
        """
       Selecciona una moneda en el picker por su código (p.ej. 'ARS' / 'USDT')
        intentando múltiples estrategias para evitar dependencias frágiles.
        """
        self.logger.info(f" Buscando moneda: {code}")

        # 1) Intentar traerla a vista
        self._scroll_text_into_view_android(code)

        # 2) Intentar click con varias alternativas
        locs = [
            # Texto exacto del código
            (AppiumBy.XPATH, f'//android.widget.TextView[@text="{code}"]'),
            (AppiumBy.XPATH, f'//*[@text="{code}"]'),
            # Texto que contiene el código (ej.: "ARS - Peso Argentino")
            (AppiumBy.XPATH, f'//*[contains(@text,"{code}")]'),
            # content-desc exacto o que contenga
            (AppiumBy.ACCESSIBILITY_ID, code),
            (AppiumBy.XPATH, f'//*[@content-desc and contains(@content-desc,"{code}")]'),
            # Contenedor clickeable que tenga un hijo con el código
            (AppiumBy.XPATH, f'//android.view.ViewGroup[.//*[@text="{code}" or contains(@text,"{code}")]]'),
        ]
        if self._click_any(locs, timeout=timeout, after_wait=0.2):
            self.take_screenshot(f"currency_{code}_selected")
            return True

        self.logger.error(f" No se pudo seleccionar la moneda {code}")
        try:
            self.logger.debug(self.driver.page_source[:2000])
        except Exception:
            pass
        return False

    # ----------------- navegación / verificaciones -----------------
    def navigate_to_crypto_section(self):
        """Navegar a la sección de Cripto desde Home"""
        try:
            self.logger.info("Navegando a sección Cripto")
            self.wait_for_seconds(1.5)
            self.take_screenshot("06_home_screen")

            if self._click_any([self.CRYPTO_TAB, self.CRYPTO_TAB_XPATH], timeout=10, after_wait=0.4):
                self.take_screenshot("07_crypto_screen")
                self.logger.info(" Navegación a Cripto exitosa")
                return True

            # Fallback UiAutomator
            self.click_element(self.CRYPTO_TAB_UIAUTOMATOR, timeout=6)
            self.take_screenshot("07_crypto_screen_uia")
            self.logger.info(" Navegación a Cripto (uiautomator)")
            return True

        except Exception as e:
            self.logger.error(f" Error navegando a Cripto: {e}")
            self.take_screenshot("error_crypto_navigation")
            raise

    def verify_intercambiar_screen(self):
        """Verificar que estamos en la pantalla de Intercambiar"""
        try:
            self.logger.info(" Verificando pantalla Intercambiar...")
            if self.is_element_visible(self.INTERCAMBIAR_TITLE, timeout=5) or \
               self.is_element_visible(self.INTERCAMBIAR_TITLE_UIAUTOMATOR, timeout=3):
                self.logger.info(" Pantalla Intercambiar confirmada")
                return True
            self.logger.warning(" No se encontró título 'Intercambiar'")
            return False
        except Exception as e:
            self.logger.error(f" Error verificando pantalla: {e}")
            return False

    # ----------------- selección de monedas -----------------
    def select_from_currency_ars(self):
        """Seleccionar ARS como moneda origen"""
        self.logger.info(" Seleccionando moneda origen: ARS")
        self._open_picker_and_wait("from")
        assert self._select_currency_by_code("ARS", timeout=10), "No se pudo elegir ARS (Desde)"
        return True

    def select_to_currency_usdt(self):
        """Seleccionar USDT como moneda destino"""
        self.logger.info(" Seleccionando moneda destino: USDT")
        self._open_picker_and_wait("to")
        assert self._select_currency_by_code("USDT", timeout=10), "No se pudo elegir USDT (Para)"
        return True

    # ----------------- monto / continuar / éxito -----------------
    def enter_amount(self, amount):
        """Ingresar monto (tap previo + clear + send_keys + esconder teclado)"""
        try:
            self.logger.info(f" Ingresando monto: {amount} ARS")
            # tap/input (probamos 3 variantes)
            for loc in [self.AMOUNT_INPUT, self.AMOUNT_INPUT_EDITTEXT, self.AMOUNT_INPUT_UIAUTOMATOR]:
                try:
                    self.click_element(loc, timeout=8)
                    break
                except Exception:
                    continue

            element = None
            for loc in [self.AMOUNT_INPUT, self.AMOUNT_INPUT_EDITTEXT, self.AMOUNT_INPUT_UIAUTOMATOR]:
                try:
                    element = self.find_element(loc, timeout=3)
                    if element:
                        break
                except Exception:
                    continue

            if not element:
                self.take_screenshot("error_amount_input_not_found")
                raise Exception("No se encontró el input de monto")

            # limpiar + escribir
            try:
                element.clear()
            except Exception:
                # fallback: seleccionar todo y borrar
                element.click()
            element.send_keys(str(amount))
            self.hide_keyboard()
            self.wait_for_seconds(1.5)  # dejar que calcule cotización
            self.take_screenshot("12_amount_entered")
            self.logger.info(" Monto ingresado")
            return True
        except Exception as e:
            self.logger.error(f" Error ingresando monto: {e}")
            self.take_screenshot("error_enter_amount")
            raise

    def is_min_amount_error_displayed(self):
        """Verificar si aparece el error de monto mínimo"""
        try:
            self.logger.info(" Verificando error de monto mínimo...")
            if self.is_element_visible(self.ERROR_MIN_AMOUNT, timeout=3) or \
               self.is_element_visible(self.ERROR_MIN_AMOUNT_UIAUTOMATOR, timeout=2):
                self.logger.info(" Error de monto mínimo detectado")
                self.take_screenshot("error_min_amount_displayed")
                return True
            self.logger.info(" No hay error de monto mínimo")
            return False
        except Exception:
            return False

    def click_continue_button(self):
        """Click en botón 'Continuar'"""
        try:
            self.logger.info(" Click en 'Continuar'")
            if self._click_any([self.CONTINUE_BUTTON, self.CONTINUE_BUTTON_XPATH, self.CONTINUE_BUTTON_TEXT], timeout=10, after_wait=0.4):
                self.take_screenshot("13_after_continue")
                self.logger.info(" Click en Continuar exitoso")
                return True
            self.take_screenshot("error_continue_button")
            raise Exception("No se pudo clickear 'Continuar'")
        except Exception as e:
            self.logger.error(f" Error haciendo click en Continuar: {e}")
            self.take_screenshot("error_continue_button_exception")
            raise

    def is_exchange_successful(self):
        """Verificar si el intercambio fue exitoso"""
        try:
            self.logger.info(" Verificando éxito del intercambio…")
            self.wait_for_seconds(2)
            ok = self.is_element_visible(self.SUCCESS_MESSAGE, timeout=10)
            if ok:
                self.logger.info(" Intercambio exitoso confirmado")
                self.take_screenshot("14_exchange_success")
                return True
            self.logger.error(" No se encontró mensaje de éxito")
            self.take_screenshot("15_no_success_message")
            return False
        except Exception as e:
            self.logger.error(f" Error verificando éxito: {e}")
            self.take_screenshot("error_verify_success")
            return False

    def wait_for_summary_screen(self, timeout=10):
        """Espera que aparezca 'Resumen de la transacción'."""
        self.logger.info(" Esperando 'Resumen de la transacción'…")
        self.find_element(self.SUMMARY_TITLE, timeout=timeout)
        self.take_screenshot("15_summary_visible")
        return True

    def click_confirm_button(self, timeout=12):
        """Click en 'Confirmar' (content-desc dinámico o TextView con/sin espacio)."""
        self.logger.info(" Click en 'Confirmar'")
        # 1) content-desc que contiene "Confirmar" (cubre contador dinámico)
        try:
            self.click_element(self.CONFIRM_BUTTON_DESC_CONTAINS, timeout=timeout)
            self.take_screenshot("16_confirm_clicked_desc")
            return True
        except Exception:
            self.logger.info("Fallback por TextView…")
        # 2) TextView exacto con espacio al final
        try:
            self.click_element(self.CONFIRM_BUTTON_TEXT_EXACT, timeout=6)
            self.take_screenshot("16_confirm_clicked_text_exact")
            return True
        except Exception:
            pass
        # 3) Fallback sin espacio
        self.click_element(self.CONFIRM_BUTTON_TEXT_TRIM, timeout=6)
        self.take_screenshot("16_confirm_clicked_text_trim")
        return True

    def confirm_success_and_go_home(self, timeout=12):
        """
       Valida la pantalla '¡Intercambio exitoso!', toca 'Ir al inicio'
        y verifica que vuelve al Home.
        """
        self.logger.info(" Validando éxito y volviendo al inicio")

        # 1) Éxito
        try:
            # exacto
            self.find_element(self.SUCCESS_TITLE_EXACT, timeout=timeout)
        except Exception:
            # fallback por xpath exacto
            self.find_element(self.SUCCESS_TITLE_XPATH, timeout=6)
        self.take_screenshot("17_success_visible")

        # 2) Click en 'Ir al inicio'
        try:
            self.click_element(self.GO_HOME_A11Y, timeout=8)
        except Exception:
            self.click_element(self.GO_HOME_XPATH, timeout=8)
        self.wait_for_seconds(3)
        # Cerrar los 3 banners con 'X'
        self.dismiss_home_banners()

        # 3) Validar Home
        self.find_element(self.HOME_INDICATOR_SIMPLE, timeout=12)
        self.take_screenshot("18_back_on_home")
        self.logger.info(" Éxito confirmado y regreso al Home")
        return True
    
    def wait_for_history_title(self, timeout=10):
        """Confirma que estamos en el Home viendo 'Historial'."""
        self.logger.info(" Verificando título 'Historial'…")
        self.find_element(self.HISTORY_TITLE, timeout=timeout)
        self.take_screenshot("19_history_title")
        return True

    def _scroll_down(self, percent=0.7):
        """Scroll simple hacia abajo usando W3C scrollGesture (sin TouchAction)."""
        try:
            size = self.driver.get_window_size()
            region = {
                "left": 10,
                "top": int(size["height"] * 0.20),
                "width": size["width"] - 20,
                "height": int(size["height"] * 0.60),
            }
            self.driver.execute_script("mobile: scrollGesture", {**region, "direction": "down", "percent": percent})
        except Exception:
            pass

    def open_first_history_item(self):
        """Baja un poco y toca el primer item cuyo content-desc contiene 'Intercambio'."""
        self.logger.info(" Abriendo el último intercambio (primer item de la lista)")

        # 1) asegurar que estamos en la pantalla con ScrollView
        sv = None
        try:
            sv = self.find_element((AppiumBy.CLASS_NAME, "android.widget.ScrollView"), timeout=6)
        except Exception:
            # a veces el título ya garantiza la vista, igual probamos scroll
            self._scroll_down(0.6)

        # 2) buscar items dentro del ScrollView (más estable que buscar global)
        items = []
        try:
            if sv:
                items = sv.find_elements(AppiumBy.XPATH, './/android.view.ViewGroup[@content-desc and contains(@content-desc,"Intercambio")]')
            if not items:
                # pequeño scroll y reintento
                self._scroll_down(0.8)
                sv = self.find_element((AppiumBy.CLASS_NAME, "android.widget.ScrollView"), timeout=4)
                items = sv.find_elements(AppiumBy.XPATH, './/android.view.ViewGroup[@content-desc and contains(@content-desc,"Intercambio")]')
        except Exception:
            pass

        # 3) si hay items, clic al primero; si no, fallback global
        if items:
            items[0].click()
            self.take_screenshot("20_first_history_item_clicked")
            self.logger.info(" Primer intercambio abierto")
            return True

        # Fallback mínimo: primer item por XPath global
        self.click_element(
            (AppiumBy.XPATH, '(//android.view.ViewGroup[@content-desc and contains(@content-desc,"Intercambio")])[1]'),
            timeout=6
        )
        self.take_screenshot("20_first_history_item_clicked_fallback")
        self.logger.info(" Primer intercambio abierto (fallback)")
        return True

    # ----------------- flujo completo -----------------
    def perform_exchange(self, from_currency="ARS", to_currency="USDT", amount=1000):
        """
       Realizar intercambio completo ARS → USDT
        1) Navegar a Cripto
        2) Verificar pantalla Intercambiar
        3) Seleccionar ARS (Desde)
        4) Seleccionar USDT (Para)
        5) Ingresar monto
        6) Continuar
        7) Verificar éxito
        """
        self.logger.info("=" * 70)
        self.logger.info(f" INICIANDO INTERCAMBIO: {amount} {from_currency} → {to_currency}")
        self.logger.info("=" * 70)
        try:
            self.navigate_to_crypto_section()
            assert self.verify_intercambiar_screen(), "No se detectó pantalla Intercambiar"

            # Selección robusta por código
            self.select_from_currency_ars()
            self.select_to_currency_usdt()

            self.enter_amount(amount)
            self.click_continue_button()

            # PASO 6.1: Resumen + Confirmar
            self.wait_for_summary_screen()
            self.click_confirm_button()

            success = self.is_exchange_successful()
            if success:
                # validar pantalla de éxito y volver al inicio
                return self.confirm_success_and_go_home()
            else:
                return False

        except Exception as e:
            self.logger.error("=" * 70)
            self.logger.error(f" ERROR DURANTE EL INTERCAMBIO: {e}")
            self.logger.error("=" * 70)
            self.take_screenshot("error_exchange_process")
            raise

    # ----------------- test negativo -----------------
    def test_min_amount_validation(self, amount=500):
        """Validar mensaje de error con monto menor a 1000 ARS"""
        self.logger.info(" TEST NEGATIVO: Monto menor a mínimo")
        try:
            self.navigate_to_crypto_section()
            assert self.verify_intercambiar_screen(), "No se detectó pantalla Intercambiar"
            self.select_from_currency_ars()
            self.select_to_currency_usdt()
            self.enter_amount(amount)
            has_error = self.is_min_amount_error_displayed()
            if has_error:
                self.logger.info(" Validación correcta: Error mostrado para monto bajo")
                return True
            self.logger.error(" No se mostró error para monto bajo")
            return False
        except Exception as e:
            self.logger.error(f" Error en test negativo: {e}")
            return False
