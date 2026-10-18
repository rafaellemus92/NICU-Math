import numpy as np, time
B=26; L=B**4; A=65
def val(w):
    v=0
    for ch in w: v=v*B+(ord(ch)-A)
    return v
def name(n):
    s=''
    while n: s=chr(A+n%B)+s; n//=B
    return s or 'A'

sieve=np.ones(L,dtype=bool); sieve[:2]=False
for i in range(2,int(L**0.5)+1):
    if sieve[i]: sieve[i*i::i]=False

# ---- verify the posted pangram ----
left="YR BQL CWH DNF GAX".split(); right="KV MT OP ESJ IUZ".split()
print("word value prime?")
for w in left+right: print(w, val(w), bool(sieve[val(w)]))
SL=sum(map(val,left)); SR=sum(map(val,right)); print("sums",SL,SR,SL==SR)
letters=''.join(left+right)
print("26 letters once:", sorted(letters)==list(map(chr,range(65,91))))
print("letter-value sums L/R:", sum(ord(c)-65 for c in ''.join(left)), sum(ord(c)-65 for c in ''.join(right)))
print("last letters:", [w[-1] for w in left+right])

# ---- distinct-letter prime words below 26^4 (<=4 letters is provably sufficient) ----
primes=np.nonzero(sieve)[0]
S=[]; maskarr=np.zeros(L,dtype=np.int64)
for p in primes:
    p=int(p); n=p; m=0; ok=True
    while n:
        d=n%B
        if m>>d &1: ok=False; break
        m|=1<<d; n//=B
    if ok: S.append(p); maskarr[p]=m
S_arr=np.array(S,dtype=np.int64); isS=maskarr>0
print("distinct-letter prime words <26^4:",len(S))
FULL=(1<<26)-1

def exact_cover(um):
    by_bit=[[] for _ in range(26)]
    for i,u in enumerate(um):
        x=u
        while x:
            b=x&-x; by_bit[b.bit_length()-1].append(i); x^=b
    sols=[]
    def rec(cov,chosen):
        if cov==FULL:
            sols.append(list(chosen)); return
        if len(chosen)==5: return
        r=~cov&FULL; b=r&-r; bi=b.bit_length()-1
        for i in by_bit[bi]:
            u=um[i]
            if u&cov==0:
                chosen.append(i); rec(cov|u,chosen); chosen.pop()
    rec(0,[])
    return sols

t=time.time(); found=[]; Ncount=0
for N in range(10, 2*L, 10):
    lo=np.searchsorted(S_arr, max(2, N-L+1))
    hi=np.searchsorted(S_arr, (N-1)//2, side='right')
    if hi<=lo: continue
    ps=S_arr[lo:hi]; qs=N-ps
    ok=isS[qs]; ps=ps[ok]; qs=qs[ok]
    if len(ps)<5: continue
    m1=maskarr[ps]; m2=maskarr[qs]
    d=(m1&m2)==0
    if d.sum()<5: continue
    um=(m1|m2)[d]; ps=ps[d]; qs=qs[d]
    if int(np.bitwise_or.reduce(um))!=FULL: continue
    Ncount+=1
    sols=exact_cover([int(x) for x in um])
    for s in sols:
        found.append((N,[(int(ps[i]),int(qs[i])) for i in s]))
print("N values reaching exact-cover stage:",Ncount,"time",round(time.time()-t,1))
print("solutions:",len(found), "distinct N:", len(set(n for n,_ in found)))
for N,pairs in found[:40]:
    print(N, ' | '.join(f"{name(p)}+{name(q)}" for p,q in pairs), ' ', pairs)
