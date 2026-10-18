// brute force: number of ways to partition a given letter set into exactly j prime words of <=K letters
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
static uint8_t *comp; static int K; static uint64_t lim;
static int L[26], nL; static uint32_t target; static long long count=0; static int J;
static int letters_ok(uint64_t n,uint32_t avail,uint32_t*m){ uint32_t mm=0; while(n){int d=n%26; if(!(avail>>d&1)||(mm>>d&1)) return 0; mm|=1u<<d; n/=26;} *m=mm; return 1; }
// recursive: lowest remaining letter c; enumerate all prime words containing c using available letters
static void rec(uint32_t avail,int words){
  if(!avail){ if(words==J) count++; return; }
  if(words>=J) return;
  int c=__builtin_ctz(avail);
  // enumerate words: all numbers whose letters are distinct, subset of avail, include c, length<=K: build by DFS over positions
  // simpler: iterate over lengths and positions of c, fill other positions from avail
  int others[26],no=0; for(uint32_t r=avail&~(1u<<c);r;r&=r-1) others[no++]=__builtin_ctz(r);
  if(c!=0 && !comp[c]) rec(avail&~(1u<<c),words+1);   /* single-letter word */
  for(int len=2;len<=K;len++){
    // positions: choose which position holds c (0..len-1); fill rest with ordered selections from others
    int idx[8];
    for(int pc=0;pc<len;pc++){
      // ordered selection of len-1 letters from others (no repeats)
      int sel[8]; int used[26]={0};
      // iterative DFS
      int depth=0; sel[0]=-1;
      while(depth>=0){
        int i=++sel[depth];
        if(i>=no){ depth--; if(depth>=0) used[others[sel[depth]]]=0; continue; }
        if(used[others[i]]) continue;
        used[others[i]]=1;
        if(depth==len-2 || len==1){
          // build word
          uint64_t v=0; int k=0; uint32_t m=0; int ok=1;
          for(int pos=0;pos<len;pos++){ int d; if(pos==pc) d=c; else d=others[sel[k++]]; if(pos==0&&d==0){ok=0;break;} v=v*26+d; m|=1u<<d; }
          if(ok && !comp[v]) rec(avail&~m,words+1);
          used[others[i]]=0;
          if(len==1){ depth=-1; break; }
          continue;
        }
        depth++; sel[depth]=-1;
      }
      if(len==1) break;
    }
  }
}
int main(int argc,char**argv){
  K=atoi(argv[1]); lim=1; for(int i=0;i<K;i++) lim*=26; comp=calloc(lim,1); comp[0]=comp[1]=1;
  for(uint64_t i=2;i*i<lim;i++) if(!comp[i]) for(uint64_t j=i*i;j<lim;j+=i) comp[j]=1;
  for(int a=2;a<argc;a++){ char*spec=argv[a]; uint32_t m=0; char*colon=strchr(spec,':'); for(char*c=spec;c<colon;c++) m|=1u<<(*c-'A'); J=atoi(colon+1); count=0; rec(m,0); printf("brute [%s][%d words] = %lld\n",spec,J,count); }
  return 0;
}
