"""
Configuration test
"""
import pytest
import requests

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from pokemon_variables.variables import Vars_stage


@pytest.fixture(scope="function")
def browser():
    """
    Main fixture
    """
    chrome_options = Options()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("start-maximized") # открываем на полный экран
    chrome_options.add_argument("--disable-infobars") # отключаем инфо сообщения
    chrome_options.add_argument("--disable-extensions") # отключаем расширения
    chrome_options.add_argument("--disable-gpu") # приложение только для ОС Windows
    chrome_options.add_argument("--disable-dev-shm-usage") 
    chrome_options.add_argument("--disable-search-engine-choice-screen") # отключаем выбор движка для поиска
    chrome_options.add_argument("--headless") # спец. режим "без браузера"

    service = Service()
    driver = webdriver.Chrome(service=service, options=chrome_options)
    yield driver
    driver.quit()


@pytest.fixture(scope="function")
def knockout():
    """
    Knockout all pokemons
    """
    header = {'Content-Type':'application/json','trainer_token': Vars_stage.TRAINER_TOKEN}
    pokemons = requests.get(url=f'{Vars_stage.API_URL}/pokemons', params={"trainer_id": Vars_stage.TRAINER_ID},
                            headers=header, timeout=3)
    if 'data' in pokemons.json():
        for pokemon in pokemons.json()['data']:
            if pokemon['status'] != 0:
                requests.post(url=f'{Vars_stage.API_URL}/pokemons/knockout', headers=header,
                              json={"pokemon_id": pokemon['id']}, timeout=3)
