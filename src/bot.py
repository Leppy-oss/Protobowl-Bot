import unicodedata
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

def get_knowledge(i):
	bundle = driver.find_elements(By.CLASS_NAME, 'bundle')[i]
	qid = bundle.get_attribute("class").split("qid-")[1].split(" ")[0]
	if i > 0: #this feels inelegant, but works
		raw_breadcrumb = bundle.find_element(By.CLASS_NAME, 'breadcrumb').text
		answer = raw_breadcrumb.split("/Edit\n")[1]
		answer = unicodedata.normalize('NFKD', answer).encode("ascii", "ignore").decode()
		answer = answer.split("(")[0] #get only the first part of the answer, not the parenthetical note
		answer = answer.split("[")[0] #get only the first part of the answer, not the parenthetical note
		answer = answer.strip() #strip whitespace characters from around the answer (presumably in between the parenthetical note and the real answer)
		answer = answer.strip(u"\u2018").strip(u"\u2019").strip(u"\u201c").strip(u"\u201d").strip("'").strip("\"") # strip all quote marks, which occasionally cause Protobowl to reject correct answers
	else:
		answer = ''
	return {'qid': qid, 'answer': answer}

def get_raw_breadcrumb(i):
	return driver.find_elements(By.CLASS_NAME, 'breadcrumb')[i].text

def get_breadcrumb(i):
	return get_raw_breadcrumb(i).split("/Edit\n")[0]

def get_answer(i):
	if i > 0: #this feels inelegant, but works
		return get_raw_breadcrumb(i).split("/Edit\n")[1]
	else:
		return ''

print(btn.__repr__())

while True:
    '''
    btn.click()
    if (btn.should_run()):
        buzz("rock")
    '''
    try:
        print (get_knowledge(0))
        print (get_answer(1))
    except Exception as e:
        print('error while getting knowledge')

    sleep(1)