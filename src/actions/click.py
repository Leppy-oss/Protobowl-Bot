from __future__ import annotations
from actions.action import Action
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement

class Click(Action):
    def __init__(self, elem: WebElement, driver=None):
        Action.__init__(self, elem=elem, script="arguments[0].click();")

    def should_run(self):
        return self.elem.is_enabled()

    def click(self):
        self.run()

    def bind_driver(self, driver: WebDriver) -> Click:
        Action.bind_driver(self, driver)
        return self