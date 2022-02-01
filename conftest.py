import pytest
from selenium import webdriver
from selenium.webdriver.support.event_firing_webdriver import EventFiringWebDriver, AbstractEventListener


def pytest_addoption(parser):
    parser.addoption("--browser", "-B",
                     action="store",
                     default="chrome",
                     help="choose your browser")


@pytest.fixture(scope="module")
def browser(request):
    browser_param = request.config.getoption("--browser")
    if browser_param == "chrome":
        options = webdriver.ChromeOptions()
        # options.add_argument("--headless")
        # Для эмуляции мобильной версии включить эти строки
        mobile_emulation = {"deviceName": "iPhone X"}
        options.add_argument(
            "user-agent=Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1")
        options.add_experimental_option("mobileEmulation", mobile_emulation)
        driver = webdriver.Chrome(options=options)
    elif browser_param == "firefox":
        options = webdriver.FirefoxOptions()
        options.add_argument("--headless")
        driver = webdriver.Firefox(options=options)
    elif browser_param == "safari":
        driver = webdriver.Safari()
    else:
        raise Exception(f"{request.param} is not supported!")

    driver.implicitly_wait(10)
    request.addfinalizer(driver.close)
    return driver


@pytest.fixture(params=["chrome", "safari", "firefox"])
def parametrize_browser(request):
    browser_param = request.param
    if browser_param == "chrome":
        driver = webdriver.Chrome()
    elif browser_param == "firefox":
        driver = webdriver.Firefox()
    elif browser_param == "safari":
        driver = webdriver.Safari()
    else:
        raise Exception(f"{request.param} is not supported!")

    driver.implicitly_wait(10)
    request.addfinalizer(driver.quit)

    return driver
