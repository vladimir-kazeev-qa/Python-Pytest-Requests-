from pokemon_variables.variables import *
import requests
import pytest

def test_status_code():
    response_get_pokemon = requests.get(url = f'{URL}/trainers')
    assert response_get_pokemon.status_code == 200

def test_part_of_response():
    response_get_pokemon_query = requests.get(url = f'{URL}/trainers',params = {'trainer_id' : TRAINER_ID})