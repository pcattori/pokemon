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

