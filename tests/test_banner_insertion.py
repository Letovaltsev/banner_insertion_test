import glob
import os
import time

import allure
import pytest
import zipfile

import selenium.common.exceptions
from allure_commons.types import AttachmentType

from locators import Banner
from page_object import IndexPage


# Распаковывает все файлы из архива в папку "domains"
def unzip_files(zip_name):
    file_path = os.path.join(os.path.dirname(__file__), '..', 'test_data')
    zip_file = file_path + '/' + zip_name
    if zipfile.is_zipfile(zip_file):
        z = zipfile.ZipFile(zip_file, 'r')
        file_list = z.namelist()
        for file in file_list:
            if os.path.isfile(os.path.join(file_path, file)):
                z.extract(file, file_path + "/domains")
        z.close()
    else:
        print("File is not ZIP archive")


# Создет список доменов и уникалых URL для параметризации теста
def get_url_list(zip_name: str, url_count: int = 0):
    url_list = []
    if zip_name:
        unzip_files(zip_name)
    domains_path = os.path.join(os.path.dirname(__file__), '..', 'test_data', 'domains')
    files = glob.glob(domains_path + '/**/*.txt', recursive=True)
    for file in files:
        with open(file, 'r', encoding='utf-8') as f:
            url_counter = 0
            for line in f:
                if "http://" not in line:
                    url_line = "http://" + line
                    url = (line[0:-1], url_line.rstrip())
                else:
                    url = (os.path.basename(file)[:-4], line.rstrip())
                if url not in url_list and url_count != url_counter:
                    url_list.append(url)
                    url_counter += 1
                else:
                    break
    print("Number of domains: " + str(len(url_list)))
    return url_list


@allure.feature("Native banner insertion")
@pytest.mark.parametrize('domain, url', get_url_list('', 150))
def test_banner_insertion(browser, domain, url):
    # Путь к скрипту подбора ключевых слов
    path_to_keywords = os.path.join(
        os.path.join(os.path.dirname(__file__), '..', 'test_data', 'keywords.js'))
    # Путь к исполняемому скрипту
    path_to_script = os.path.join(
        os.path.join(os.path.dirname(__file__), '..', 'test_data', 'obfuscated_placement_check_t2.js'))
    # Путь к папке со скриншотами для текущего домена
    path_to_screenshots = os.path.join(
        os.path.join(os.path.dirname(__file__), '..', 'test_data', 'screenshots', domain))
    with open(path_to_keywords, 'r', encoding='utf-8') as script:
        keywords_script = script.read()
    with open(path_to_script, 'r', encoding='utf-8') as script:
        native_script = script.read()
    browser.get(url)
    time.sleep(2)
    assert 'https://' not in browser.current_url, "It is https site"
    # Исполняем скрипт подбора ключевых слов
    browser.execute_script(keywords_script)
    # Проверяем наличие мест под баннеры
    places = browser.execute_script('return Boolean(window["1E1B9nedt"])')
    if not places:
        pytest.skip("No places for banners")
    else:
        browser.execute_script(native_script)
        # Берет текущую страницу браузера и ищет тестовый баннер
        index_page = IndexPage(browser)
        # Ищем возможные баннеры
        banner_types = [Banner.ad_small_banner, Banner.ad_medium_banner, Banner.ad_large_banner]
        banners_counter = 0
        for banner_type in banner_types:
            banners = index_page.find_ad_banners(banner_type)
            if banners:
                for banner in banners:
                    if banner and banner.is_displayed():
                        # При успешном отображении баннера прокручивает до него страницу
                        try:
                            index_page.goto_banner_with_offset(banner, 0, banner.size['height'])
                        except selenium.common.exceptions.MoveTargetOutOfBoundsException:
                            continue
                        banners_counter += 1
                        allure.attach(browser.get_screenshot_as_png(), name="Screenshot", attachment_type=AttachmentType.PNG)
                        # Создает папку под скриншоты для каждого домена, затем добавляет скриншот в папку по порядку
                        if not os.path.isdir(path_to_screenshots):
                            os.mkdir(path_to_screenshots)
                        screenshot_count = len(os.listdir(path_to_screenshots))
                        with open(path_to_screenshots + "/" + str(screenshot_count + 1) + ".png", 'wb') as f:
                            f.write(browser.get_screenshot_as_png())
        if banners_counter == 0:
            assert False, "Banner was not displayed"
