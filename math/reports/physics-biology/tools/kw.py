import sys, re, html
# usage: kw.py file width kw1 kw2 ...
data = open(sys.argv[1], errors='ignore').read()
w = int(sys.argv[2])
t = html.unescape(re.sub(r'<[^>]+>',' ',data)); t = re.sub(r'\s+',' ',t)
m = re.search(r'<article-title>(.*?)</article-title>', data, re.S)
print('TITLE:', re.sub(r'<[^>]+>','',m.group(1)) if m else None, '| chars:', len(t))
for kw in sys.argv[3:]:
    hits = [mm.start() for mm in re.finditer(kw, t)]
    print(f'== [{kw}] {len(hits)} hits')
    for h in hits[:3]:
        print('  ...', t[max(0,h-w):h+w]); print()
