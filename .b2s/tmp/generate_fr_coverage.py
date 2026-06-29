import re
from pathlib import Path
req_path=Path('initiatives/I654-N5/requirements/atomic-requirements.md')
out_path=Path('initiatives/I654-N5/planning/fr-coverage.md')
text=req_path.read_text(encoding='utf-8')
ids=sorted(dict.fromkeys(re.findall(r"(?:FR|NFR|C|OBJ)-\d{3}",text)))
covered={'FR-001':'S-001.1','FR-002':'S-001.1','FR-003':'S-001.2','FR-004':'S-001.4','FR-005':'S-001.3','NFR-001':'S-001.2'}
with out_path.open('w',encoding='utf-8') as f:
    f.write('# FR Coverage\n\nThis artifact maps functional and non-functional requirements to epic `E-001` stories.\n\n')
    f.write('## Epic E-001 — Loan Application Intake\n\n| Requirement | Covered by Story(s) | Notes |\n|---|---|---|\n')
    for rid in ['FR-001','FR-002','FR-003','FR-004','FR-005','NFR-001']:
        cov=covered.get(rid,'')
        note=''
        f.write(f'| {rid} | {cov or "Deferred"} | {note} |\n')
    f.write('\n## Full Coverage Matrix\n\n| Requirement | Coverage | Notes |\n|---|---|---|\n')
    for rid in ids:
        cov='Covered by '+covered[rid] if rid in covered else 'Deferred'
        f.write(f'| {rid} | {cov} | |\n')
    f.write('\n## Coverage Summary\n\n- All canonical requirements are listed above with coverage status.\n')
print('WROTE', out_path)
