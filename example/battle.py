import pokemon
from pokemon.battle.battle import Battle, MoveChoice
from pokemon.battle.events import commentate_event
import time

if __name__ == '__main__':
    red_team = [
        pokemon.pokemon('charmander', level=3, moves=[
            'scratch', 'growl', 'ember', 'leer'])]
    blue_team = [
        pokemon.pokemon('squirtle', level=3, moves=[
            'tackle', 'tail whip', 'bubble', 'water gun'])]
    teams = (red_team, blue_team)

    battle = Battle(teams)

    while not battle.ended:
        for team in battle.teams:
            print(f'{team.fighter.name} has {team.fighter.hp} hp')
        move_choices = []
        for i, team in enumerate(battle.teams):
            other_team = teams[(i + 1) % 2]
            print(f'What will {team.fighter.name} do?')
            print(*list(team.fighter.moves.keys()), sep='\n')
            move_name = input('>> ')
            move_choices.append(MoveChoice(
                fighter=team.fighter, move_name=move_name))
        turn_summary = list(battle.next_turn(move_choices))
        for event in turn_summary:
            print(*(commentate_event(battle.teams, event)), sep='\n')
            input('')

