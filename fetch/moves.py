from bs4 import BeautifulSoup
import json
import requests
import itertools

# TODO detect high critical hit ratio: http://bulbapedia.bulbagarden.net/wiki/Category:Moves_with_a_high_critical-hit_ratio
# TODO priority moves: http://bulbapedia.bulbagarden.net/wiki/Priority#Generation_I

def int_or_None(string):
    if string == '—':
        return None
    return int(string)

def probability_or_None(string):
    if string in {'—', '∞'}:
        return None
    else:
        return int(string) / 100

pokemondb_url = 'http://pokemondb.net'
response = requests.get(pokemondb_url + '/move/generation/1')
soup = BeautifulSoup(response.content, 'html.parser')
move_rows = soup.find('table', id='moves').tbody.find_all('tr', recursive=False)
for move_row in move_rows:
    name = move_row.td.a.string.lower()
    response = requests.get(pokemondb_url + move_row.td.a['href'])
    move_soup = BeautifulSoup(response.content, 'html.parser')
    move_data = move_soup.find('h2', text='Move data').find_next('table')
    move_data_rows = move_data.tbody.find_all('tr', recursive=False)

    move = {'name': name}
    details = ('type', 'category', 'power', 'accuracy', 'pp')
    for detail, move_data_row in zip(details, move_data_rows):
        assert(move_data_row.th.string.lower() == detail)
        move[detail] = move_data_row.td.get_text().split()[0].lower()

    # http://bulbapedia.bulbagarden.net/wiki/Priority#Generation_I
    priority = 0
    if name == 'quick attack':
        priority = +1
    elif name == 'counter':
        priority = -1
    move['priority'] = priority

    move['power'] = int_or_None(move['power'])
    move['accuracy'] = probability_or_None(move['accuracy'])
    move['pp'] = int_or_None(move['pp'])

    effects = move_soup.find('h2', id='move-effects')
    changes = effects.find_next('h3', text='Changes')

    # move['clean-effects'] = []
    # for effect in effects.find_next_siblings():
    #     if effect.name != 'p':
    #         break
    #     print(effect)
    #     assert('Z-Move' not in effect.get_text())
    #     move['clean-effects'].append(effect.get_text())

    move['effects'] = [
        effect.get_text().split('Z-Move')[0].strip()
        for effect in itertools.takewhile(
            lambda tag: tag.name == 'p',
            effects.find_next_siblings())]

    if changes:
        move['changes'] = [
            change.get_text()
            for change in itertools.takewhile(
                lambda tag: tag.name == 'p',
                changes.find_next_siblings())]

    print(json.dumps(move, ensure_ascii=False))

