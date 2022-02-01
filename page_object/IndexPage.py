from selenium.common.exceptions import JavascriptException

from locators import Banner
from page_object.BasePage import BasePage


class IndexPage(BasePage):

    def find_banner(self):
        return self._get_element(Banner.ad_banner)

    def goto_banner(self):
        self._move_to_element(Banner.ad_banner)

    def find_ad_banner(self, banner):
        return self._get_element(banner)

    def find_ad_banners(self, banner):
        return self._get_elements(banner)

    def goto_ad_banner(self, banner):
        self._move_to_element(banner)

    def goto_banner_with_offset(self, banner, xoffset, yoffset):
        self._move_to_element_with_offset(banner, xoffset, yoffset)


