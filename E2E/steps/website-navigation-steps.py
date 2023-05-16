import os

from behave import *
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options

# TODO: context.driver.close() (oder ähnlich) am Ende des Tests, damit Firefox Prozess geschlossen wird
# TODO: Tests laufen zu schnell, sollten auf Websocket Antwort warten bis nächster Step ausgeführt wird.
#  Derzeit Probleme da Steps nicht in richtiger Reihenfolge ausgeführt werden


@given('The Enigma Website is opened')
def step_impl(context):
    # spin up driver
    options = Options()
    options.headless = True
    context.driver = webdriver.Firefox(options=options)
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
