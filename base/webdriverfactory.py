"""
@package base

WebDriver Factory class implementation
It creates a webdriver instance based on browser configurations

Example:
    wdf = WebDriverFactory(browser)
    wdf.getWebDriverInstance()
"""
import traceback
from selenium import webdriver
import os


class WebDriverFactory():

    def __init__(self, browser):
        """
        Initializes WebDriverFactory class
        """
        self.browser = browser

    def get_web_driver_instance(self):
        """
        Get WebDriver Instance based on the browser configuration
        """
        base_URL = "https://trello.com"

        if self.browser == "safari":
            server_location = "/Users/vasily_vlasov/Documents/workspace/selenium/selenium-server-standalone-3.3.1.jar"
            os.environ['SELENIUM_SERVER_JAR'] = server_location
            driver = webdriver.Safari()

        elif self.browser == "firefox":
            driver = webdriver.Firefox()

        elif self.browser == "chrome":
            driver_location = "/Users/vasily_vlasov/Documents/workspace/selenium/chromedriver"
            os.environ['webdriver.chrome.driver'] = driver_location
            driver = webdriver.Chrome(driver_location)

        else:
            driver = webdriver.Firefox()

        # Setting Driver Implicit Time out for An Element
        driver.implicitly_wait(10)
        # Maximize the window
        driver.maximize_window()
        # Loading browser with App URL
        driver.get(base_URL)

        return driver