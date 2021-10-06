from selenium import webdriver
import pytest
from settings import *


@pytest.fixture(autouse=True)
def web_browser():
    options = webdriver.ChromeOptions()
    options.headless = True

    browser = webdriver.Chrome(executable_path=link_chromedriver, options=options)
    # browser.binary_location = link_chromedriver

    # Применяем неявное ожидание 10 секунд для всех элементов
    browser.implicitly_wait(10)
    browser.get(link_login)
    browser.find_element_by_id('email').send_keys(valid_email)
    browser.find_element_by_id('pass').send_keys(valid_password)
    browser.find_element_by_css_selector('.btn.btn-success').click()
    browser.find_element_by_class_name('navbar-toggler').click()
    browser.find_element_by_class_name('nav-link').click()

    yield browser
    browser.find_element_by_css_selector('.btn.btn-outline-secondary').click()
    browser.quit()
