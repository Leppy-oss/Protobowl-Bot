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

def buzz(text):
    guess_input = driver.find_element(By.CLASS_NAME, 'guess_input') # input
    print('Buzzing')
    while not guess_input.is_enabled() and not btn.should_run():
        print ('not avialable')
        continue

    sleep(0.5) # let the guess box appear
    guess_input.send_keys(text + '\n')
    sleep(0.5) # let the guess box appear

print(btn.__repr__())

while True:
    btn.click()
    if (btn.should_run()):
        buzz("rock")

    sleep(1)