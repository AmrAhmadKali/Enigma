import time


def after_scenario(context, scenario):
    context.driver.quit()


def after_step(context, step):
    time.sleep(2)
