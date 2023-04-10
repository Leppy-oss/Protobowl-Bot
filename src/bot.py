import json
import unicodedata
import selenium
from selenium import webdriver
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
import time
from actions.click import Click
from util import natural
import random
import string
import tkinter as tk
from tkinter import *

driver = None

name = ''
root = tk.Tk()
root.title('Protobowl Bot Interface')
root.geometry('400x400')

buzzbtn = None
nextbtn = None
skipbtn = None

is_botting = False
should_quit = False
rapid_launch = True

caption = Label(
    root, text='Welcome to Protobowl Bot! Pardon the primitive UI, it\'s still a WIP...')
caption.pack()
nameInput = tk.Text(root, height=1, width=10)
tk.Label(root, text='Enter bot name here...').pack()
nameInput.pack()
tk.Label(root, text='Enter room name here...').pack()
roomInput = tk.Text(root, height=1, width=10)
roomInput.pack()
stop_label = tk.Label(root, text='Stopping...')
should_natural = True


def launch_bot():
    global is_botting, driver, buzzbtn, nextbtn, skipbtn, nameInput, roomInput
    if not is_botting:
        is_botting = True
        driver = webdriver.Chrome()
        driver.get('https://protobowl.com/' +
                   (str(roomInput.get(1.0, 'end-1c')) if not rapid_launch else 'msquizbowl'))
        while not driver.find_element(By.ID, 'username').is_displayed():
            sleep(.1)  # wait for the page to load

        username = driver.find_element(By.ID, 'username')
        username.clear()
        username.send_keys((str(nameInput.get(1.0, 'end-1c'))
                           if not rapid_launch else 'natty bot') + Keys.RETURN)

        # initialize buttons
        buzzbtn = Click(driver.find_element(
            By.CLASS_NAME, 'buzzbtn')).bind_driver(driver)
        nextbtn = Click(driver.find_element(
            By.CLASS_NAME, 'nextbtn')).bind_driver(driver)
        skipbtn = Click(driver.find_element(
            By.CLASS_NAME, 'skipbtn')).bind_driver(driver)


def stop_bot():
    global is_botting, driver, should_quit
    if is_botting:
        is_botting = False
        driver.close()
    stop_label.pack()
    root.destroy()
    should_quit = True
    quit()


start_btn = Button(root, text='LAUNCH BOT', command=launch_bot)
start_btn.pack()
stop_btn = Button(root, text='STOP BOT', command=stop_bot)
stop_btn.pack()


def buzz(guess):
    guess_input = driver.find_element(By.CLASS_NAME, 'guess_input')
    print('Buzzing')

    '''
    while not (guess_input.is_displayed()):
        print('waiting for the text field to become available')
    '''

    if should_natural:
        # natural delay before typing
        # sleep(random.randint(500, 1000) / 1000 * 1.25)
        pass

    else:
        sleep(1)

    if should_natural:
        splits = natural.naturalized_splits(guess)
        start_time = time.time()
        print('initialized splits')
        for split in splits:
            type_successful = False
            try:
                guess_input.send_keys(split[0])
            except:
                continue
            '''
            while not type_successful:
                if time.time() - start_time > 5:
                    break
                try:
                    type_successful = True
                except:
                    continue
            '''

            sleep(split[1])
    else:
        type_successful = False
        print('oloop prev')
        while not type_successful:
            print('oloop ')
            try:
                buzzbtn.click()
                guess_input.send_keys(guess)
                type_successful = True
            except Exception as e:
                print(e)
                continue

    try:
        guess_input.send_keys('\n')
    except:
        pass


def get_knowledge(i):
    bundle = driver.find_elements(By.CLASS_NAME, 'bundle')[i]
    qid = bundle.get_attribute("class").split("qid-")[1].split(" ")[0]
    if i > 0:  # only return a non-empty answer if it is a past question
        raw_breadcrumb = bundle.find_element(By.CLASS_NAME, 'breadcrumb').text
        answer = raw_breadcrumb.split("/Edit\n")[1]
        answer = unicodedata.normalize(
            'NFKD', answer).encode("ascii", "ignore").decode()

        # remove the parenthesised part of the answer
        answer = answer.split("(")[0]
        answer = answer.split("[")[0]
        answer = answer.strip()
    else:
        answer = ''
    return {'qid': qid, 'answer': answer}


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
        json.dump(object, f, sort_keys=True)


prevqid = ''

while not is_botting and not should_quit and not rapid_launch:
    root.update()

if rapid_launch:
    launch_bot()

while is_botting and not should_quit:
    try:
        try:
            nextbtn.click()
            # sleep(0.2)
        except:
            pass
        got_knowledge = get_knowledge(0)
        if got_knowledge['qid'] != prevqid:
            print('new question occurred')
            guess: str = guess_answer(got_knowledge['qid'])
            print(guess)
            if guess != '':
                if should_natural:
                    # sleep(random.randint(500, 1000) / 1000 * 0.5)
                    pass

                try:
                    sleep(0.25)
                    buzzbtn.click()

                except:
                    print('buzz failed')

                try:
                    if should_natural:
                        sleep(random.randint(500, 1000) / 1000 * 1.5)

                    buzz(natural.naturalize_guess(guess.lower().replace('-', ' ').translate(
                        str.maketrans('', '', string.punctuation))) if should_natural else guess.lower().replace('-', ' ').translate(
                        str.maketrans('', '', string.punctuation)))
                except Exception as e:
                    print('guess failed: ' + str(e))
            else:
                try:
                    sleep(0.5)
                    skipbtn.click()
                    print('attempted to skip')
                except Exception as e:
                    print('couldnt skip rip: ' + str(e))

            try:
                a = get_knowledge(1)
                record_answer(a['qid'], a['answer'])
                print('answer to previous question: ' + a['answer'])
            except Exception as e:
                print('error while trying to save knowledge: ' + str(e))

            write_out('../res/knowledge.json')
            print('knowledge now contains ' + str(len(knowledge)) + ' pairs')
        prevqid = got_knowledge['qid']

    except Exception as e:
        # print('bot operation failed: ' + str(e))
        pass

    root.update()
    # sleep(0.2)
