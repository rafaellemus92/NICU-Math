// brute-force enumeration of perfect pangrams (words <=K letters), time-limited; counts balanced 5|5 splits
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#include <time.h>
static uint8_t *comp; static int K; static uint64_t lim;
static long long count=0, bal=0; static uint64_t wv[10]; static clock_t tend; static int stop=0;
static void rec(uint32_t avail,int words){
  if(stop) return;
  if(!avail){ if(words==10){ count++; uint64_t tot=0; for(int i=0;i<10;i++) tot+=wv[i]; if(!(tot&1)){ uint64_t half=tot/2; for(int m=0;m<512;m++){ if(__builtin_popcount(m)!=4) continue; uint64_t s=wv[0]; for(int b=0;b<9;b++) if(m>>b&1) s+=wv[b+1]; if(s==half){bal++;break;} } }
      if((count&0x3ffff)==0 && clock()>tend) stop=1; } return; }
  if(words>=10) return;
  int rem=__builtin_popcount(avail); if(rem>(10-words)*K || rem<10-words) return;
  int c=__builtin_ctz(avail);
  if(c!=0 && !comp[c]){ wv[words]=c; rec(avail&~(1u<<c),words+1); }
  int others[26],no=0; for(uint32_t r=avail&~(1u<<c);r;r&=r-1) others[no++]=__builtin_ctz(r);
  for(int len=2;len<=K;len++){
    if(len-1>no) break;
    for(int pc=0;pc<len;pc++){
      int sel[8]; int used[26]={0}; int depth=0; sel[0]=-1;
      while(depth>=0){
        int i=++sel[depth];
        if(i>=no){ depth--; if(depth>=0) used[others[sel[depth]]]=0; continue; }
        if(used[others[i]]) continue;
        used[others[i]]=1;
        if(depth==len-2){
          uint64_t v=0; int k=0; uint32_t m=0; int ok=1;
          for(int pos=0;pos<len;pos++){ int d; if(pos==pc) d=c; else d=others[sel[k++]]; if(pos==0&&d==0){ok=0;break;} v=v*26+d; m|=1u<<d; }
          if(ok && !comp[v]){ wv[words]=v; rec(avail&~m,words+1); }
          used[others[i]]=0; continue;
        }
        depth++; sel[depth]=-1;
      }
    }
  }
}
int main(int argc,char**argv){
  K=atoi(argv[1]); int secs=atoi(argv[2]); lim=1; for(int i=0;i<K;i++) lim*=26; comp=calloc(lim,1); comp[0]=comp[1]=1;
  for(uint64_t i=2;i*i<lim;i++) if(!comp[i]) for(uint64_t j=i*i;j<lim;j+=i) comp[j]=1;
  clock_t t0=clock(); tend=t0+secs*CLOCKS_PER_SEC; rec((1u<<26)-1,0);
  double el=(double)(clock()-t0)/CLOCKS_PER_SEC;
  printf("brute force K=%d: %.1fs, %lld pangrams enumerated (%.3e per second), %lld had a balanced split (%.2e)\n",K,el,count,count/el,bal,(double)bal/count);
  return 0;
}
