import sys, re, html, urllib.request, json
# usage: epmc.py PMCID outfile kw1 kw2 ...
pmc, out = sys.argv[1], sys.argv[2]
url = f"https://www.ebi.ac.uk/europepmc/webservices/rest/{pmc}/fullTextXML"
data = urllib.request.urlopen(url, timeout=60).read().decode('utf-8','ignore')
open(out,'w').write(data)
t = html.unescape(re.sub(r'<[^>]+>',' ',data)); t = re.sub(r'\s+',' ',t)
m = re.search(r'<article-title>(.*?)</article-title>', data, re.S)
print('TITLE:', re.sub(r'<[^>]+>','',m.group(1)) if m else None)
for kw in sys.argv[3:]:
    hits = [mm.start() for mm in re.finditer(re.escape(kw), t)]
    for h in hits[:2]:
        print(f'>> [{kw}]', t[max(0,h-300):h+300]); print()
