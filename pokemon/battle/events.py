import collections

UnableToAttack = collections.namedtuple('UnableToAttack', [
    'team_index', 'reason'])
PowerPointDecrement = collections.namedtuple('PowerPointDecrement', [
    'team_index', 'move_name'])
MoveMiss = collections.namedtuple('MoveMiss', ['team_index', 'move_name'])
MoveHit = collections.namedtuple('MoveHit', [
    'team_index', 'move_name', 'opponent_team_index', 'damage_result'])
StatStageChange = collections.namedtuple('StatStageChange', [
    'team_index', 'stat', 'stage_delta', 'new_stage'])
AddStatusCondition = collections.namedtuple('AddStatusCondition', [
    'team_index', 'status_condition', 'turns'])
RemoveStatusCondition = collections.namedtuple('RemoveStatusCondition', [
    'team_index', 'status_condition'])
StatusConditionDamage = collections.namedtuple('StatusConditionDamage', [
    'team_index', 'status_condition', 'damage'])
StatusConditionRecover = collections.namedtuple('StatusConditionRecover', [
    'team_index', 'status_condition', 'hp_recovered'])
Fainted = collections.namedtuple('Fainted', ['team_index'])

unable_messages = {
    'paralysis': 'is paralyzed',
    'freeze': 'is frozen solid',
    'sleep': 'is fast asleep',
    'flinch': 'flinched',
    'bound': 'is bound',
    'confused': None
}

effectivness_messages = {
    0: "It has no effect",
    1: None,
    2: "It's super effective!",
    4: "It's super effective!",
    0.5: "It's not very effective...",
    0.25: "It's not very effective..."
}

stage_change_messages = {
    0: None, # TODO 'It failed!' if this was a status move
    1: 'rose',
    -1: 'fell',
    2: 'greatly rose',
    -2: 'greatly fell'
}

add_status_messages = {
    'burn': 'was burned',
    'freeze': 'froze',
    'paralyzed': 'was paralyzed',
    'poison': 'was poisoned',
    'sleep': 'fell asleep',
    'bound': 'was bound',
    'confusion': 'became confused',
    'flinch': None,
    'leech seed': 'was seeded'
}

remove_status_messages = {
    'burn': 'is no longer burned',
    'freeze': 'thawed out',
    'paralyzed': 'is no longer paralyzed',
    'poison': 'was cured',
    'sleep': 'woke up',
    'bound': 'broke free',
    'confusion': 'is no longer confused',
    'flinch': None,
    'leech seed': None
}

def commentate_event(teams, event):
    fighter = teams[event.team_index].fighter

    if isinstance(event, UnableToAttack):
        unable_message = unable_messages[event.reason]
        if unable_message:
            yield f"{fighter.name} {unable_message}! It can't move!"

    elif isinstance(event, PowerPointDecrement):
        yield f'{fighter.name} used {event.move_name}!'

    elif isinstance(event, MoveMiss):
        yield f'{event.move_name} missed!'

    elif isinstance(event, MoveHit):
        opponent = teams[(event.team_index + 1) % 2].fighter
        dmg = event.damage_result
        if dmg.critical_hit:
            yield 'Critical hit!'
        effectivness_message = effectivness_messages[dmg.effectiveness]
        if effectivness_message:
            yield effectivness_message
        yield f'{opponent.name} took {dmg.damage} damage'

    elif isinstance(event, StatStageChange):
        stage_change_message = stage_change_messages[event.stage_delta]
        if stage_change_message:
            yield f"{fighter.name}'s {event.stat} {stage_change_message}"

    elif isinstance(event, AddStatusCondition):
        add_status_msg = add_status_messages[event.status_condition]
        if add_status_msg:
            yield f'{fighter.name} {add_status_msg}!'

    elif isinstance(event, RemoveStatusCondition):
        remove_status_msg = remove_status_messages[event.status_condition]
        if remove_status_msg:
            yield f'{fighter.name} {remove_status_msg}!'

    elif isinstance(event, StatusConditionDamage):
        yield f'{fighter.name} was hurt by its {event.status_condition}'

    elif isinstance(event, StatusConditionRecover):
        yield f'{fighter.name} sapped energy'

    elif isinstance(event, Fainted):
        yield f'{fighter.name} fainted!'

    else:
        raise ValueError
