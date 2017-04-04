# TestTrello

## Introduction:

Few selenium tests and requests to check if tests are passed. 

## Software stack:

* Python 3.6
* Selenium
* Py-Test

## Project structure:
```
├── base (
    ├── __init__.py
    ├── basepage.py (Page Object Pattern (POP) base page)
    ├── selenium_driver.py (useful methods for selenium tests)
    ├── webdriverfactory.py (method to define what browser to drive) 
├── pages 
    ├── board_page
    │   ├── __init__.py 
    │   ├── base_page.py (actions methods for specific board page)
    ├── home
    │   ├── __init__.py
    │   ├── login_page.py (actions for authentication)
    ├── main_page
    │   ├── __init__.py
    │   ├── main_page.py (actions of main page with boards for authorised user)
├── screenshots
├── tests (contains all tests)
    ├── board_page
    │   ├── __init__.py 
    │   ├── card_test.py (tests for board page actions)
    ├── home
    │   ├── __init__.py
    │   ├── login_test.py (authentication tests)
    ├── main_page
    │   ├── __init__.py
    │   ├── board_test.py (simple create/delete tests)
    ├── __init__.py
    ├── conftest.py (pytest options) 
├── utilities 
    ├── __init__.py
    ├── custom_logger.py (messages logger)
    ├── teststatus.py (methods to get tests statuses)
    ├── util.py (useful methods for tests)
└── requirements.txt (file that contains all needed set of tools to install)
```

## Installation instructions:
1. Create project folder:
    * $ mkdir testTrello
    * $ cd testTrello

2. Clone all repositories:
    * $ git clone git@github.com:WilliamBuddhaSoft/TestTrello.git

3. Create virtual environment for your project and install requirements:
    * $ mkvirtualenv --python=path/to/python3 testTrello
    * $ pip install -r requirements.txt
4. Download chromedriver from https://sites.google.com/a/chromium.org/chromedriver/downloads

5. In file "webdriverfactory.py" change path to your chomedriver.exe file

6. Run tests from command line
    * $ py.test path/to/project/tests --browser chrome --html=report.html
