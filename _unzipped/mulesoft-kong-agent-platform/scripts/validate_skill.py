from pathlib import Path
import re
root=Path(__file__).resolve().parents[1]
text=(root/'SKILL.md').read_text(encoding='utf-8')
match=re.match(r'^---\n(.*?)\n---\n',text,re.S)
assert match, 'Missing YAML frontmatter'
name=re.search(r'^name:\s*(.+)$',match.group(1),re.M)
assert name and name.group(1).strip()==root.name, 'Skill name must match folder'
assert re.search(r'^description:\s*.+$',match.group(1),re.M), 'Missing description'
assert (root/'README.md').exists()
print('Skill structure OK:',root.name)
