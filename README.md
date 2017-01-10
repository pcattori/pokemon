# pokemon

Python Pokémon API : 1st Generation Pokédex and Battle Simulation


![pokemon-starters](assets/pokemon-starters.png)

:zap: Batteries included: Comes bundled with JSON data for 1st Generation
- [Pokémon Species](pokemon/data/species.json)
- [Moves](pokemon/data/moves.json)
- [Type Chart](pokemon/data/type_effectiveness.json)

## Install

```sh
$ git clone https://github.com/pcattori/pokemon.git
$ cd pokemon
$ pip install -e . # .[fetch] for scraping capabilities
```

If you don't want to rely on the built-in JSON data or want data scraping
capabilities, do `pip install -e .[fetch]` instead.

## Pokédex

```python
>>> import pokemon
>>> charmander = pokemon.Pokemon(pokemon.species('charmander'), level=3, moves=[
    pokemon.move(move) for move in ('scratch', 'growl', 'ember', 'leer')])
>>> charmander.species
Species(national_pokedex_number=4, name='charmander', types=['fire'], base_stats=Stats(hp=39, attack=52, defense=43, special=50, speed=65))
>>> charmander.level
3
>>> charmander.ivs # generated as if its a wild pokemon, but can be specified via `ivs` kwarg in pokemon.Pokemon
Stats(hp=0, attack=4, defense=4, special=12, speed=10)
>>> charmander.evs # zeroed out by default, but can be specified via `evs` kwarg in pokemon.Pokemon
Stats(hp=0, attack=0, defense=0, special=0, speed=0)
>>> charmander.stats # dynamically calculated from base stats, ivs, and evs
Stats(hp=15, attack=8, defense=7, special=8, speed=9)
>>> charmander.moves
{'scratch': Move(name='scratch', type_='normal', category='physical', power=40, accuracy=100, pp=35), 'growl': Move(name='growl', type_='normal', category='status', power=None, accuracy=100, pp=40), 'ember': Move(name='ember', type_='fire', category='special', power=40, accuracy=100, pp=25), 'leer': Move(name='leer', type_='normal', category='status', power=None, accuracy=100, pp=30)}
```

## Battle Simulation

```python
>>> import pokemon
>>> charmander = pokemon.Pokemon(pokemon.species('charmander'), level=3, moves=[
    pokemon.move(move) for move in ('scratch', 'growl', 'ember', 'leer')])
>>> squirtle = pokemon.Pokemon(pokemon.species('squirtle'), level=3, moves=[
    pokemon.move(move) for move in ('tackle', 'tail whip', 'bubble', 'water gun')])
>>> pokemon.formulas.damage(squirtle, squirtle.moves['bubble'], charmander)
Damage(damage=27, luck=0.9927695832242377, critical_hit=True, effectiveness=2) # non-deterministic, so your results may vary
```
