import pokemon

blue = pokemon.Team(name='blue', [
    pokemon.pokemon('pidgeot', level=61, moves=[
        'wing attack', 'mirror move', 'sky attack', 'whirlwind']),
    pokemon.pokemon('alakazam', level=59, moves=[
        'psybeam', 'psychic', 'reflect', 'recover']),
    pokemon.pokemon('rhydon', level=61, moves=[
        'leer', 'tail whip', 'fury attack', 'horn drill']),
    pokemon.pokemon('exeggutor', level=63, moves=[
        'hypnosis', 'barrage', 'stomp']),
    pokemon.pokemon('arcanine', level=61, moves=[
        'roar', 'leer', 'ember', 'take down']),
    pokemon.pokemon('blastoise', level=65, moves=[
        'hydro pump', 'blizzard', 'bite', 'withdraw'])
])

red = pokemon.Team(name='red', [
    pokemon.pokemon('zapdos', nickname='AA-j', level=81, moves=[
        'thundershock', 'drill peck', 'take down', 'thunder']),
    pokemon.pokemon('lapras', nickname='AIIIIIIRRR',  level=31, moves=[
        'confuse ray', 'mist', 'surf', 'strength']),
    pokemon.pokemon('venomoth', nickname='AATTVVV', level=39, moves=[
        'disable', 'poison powder', 'leech life', 'stun spore']),
    pokemon.pokemon('pidgeot', level=69, nickname='aaabaaajss', moves=[
        'mirror move', 'sand attack', 'quick attack', 'sky attack']),
    pokemon.pokemon('nidoking', level=54, nickname='AAAAAAAAAA', moves=[
        'surf', 'poison sting', 'strength', 'fury attack']),
    pokemon.pokemon('omastar', level=52, moves=[
        'hydro pump', 'withdraw', 'surf', 'horn attack'])
])

# TODO implement copy/deepcopy
battle = pokemon.Battle([red, blue]) # mutates

def simulate_battle(teams):
    teams = copy.deepcopy(teams)
    return Battle(teams)

simulated_battle = pokemon.simulate_battle([red, blue]) # does not mutate

while not battle.ended:
