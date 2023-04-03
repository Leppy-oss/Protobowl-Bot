from __future__ import annotations
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.remote.webdriver import WebDriver

class Action:
    def __init__(self: object, elem: WebElement, script: str, driver=None):
        self.elem = elem
        self.script = script
        self.driver = None

    def __repr__(self) -> str:
        return f"{type(self).__name__}(elem={self.elem}, script={self.script})"

    def set_elem(self, elem: WebElement):
        self.elem = elem

    def get_elem(self) -> WebElement:
        return self.elem
    
    def set_script(self, script: str):
        self.script = script

    def get_script(self) -> str:
        return self.script

    def run(self):
        if self.should_run():
            if (self.driver is None):
                print('Driver was not properly bound to the action, try using runwith() and pass in the driver instead. Or, bind the driver first.')
            else:
                try:
                    self.driver.execute_script(self.script, self.elem)
                except:
                    print('Action failed to run')

    def runwith(self, driver: WebDriver):
        if self.should_run():
            driver.execute_script(self.script, self.elem)

    def run_async(self):
        if self.should_run():
            if (self.driver is None):
                print('Driver was not properly bound to the action, try using run_with_async() and pass in the driver instead. Or, bind the driver first.')
            else:
                try:
                    self.driver.execute_async_script(self.script, self.elem)
                except:
                    print('Action failed to run')

    def run__with_async(self, driver: WebDriver):
        if self.should_run():
            driver.execute_async_script(self.script, self.elem)

    def should_run(self):
        return True

    def bind_driver(self, driver: WebDriver) -> Action:
        self.driver = driver
        return self