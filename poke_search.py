import requests

class PokemonInfo:
    def __init__(self) -> None:
        self.URL = "https://pokeapi.co/api/v2/"

    def _get_type_data(self,type_name:str)->dict:
        try:
            response = requests.get(f"{self.URL}type/{type_name}")
            if response.status_code == 200:
                type_data = response.json()
                damage_relations = type_data['damage_relations']
                double_damage = [damage['name'] for damage in damage_relations['double_damage_from']] 
                no_damage = [damage['name'] for damage in damage_relations['no_damage_from']]
                return {
                    "weak": double_damage,
                    "no_dmg": no_damage
                }
        except Exception as e:
            return {"error": str(e)}

    def get_pokemon_info(self, pk_name: str) -> dict:
        try:
            response = requests.get(f"{self.URL}pokemon/{pk_name}")
            if response.status_code == 200:
                pokemon_data = response.json()
                types = [type_data['type']['name'] for type_data in pokemon_data['types']]
                abilities = [ability_data['ability']['name'] for ability_data in pokemon_data['abilities']]
                sprite = pokemon_data['sprites']['front_default']

                types_data = [self._get_type_data(type_name) for type_name in types]

                # Combinar la información de tipo de daño de todos los tipos
                weak_types = set()
                no_damage_types = set()
                for data in types_data:
                    if data:
                        weak_types.update(data.get('weak', []))
                        no_damage_types.update(data.get('no_dmg', []))

                pokemon_info = {
                    'name': pokemon_data['name'],
                    'id': pokemon_data['id'],
                    'sprite': sprite,
                    'types': types,
                    'abilities': abilities,
                    'weight': pokemon_data['weight'],
                    'weaknesses': list(weak_types),
                    'inmune_to': list(no_damage_types)
                }
                return pokemon_info
            else:
                return {"error": "Pokemon not found"}
        except Exception as e:
            return {"error": str(e)}

# Ejemplo de uso
#poke_info = PokemonInfo()
#pokemon_data = poke_info.get_pokemon_info("tyranitar")
#print(pokemon_data)
#type_data = poke_info.get_type_data("electric")
#print(type_data)