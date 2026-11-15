import re, base64, urllib.request, sys
css = open('fonts.css').read()
blocks = re.findall(r'/\* (\S+) \*/\s*@font-face\s*\{(.*?)\}', css, re.S)
out = []
for sub, body in blocks:
    if sub not in ('latin', 'vietnamese'):
        continue
    fam = re.search(r"font-family:\s*'([^']+)'", body).group(1)
    w = re.search(r'font-weight:\s*([^;]+);', body).group(1)
    url = re.search(r'url\((\S+?)\)', body).group(1)
    ur = re.search(r'unicode-range:\s*([^;]+);', body).group(1)
    data = urllib.request.urlopen(url).read()
    print(fam, sub, w, len(data), file=sys.stderr)
    out.append("@font-face{font-family:'%s';font-style:normal;font-weight:%s;font-display:swap;src:url(data:font/woff2;base64,%s) format('woff2');unicode-range:%s}"
               % (fam, w, base64.b64encode(data).decode(), ur))
open('fontface.css', 'w').write('\n'.join(out))
