import subprocess, json, time, yaml
from pathlib import Path
workspace='initiatives/I982-ISA'
state_path=Path(workspace)/'.b2s'/'state'/'workflow-state.json'
max_loops=100
loops=0
actions_completed=0
while loops<max_loops:
    loops+=1
    subprocess.run(['python','.b2s/scripts/b2s_cli.py','next-step','--workspace-root',workspace])
    time.sleep(0.1)
    if not state_path.exists():
        print('no state file; abort'); break
    ws=json.load(open(state_path))
    if ws.get('awaiting_human'):
        print('AWAITING_HUMAN')
        break
    next_action=ws.get('next_action') or ws.get('active_action')
    if not next_action:
        print('WORKFLOW_COMPLETE')
        break
    # collect inputs and validate
    subprocess.run(['python','.b2s/scripts/b2s_cli.py','collect-inputs','--workspace-root',workspace])
    subprocess.run(['python','.b2s/scripts/b2s_cli.py','validate-artifact','--workspace-root',workspace])
    time.sleep(0.1)
    val_path=Path(workspace)/'.b2s'/'tmp'/'current-validation.yaml'
    cv=None
    if val_path.exists():
        try:
            cv=yaml.safe_load(open(val_path))
        except Exception as e:
            print('error reading validation',e)
    ok = cv and cv.get('overall')=='pass'
    if ok:
        subprocess.run(['python','.b2s/scripts/b2s_cli.py','update-state','--workspace-root',workspace])
        actions_completed+=1
        continue
    # retry up to 3 times
    retries=0
    while retries<3 and not ok:
        retries+=1
        subprocess.run(['python','.b2s/scripts/b2s_cli.py','collect-inputs','--workspace-root',workspace])
        subprocess.run(['python','.b2s/scripts/b2s_cli.py','validate-artifact','--workspace-root',workspace])
        time.sleep(0.1)
        if val_path.exists():
            cv=yaml.safe_load(open(val_path))
            ok = cv and cv.get('overall')=='pass'
    if ok:
        subprocess.run(['python','.b2s/scripts/b2s_cli.py','update-state','--workspace-root',workspace])
        actions_completed+=1
        continue
    else:
        print('VALIDATION_FAILED')
        break
# final state read
if state_path.exists():
    ws=json.load(open(state_path))
    print('FINAL_STATE',ws.get('last_completed_action'),ws.get('next_action'), 'awaiting_human=', ws.get('awaiting_human'))
print('LOOPS',loops,'ACTIONS_COMPLETED',actions_completed)
