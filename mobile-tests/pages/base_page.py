from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import logging
import os
from datetime import datetime

class BasePage:
    
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 20)
        self.logger = logging.getLogger(__name__)
        
    def find_element(self, locator, timeout=20):
        try:
            element = WebDriverWait(self.driver, timeout).until(
               EC.presence_of_element_located(locator)
            )
            self.logger.info(f" Elemento encontrado: {locator}")
            return element
        except TimeoutException:
            self.logger.error(f" Timeout buscando elemento: {locator}")
            self.take_screenshot(f"error_element_not_found")
            raise
    
    def find_elements(self, locator, timeout=20):
        try:
            elements = WebDriverWait(self.driver, timeout).until(
               EC.presence_of_all_elements_located(locator)
            )
            self.logger.info(f" Elementos encontrados: {len(elements)}")
            return elements
        except TimeoutException:
            self.logger.error(f" Timeout buscando elementos: {locator}")
            return []
    
    def click_element(self, locator, timeout=20):
        try:
            element = WebDriverWait(self.driver, timeout).until(
               EC.element_to_be_clickable(locator)
            )
            element.click()
            self.logger.info(f" Click realizado en: {locator}")
        except TimeoutException:
            self.logger.error(f" Elemento no clickeable: {locator}")
            self.take_screenshot(f"error_element_not_clickable")
            raise
    
    def send_keys(self, locator, text, clear_first=True, timeout=20):
        try:
            element = self.find_element(locator, timeout)
            if clear_first:
                element.clear()
            element.send_keys(text)
            self.logger.info(f" Texto ingresado en {locator}")
        except Exception as e:
            self.logger.error(f" Error ingresando texto: {e}")
            self.take_screenshot(f"error_send_keys")
            raise
    
    def get_text(self, locator, timeout=20):
        try:
            element = self.find_element(locator, timeout)
            text = element.text
            self.logger.info(f" Texto obtenido: {text}")
            return text
        except Exception as e:
            self.logger.error(f" Error obteniendo texto: {e}")
            return ""
    
    def is_element_visible(self, locator, timeout=10):
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located(locator)
            )
            self.logger.info(f" Elemento visible: {locator}")
            return True
        except TimeoutException:
            self.logger.warning(f" Elemento no visible: {locator}")
            return False
    
    def wait_for_element_disappear(self, locator, timeout=20):
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.invisibility_of_element_located(locator)
            )
            self.logger.info(f" Elemento desapareció: {locator}")
            return True
        except TimeoutException:
            self.logger.warning(f" Elemento aún visible: {locator}")
            return False
    
    def scroll_to_element(self, locator):
        try:
            element = self.find_element(locator)
            self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
            self.logger.info(f" Scroll realizado hacia: {locator}")
        except Exception as e:
            self.logger.error(f" Error en scroll: {e}")
    
    def swipe_up(self, duration=800):
        try:
            size = self.driver.get_window_size()
            start_x = size['width'] // 2
            start_y = int(size['height'] * 0.8)
            end_y = int(size['height'] * 0.2)
            
            self.driver.swipe(start_x, start_y, start_x, end_y, duration)
            self.logger.info(" Swipe up realizado")
        except Exception as e:
            self.logger.error(f" Error en swipe: {e}")
    
    def swipe_down(self, duration=800):
        try:
            size = self.driver.get_window_size()
            start_x = size['width'] // 2
            start_y = int(size['height'] * 0.2)
            end_y = int(size['height'] * 0.8)
            
            self.driver.swipe(start_x, start_y, start_x, end_y, duration)
            self.logger.info(" Swipe down realizado")
        except Exception as e:
            self.logger.error(f" Error en swipe: {e}")
    
    def hide_keyboard(self):
        try:
            if self.driver.is_keyboard_shown():
                self.driver.hide_keyboard()
                self.logger.info(" Teclado ocultado")
        except:
            pass
    
    def take_screenshot(self, name):
        try:
            # Crear carpeta si no existe
            os.makedirs("reports/screenshots", exist_ok=True)
            
            filename = f"reports/screenshots/{name}_{self._get_timestamp()}.png"
            self.driver.save_screenshot(filename)
            self.logger.info(f"Screenshot guardado: {filename}")
        except Exception as e:
            self.logger.error(f"Error guardando screenshot: {e}")

    def _get_timestamp(self):
        return datetime.now().strftime("%Y%m%d_%H%M%S")

    def wait_for_seconds(self, seconds):
        import time
        time.sleep(seconds)
        self.logger.info(f"Esperando {seconds} segundos...")
    
    def find_element_by_text(self, text, exact=True):
        try:
            if exact:
                xpath = f"//*[@text='{text}']"
            else:
                xpath = f"//*[contains(@text, '{text}')]"
            
            locator = (AppiumBy.XPATH, xpath)
            return self.find_element(locator)
        except:
            self.logger.error(f" No se encontró elemento con texto: {text}")
            raise
    
    def click_by_text(self, text, exact=True):
        try:
            element = self.find_element_by_text(text, exact)
            element.click()
            self.logger.info(f" Click en elemento con texto: {text}")
        except Exception as e:
            self.logger.error(f" Error haciendo click en texto '{text}': {e}")
            raise