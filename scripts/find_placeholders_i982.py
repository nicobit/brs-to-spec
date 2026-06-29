import re
from pathlib import Path
f = Path('initiatives/I982-ISA/requirements/atomic-requirements.md')
text = f.read_text(encoding='utf-8')
patterns = [
    r"\[fill in\]",
    r"Goal Title",
    r"Actor Name",
    r"\[role\]",
    r"\[goal\]",
    r"\[benefit\]",
    r"\bDEFERRED\b",
    r"\(missing\s*—\s*fill in\b",
    r"\bawaiting\s+\w+\s+text\b",
    r"\bfill in BRS\b",
    r"Preserved\s*—\s*see\b",
    r"\b(?:High|Medium|Low)\s*/\s*(?:High|Medium|Low)",
    r"\bPerformance\s*/\s*Security",
    r"\bTechnical\s*/\s*Regulatory",
    r"\bCritical\s*/\s*High\s*/\s*Medium",
    r"\bOpen\s*/\s*Mitigated\s*/\s*Accepted",
    r"\bFix\s*/\s*Merge\s*/\s*Release",
    r"\bBRS section\s*/\s*intake reference",
]
found = []
for p in patterns:
    m = re.search(p, text, flags=re.IGNORECASE)
    if m:
        found.append((p, m.group(0)))
if not found:
    print('NO_PLACEHOLDERS')
else:
    for p, g in found:
        print('PATTERN:', p)
        print('MATCH:', g)
        print('---')
