/* Enumerate EVERY five-pair prime pangram with even common sum N in [lo, hi].
   usage: pangram_all coupled|plain lo hi
   Prints one line per solution: N  p1 q1  p2 q2  ...  (p < q in each pair).
   Exhaustive: for each N, every unordered pair (p, N-p) of odd primes with
   letter-disjoint names is a candidate; exact cover over the 26 letters,
   branching on the uncovered letter with the fewest candidates, finds each
   5-pair cover exactly once.  Prime 2 is skipped (ruled out by parity). */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#define FULL ((1u<<26)-1)
static int plain;
static uint32_t mask_of(uint32_t n){
  int d[8],k=0; while(n){d[k++]=n%26;n/=26;}
  uint32_t m=0;
  for(int j=0;j<k;j++){int a=plain?d[j]:(d[j]+(j?d[j-1]:0))%26; uint32_t b=1u<<a; if(m&b)return 0; m|=b;}
  return m;
}
static int npairs; static uint32_t *pm; static int *pp,*pq;
static int *bl[26], blc[26];
static long nsol; static int cur_N;
static void rec(uint32_t used,int depth,int *chosen){
  if(depth==5){ if(used==FULL){ nsol++; printf("%d",cur_N); for(int i=0;i<5;i++)printf("  %d %d",pp[chosen[i]],pq[chosen[i]]); printf("\n"); fflush(stdout);} return; }
  int bestb=-1,bestcnt=1<<30;
  for(int b=0;b<26;b++){ if(used>>b&1)continue; int cnt=0; for(int t=0;t<blc[b];t++) if(!(pm[bl[b][t]]&used))cnt++;
    if(cnt==0)return; if(cnt<bestcnt){bestcnt=cnt;bestb=b;} }
  if(bestb<0)return;              /* all letters covered with fewer than 5 pairs */
  for(int t=0;t<blc[bestb];t++){ int i=bl[bestb][t]; if(pm[i]&used)continue; chosen[depth]=i; rec(used|pm[i],depth+1,chosen); }
}
int main(int argc,char**argv){
  plain=strcmp(argv[1],"plain")==0; int lo=atoi(argv[2]),hi=atoi(argv[3]);
  uint8_t *isp=calloc(hi+1,1); for(int i=2;i<=hi;i++)isp[i]=1;
  for(long i=2;i*i<=hi;i++) if(isp[i]) for(long j=i*i;j<=hi;j+=i) isp[j]=0;
  uint32_t *mk=calloc(hi+1,4); int *primes=malloc(sizeof(int)*(hi+1)); int np=0;
  for(int p=3;p<=hi;p+=2) if(isp[p]){ mk[p]=mask_of(p); primes[np++]=p; }
  pm=malloc(4*np); pp=malloc(4*np); pq=malloc(4*np);
  for(int b=0;b<26;b++) bl[b]=malloc(4*np);
  int chosen[5]; long checked=0;
  for(int N=lo+(lo&1); N<=hi; N+=2){
    npairs=0;
    for(int t=0;t<np && 2*primes[t]<N;t++){ int p=primes[t],q=N-p;
      if(!isp[q]||!mk[p]||!mk[q]||(mk[p]&mk[q]))continue; pp[npairs]=p;pq[npairs]=q;pm[npairs]=mk[p]|mk[q];npairs++; }
    uint32_t cover=0; for(int i=0;i<npairs;i++)cover|=pm[i];
    if(npairs<5||cover!=FULL)continue;
    checked++;
    for(int b=0;b<26;b++)blc[b]=0;
    for(int i=0;i<npairs;i++) for(int b=0;b<26;b++) if(pm[i]>>b&1) bl[b][blc[b]++]=i;
    cur_N=N; rec(0,0,chosen);
    if(N%50000<2) fprintf(stderr,"progress N=%d\n",N);
  }
  fprintf(stderr,"done %s [%d,%d]: %ld sums with a full-alphabet pair set searched, %ld solutions\n",argv[1],lo,hi,checked,nsol);
  return 0;
}
