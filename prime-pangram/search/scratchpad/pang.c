// Prime-26 perfect pangrams (10 distinct-letter prime words using A..Z once each).
// Modes:
//   exact4            exact count of pangrams whose words have <=4 letters (DP over letter subsets)
//   sample K N seed   Knuth-style sequential importance sampling: unbiased estimates of
//                     (a) #pangrams with words <=K letters, (b) #(pangram, balanced 5|5 split) pairs
//   enum K secs       brute-force DFS throughput for `secs` seconds
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#include <math.h>
#include <time.h>

#define FULL ((1u<<26)-1)
static uint8_t *comp; static uint64_t LIM;
static void sieve(uint64_t lim){ LIM=lim; comp=calloc(lim,1); comp[0]=comp[1]=1;
  for(uint64_t i=2;i*i<lim;i++) if(!comp[i]) for(uint64_t j=i*i;j<lim;j+=i) comp[j]=1; }
static uint64_t pow26(int k){ uint64_t r=1; while(k--) r*=26; return r; }
static int letters_mask(uint64_t n, uint32_t*m){ uint32_t mm=0; while(n){ int d=n%26; if(mm>>d&1) return 0; mm|=1u<<d; n/=26;} *m=mm; return 1; }
static void name(uint64_t n,char*b){char t[12];int k=0;while(n){t[k++]='A'+n%26;n/=26;}for(int i=0;i<k;i++)b[i]=t[k-1-i];b[k]=0;}

/* ---------- word table: w[mask] = #prime arrangements of that letter set ---------- */
static uint16_t *w16;
static void build_w(int K){
  uint64_t lim=pow26(K); sieve(lim); w16=calloc(1u<<26,2);
  for(uint64_t n=2;n<lim;n++){ if(comp[n]) continue; uint32_t m; if(letters_mask(n,&m)) w16[m]++; }
}
/* t-th (0-based) prime arrangement of letter set mask, in increasing numeric order */
static int nw_L[26], nw_k, nw_t, nw_cnt; static uint64_t nw_ans;
static int nw_rec(int depth,int used,uint64_t val){
  if(depth==nw_k){ if(!comp[val]){ if(nw_cnt==nw_t){ nw_ans=val; return 1;} nw_cnt++; } return 0; }
  for(int i=0;i<nw_k;i++){ if(used>>i&1) continue; if(depth==0 && nw_L[i]==0) continue; if(nw_rec(depth+1,used|(1<<i),val*26+nw_L[i])) return 1; }
  return 0;
}
static uint64_t nth_word(uint32_t mask,int t){ nw_k=0; for(int b=0;b<26;b++) if(mask>>b&1) nw_L[nw_k++]=b; nw_t=t; nw_cnt=0; nw_ans=0; nw_rec(0,0,0); return nw_ans; }

/* ---------- exact DP for K<=4 ---------- */
static inline int jlo(int s){ int a=(s+3)/4, b=s-16; return a>b?a:b; }
static inline int jhi(int s){ int a=s, b=10-(26-s+3)/4; return a<b?a:b; }
static void exact4(void){
  build_w(4);
  uint64_t (*dp)[4]=calloc((size_t)1<<26, 32);
  dp[0][0]=1;
  clock_t t0=clock();
  for(uint32_t mask=1; mask; mask++){
    int s=__builtin_popcount(mask); int lo=jlo(s),hi=jhi(s); if(lo>hi) { if(mask==FULL) break; continue; }
    int low=__builtin_ctz(mask); uint32_t rest=mask&~(1u<<low);
    int bits[26],nb=0; for(uint32_t r=rest;r;r&=r-1) bits[nb++]=__builtin_ctz(r);
    uint64_t acc[4]={0,0,0,0};
    #define ADD(B,sz) do{ uint32_t _B=(B); int ww=w16[_B]; if(ww){ uint32_t prev=mask^_B; int sp=s-(sz); int plo=jlo(sp),phi=jhi(sp); \
        for(int j=lo;j<=hi;j++){ int jp=j-1; if(jp>=plo&&jp<=phi) acc[j-lo]+= (uint64_t)ww*dp[prev][jp-plo]; } } }while(0)
    ADD(1u<<low,1);
    for(int a=0;a<nb;a++){ uint32_t Ba=(1u<<low)|(1u<<bits[a]); ADD(Ba,2);
      for(int b=a+1;b<nb;b++){ uint32_t Bb=Ba|(1u<<bits[b]); ADD(Bb,3);
        for(int c=b+1;c<nb;c++){ ADD(Bb|(1u<<bits[c]),4); } } }
    for(int j=lo;j<=hi;j++) dp[mask][j-lo]=acc[j-lo];
    if(mask==FULL) break;
  }
  printf("exact: perfect pangrams (10 prime words, each <=4 letters) = %llu  (%.3e)  time %.0fs\n",
         (unsigned long long)dp[FULL][0], (double)dp[FULL][0], (double)(clock()-t0)/CLOCKS_PER_SEC);
}

/* ---------- sampler ---------- */
static uint64_t rs=88172645463325252ULL;
static inline uint64_t rnd(void){ uint64_t x=rs; x^=x>>12; x^=x<<25; x^=x>>27; rs=x; return x*0x2545F4914F6CDD1DULL; }
static uint32_t *bufB; static uint16_t *bufW; static int nbuf; static uint64_t totW;
static int Kg; static int bitsg[26]; static int nbg; static uint32_t lowg; static int nUg, mleft; static uint32_t Ug;
#define FMASK ((1u<<1)|(1u<<3)|(1u<<5)|(1u<<7)|(1u<<9)|(1u<<11)|(1u<<15)|(1u<<17)|(1u<<19)|(1u<<21)|(1u<<23)|(1u<<25))
static void gen(int idx,int cnt,uint32_t m){
  uint32_t B=lowg|m; int sz=cnt+1; int r=nUg-sz;            // feasibility of the remainder
  int feas=0; if(mleft==0){ feas=(r==0); } else if(r>=mleft && r<=Kg*mleft){ uint32_t Up=Ug^B; int fin=__builtin_popcount(Up&FMASK)+((Up>>2)&1)+((Up>>13)&1); feas=(fin>=mleft); }
  if(feas){ int ww=w16[B]; if(ww){ bufB[nbuf]=B; bufW[nbuf]=ww; nbuf++; totW+=ww; } }
  if(cnt+1>=Kg) return;
  for(int i=idx;i<nbg;i++) gen(i+1,cnt+1,m|(1u<<bitsg[i]));
}
typedef struct { uint32_t key; double wsum; double esum; long n; } prof_t;
static prof_t profs[4096]; static int nprof=0;
static void addprof(uint32_t key,double W,double E){ for(int i=0;i<nprof;i++) if(profs[i].key==key){profs[i].wsum+=W;profs[i].esum+=E;profs[i].n++;return;} if(nprof<4096){profs[nprof].key=key;profs[nprof].wsum=W;profs[nprof].esum=E;profs[nprof].n=1;nprof++;} }
static int cmpprof(const void*a,const void*b){ double x=((prof_t*)a)->esum,y=((prof_t*)b)->esum; return x<y?1:x>y?-1:0; }
static void sample(int K,long N,uint64_t seed){
  Kg=K; build_w(K); rs^=seed*0x9E3779B97F4A7C15ULL; bufB=malloc(4u<<20); bufW=malloc(2u<<20);
  double sW=0,sW2=0,sE=0,sE2=0; long hits=0, dead=0; clock_t t0=clock();
  for(long it=0;it<N;it++){
    uint32_t U=FULL; double W=1; uint64_t words[10]; int lens[10]; int ok=1;
    for(int j=0;j<10;j++){
      if(!U){ok=0;break;}
      lowg=1u<<__builtin_ctz(U); uint32_t rest=U&~lowg; nbg=0; for(uint32_t r=rest;r;r&=r-1) bitsg[nbg++]=__builtin_ctz(r);
      Ug=U; nUg=__builtin_popcount(U); mleft=10-j-1; nbuf=0; totW=0; gen(0,0,0);
      if(!totW){ok=0;break;}
      W*=(double)totW; uint64_t r=rnd()%totW; int i=0; while(r>=bufW[i]){ r-=bufW[i]; i++; }
      uint32_t B=bufB[i]; words[j]=nth_word(B,(int)r); lens[j]=__builtin_popcount(B); U^=B;
    }
    if(!ok||U){ dead++; continue; }
    uint64_t tot=0; for(int j=0;j<10;j++) tot+=words[j];
    int bal=0;
    if(!(tot&1)){ uint64_t half=tot/2; for(int m=0;m<512;m++){ if(__builtin_popcount(m)!=4) continue; uint64_t s=words[0]; for(int b=0;b<9;b++) if(m>>b&1) s+=words[b+1]; if(s==half) bal++; } }
    if(bal && hits<3){ printf("  example balanced pangram:"); for(int j=0;j<10;j++){char b[12]; name(words[j],b); printf(" %s",b);} printf("\n"); }
    double E=W*bal; sW+=W; sW2+=W*W; sE+=E; sE2+=E*E; if(bal) hits++;
    int cntl[7]={0}; for(int j=0;j<10;j++) cntl[lens[j]]++; uint32_t key=0; for(int l=1;l<=6;l++) key=key*11+cntl[l];
    addprof(key,W,E);
  }
  double mW=sW/N, seW=sqrt((sW2/N-mW*mW)/N), mE=sE/N, seE=sqrt((sE2/N-mE*mE)/N);
  printf("K=%d N=%ld seed=%llu dead=%ld balanced-hits=%ld time %.0fs\n",K,N,(unsigned long long)seed,dead,hits,(double)(clock()-t0)/CLOCKS_PER_SEC);
  printf("  #pangrams (words<=%d letters): %.4e  +- %.1e (1 s.e.)\n",K,mW,seW);
  printf("  #(pangram, balanced 5|5 split): %.4e  +- %.1e (1 s.e.)\n",mE,seE);
  qsort(profs,nprof,sizeof(prof_t),cmpprof);
  printf("  top length profiles among balanced solutions (counts of 1..%d-letter words : est. share):\n",K);
  for(int i=0;i<nprof&&i<12;i++){ if(profs[i].esum<=0) break; uint32_t key=profs[i].key; int c[7]; for(int l=6;l>=1;l--){c[l]=key%11;key/=11;} printf("    ");
    for(int l=1;l<=K;l++) printf("%d×%d ",c[l],l); printf(": %.1f%%\n",100*profs[i].esum/sE); }
  // one example from the last balanced hit
}
/* ---------- brute-force throughput ---------- */
static uint32_t *wstart; static uint64_t *wlist; static long nwords;
static uint32_t lvlbuf[10][80000]; static long cntP=0,cntE=0; static clock_t tend; static int stop=0; static uint64_t wv[10];
static void dfs(uint32_t U,int j){
  if(stop) return;
  if(j==10){ cntP++; uint64_t tot=0; for(int i=0;i<10;i++) tot+=wv[i]; if(!(tot&1)){ uint64_t half=tot/2; for(int m=0;m<512;m++){ if(__builtin_popcount(m)!=4) continue; uint64_t s=wv[0]; for(int b=0;b<9;b++) if(m>>b&1) s+=wv[b+1]; if(s==half){cntE++;break;} } }
    if((cntP&0xfffff)==0 && clock()>tend) stop=1; return; }
  lowg=1u<<__builtin_ctz(U); uint32_t rest=U&~lowg; nbg=0; for(uint32_t r=rest;r;r&=r-1) bitsg[nbg++]=__builtin_ctz(r);
  Ug=U; nUg=__builtin_popcount(U); mleft=10-j-1; nbuf=0; totW=0; gen(0,0,0);
  uint32_t *myB=lvlbuf[j]; int n=nbuf; memcpy(myB,bufB,n*4);
  for(int i=0;i<n&&!stop;i++){ uint32_t B=myB[i]; for(uint32_t t=wstart[B];t<wstart[B+1];t++){ wv[j]=wlist[t]; dfs(U^B,j+1); } }
}
static void enumerate(int K,int secs){
  Kg=K; build_w(K); bufB=malloc(4u<<20); bufW=malloc(2u<<20);
  wstart=calloc((1u<<26)+1,4); for(uint64_t m=0;m<=FULL;m++) wstart[m+1]=wstart[m]+w16[m];
  nwords=wstart[FULL]+w16[FULL]; wlist=malloc(nwords*8); uint32_t *fill=calloc(1u<<26,4);
  uint64_t lim=pow26(K); for(uint64_t n=2;n<lim;n++){ if(comp[n]) continue; uint32_t m; if(letters_mask(n,&m)){ wlist[wstart[m]+fill[m]++]=n; } }
  tend=clock()+secs*CLOCKS_PER_SEC; clock_t t0=clock(); dfs(FULL,0);
  double el=(double)(clock()-t0)/CLOCKS_PER_SEC;
  printf("brute force K=%d: %.1fs -> %ld pangrams (%.2e/s), %ld with a balanced split\n",K,el,cntP,cntP/el,cntE);
}
int main(int argc,char**argv){
  if(!strcmp(argv[1],"exact4")) exact4();
  else if(!strcmp(argv[1],"sample")) sample(atoi(argv[2]),atol(argv[3]),strtoull(argv[4],0,10));
  else if(!strcmp(argv[1],"enum")) enumerate(atoi(argv[2]),atoi(argv[3]));
  return 0;
}
