from bs4 import BeautifulSoup
import collections
import json
import requests

# TODO detect high critical hit ratio

def int_or_None(string):
    try:
        return int(string)
    except ValueError:
        return None

response = requests.get('http://pokemondb.net/move/generation/1')
soup = BeautifulSoup(response.text, 'html.parser')
moves_soup = soup.find(id='moves').tbody.find_all('tr')
for move_soup in moves_soup:
    move_details = move_soup.find_all('td')
    name = move_details[0].a.string.lower()
    type_ = move_details[1].a.string.lower()
    category = move_details[2].img['title'].lower()
    power = int_or_None(move_details[3].string.lower())
    accuracy = int_or_None(move_details[4].string.lower())
    pp = int_or_None(move_details[5].string.lower())
    move = {
        'name': name, 'type': type_, 'category': category, 'power': power,
        'accuracy': accuracy, 'pp': pp}
    print(json.dumps(move))
