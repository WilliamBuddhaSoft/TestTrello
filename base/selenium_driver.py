from selenium.webdriver.common.by import By
from traceback import print_stack
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import *
import utilities.custom_logger as cl
import logging
import time
import os


class SeleniumDriver():

    log = cl.custom_logger(logging.DEBUG)

    def __init__(self, driver):
        self.driver = driver

    def screen_shot(self, result_message):
        """
        Takes screenshot of the current open web page
        """
        file_name = result_message + "." + str(round(time.time() * 1000)) + ".png"
        screenshot_directory = "../screenshots/"
        relative_file_name = screenshot_directory + file_name
        current_directory = os.path.dirname(__file__)
        destination_file = os.path.join(current_directory, relative_file_name)
        destination_directory = os.path.join(current_directory, screenshot_directory)

        try:

            if not os.path.exists(destination_directory):
                os.makedirs(destination_directory)

            self.driver.save_screenshot(destination_file)
            self.log.info("Screenshot save to directory: %s" % destination_file)
        except:
            self.log.error("### Exception Occurred when taking screenshot")

    def get_title(self):
        return self.driver.title

    def get_by_type(self, locatorType):
        locatorType = locatorType.lower()

        if locatorType == "id":
            return By.ID
        elif locatorType == "name":
            return By.NAME
        elif locatorType == "xpath":
            return By.XPATH
        elif locatorType == "css":
            return By.CSS_SELECTOR
        elif locatorType == "class":
            return By.CLASS_NAME
        elif locatorType == "link":
            return By.LINK_TEXT
        else:
            self.log.info("Locator type %s not correct/supported" % locatorType)

        return False

    def get_element(self, locator, locator_type="id"):
        element = None

        try:
            locator_type = locator_type.lower()
            byType = self.get_by_type(locator_type)
            element = self.driver.find_element(byType, locator)
            self.log.info("Element found with locator %s and  locatorType %s" % (locator, locator_type))
        except:
            self.log.info("Element not found with locator %s and locatorType %s" % (locator, locator_type))

        return element

    def get_element_list(self, locator, locator_type="id"):
        """
        Get list of elements
        """
        element = None

        try:
            locator_type = locator_type.lower()
            by_type = self.get_by_type(locator_type)
            element = self.driver.find_elements(by_type, locator)
            self.log.info("Element list found with locator %s and locatorType %s" % (locator, locator_type))
        except:
            self.log.info("Element list not found with locator %s and locatorType %s" % (locator, locator_type))

        return element

    def element_click(self, locator="", locator_type="id", element=None):
        """
        Click on an element
        Either provide element or a combination of locator and locatorType
        """
        try:
            if locator:  # This means if locator is not empty
                element = self.get_element(locator, locator_type)
            element.click()
            self.log.info("Clicked on element with locator %s and locatorType %s" % (locator, locator_type))
        except:
            self.log.info("Cannot click on the element with locator %s and locatorType %s" % (locator, locator_type))
            print_stack()

    def send_keys(self, data, locator="", locator_type="id", element=None):
        """
        Send keys to an element
        Either provide element or a combination of locator and locator_type
        """
        try:
            if locator:  # This means if locator is not empty
                element = self.get_element(locator, locator_type)
            element.send_keys(data)
            self.log.info("Sent data on element with locator %s and locatorType %s" % (locator, locator_type))
        except:
            self.log.info("Can't send data on the element with locator %s and locatorType %s" % (locator, locator_type))
            print_stack()

    def get_text(self, locator="", locator_type="id", element=None, info=""):
        """
        Get 'Text' on an element
        Either provide element or a combination of locator and locator_type
        """
        try:
            if locator: # This means if locator is not empty
                self.log.debug("In locator condition")
                element = self.get_element(locator, locator_type)
            self.log.debug("Before finding text")
            text = element.text
            self.log.debug("After finding element, size is: %s" % str(len(text)))
            if len(text) == 0:
                text = element.get_attribute("innerText")
            if len(text) != 0:
                self.log.info("Getting text on element %s " %  info)
                self.log.info("The text is :: %s" % text)
                text = text.strip()
        except:
            self.log.error("Failed to get text on element " + info)
            print_stack()
            text = None
        return text

    def is_element_present(self, locator="", locator_type="id", element=None):
        """
        Check if element is present
        Either provide element or a combination of locator and locator_type
        """
        try:
            if locator:  # This means if locator is not empty
                element = self.get_element(locator, locator_type)
            if element is not None:
                self.log.info("Element present with locator %s and locatorType %s" % (locator, locator_type))
                return True
            else:
                self.log.info("Element not present with locator %s and locatorType %s" % (locator, locator_type))
                return False
        except:
            print("Element not found")
            return False

    def is_element_displayed(self, locator="", locator_type="id", element=None):
        """
        Check if element is displayed
        Either provide element or a combination of locator and locator_type
        """
        isDisplayed = False
        try:
            if locator:  # This means if locator is not empty
                element = self.get_element(locator, locator_type)
            if element is not None:
                isDisplayed = element.is_displayed()
                self.log.info("Element is displayed with locator %s and locatorType %s" % (locator, locator_type))
            else:
                self.log.info("Element not displayed with locator %s and locatorType %s" % (locator, locator_type))
            return isDisplayed
        except:
            print("Element not found")
            return False

    def element_presence_check(self, locator, by_type):
        """
        Check if element is present
        """
        try:
            element_list = self.driver.find_elements(by_type, locator)
            if len(element_list) > 0:
                self.log.info("Element present with locator %s and locatorType %s" % (locator, str(by_type)))
                return True
            else:
                self.log.info("Element not present with locator %s and locatorType %s" % (locator, str(by_type)))
                return False
        except:
            self.log.info("Element not found")
            return False

    def wait_for_element(self, locator, locator_type="id",
                         timeout=10, poll_frequency=0.5):
        """
        Explicit waiting for element
        """
        element = None
        try:
            by_type = self.get_by_type(locator_type)
            self.log.info("Waiting for maximum $s seconds for element to be clickable" % str(timeout))
            wait = WebDriverWait(self.driver, timeout=timeout,
                                 poll_frequency=poll_frequency,
                                 ignored_exceptions=[NoSuchElementException,
                                                     ElementNotVisibleException,
                                                     ElementNotSelectableException])
            element = wait.until(EC.element_to_be_clickable((by_type, locator)))
            self.log.info("Element appeared on the web page")
        except:
            self.log.info("Element not appeared on the web page")
            print_stack()
        return element

    def web_scroll(self, direction="up"):
        """
        Scroll page up or down
        :param direction:
        :return:
        """
        if direction == "up":
            # Scroll Up
            self.driver.execute_script("window.scrollBy(0, -1000);")

        if direction == "down":
            # Scroll Down
            self.driver.execute_script("window.scrollBy(0, 1000);")