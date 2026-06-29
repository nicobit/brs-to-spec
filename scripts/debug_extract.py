import re
p='c:/Users/nicol/source/brs-to-spec/initiatives/I982-ISA/planning/delivery-skeleton.md'
text=open(p,encoding='utf-8').read()
pattern=re.compile(r'(?ms)^## Requirement Coverage\s*(.*?)(?=^## |\Z)')
m=pattern.search(text)
block=m.group(1) if m else ''
ids=set(re.findall(r'(?:FR|REQ)-\d{3}',block))
print('FOUND',len(ids),sorted(ids)[:200])
print('\nBLOCK PREVIEW:\n',block[:800])
