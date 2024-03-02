import requests

class PokemonInfo:
    def __init__(self) -> None:
        self.URL = "https://pokeapi.co/api/v2/"

    def get_pokemon_info(self, pk_name: str) -> dict:
        try:
            response = requests.get(f"{self.URL}pokemon/{pk_name}")
            if response.status_code == 200:
                pokemon_data = response.json()
                types = [type_data['type']['name'] for type_data in pokemon_data['types']]
                abilities = [ability_data['ability']['name'] for ability_data in pokemon_data['abilities']]
                sprite = pokemon_data['sprites']['front_default']

                pokemon_info = {
                    'name': pokemon_data['name'],
                    'id': pokemon_data['id'],
                    'sprite': sprite,
                    'types': types,
                    'abilities': abilities,
                    'weight': pokemon_data['weight']
                }
                return pokemon_info
            else:
                return {"error": "Pokemon not found"}
        except Exception as e:
            return {"error": str(e)}

# Ejemplo de uso
poke_info = PokemonInfo()
pokemon_data = poke_info.get_pokemon_info("snivy")
print(pokemon_data)