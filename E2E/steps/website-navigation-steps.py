import os
import time

from behave import *
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from webdriver_manager.firefox import GeckoDriverManager
from selenium.common.exceptions import NoAlertPresentException, NoSuchElementException, StaleElementReferenceException, TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait, Select


@given('The Enigma Website is opened')
def step_impl(context):
    # spin up driver
    options = Options()
    options.headless = True
    context.driver = webdriver.Firefox(options=options, service=Service(GeckoDriverManager().install()))
    if "CI" in os.environ.keys():
        context.driver.get("http://frontend")
        assert context.driver.title == "CC-Enigma"
    else:
        context.driver.get("http://localhost")
        assert context.driver.title == "CC-Enigma"



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


@then('The letter {letter} should be highlighted on the virtual keyboard')
def step_impl(context, letter):
    key = context.driver.find_element(By.NAME, f'k_{letter}')

    background_color = key.value_of_css_property("background-color")
    GREEN = 'rgb(0, 128, 0)'
    assert background_color == GREEN, f"The Key {letter} didn't light up"


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


@then('The plugboard box should be empty')
def step_impl(context):
    text = context.driver.find_element(By.CSS_SELECTOR, '.plugboardContainer').text
    assert text == '', 'Plugboard Container should be empty, but is not'


@when('I press the {letter} key {limit} times on the keyboard')
def step_impl(context, letter, limit):
    key = context.driver.find_element(By.NAME, f"k_{letter}")
    for i in range(int(limit) + 1):
        key.click()


@then('I see only {limit} characters in the {box} box')
def step_impl(context, limit, box):
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
    element = context.driver.find_element(By.NAME, f"l_{lamp}")
    background_color = element.value_of_css_property("background-color")
    YELLOW = 'rgb(255, 255, 0)'
    assert background_color == YELLOW, f"The lamp {lamp} didn't light up"


@when('I click setting symbol')
def step_impl(context):
    ignored_exceptions = [NoSuchElementException, StaleElementReferenceException]
    time.sleep(3)
    try:
        element = WebDriverWait(context.driver, 5, ignored_exceptions=ignored_exceptions) \
        .until(EC.presence_of_element_located((By.ID, "showMenuBtn")))
        element.click()

    except Exception as e:
        print(e)


@when('I choose the variant {variant}')
def step_impl(context, variant):
    time.sleep(2)
    dropdown = context.driver.find_element(By.CSS_SELECTOR, '#variants')
    dropdown.click()

    variant_choice = context.driver.find_element(By.CSS_SELECTOR, f'option[value="{variant}"]')
    variant_choice.click()


@when('I choose the Reflector {reflector}')
def step_impl(context, reflector):
    dropdown = context.driver.find_element(By.CSS_SELECTOR, 'select[id="reflector"]')
    # Get the position of the element
    dropdown_position = dropdown.location
    # Scroll to the position of the element
    scroll_script = f"window.scrollTo({dropdown_position['x']}, {dropdown_position['y']})"
    context.driver.execute_script(scroll_script)
    try:
        wait = WebDriverWait(context.driver, 5)
        wait.until(EC.visibility_of(dropdown)).click()
    except Exception as e:
        print(f'dropdown.location :     {dropdown.location}\ndropdown_position:    {dropdown_position}\n scroll_script :   {scroll_script}')
        print(f' Is dropdown displayed:     {dropdown.is_displayed()}')
        # print(e)
        raise RuntimeError("Unable to process input") from e

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
    assert element == encrypted_letter, f'Output Container does not contain {encrypted_letter}, but {element}'


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


# Scenarios in session.feature
@when('I press the reset button')
def step_impl(context):
    element = context.driver.find_element(By.CSS_SELECTOR, 'button[id="resetBtn"]')
    element.click()


@when('I close the Alert')
def step_impl(context):
    try:
        WebDriverWait(context.driver, 3).until(EC.alert_is_present())
        alert = context.driver.switch_to.alert

        alert.accept()
    except (NoAlertPresentException, TimeoutException):
        pass


@then('Variant is set to {default_variant}')
def step_impl(context, default_variant):
    select_element = context.driver.find_element(By.ID, 'variants')
    select = Select(select_element)
    selected_option_text = select.first_selected_option.text
    assert selected_option_text == default_variant, f'{default_variant} is not selected but {selected_option_text}'


@then('Reflector is set to {default_reflector}')
def step_impl(context, default_reflector):
    select_element = context.driver.find_element(By.ID, 'reflector')
    select = Select(select_element)
    print(select.first_selected_option.text)
    selected_option_text = select.first_selected_option.text

    assert selected_option_text == default_reflector, f'{default_reflector} is not selected but {selected_option_text}'


@then('Rotor 1 is set to {default_rotor1}')
def step_impl(context, default_rotor1):
    select_element = context.driver.find_element(By.ID, 'r1')
    select = Select(select_element)
    print(select.first_selected_option.text)
    selected_option_text = select.first_selected_option.text

    assert selected_option_text == default_rotor1, f'{default_rotor1} is not selected but {selected_option_text}'


@then('Rotor 2 is set to {default_rotor2}')
def step_impl(context, default_rotor2):
    select_element = context.driver.find_element(By.ID, 'r2')
    select = Select(select_element)
    print(select.first_selected_option.text)
    selected_option_text = select.first_selected_option.text

    assert selected_option_text == default_rotor2, f'{default_rotor2} is not selected but {selected_option_text}'


@then('Rotor 3 is set to {default_rotor3}')
def step_impl(context, default_rotor3):
    select_element = context.driver.find_element(By.ID, 'r3')
    select = Select(select_element)
    print(select.first_selected_option.text)
    selected_option_text = select.first_selected_option.text

    assert selected_option_text == default_rotor3, f'{default_rotor3} is not selected but {selected_option_text}'


@when('I refresh page and close Alert')
def step_impl(context):
    context.driver.execute_script('save().then(uuid => {setCookie(uuid)})')
    time.sleep(3)
    context.driver.refresh()


@when('I set rotor 1 ring setting to {ring1}')
def step_impl(context, ring1):
    add1 = context.driver.find_element(By.CSS_SELECTOR, 'button[onclick="changeRingsetting(\'ring_r1\', 1)"]')
    if int(ring1) < 26:

        for i in range(int(ring1)):
            add1.click()


@when('I set rotor 2 ring setting to {ring2}')
def step_impl(context, ring2):
    add1 = context.driver.find_element(By.CSS_SELECTOR, 'button[onclick="changeRingsetting(\'ring_r2\', 1)"]')

    if int(ring2) < 26:
        for i in range(int(ring2)):
            add1.click()


@when('I set rotor 3 ring setting to {ring3}')
def step_impl(context, ring3):
    add1 = context.driver.find_element(By.CSS_SELECTOR, 'button[onclick="changeRingsetting(\'ring_r3\', 1)"]')

    if int(ring3) < 26:
        for i in range(int(ring3)):
            add1.click()
