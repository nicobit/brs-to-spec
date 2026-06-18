import json, subprocess, sys, os

ws = 'initiatives/I013-NEXT13'
cli = os.path.join('.b2s', 'scripts', 'b2s_cli.py')
max_iter = 50
prev_updated = None

for i in range(max_iter):
    subprocess.run([sys.executable, cli, 'next-step', '--workspace-root', ws], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    state_path = os.path.join(ws, '.b2s', 'state', 'workflow-state.json')
    try:
        with open(state_path, 'r', encoding='utf-8') as f:
            s = json.load(f)
    except Exception as e:
        print('ERROR reading state:', e)
        sys.exit(1)
    updated = s.get('last_updated')
    print(f"ITER {i+1}: active_action={s.get('active_action')} next_action={s.get('next_action')} awaiting_human={s.get('awaiting_human')} last_updated={updated}")
    if s.get('awaiting_human'):
        print('Awaiting human approval; stopping.')
        break
    if prev_updated == updated:
        print('No state change detected; stopping.')
        break
    prev_updated = updated

print('DISPATCH-ALL COMPLETE')
