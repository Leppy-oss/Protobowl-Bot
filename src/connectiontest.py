import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep

'''
right now this can only buzz lmao
'''

driver = webdriver.Firefox()
driver.get('https://protobowl.com/msquizbowl')
name = 'Rappa Hosyckc'

while not driver.find_element(By.ID, 'username').is_displayed():
	sleep(.1) # wait for the page to load
# set name
elem = driver.find_element(By.ID, 'username') # find the username box
elem.clear()
elem.send_keys(name + Keys.RETURN)

btn = driver.find_element(By.CLASS_NAME, 'buzzbtn')
driver.execute_script("arguments[0].scrollIntoView();", btn)

'''
while True:
    if (btn.is_enabled()):
        button = driver.find_element(By.CSS_SELECTOR, 'button.btn.btn-danger.buzzbtn')
        driver.execute_script("arguments[0].click();", button)
    sleep(1)
'''