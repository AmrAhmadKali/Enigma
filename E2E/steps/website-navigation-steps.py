import os

from behave import *
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from webdriver_manager.firefox import GeckoDriverManager
from selenium.common.exceptions import NoAlertPresentException


# TODO: context.driver.close() (oder ähnlich) am Ende des Tests, damit Firefox Prozess geschlossen wird
# TODO: Tests laufen zu schnell, sollten auf Websocket Antwort warten bis nächster Step ausgeführt wird.
#  Derzeit Probleme da Steps nicht in richtiger Reihenfolge ausgeführt werden


@given('The Enigma Website is opened')
def step_impl(context):
    # spin up driver
    options = Options()
    options.headless = True  # To change
    context.driver = webdriver.Firefox(options=options, service=Service(GeckoDriverManager().install()))
    context.action_chains = ActionChains(context.driver)
    if "CI" in os.environ.keys():
        context.driver.get("http://frontend")
    else:
        context.driver.get("http://localhost")
        assert context.driver.title == "Enigma"


@when('I press the {letter} key on the {keyboard} keyboard')
def step_impl(context, letter, keyboard):
    if keyboard == 'virtual':
        key = context.driver.find_element(By.NAME, f"k_{letter}")
        key.click()
    elif keyboard == 'physical':
        context.driver.find_element(By.CSS_SELECTOR, 'body').send_keys(f"{letter}")
    else:
        assert 0, "Wrong keyboard argument given"


@when('I press the {letter} key on the plugboard')
def step_impl(context, letter):
    key = context.driver.find_element(By.NAME, f"p_{letter}")
    key.click()


@when('I press the reset button on the plugboard')
def step_impl(context):
    key = context.driver.find_element(By.NAME, "plugboard_reset")
    key.click()


@then('The letter {letter} should be displayed in the {box} box')
def step_impl(context, letter, box):
    if box == 'input':
        element = context.driver.find_element(By.CSS_SELECTOR, '.inputContainer').text
        assert element == letter, f'Input Container does not contain {letter}, but {element}'
    elif box == 'output':
        element = context.driver.find_element(By.CSS_SELECTOR, '.outputContainer').text
        assert element == letter, f'Output Container does not contain {letter}, but {element}'
    else:
        assert 0, "Wrong box argument given"


@when('I press the {letter} key {limit} times on the keyboard')
def step_impl(context, letter, limit):
    key = context.driver.find_element(By.NAME, f"k_{letter}")
    for i in range(int(limit) + 1):
        key.click()


@then('I see only {limit} characters in the {box} box')
def step_impl(context, limit, box):
    context.driver.implicitly_wait(0.5)
    if box == 'input':
        input_box = context.driver.find_element(By.CSS_SELECTOR, '.inputContainer').text
        assert len(input_box) == int(limit), f'Input box should have {limit} characters at most not {len(input_box)}'
    elif box == 'output':
        output_box = context.driver.find_element(By.CSS_SELECTOR, '.outputContainer').text
        assert len(output_box) == int(limit), f'Output box should have {limit} characters at most not {len(output_box)}'
    else:
        assert 0, "Wrong box argument given"


@given('I have a list of keys {keys}')
def step_impl(context, keys):
    context.values = []
    splitted_keys = keys.split(', ')
    context.values = splitted_keys
    print(splitted_keys)
    print(context.values)


@when('I press on the specified keys on the plugboard')
def step_impl(context):
    plugboard_limit = 10
    for i in range(plugboard_limit*2):
        button = context.driver.find_element(By.NAME, f"p_{context.values[i]}")
        button.click()


@then('an alert is shown')
def step_impl(context):
    try:
        alert = context.driver.switch_to.alert
        assert alert, 'No alert is shown'
        alert.accept()
    except NoAlertPresentException:
        assert 0, 'No alert is shown'
