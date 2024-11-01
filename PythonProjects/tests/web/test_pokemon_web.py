import pytest
import requests

from loguru import logger
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pokemon_variables.variables import Vars_stage
from pokemon_variables.utils import wait_for


def test_positive_login(browser):
    """
    Test case POC-1
    """
		# определяем адрес страницы для теста и переходим на неё
    browser.get(url=Vars_stage.URL)
		
		# ищем по селектору инпут "Email", кликаем по нему и вводим значение email
    email_input = WebDriverWait(browser, timeout=10, poll_frequency=2).until(EC.element_to_be_clickable((By.CSS_SELECTOR, '[class*="f_email"]')))
    email_input.click()
    email_input.send_keys(Vars_stage.VALID['email']) # введи тут email своего тестового аккаунта на stage окружении
		
		# ищем по селектору инпут "Password", кликаем по нему и вводим значение пароля
    password_input = browser.find_element(by=By.CSS_SELECTOR, value='[class*="f_pass"]')
    password_input.click()
    password_input.send_keys(Vars_stage.VALID['password']) # введи тут пароль своего тестового аккаунта на stage окружении
		
		# ищем по селектору кнопку "Войти" и кликаем по ней
    button = browser.find_element(by=By.CSS_SELECTOR, value='[class*="send_auth"]')
    button.click()
    
    # ждем успешного входа и обновления страницы
    WebDriverWait(browser, timeout=10, poll_frequency=2).until(EC.url_to_be('https://pokemonbattle-stage.ru/'))
		
		# ищем элемент на странице, который содержит ID тренера
    trainer_id = browser.find_element(by=By.CLASS_NAME, value='header__id-texts')
		
		# сравниваем полученный ID из кода теста с ID вашего тестового тренера
    assert trainer_id.text.replace('\n', ': ') == 'ID: 858', 'Unexpected ID trainer' # введи тут ID своего тренера



CASES = [
    ('1', Vars_stage.INVALID['email'], Vars_stage.VALID['password'], ['Введите почту', '']),
    ('2', Vars_stage.VALID['email'], Vars_stage.INVALID['password'], ['', 'Неверные логин или пароль']),
    ('3', '', Vars_stage.VALID['password'], ['Введите почту', '']),
    ('4', Vars_stage.VALID['email'], '', ['', 'Введите пароль'])
]

@pytest.mark.parametrize('case, email, password, exp_alert', CASES)
def test_negative_login(case, email, password, exp_alert, browser):
    """
    POC-2. Negative cases for login
    """
    def check_alerts(browser):
        alerts = browser.find_elements(by=By.CSS_SELECTOR, value='[class*="auth__error"]')
        return [alert.text for alert in alerts]

    browser.get(url=Vars_stage.URL)

    email_input = WebDriverWait(browser, timeout=10, poll_frequency=2).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, '[class*="f_email"]')))
    email_input.click()
    email_input.send_keys(email)

    password_input = browser.find_element(by=By.CSS_SELECTOR, value='[class*="f_pass"]')
    password_input.click()
    password_input.send_keys(password)

    enter_button = browser.find_element(by=By.CSS_SELECTOR, value='[class*="send_auth"]')
    enter_button.click()

    assert wait_for(lambda: check_alerts(browser) == exp_alert)(), 'Unexpected alert message'


def test_check_api(browser, knockout):
    """
    POC-3. Check create pokemon by api request
    """
    browser.get(url=Vars_stage.URL)

    email = WebDriverWait(browser, timeout=10, poll_frequency=2).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, '[class*="f_email"]')))
    email.click()
    email.send_keys(Vars_stage.VALID['email'])

    password = browser.find_element(by=By.CSS_SELECTOR, value='[class*="f_pass"]')
    password.click()
    password.send_keys(Vars_stage.VALID['password'])

    enter = browser.find_element(by=By.CSS_SELECTOR, value='[class*="send_auth"]')
    enter.click()
    
    WebDriverWait(browser, timeout=5, poll_frequency=1).until(EC.url_to_be(f'{Vars_stage.URL}/'))
    
    browser.find_element(by=By.CLASS_NAME, value='header__id-texts').click()
    WebDriverWait(browser, timeout=5, poll_frequency=1).until(EC.url_to_be(f'{Vars_stage.URL}/trainer/{Vars_stage.TRAINER_ID}'))

    pokemon_count_before = browser.find_element(by=By.CSS_SELECTOR, value='[class="pokemons-info"] [class*="total-count"]')
    count_before = int(pokemon_count_before.text)

    body_create = {
        "name": "generate",
        "photo_id": 1
    }
    header = {'Content-Type':'application/json','trainer_token': Vars_stage.TRAINER_TOKEN}
    response_create = requests.post(url=f'{Vars_stage.API_URL}/pokemons', headers=header, json=body_create, timeout=3)
    assert response_create.status_code == 201, 'Unexpected response status_code'

    browser.refresh()

    assert WebDriverWait(browser, timeout=5, poll_frequency=1).until(EC.text_to_be_present_in_element(
        (By.CSS_SELECTOR, '[class="pokemons-info"] [class*="total-count"]'), f'{count_before+1}')), \
            'Unexpected pokemons count'
