from pokemon_variables.variables import Vars
import requests
import pytest

def test_status_code():
     response_get_pokemon = requests.get(url = f'{Vars.URL}/trainers')
     assert response_get_pokemon.status_code == 200

def test_part_of_response():
     response_get_pokemon_query = requests.get(url = f'{Vars.URL}/trainers',params = {'trainer_id' : Vars.TRAINER_ID})
     assert response_get_pokemon_query.json()["data"][0]["trainer_name"] == 'Ubuntutu'
