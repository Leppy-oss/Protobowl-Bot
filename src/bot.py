import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
from actions.click import Click

driver = webdriver.Chrome()
driver.get('https://protobowl.com/Rappa Hosyckc')

name = 'Rappa Hosyckc'

while not driver.find_element(By.ID, 'username').is_displayed():
	sleep(.1) # wait for the page to load
# set name
username = driver.find_element(By.ID, 'username') # find the username box
username.clear()
username.send_keys(name + Keys.RETURN)

btn = Click(driver.find_element(By.CLASS_NAME, 'buzzbtn')).bind_driver(driver)

print(btn.__repr__())

while True:
    btn.run()

    sleep(1)