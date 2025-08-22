from pathlib import Path
p = Path('proto')
for f in p.glob('*_pb2.py'):
    s = f.read_text()
    s = s.replace('import ', 'from proto import ')
    f.write_text(s)
print('fixed imports')
