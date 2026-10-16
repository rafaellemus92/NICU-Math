// For each even D: candidate pairs (p,p+D) of distinct-letter prime words (<26^4) with disjoint letters;
// report #candidates, #2-letter-only pairs, and the largest number of pairwise-disjoint pairs (capped at 5).
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#define L 456976
#define FULL ((1u<<26)-1)
static unsigned char comp[L]; static uint32_t mask[L]; static int S[L]; static int nS;
static uint32_t cu[60000]; static int nc; static int best;
static void rec(int idx,uint32_t cov,int depth){
  if(depth>best) best=depth; if(best>=5) return;
  if(nc-idx < 5-depth) ; // no bound needed
  for(int i=idx;i<nc && best<5;i++) if((cu[i]&cov)==0) rec(i+1,cov|cu[i],depth+1);
}
int main(){
  for(long i=2;i<L;i++) if(!comp[i]) for(long j=i*i;j<L;j+=i) comp[j]=1;
  for(int p=2;p<L;p++){ if(comp[p]) continue; int n=p; uint32_t m=0; int ok=1; while(n){int d=n%26; if(m>>d&1){ok=0;break;} m|=1u<<d; n/=26;} if(ok){mask[p]=m; S[nS++]=p;} }
  for(int D=28; D<17576; D+=2){
    nc=0; int n2=0;
    for(int idx=0; idx<nS && S[idx]+D<L; idx++){ int p=S[idx],q=p+D; if(!mask[q]) continue; if(mask[p]&mask[q]) continue; cu[nc++]=mask[p]|mask[q]; if(p<676&&q<676) n2++; }
    best=0; if(nc) rec(0,0,0);
    printf("%d %d %d %d\n",D,nc,n2,best);
  }
  return 0;
}
