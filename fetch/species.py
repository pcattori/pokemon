from bs4 import BeautifulSoup
import json
import requests

bulbapedia_url = 'http://bulbapedia.bulbagarden.net'

# grab Gen-I species links
response = requests.get(
    bulbapedia_url + '/wiki/Category:Generation_I_Pok%C3%A9mon')
soup = BeautifulSoup(response.content, 'html.parser')
species_links = [
    species.a['href']
    for group in soup.find_all('div', class_='mw-category-group')
    for species in group.find_all('li')]

# visit Gen-I species links, grab (pokedex number, name, types, base stats)
for species_link in species_links:
    response = requests.get(
        bulbapedia_url + species_link)
    soup = BeautifulSoup(response.text, 'html.parser')

    # number and name
    info_rows = soup.find('table', class_='roundy').find_all('tr', recursive=False)
    name_number = info_rows[0].td.table.find('tr')
    name = name_number.td.table.tr.find('td').big.big.b.string.lower()
    number = int(name_number.th.big.big.a.span.string[1:]) # number is in #000 style

    # types
    types = [
        cell.a.span.b.string
        for cell in info_rows[1].td.table.tr.td.table.tr.find_all('td')]
    types = [t.lower() for t in types if t != 'Unknown']

    # base stats
    base_stats_soup = soup.find(id='Base_stats').find_next('table').find_all(
        'tr', recursive=False)
    base_stats_rows = [
        cell.td.table.tr.find_all('th', recursive=False)
        for cell in base_stats_soup[2:8]]
    base_stats = {
        row[0].a.span.string.lower(): int(row[1].string.strip())
        for row in base_stats_rows}
    # Gen-I special
    special = int(base_stats_soup[-1].td.ul.find_all('li', recursive=False)[-1].b.string)
    base_stats['special'] = special
    del base_stats['sp.atk']
    del base_stats['sp.def']

    species = {
        'national_pokedex_number': number,
        'name': name,
        'types': types,
        'baseStats': base_stats}
    print(json.dumps(species, ensure_ascii=False), flush=True)


