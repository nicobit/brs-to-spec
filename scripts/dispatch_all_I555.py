import subprocess, json, time
from pathlib import Path

WS = Path('initiatives/I555-N5')
STATE_LOG = WS / '.b2s' / 'state' / 'execution-log.jsonl'
TMP_VALIDATION = WS / '.b2s' / 'tmp' / 'current-validation.yaml'

completed = 0
artifacts = []

def run(cmd):
    print('RUNNING:', ' '.join(cmd))
    r = subprocess.run(cmd, capture_output=True, text=True)
    print(r.stdout)
    if r.stderr:
        print('ERR:', r.stderr)
    return r.returncode

while True:
    rc = run(['python', '.b2s/scripts/b2s_cli.py', 'next-step', '--workspace-root', str(WS)])
    time.sleep(0.3)
    # read last execution-log entry
    if not STATE_LOG.exists():
        print('No execution log found; stopping')
        break
    with STATE_LOG.open('r', encoding='utf-8') as f:
        lines = [l for l in f.read().splitlines() if l.strip()]
    last = json.loads(lines[-1])
    active = last.get('active_action')
    awaiting = last.get('awaiting_human')
    next_action = last.get('next_action')
    print('Selected action:', active, 'Awaiting human:', awaiting, 'Next action:', next_action)
    if active is None:
        print('Workflow complete (no active action).')
        break
    if awaiting:
        print('Human gate opened; stopping for approval.')
        break
    # Per-action execution
    # collect inputs
    run(['python', '.b2s/scripts/b2s_cli.py', 'collect-inputs', '--workspace-root', str(WS)])
    # validate artifact (retry up to 3)
    retries = 0
    while True:
        rc = run(['python', '.b2s/scripts/b2s_cli.py', 'validate-artifact', '--workspace-root', str(WS)])
        time.sleep(0.2)
        if TMP_VALIDATION.exists():
            import yaml
            data = yaml.safe_load(TMP_VALIDATION.read_text(encoding='utf-8'))
            if data.get('overall') == 'pass':
                print('Validation passed for', data.get('artifact_path'))
                artifacts.append(data.get('artifact_path'))
                break
            else:
                retries += 1
                print('Validation failed; retry', retries)
                if retries >= 3:
                    print('Validation failed after 3 retries; stopping')
                    print(data)
                    raise SystemExit(1)
                # small wait before retry
                time.sleep(0.5)
        else:
            print('No validation output produced; stopping')
            raise SystemExit(1)
    # update state
    run(['python', '.b2s/scripts/b2s_cli.py', 'update-state', '--workspace-root', str(WS)])
    completed += 1
    # small delay
    time.sleep(0.2)

# summary
print('\nSUMMARY')
print('Actions completed:', completed)
print('Artifacts produced:')
for a in artifacts:
    print('-', a)

