"""Build ../index.html from src.html: inline fonts, photos and tech icons.

Run:  cd ~/haldoren/build && python3 build.py
"""
import base64
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(HERE, '..', 'assets')


def b64(path):
    with open(path, 'rb') as f:
        return base64.b64encode(f.read()).decode()


icons_dir = os.path.join(ASSETS, 'icons')
icons = {
    name[:-len('-original.svg')]: 'data:image/svg+xml;base64,' + b64(os.path.join(icons_dir, name))
    for name in sorted(os.listdir(icons_dir)) if name.endswith('-original.svg')
}

with open(os.path.join(HERE, 'src.html')) as f:
    s = f.read()
with open(os.path.join(HERE, 'fontface.css')) as f:
    fonts = f.read()

s = (s.replace('/*FONTS*/', fonts, 1)
      .replace('/*ME*/', b64(os.path.join(ASSETS, 'me-badge.jpg')), 1)
      .replace('/*MECUT*/', b64(os.path.join(ASSETS, 'me-cut.png')), 1)
      .replace('/*ICONS*/{}', json.dumps(icons), 1))

out = os.path.join(HERE, '..', 'index.html')
with open(out, 'w') as f:
    f.write(s)
print('built', os.path.normpath(out), f'{len(s) // 1024} KB, {len(icons)} icons')
