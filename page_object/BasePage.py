from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class BasePage:

    def __init__(self, driver):
        self.driver = driver

    def __element(self, selector: dict, index: int, link_text: str = None):
        try:
            return self.__elements(selector, link_text)[index]
        except IndexError:
            return None

    def __elements(self, selector: dict, link_text: str = None):
        by = None
        if link_text:
            by = By.LINK_TEXT
        elif 'css' in selector.keys():
            by = By.CSS_SELECTOR
            selector = selector['css']
        return self.driver.find_elements(by, selector)

    def _input(self, selector, value, index=0):
        element = self.__element(selector, index)
        element.clear()
        element.send_keys(value)

    def _get_element(self, selector, index=0):
        return self.__element(selector, index)

    def _get_elements(self, selector):
        return self.__elements(selector)

    def _get_element_text(self, selector, index=0):
        return self.__element(selector, index).text

    def _click(self, selector, index=0):
        ActionChains(self.driver).move_to_element(self.__element(selector, index)).click().perform()

    def _wait_for_visible(self, selector, link_text=None, index=0, wait=3):
        return WebDriverWait(self.driver, wait).until(EC.visibility_of(self.__element(selector, index, link_text)))

    def _wait_for_dissapear(self, selector, link_text=None, index=0, wait=1):
        return WebDriverWait(self.driver, wait).until(EC.staleness_of(self.__element(selector, index, link_text)))

    def _move_to_element(self, selector, index=0):
        ActionChains(self.driver).move_to_element(self.__element(selector, index)).perform()

    def _move_to_element_with_offset(self, element, xoffset, yoffset, index=0):
        ActionChains(self.driver).move_to_element_with_offset(element, xoffset, yoffset).perform()
