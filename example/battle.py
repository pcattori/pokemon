import pokemon
import pokemon.battle.battle as pokebattle

if __name__ == '__main__':
    red_team = [
        pokemon.pokemon('charmander', level=3, moves=[
            'scratch', 'growl', 'ember', 'leer'])]
    blue_team = [
        pokemon.pokemon('squirtle', level=3, moves=[
            'tackle', 'tail whip', 'bubble', 'water gun'])]
    teams = (red_team, blue_team)

    battle = pokebattle.Battle(teams)

    while not battle.ended:
        for team in battle.teams:
            print(f'{team.fighter.name} has {team.fighter.hp} hp')
        move_choices = []
        for i, team in enumerate(battle.teams):
            other_team = teams[(i + 1) % 2]
            print(f'What will {team.fighter.name} do?')
            print(*list(team.fighter.moves.keys()), sep='\n')
            move_name = input('>> ')
            move_choices.append(pokebattle.MoveChoice(
                fighter=team.fighter, move_name=move_name))
        turn_summary = list(battle.next_turn(move_choices))
        print(*turn_summary, sep='\n')

