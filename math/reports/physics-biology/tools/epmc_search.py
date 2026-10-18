import json, sys, urllib.request, urllib.parse
q = sys.argv[1]; n = int(sys.argv[2]) if len(sys.argv)>2 else 2500
url = "https://www.ebi.ac.uk/europepmc/webservices/rest/search?" + urllib.parse.urlencode({'query':q,'format':'json','resultType':'core','pageSize':8})
d = json.load(urllib.request.urlopen(url, timeout=60))
for r in d['resultList']['result']:
    ji = r.get('journalInfo',{})
    print(r.get('pmid'), r.get('pmcid'), r.get('doi'), '|', ji.get('journal',{}).get('title'), r.get('pubYear'), ji.get('volume'), r.get('pageInfo'), '|', r.get('title'))
    print('  AUTH:', r.get('authorString','')[:200])
    print('  ABS:', r.get('abstractText','')[:n]); print()
