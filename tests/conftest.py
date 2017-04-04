import pytest
from base.webdriverfactory import WebDriverFactory

@pytest.yield_fixture()
def setUp(request, browser):
    wdf = WebDriverFactory(browser)
    driver = wdf.get_web_driver_instance()
    if request.cls is not None:
        request.cls.driver = driver
    yield driver
    driver.quit()

def pytest_addoption(parser):
    parser.addoption("--browser")

@pytest.fixture(scope="session")
def browser(request):
    return request.config.getoption("--browser")

@pytest.fixture(scope="session")
def osType(request):
    return request.config.getoption("--osType")