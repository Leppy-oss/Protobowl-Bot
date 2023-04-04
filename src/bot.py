import json
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
driver.get('https://protobowl.com/msquizbowl')

name = 'Rappa Hosyckc'

while not driver.find_element(By.ID, 'username').is_displayed():
    sleep(.1)  # wait for the page to load

# set name
username = driver.find_element(By.ID, 'username')  # find the username box
username.clear()
username.send_keys(name + Keys.RETURN)

btn = Click(driver.find_element(By.CLASS_NAME, 'buzzbtn')).bind_driver(driver)


def buzz(text):
    guess_input = driver.find_element(By.CLASS_NAME, 'guess_input')  # input
    print('Buzzing')
    while not guess_input.is_enabled() and not btn.should_run():
        print('not avialable')
        continue

    sleep(0.5)  # let the guess box appear
    guess_input.send_keys(text + '\n')
    sleep(0.5)  # let the guess box appear


def get_knowledge(i):
    bundle = driver.find_elements(By.CLASS_NAME, 'bundle')[i]
    qid = bundle.get_attribute("class").split("qid-")[1].split(" ")[0]
    if i > 0:  # this feels inelegant, but works
        raw_breadcrumb = bundle.find_element(By.CLASS_NAME, 'breadcrumb').text
        answer = raw_breadcrumb.split("/Edit\n")[1]
        answer = unicodedata.normalize(
            'NFKD', answer).encode("ascii", "ignore").decode()
        # get only the first part of the answer, not the parenthetical note
        answer = answer.split("(")[0]
        # get only the first part of the answer, not the parenthetical note
        answer = answer.split("[")[0]
        # strip whitespace characters from around the answer (presumably in between the parenthetical note and the real answer)
        answer = answer.strip()
        answer = answer.strip(u"\u2018").strip(u"\u2019").strip(u"\u201c").strip(u"\u201d").strip("'").strip(
            "\"")  # strip all quote marks, which occasionally cause Protobowl to reject correct answers
    else:
        answer = ''
    return {'qid': qid, 'answer': answer}


def get_raw_breadcrumb(i):
    return driver.find_elements(By.CLASS_NAME, 'breadcrumb')[i].text


def get_breadcrumb(i):
    return get_raw_breadcrumb(i).split("/Edit\n")[0]


def get_answer(i):
    if i > 0:
        return get_raw_breadcrumb(i).split("/Edit\n")[1]
    else:
        return ''


knowledge = {}
try:
    with open('../res/knowledge.json', 'r') as f:
        knowledge = json.load(f)
except Exception as e:
    print(str(e))

initial_knowledge_length = len(knowledge)
print("knowledge currently consists of "+str(len(knowledge))+" pairs.")


def guess_answer(qid) -> str:
    if qid in knowledge:
        return knowledge[qid]
    return ""


def record_answer(qid, answer):
    knowledge[qid] = answer


def write_out(filename, object=knowledge):
    with open(filename, 'w') as f:
        # keys sorted to reduce deltas in our version control system
        json.dump(object, f, sort_keys=True)


print(btn.__repr__())
prevqid = ''

while True:
    '''
    btn.click()
    if (btn.should_run()):
        buzz("rock")
    '''
    try:
        if get_knowledge(0)['qid'] != prevqid:
            guess: str = guess_answer(get_knowledge(0)['qid'])
            print(guess)
            try:
                a = get_knowledge(1)
                record_answer(a['qid'], a['answer'])
                print('answer to previous question: ' + a['answer'])
            except Exception as e:
                print('error while trying to save knowledge: ' + str(e))

            write_out('../res/knowledge.json')
            print('knowledge now contains ' + str(len(knowledge)) + ' pairs')
        prevqid = get_knowledge(0)['qid']

    except Exception as e:
        print('error while getting knowledge: ' + str(e))

    sleep(.1)
