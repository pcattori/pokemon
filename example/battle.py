import pokemon
import pokemon.battle

if __name__ == '__main__':
    red_team = pokemon.battle.Team([
        pokemon.Pokemon(pokemon.species('charmander'), level=3, moves=[
            pokemon.move(move) for move in (
                'scratch', 'growl', 'ember', 'leer')])])
    blue_team = pokemon.battle.Team([
        pokemon.Pokemon(pokemon.species('squirtle'), level=3, moves=[
            pokemon.move(move) for move in (
                'tackle', 'tail whip', 'bubble', 'water gun')])])
    teams = (red_team, blue_team)

    while all(not team.blacked_out() for team in teams):
        for team in teams:
            print(f'{team.fighter.name} has {team.fighter.hp} hp')
        fight_actions = []
        for i, team in enumerate(teams):
            other_team = teams[(i + 1) % 2]
            print(f'What will {team.fighter.name} do?')
            print(*list(team.fighter.moves.keys()), sep='\n')
            move_name = input('>> ')
            fight_actions.append(pokemon.battle.FightAction(
                pokemon=team.fighter, move=move_name, target=other_team.fighter))
        for result in pokemon.battle.fight(fight_actions):
            print(f'{result.action.pokemon.name} used {result.action.move}!')
            if result.miss:
                print(f'{result.action.move} missed!')
                continue
            if result.damage.critical_hit:
                print('Critical hit!')
            print(f'{result.damage.effectiveness}x effective')
            if result.ko:
                print(f'{result.action.target.name} fainted!')
            else:
                print(f'{result.action.target.name} now has {result.action.target.hp} hp')
        print('\n==================\n')
