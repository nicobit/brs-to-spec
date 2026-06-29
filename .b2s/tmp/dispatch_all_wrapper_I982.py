#!/usr/bin/env python3
import subprocess, sys, os, time
workspace='initiatives/I982-ISA'
cmd=[sys.executable, os.path.join('.b2s','scripts','b2s_cli.py'), 'dispatch-next', '--workspace-root', workspace]

actions=0
max_iter=200
stop_reason=None
print('Starting dispatch-next loop for', workspace)
for i in range(max_iter):
    print('\n--- iteration', i+1, '---')
    p=subprocess.run(cmd, capture_output=True, text=True)
    out = p.stdout + p.stderr
    print(out)
    # Detect gate open
    if 'awaiting_human' in out and ('true' in out or 'True' in out):
        stop_reason='human_gate_opened'
        print('Detected human gate opened')
        break
    # Detect workflow complete
    if 'selected_action' in out and ('null' in out or 'None' in out):
        stop_reason='workflow_complete'
        print('Detected workflow complete (selected_action null)')
        break
    if p.returncode!=0:
        stop_reason='cli_error_returncode_{}'.format(p.returncode)
        print('CLI returned non-zero exit code:', p.returncode)
        break
    # Heuristic: count actions when output includes 'current_item' or 'selected_action'
    if 'current_item' in out or 'selected_action' in out or 'Action completed' in out:
        actions += 1
    # short pause to avoid busy loop
    time.sleep(0.1)
else:
    stop_reason='max_iterations_reached'
    print('Reached max iterations')

# Collect recently modified files under the workspace
modified_files=[]
now=time.time()
for root,dirs,files in os.walk(workspace):
    for f in files:
        path=os.path.join(root,f)
        try:
            m=os.path.getmtime(path)
        except Exception:
            continue
        if now - m < 300:  # changed within last 5 minutes
            modified_files.append(path)

print('\n==SUMMARY==')
print('actions_completed=', actions)
print('stop_reason=', stop_reason)
print('recently_modified_files_count=', len(modified_files))
for p in modified_files[:200]:
    print('ARTIFACT:', p)

# Exit with 0
sys.exit(0)
