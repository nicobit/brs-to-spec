import re
from pathlib import Path

f = Path('initiatives/I555-N5/requirements/atomic-requirements.md')
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

for p in patterns:
    m = re.search(p, text, flags=re.IGNORECASE)
    print(p, '=>', bool(m), 'match:', m.group(0) if m else '')
