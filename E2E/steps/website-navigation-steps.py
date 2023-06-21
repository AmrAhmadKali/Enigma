import os

from behave import *
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from webdriver_manager.firefox import GeckoDriverManager
from selenium.common.exceptions import NoAlertPresentException, ElementNotInteractableException


# TODO: Tests laufen zu schnell, sollten auf Websocket Antwort warten bis nächster Step ausgeführt wird.
#  Derzeit Probleme da Steps nicht in richtiger Reihenfolge ausgeführt werden


@given('The Enigma Website is opened')
def step_impl(context):
    # spin up driver
    options = Options()
    options.headless = False  # To change
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
    # context.driver.implicitly_wait(0.5)
    if box == 'input':
        element = context.driver.find_element(By.CSS_SELECTOR, '.inputContainer').text
        assert element == letter, f'Input Container does not contain {letter}, but {element}'
    elif box == 'output':
        element = context.driver.find_element(By.CSS_SELECTOR, '.outputContainer').text
        assert element == letter, f'Output Container does not contain {letter}, but {element}'
    else:
        assert 0, "Wrong box argument given"


@then('The plugboard box should be empty')
def step_impl(context):
    text = context.driver.find_element(By.CSS_SELECTOR, '.plugboardContainer').text
    # WebDriverWait(context.driver, timeout=20).until(
    #     EC.text_to_be_present_in_element((By.CLASS_NAME, "plugboardContainer"), ''))
    assert text == '', 'Plugboard Container should be empty, but is not'


@when('I press the {letter} key {limit} times on the keyboard')
def step_impl(context, letter, limit):
    key = context.driver.find_element(By.NAME, f"k_{letter}")
    for i in range(int(limit) + 1):
        key.click()


@then('I see only {limit} characters in the {box} box')
def step_impl(context, limit, box):
    # context.driver.implicitly_wait(0.5)
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


@when('I press on the specified keys on the plugboard')
def step_impl(context):
    plugboard_limit = 10
    for i in range(plugboard_limit * 2):
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


@then('The lamp {lamp} lights up')
def step_impl(context, lamp):
    # context.driver.implicitly_wait(0.5)
    element = context.driver.find_element(By.NAME, f"l_{lamp}")
    background_color = element.value_of_css_property("background-color")
    YELLOW = 'rgb(255, 255, 0)'
    assert background_color == YELLOW, f"The lamp {lamp} didn't light up"


@when('I click setting symbol')
def step_impl(context):
    element = context.driver.find_element(By.ID, 'showMenuBtn')
    element.click()
    # WebDriverWait(context.driver, timeout=10).until(EC.element_to_be_clickable((By.ID, "variants")))


@when('I choose the variant {variant}')
def step_impl(context, variant):
    dropdown = context.driver.find_element(By.CSS_SELECTOR, '#variants')
    dropdown.click()

    variant_choice = context.driver.find_element(By.CSS_SELECTOR, f'option[value="{variant}"]')
    variant_choice.click()


@when('I choose the Reflector {reflector}')
def step_impl(context, reflector):
    dropdown = context.driver.find_element(By.ID, 'reflector')
    # Get the position of the element
    dropdown_position = dropdown.location
    # Scroll to the position of the element
    scroll_script = f"window.scrollTo({dropdown_position['x']}, {dropdown_position['y']})"
    context.driver.execute_script(scroll_script)
    try:
        dropdown.click()
    except ElementNotInteractableException:
        print(f'dropdown.location :     {dropdown.location}\ndropdown_position:    {dropdown_position}\nscroll_script :   {scroll_script}')

    reflector_choice = context.driver.find_element(By.CSS_SELECTOR, f'option[value="{reflector}"]')
    reflector_choice.click()


@when('I choose the Rotor 1 {rotor1}')
def step_impl(context, rotor1):
    dropdown = context.driver.find_element(By.CSS_SELECTOR, '#r1')
    dropdown.click()

    rotor_choice = context.driver.find_element(By.CSS_SELECTOR, f'#r1 option[value="{rotor1}"')
    rotor_choice.click()


@when('I choose the Rotor 2 {rotor2}')
def step_impl(context, rotor2):
    dropdown = context.driver.find_element(By.CSS_SELECTOR, '#r2')
    dropdown.click()

    rotor_choice = context.driver.find_element(By.CSS_SELECTOR, f'#r2 option[value="{rotor2}"]')
    rotor_choice.click()


@when('I choose the Rotor 3 {rotor3}')
def step_impl(context, rotor3):
    dropdown = context.driver.find_element(By.CSS_SELECTOR, '#r3')
    dropdown.click()

    rotor_choice = context.driver.find_element(By.CSS_SELECTOR, f'#r3 option[value="{rotor3}"')
    rotor_choice.click()


@when('I click submit')
def step_impl(context):
    element = context.driver.find_element(By.CSS_SELECTOR, 'input[type="submit"][id="submitBtn"]')
    element.click()


@then('The {encrypted_letter} letter should be displayed in the output box')
def step_impl(context, encrypted_letter):
    element = context.driver.find_element(By.CSS_SELECTOR, '.outputContainer').text
    #print('Assert is about to be done')
    assert element == encrypted_letter, f'Output Container does not contain {encrypted_letter}, but {element}'


@when('I uncheck the Plugboard checkbox')
def step_impl(context):
    element = context.driver.find_element(By.CSS_SELECTOR, 'input[id="deactivate_plugboard"]')

    if element.get_attribute('checked'):
        element.click()


@then('Plugboard is disappeared')
def step_impl(context):
    element = context.driver.find_element(By.CSS_SELECTOR, 'tr[id="plugboard-row"]')

    assert element.get_attribute('hidden')


@when('I set rotor 1 offset to {offset1}')
def step_impl(context, offset1):
    element = context.driver.find_element(By.CSS_SELECTOR, 'input[id="offset_r1"]')

    element.clear()
    element.send_keys(offset1)


@when('I set rotor 2 offset to {offset2}')
def step_impl(context, offset2):
    element = context.driver.find_element(By.CSS_SELECTOR, 'input[id="offset_r2"]')

    element.clear()
    element.send_keys(offset2)


@when('I set rotor 3 offset to {offset3}')
def step_impl(context, offset3):
    element = context.driver.find_element(By.CSS_SELECTOR, 'input[id="offset_r3"]')

    element.clear()
    element.send_keys(offset3)
