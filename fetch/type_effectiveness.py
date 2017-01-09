from bs4 import BeautifulSoup
import collections
import json
import requests
import pokemon

effectiveness_to_number = {None: 1, '2': 2, '½': .5, '0': 0}

response = requests.get('http://pokemondb.net/type')
soup = BeautifulSoup(response.text, 'html.parser')
type_rows = soup.find(class_='type-table').tbody.find_all('tr')
for type_row in type_rows[:-3]: # ignore new type rows
    for type_cell in type_row.find_all('td')[:-3]: # ignore new type columns
        attack, _, defend = type_cell['title'].lower().split()[:3]
        effectiveness = effectiveness_to_number[type_cell.string]

        # generation 1 fixes
        if attack == 'ghost' and defend == 'psychic':
            # TODO Note that this only affected Lick as Confuse Ray and
            # Night Shade affected all Pokémon equally.
            effectiveness = 0
        if frozenset([attack, defend]) == frozenset(['bug', 'poison']):
            effectiveness = 2
        if attack == 'ice' and defend == 'fire':
            effectiveness = 1

        type_effectiveness = pokemon.TypeEffectiveness(attack, defend, effectiveness)
        print(json.dumps(type_effectiveness._asdict()))

