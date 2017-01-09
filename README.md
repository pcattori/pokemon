# pokemon

Python Pokémon API : 1st Generation Pokédex and Battle Simulation

![pokemon-starters](assets/pokemon-starters.png)

## Pokédex

```python
import pokemon
moves = ('scratch', 'growl', 'ember', 'leer')
charmander = pokemon.Pokemon(pokemon.species('charmander'), level=3, moves=[
    pokemon.move(move) for move in moves])
>>> charmander.species
Species(national_pokedex_number=4, name='charmander', types=['fire'], base_stats=Stats(hp=39, attack=52, defense=43, special=50, speed=65))
>>> charmander.level
3
>>> charmander.ivs
Stats(hp=0, attack=4, defense=4, special=12, speed=10)
>>> charmander.evs
Stats(hp=0, attack=0, defense=0, special=0, speed=0)
>>> charmander.stats
Stats(hp=15, attack=8, defense=7, special=8, speed=9)
>>> charmander.moves
[Move(name='scratch', type_='normal', category='physical', power=40, accuracy=100, pp=35), Move(name='growl', type_='normal', category='status', power=None, accuracy=100, pp=40), Move(name='ember', type_='fire', category='special', power=40, accuracy=100, pp=25), Move(name='leer', type_='normal', category='status', power=None, accuracy=100, pp=30)]
```

## Battle Simulation

NOT YET IMPLEMENTED
