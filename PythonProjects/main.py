import requests
from pokemon_variables.variables import *

body_create_pokemon = {
    "name": "generate",
    "photo_id": -1
}

# Запрос на создание покемона
response_create_pokemon = requests.post(url = f'{URL}/pokemons', headers = HADER, json = body_create_pokemon)
print(response_create_pokemon.text)
POKEMON_ID =  response_create_pokemon.json()['id']

body_rename_pokemon = {
    "pokemon_id": POKEMON_ID,
    "name": "generate",
    "photo_id": -1
}

#Запрос на изменение имени покемона "Знаю, что фото тоже поменяется. Просто в ТЗ указан метод PUT, а не PATCH"
response_rename_pokemon = requests.put(url = f'{URL}/pokemons', headers = HADER, json = body_rename_pokemon)
print(response_rename_pokemon.text)

body_addPokeball_pokemon = {
    "pokemon_id": POKEMON_ID
}

#Запрос на добавление покемона в покеболл
response_addPokeball_pokemon = requests.post(url = f'{URL}/trainers/add_pokeball', headers = HADER, json = body_addPokeball_pokemon)
print(response_addPokeball_pokemon.text)