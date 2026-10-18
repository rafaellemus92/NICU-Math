#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#include <time.h>
#define L 456976
#define FULL ((1u<<26)-1)
#define MAXC 60000
static unsigned char comp[L]; static uint32_t mask[L]; static int S[L]; static int nS=0;
static int cp[MAXC], cq[MAXC]; static uint32_t cu[MAXC]; static int nc;
static int bybit[26][MAXC]; static int nbb[26]; static int chosen[5];
static long nsol=0; static int Dcur; static int printed=0; static int distinctD=0,lastD=-1;
static void name(int n,char*b){char t[8];int k=0;while(n){t[k++]='A'+n%26;n/=26;}for(int i=0;i<k;i++)b[i]=t[k-1-i];b[k]=0;}
static void rec(uint32_t cov,int depth){
  if(cov==FULL){ if(depth!=5) return; nsol++; if(Dcur!=lastD){distinctD++;lastD=Dcur;}
    if(printed<12){printed++; printf("D=%d: ",Dcur); int ls=0; for(int d=0;d<5;d++){char a[8],b[8];name(cp[chosen[d]],a);name(cq[chosen[d]],b);printf("%s->%s (%d->%d) ",a,b,cp[chosen[d]],cq[chosen[d]]); for(char*c=a;*c;c++)ls+=*c-'A';} printf(" | sum of letter values of the five smaller words = %d, 10D mod 25 = %d, that sum mod 25 = %d\n",ls,(10*Dcur)%25,ls%25); fflush(stdout);} return; }
  if(depth==5) return;
  int b=__builtin_ctz(~cov&FULL); int*lst=bybit[b],n=nbb[b];
  for(int j=0;j<n;j++){int i=lst[j]; if((cu[i]&cov)==0){chosen[depth]=i; rec(cov|cu[i],depth+1);}}
}
int main(int argc,char**argv){
  int Dmax=atoi(argv[1]);
  for(long i=2;i<L;i++) if(!comp[i]) for(long j=i*i;j<L;j+=i) comp[j]=1;
  for(int p=2;p<L;p++){ if(comp[p]) continue; int n=p; uint32_t m=0; int ok=1; while(n){int d=n%26; if(m>>d&1){ok=0;break;} m|=1u<<d; n/=26;} if(ok){mask[p]=m; S[nS++]=p;} }
  clock_t t0=clock();
  for(int D=2; D<=Dmax; D+=2){
    nc=0; uint32_t uni=0;
    for(int idx=0; idx<nS && S[idx]+D<L; idx++){ int p=S[idx], q=p+D; uint32_t mq=mask[q]; if(!mq) continue; uint32_t mp=mask[p]; if(mp&mq) continue; cp[nc]=p;cq[nc]=q;cu[nc]=mp|mq; uni|=cu[nc]; nc++; }
    if(uni!=FULL||nc<5) continue;
    memset(nbb,0,sizeof nbb);
    for(int i=0;i<nc;i++){uint32_t x=cu[i]; while(x){int b=__builtin_ctz(x); bybit[b][nbb[b]++]=i; x&=x-1;}}
    Dcur=D; rec(0,0);
  }
  fprintf(stderr,"time %.1fs\n",(double)(clock()-t0)/CLOCKS_PER_SEC);
  printf("D<=%d: solutions %ld over %d distinct D\n",Dmax,nsol,distinctD);
  return 0;
}
