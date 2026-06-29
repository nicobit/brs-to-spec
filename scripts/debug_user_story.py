import re
p=r'c:\\Users\\nicol\\source\\brs-to-spec\\initiatives\\I982-ISA\\epics\\E-002\\stories\\S-006.1.md'
text=open(p, encoding='utf-8').read()
print('has_user_story:', bool(re.search(r'(?i)##\s*user story', text)))
pattern=re.compile(rf"(?ms)^{re.escape('## User Story')}\s*(.*?)(?=^## |\Z)")
match=pattern.search(text)
print('pattern_match:', bool(match))
if match:
    block=match.group(1)
    print('block_preview:', repr(block[:300]))
    print('block_len:', len(block.strip()))
else:
    print('no match found')
