import collections
import json
import sys

cols = (
    'name', 'type', 'category', 'power', 'accuracy', 'pp', 'priority',
    'highCriticalHitRatio', 'effect')

def to_percent(acc):
    if acc is None:
        return str(None)
    return str(int(acc * 100)) + '%'

moves = collections.defaultdict(list)
unaccounted_keys = set()
with open(sys.argv[1]) as f:
    for line in f:
        move = json.loads(line)
        unaccounted_keys.update(frozenset(move.keys()) - frozenset(cols))
        row = (
            move['name'],
            move['type'],
            move['category'],
            str(move['power']),
            to_percent(move['accuracy']),
            str(move['pp']),
            str(move.get('priority', 0)),
            str(move.get('highCriticalHitRatio', False)),
            json.dumps(move.get('effect', None)))

        if 'effects' in move or 'changes' in move:
            moves['unsupported'].append(row)
        else:
            moves['supported'].append(row)


for status, rows in sorted(moves.items()):
    print(f'# {status} moves ({len(rows)})\n')

    # header
    print('|'.join(col for col in cols))
    print('|'.join('---' for col in cols))
    for row in rows:
        print('|'.join(row))

    print('\n')

if unaccounted_keys:
    print('unaccounted_keys:', list(unaccounted_keys), file=sys.stderr)
