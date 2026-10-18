// Prime-26 puzzle: 10 distinct-letter prime "words" (base-26, A=0..Z=25), every letter once,
// arranged as 5 pairs with equal sums N.  Exhaustive search over all even N < 2*26^4.
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#include <time.h>

#define L 456976          /* 26^4 */
#define FULL ((1u<<26)-1)
#define MAXC 60000

static unsigned char comp[L];
static uint32_t mask[L];           /* 0 unless prime with pairwise-distinct letters */
static int S[L]; static int nS=0;
static int cp[MAXC], cq[MAXC]; static uint32_t cu[MAXC]; static int nc;
static int bybit[26][MAXC]; static int nbb[26];
static int chosen[5];
static long nsol5=0, nsol4=0; static int Ncur; static int printed=0;
static long byMod10[10]; static int lastN=-1, distinctN=0;
static int minN=0x7fffffff, maxN=0;

static void name(int n, char*buf){ char t[8]; int k=0; while(n){t[k++]='A'+n%26; n/=26;} for(int i=0;i<k;i++)buf[i]=t[k-1-i]; buf[k]=0; }

static void record(int depth){
  if(depth==5){ nsol5++; byMod10[Ncur%10]++; if(Ncur!=lastN){distinctN++; lastN=Ncur;} if(Ncur<minN)minN=Ncur; if(Ncur>maxN)maxN=Ncur; }
  else nsol4++;
  if(printed<40){
    printed++;
    printf("N=%d  (%d pairs) ", Ncur, depth);
    for(int d=0;d<depth;d++){ char a[8],b[8]; name(cp[chosen[d]],a); name(cq[chosen[d]],b); printf("%s+%s(%d+%d) ", a,b,cp[chosen[d]],cq[chosen[d]]); }
    printf("\n"); fflush(stdout);
  }
}
static void rec(uint32_t cov,int depth){
  if(cov==FULL){ record(depth); return; }
  if(depth==5) return;
  int b=__builtin_ctz(~cov & FULL);
  int *lst=bybit[b], n=nbb[b];
  for(int j=0;j<n;j++){ int i=lst[j]; if((cu[i]&cov)==0){ chosen[depth]=i; rec(cov|cu[i],depth+1);} }
}
int main(int argc,char**argv){
  long Nmax = (argc>1)? atol(argv[1]) : 2L*L;
  for(long i=2;i<L;i++) if(!comp[i]) for(long j=i*i;j<L;j+=i) comp[j]=1;
  for(int p=2;p<L;p++){ if(comp[p]) continue; int n=p; uint32_t m=0; int ok=1; while(n){int d=n%26; if(m>>d&1){ok=0;break;} m|=1u<<d; n/=26;} if(ok){mask[p]=m; S[nS++]=p;} }
  fprintf(stderr,"distinct-letter prime words below 26^4: %d\n",nS);
  clock_t t0=clock(); int start=0; long Nwithcover=0;
  for(long N=4; N<Nmax; N+=2){
    long lo=N-L+1; while(start<nS && S[start]<lo) start++;
    nc=0; uint32_t uni=0;
    for(int idx=start; idx<nS && 2L*S[idx]<N; idx++){ int p=S[idx]; int q=(int)(N-p); uint32_t mq=mask[q]; if(!mq) continue; uint32_t mp=mask[p]; if(mp&mq) continue; cp[nc]=p; cq[nc]=q; cu[nc]=mp|mq; uni|=cu[nc]; nc++; }
    if(uni!=FULL || nc<4) continue;
    Nwithcover++;
    memset(nbb,0,sizeof nbb);
    for(int i=0;i<nc;i++){ uint32_t x=cu[i]; while(x){ int b=__builtin_ctz(x); bybit[b][nbb[b]++]=i; x&=x-1; } }
    Ncur=(int)N; rec(0,0);
  }
  fprintf(stderr,"time %.1fs; N values reaching cover stage: %ld\n",(double)(clock()-t0)/CLOCKS_PER_SEC,Nwithcover);
  printf("5-pair solutions: %ld over %d distinct N (min N=%d, max N=%d); 4-pair (8-word) covers: %ld\n",nsol5,distinctN,minN,maxN,nsol4);
  printf("5-pair solutions by N mod 10:"); for(int r=0;r<10;r++) printf(" [%d]=%ld",r,byMod10[r]); printf("\n");
  return 0;
}
