"""Hard resource gate for the preregistered diagnostic; no solver edits."""
import hashlib,json,os,resource,subprocess,sys,time
from pathlib import Path
HERE=Path(__file__).resolve().parent;OUT=HERE/'results'
def limits():
    resource.setrlimit(resource.RLIMIT_AS,(512*1024**2,512*1024**2))
def execute(name,N,dt,steps,cap):
    cmd=[sys.executable,'-B',str(HERE/'diagnostic.py'),'--N',str(N),'--dt',str(dt),'--steps',str(steps),'--out',str(OUT/name)]
    start=time.monotonic()
    try:
        p=subprocess.run(cmd,capture_output=True,text=True,timeout=cap,preexec_fn=limits,
            env={**os.environ,'OPENBLAS_NUM_THREADS':'1','OMP_NUM_THREADS':'1','MKL_NUM_THREADS':'1'})
        log=p.stdout+p.stderr;code=p.returncode
    except subprocess.TimeoutExpired as e:
        log=str(e.stdout)+str(e.stderr)+'\nHARD TIMEOUT';code=124
    elapsed=time.monotonic()-start
    with (OUT/(name+'.log')).open('x') as f:f.write(log)
    rec=dict(command=cmd,wall_seconds=elapsed,exit_code=code,timeout_seconds=cap,memory_limit_MiB=512)
    with (OUT/(name+'.process.json')).open('x') as f:json.dump(rec,f,indent=2)
    print(name,json.dumps(rec),flush=True)
    if code:raise SystemExit('stopped on failed execution; see preserved log')
    if sum(f.stat().st_size for f in OUT.iterdir() if f.is_file())>=1024**2:raise SystemExit('scalar output cap')
    return rec,json.loads((OUT/(name+'.json')).read_text())
for n,h in json.loads((HERE/'FREEZE.json').read_text()).items():
    assert hashlib.sha256((HERE/n).read_bytes()).hexdigest()==h,'frozen source mismatch'
if sys.argv[1]=='pilot':
    rec,result=execute('pilot',32,.0025,10,30)
    projected=rec['wall_seconds']+1.5*(rec['wall_seconds']/10)*400+15
    gate=dict(projected_total_seconds=projected,peak_rss_MiB=result['peak_rss_MiB'],
              passes=projected<300 and result['peak_rss_MiB']<512)
    with (OUT/'gate.json').open('x') as f:json.dump(gate,f,indent=2)
    print('GATE',json.dumps(gate),flush=True)
elif sys.argv[1]=='full':
    assert json.loads((OUT/'gate.json').read_text())['passes']
    elapsed=sum(json.loads(p.read_text())['wall_seconds'] for p in OUT.glob('*.process.json'))
    for name,N,dt in [('n24_coarse',24,.0025),('n24_fine',24,.00125),('n32_coarse',32,.0025)]:
        remaining=300-elapsed-15
        if remaining<=0:raise SystemExit('aggregate budget exhausted')
        rec,result=execute(name,N,dt,round(.25/dt),remaining);elapsed+=rec['wall_seconds']
    print('TOTAL PROCESS SECONDS',elapsed)
else:raise SystemExit('pilot or full required')
