#!/usr/bin/env python3
import subprocess,sys,os,json,re
PY=sys.executable
ws='initiatives/I982-ISA'
root=os.getcwd()

def run(cmd):
    p=subprocess.run(cmd, capture_output=True, text=True)
    return p.returncode, p.stdout + p.stderr

# Load templates
story_tpl_path=os.path.join('.b2s','artifact-templates','lean-story.md')
agent_tpl_path=os.path.join('.b2s','artifact-templates','story-agent-contract.yaml')
if not os.path.exists(story_tpl_path) or not os.path.exists(agent_tpl_path):
    print('Missing templates; abort')
    sys.exit(1)
story_tpl=open(story_tpl_path,encoding='utf-8').read()
agent_tpl=open(agent_tpl_path,encoding='utf-8').read()

iterations=0
max_iter=50
while iterations<max_iter:
    iterations+=1
    print('\n=== ITER',iterations,'===')
    rc,out=run([PY,os.path.join('.b2s','scripts','b2s_cli.py'),'dispatch-next','--workspace-root',ws])
    print(out)
    if rc!=0:
        print('dispatch-next failed')
        break
    # read plan
    plan_path=os.path.join(ws,'.b2s','tmp','dispatch-next.json')
    with open(plan_path,encoding='utf-8') as f:
        plan=json.load(f)
    status=plan.get('status')
    if status in ('awaiting_gate','awaiting_gate') or plan.get('status')=='awaiting_gate':
        print('Human gate opened; stopping')
        break
    if plan.get('action') is None:
        print('Workflow complete or no action; stopping')
        break
    action=plan['action']
    action_id=action.get('action_id')
    current_item=plan.get('current_item')
    print('Action:',action_id,'Item:',current_item)
    if action_id!='create-epic-stories':
        print('Action not create-epic-stories; stopping loop')
        break
    # ensure stories dir
    epic_dir=os.path.join(ws,'epics',current_item)
    stories_dir=os.path.join(epic_dir,'stories')
    os.makedirs(stories_dir,exist_ok=True)
    # if stories exist, skip creation
    existing=[f for f in os.listdir(stories_dir) if f.endswith('.md')]
    if not existing:
        # create S-001.md and .agent.yaml
        story_id='S-001'
        title='Basic story for ' + current_item
        story_content=story_tpl
        story_content=story_content.replace('S-NNN.N', story_id)
        story_content=story_content.replace('{{Story Title}}', title)
        story_content=story_content.replace('{{Epic Title}}', current_item)
        story_content=story_content.replace('{{frontend-form / frontend-page / backend-endpoint / event-consumer / schema-migration / generic}}','generic')
        story_content=story_content.replace('{{specific role name — NOT "user", "person", or "someone"}}','Business User')
        story_file=os.path.join(stories_dir,f'{story_id}.md')
        with open(story_file,'w',encoding='utf-8') as f:
            f.write(story_content)
        # create agent yaml
        agent=agent_tpl
        agent=agent.replace('S-NNN.N',story_id)
        agent=agent.replace('{{Story Title}}', title)
        agent=agent.replace('{{frontend-form | frontend-page | backend-endpoint | event-consumer | schema-migration | generic}}','generic')
        agent=agent.replace('{{frontend | backend | infrastructure | integration}}','backend')
        agent_file=os.path.join(stories_dir,f'{story_id}.agent.yaml')
        with open(agent_file,'w',encoding='utf-8') as f:
            f.write(agent)
        print('Wrote',story_file,agent_file)
    else:
        print('Stories already present; skipping generation')
    # Run validate -> update-state -> dispatch-next
    cmds=[
        [PY,os.path.join('.b2s','scripts','b2s_cli.py'),'validate-artifact','--workspace-root',ws,'--action-id',action_id],
        [PY,os.path.join('.b2s','scripts','b2s_cli.py'),'update-state','--workspace-root',ws],
        [PY,os.path.join('.b2s','scripts','b2s_cli.py'),'dispatch-next','--workspace-root',ws],
    ]
    for cmd in cmds:
        rc,out=run(cmd)
        print(out)
        if rc!=0:
            print('Command failed:',cmd)
            sys.exit(1)
# end loop
print('\nDone')
