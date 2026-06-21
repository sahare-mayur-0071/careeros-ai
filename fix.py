import os

for root, dirs, files in os.walk('d:/careeros-ai'):
    for f in files:
        if f.endswith('.py'):
            p = os.path.join(root, f)
            with open(p, 'r', encoding='utf-8') as file:
                content = file.read()
            if r'"' in content:
                content = content.replace(r'"', '"')
                with open(p, 'w', encoding='utf-8') as file:
                    file.write(content)
                print(f"Fixed {p}")
