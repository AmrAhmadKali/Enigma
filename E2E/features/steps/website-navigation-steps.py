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


@when('I press the {letter} key on the VIRTUAL keyboard')
def step_impl(context, letter):
    key = context.driver.find_element(By.NAME, f"{letter}")
    key.click()


@when('I press the {letter} key on the PHYSICAL keyboard')
def step_impl(context, letter):
    context.driver.find_element(By.CSS_SELECTOR, 'body').send_keys(f"{letter}")


@then('The letter {letter} should be displayed in the INPUT box')
def step_impl(context, letter):
    element = context.driver.find_element(By.CSS_SELECTOR, '.inputContainer').text
    assert element == letter


@then('The letter {letter} should be displayed in the OUTPUT box')
def step_impl(context, letter):
    element = context.driver.find_element(By.CSS_SELECTOR, '.outputContainer').text
    assert element == letter
