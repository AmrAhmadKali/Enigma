from behave import given, when, then

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
from selenium.webdriver.firefox.service import Service
from webdriver_manager.firefox import GeckoDriverManager


@given('The Enigma Website is opened')
def step_impl(context):
    # spin up driver
    context.driver = webdriver.Firefox(service=Service(GeckoDriverManager().install()))
    context.driver.set_window_size(1920, 1080, context.driver.window_handles[0])
    context.action_chains = ActionChains(context.driver)

    context.driver.get("http://localhost")
    assert context.driver.title == "Enigma"


@when('I press the {letter} key on the {keyboard} keyboard')
def step_impl(context, letter, keyboard):
    if keyboard == 'virtual':
        key = context.driver.find_element(By.NAME, f"{letter}")
        key.click()
    elif keyboard == 'physical':
        context.driver.find_element(By.CSS_SELECTOR, 'body').send_keys(f"{letter}")
    else:
        assert 0, "Wrong keyboard argument given"


@then('The letter {letter} should be displayed in the {box} box')
def step_impl(context, letter, box):
    if box == 'input':
        element = context.driver.find_element(By.CSS_SELECTOR, '.inputContainer').text
        assert element == letter, 'Input Container does not contain '+f"{letter}"+', but '+f"{element}"
    elif box == 'output':
        element = context.driver.find_element(By.CSS_SELECTOR, '.outputContainer').text
        assert element == letter, 'Output Container does not contain '+f"{letter}"+', but '+f"{element}"
    else:
        assert 0, "Wrong box argument given"
