class Vars:
 URL = 'https://api.pokemonbattle.ru/v2'
 TOKEN = '8bf'  # Здесь должен быть ваш токен !!!
 HADER = {'Content-Type':'application/json', 'trainer_token':TOKEN}
 TRAINER_ID = '7263'

class Vars_stage:
    URL ='https://pokemonbattle-stage.ru'
    API_URL = 'https://api.pokemonbattle-stage.ru/v2'
    VALID = {
        'email': 'email@gmail.com', # Ваша валидная почта
        'password': 'Password' # Ваш валидный пароль
    }
    INVALID = {
        'email': 'emailgmail.com',  # Ваша невалидная почта
        'password': 'Passwor'  # Ваш невалидный пароль
    }
    TRAINER_ID = 858  # Ваш Id тренера
    TRAINER_TOKEN = '8bf' # Здесь должен быть ваш токен !!!