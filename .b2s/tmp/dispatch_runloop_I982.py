#!/usr/bin/env python3
import subprocess,sys,os,re,time
PY=sys.executable
ws='initiatives/I982-ISA'
max_iter=200
actions=0
stop_reason=None
modified_files=set()

def run(cmd):
    p=subprocess.run(cmd, capture_output=True, text=True)
    return p.returncode, p.stdout + p.stderr

print('Starting run loop for', ws)
for i in range(max_iter):
    print('\n--- ITER', i+1, '---')
    # get next step
    rc, out = run([PY, os.path.join('.b2s','scripts','b2s_cli.py'), 'dispatch-next', '--workspace-root', ws])
    print(out)
    if rc!=0:
        stop_reason=f'dispatch-next-error-{rc}'
        break
    if re.search(r"awaiting_human\s*:\s*(true|True)", out):
        stop_reason='human_gate_opened'
        break
    if re.search(r"selected_action\s*:\s*(null|None)", out):
        stop_reason='workflow_complete'
        break
    m=re.search(r"Ready to execute [`']?([\w\-]+)[`']?", out)
    if not m:
        # fallback: look for Execute `action-id`
        m=re.search(r"execute [`']?([\w\-]+)[`']?", out)
    if not m:
        stop_reason='no_action_found'
        break
    action_id=m.group(1)
    print('Action id:', action_id)
    # run-action
    rc, out = run([PY, os.path.join('.b2s','scripts','b2s_cli.py'), 'run-action', '--workspace-root', ws, '--action-id', action_id])
    print(out)
    if rc!=0:
        stop_reason=f'run-action-error-{rc}'
        break
    # validate-artifact
    rc, out = run([PY, os.path.join('.b2s','scripts','b2s_cli.py'), 'validate-artifact', '--workspace-root', ws, '--action-id', action_id])
    print(out)
    if rc!=0:
        stop_reason=f'validate-error-{rc}'
        break
    # update-state
    rc, out = run([PY, os.path.join('.b2s','scripts','b2s_cli.py'), 'update-state', '--workspace-root', ws])
    print(out)
    if rc!=0:
        stop_reason=f'update-state-error-{rc}'
        break
    actions += 1
    time.sleep(0.1)
else:
    stop_reason='max_iterations_reached'

# gather recent artifacts
now=time.time()
for root,dirs,files in os.walk(ws):
    for f in files:
        p=os.path.join(root,f)
        try:
            if now - os.path.getmtime(p) < 300:
                modified_files.add(p)
        except Exception:
            pass

print('\n==SUMMARY==')
print('actions_completed=', actions)
print('stop_reason=', stop_reason)
print('recently_modified_files_count=', len(modified_files))
for p in sorted(modified_files):
    print('ARTIFACT:', p)

sys.exit(0)
