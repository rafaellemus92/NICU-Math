// Exact count of Prime-26 perfect pangrams (10 prime words, pairwise-distinct letters, A..Z each once,
// words of <=K letters) by DP over letter subsets, then uniform sampling from the DP to estimate the
// fraction admitting a balanced 5|5 split (an "equation pangram").
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#include <math.h>
#include <time.h>
#define FULL ((1u<<26)-1)
static uint8_t *comp;
static void sieve(uint64_t lim){ comp=calloc(lim,1); comp[0]=comp[1]=1; for(uint64_t i=2;i*i<lim;i++) if(!comp[i]) for(uint64_t j=i*i;j<lim;j+=i) comp[j]=1; }
static uint64_t pow26(int k){ uint64_t r=1; while(k--) r*=26; return r; }
static int letters_mask(uint64_t n, uint32_t*m){ uint32_t mm=0; while(n){ int d=n%26; if(mm>>d&1) return 0; mm|=1u<<d; n/=26;} *m=mm; return 1; }
static void name(uint64_t n,char*b){char t[12];int k=0;while(n){t[k++]='A'+n%26;n/=26;}for(int i=0;i<k;i++)b[i]=t[k-1-i];b[k]=0;}
static uint16_t *w16; static int K;
static int nw_L[26], nw_k, nw_t, nw_cnt; static uint64_t nw_ans;
static int nw_rec(int depth,int used,uint64_t val){
  if(depth==nw_k){ if(!comp[val]){ if(nw_cnt==nw_t){ nw_ans=val; return 1;} nw_cnt++; } return 0; }
  for(int i=0;i<nw_k;i++){ if(used>>i&1) continue; if(depth==0 && nw_L[i]==0) continue; if(nw_rec(depth+1,used|(1<<i),val*26+nw_L[i])) return 1; }
  return 0;
}
static uint64_t nth_word(uint32_t mask,int t){ nw_k=0; for(int b=0;b<26;b++) if(mask>>b&1) nw_L[nw_k++]=b; nw_t=t; nw_cnt=0; nw_ans=0; nw_rec(0,0,0); return nw_ans; }

static inline int jlo(int s){ int a=(s+K-1)/K, b=s-16; return a>b?a:b; }
static inline int jhi(int s){ int a=s, b=10-(26-s+K-1)/K; return a<b?a:b; }
static int WIN; static uint64_t *dp;   /* dp[mask*WIN + (j-jlo(s))] */

static uint64_t rs=88172645463325252ULL;
static inline uint64_t rnd(void){ uint64_t x=rs; x^=x>>12; x^=x<<25; x^=x>>27; rs=x; return x*0x2545F4914F6CDD1DULL; }

/* enumerate all B = low | subset(rest), |B|<=K, calling cb */
static int bits[26], nb; static uint32_t lowbit;
static uint32_t *eB; static uint64_t *eW; static int ne;
static void gen(int idx,int cnt,uint32_t m){
  eB[ne++]=lowbit|m;
  if(cnt+1>=K) return;
  for(int i=idx;i<nb;i++) gen(i+1,cnt+1,m|(1u<<bits[i]));
}
int main(int argc,char**argv){
  K=atoi(argv[1]); long NS=atol(argv[2]); uint64_t seed=strtoull(argv[3],0,10); rs^=seed*0x9E3779B97F4A7C15ULL;
  uint64_t lim=pow26(K); sieve(lim); w16=calloc(1u<<26,2);
  long nwords=0; for(uint64_t n=2;n<lim;n++){ if(comp[n]) continue; uint32_t m; if(letters_mask(n,&m)){ w16[m]++; nwords++; } }
  fprintf(stderr,"K=%d: %ld distinct-letter prime words\n",K,nwords);
  WIN=0; for(int s=0;s<=26;s++){ int d=jhi(s)-jlo(s)+1; if(d>WIN) WIN=d; }
  dp=calloc((size_t)(1u<<26)*WIN,8); if(!dp){fprintf(stderr,"alloc fail\n");return 1;}
  eB=malloc(sizeof(uint32_t)*400000); eW=malloc(sizeof(uint64_t)*400000);
  dp[0]=1; clock_t t0=clock();
  for(uint64_t mask=1; mask<=FULL; mask++){
    int s=__builtin_popcount((uint32_t)mask); int lo=jlo(s),hi=jhi(s); if(lo>hi) continue;
    int low=__builtin_ctz((uint32_t)mask); lowbit=1u<<low; uint32_t rest=(uint32_t)mask&~lowbit;
    nb=0; for(uint32_t r=rest;r;r&=r-1) bits[nb++]=__builtin_ctz(r);
    ne=0; gen(0,0,0);
    uint64_t acc[8]={0};
    for(int i=0;i<ne;i++){ uint32_t B=eB[i]; int ww=w16[B]; if(!ww) continue; uint32_t prev=(uint32_t)mask^B; int sp=s-__builtin_popcount(B); int plo=jlo(sp),phi=jhi(sp);
      uint64_t *dprev=dp+(size_t)prev*WIN;
      for(int j=lo;j<=hi;j++){ int jp=j-1; if(jp>=plo&&jp<=phi) acc[j-lo]+=(uint64_t)ww*dprev[jp-plo]; } }
    uint64_t *d=dp+(size_t)mask*WIN; for(int j=lo;j<=hi;j++) d[j-lo]=acc[j-lo];
    if((mask&0xffffff)==0) fprintf(stderr,"  %.1f%% %.0fs\n",100.0*mask/FULL,(double)(clock()-t0)/CLOCKS_PER_SEC);
  }
  uint64_t total=dp[(size_t)FULL*WIN+0];
  printf("K=%d exact: #perfect pangrams with words <=%d letters = %llu (%.4e)   [%.0fs]\n",K,K,(unsigned long long)total,(double)total,(double)(clock()-t0)/CLOCKS_PER_SEC);
  fflush(stdout);
  for(int a=4;a<argc;a++){ char*spec=argv[a]; uint32_t m=0; int j=0; char*colon=strchr(spec,':'); for(char*c=spec;c<colon;c++) m|=1u<<(*c-'A'); j=atoi(colon+1);
    int s=__builtin_popcount(m); uint64_t v=(j>=jlo(s)&&j<=jhi(s))? dp[(size_t)m*WIN+(j-jlo(s))] : 0; printf("check dp[%s][%d words] = %llu\n",spec,j,(unsigned long long)v); }
  fflush(stdout);
  /* ---- uniform sampling from the DP ---- */
  double sumbal=0, sumbal2=0; long hits=0; clock_t t1=clock();
  typedef struct { uint32_t key; double e; long n; } prof_t; prof_t profs[2048]; int nprof=0;
  int shown=0;
  for(long it=0;it<NS;it++){
    uint32_t mask=FULL; int j=10; uint64_t words[10]; int lens[10]; int ok=1;
    for(int step=0;step<10;step++){
      int s=__builtin_popcount(mask); int low=__builtin_ctz(mask); lowbit=1u<<low; uint32_t rest=mask&~lowbit;
      nb=0; for(uint32_t r=rest;r;r&=r-1) bits[nb++]=__builtin_ctz(r);
      ne=0; gen(0,0,0);
      uint64_t tot=0;
      for(int i=0;i<ne;i++){ uint32_t B=eB[i]; int ww=w16[B]; uint64_t v=0; if(ww){ uint32_t prev=mask^B; int sp=s-__builtin_popcount(B); int plo=jlo(sp),phi=jhi(sp); int jp=j-1; if(jp>=plo&&jp<=phi) v=(uint64_t)ww*dp[(size_t)prev*WIN+(jp-plo)]; } eW[i]=v; tot+=v; }
      if(!tot){ ok=0; break; }
      uint64_t r=rnd()%tot; int i=0; while(r>=eW[i]){ r-=eW[i]; i++; }
      uint32_t B=eB[i]; int t=(int)(r % w16[B]);   /* r < w*dp => arrangement index uniform */
      words[step]=nth_word(B,t); lens[step]=__builtin_popcount(B); mask^=B; j--;
    }
    if(!ok||mask){ fprintf(stderr,"sampling inconsistency\n"); return 1; }
    uint64_t tot=0; for(int q=0;q<10;q++) tot+=words[q]; int bal=0;
    if(!(tot&1)){ uint64_t half=tot/2; for(int m=0;m<512;m++){ if(__builtin_popcount(m)!=4) continue; uint64_t sm=words[0]; for(int b=0;b<9;b++) if(m>>b&1) sm+=words[b+1]; if(sm==half) bal++; } }
    sumbal+=bal; sumbal2+=(double)bal*bal; if(bal) hits++;
    if(bal && shown<4){ shown++; printf("  sample equation pangram:"); for(int q=0;q<10;q++){char b[12]; name(words[q],b); printf(" %s",b);} printf("\n"); fflush(stdout); }
    int c[8]={0}; for(int q=0;q<10;q++) c[lens[q]]++; uint32_t key=0; for(int l=1;l<=K;l++) key=key*11+c[l];
    int f=-1; for(int p=0;p<nprof;p++) if(profs[p].key==key){f=p;break;} if(f<0&&nprof<2048){f=nprof++; profs[f].key=key; profs[f].e=0; profs[f].n=0;} if(f>=0){profs[f].e+=bal; profs[f].n++;}
  }
  double mb=sumbal/NS, se=sqrt((sumbal2/NS-mb*mb)/NS);
  printf("uniform samples: %ld, pangrams with a balanced split: %ld (%.3e per pangram +- %.1e)\n",NS,hits,mb,se);
  printf("=> #equation pangrams (words<=%d letters) ~ %.3e  +- %.1e\n",K,mb*(double)total,se*(double)total);
  printf("sampling time %.0fs\n",(double)(clock()-t1)/CLOCKS_PER_SEC);
  /* profile report: share of all pangrams and of balanced ones */
  for(int a=0;a<nprof;a++) for(int b=a+1;b<nprof;b++) if(profs[b].n>profs[a].n){prof_t t=profs[a];profs[a]=profs[b];profs[b]=t;}
  printf("length profiles (count of 1..%d-letter words): share of pangrams | share of balanced hits\n",K);
  for(int p=0;p<nprof&&p<15;p++){ uint32_t key=profs[p].key; int c[8]; for(int l=K;l>=1;l--){c[l]=key%11;key/=11;} printf("   ");
    for(int l=1;l<=K;l++) printf("%d×%d ",c[l],l); printf(": %5.2f%% | %5.2f%%\n",100.0*profs[p].n/NS, sumbal>0?100.0*profs[p].e/sumbal:0); }
  printf("all profiles with balanced hits (samples, hits, hits/sample):\n");
  for(int p=0;p<nprof;p++){ if(profs[p].e<=0) continue; uint32_t key=profs[p].key; int c[8]; for(int l=K;l>=1;l--){c[l]=key%11;key/=11;} printf("   ");
    for(int l=1;l<=K;l++) printf("%d×%d ",c[l],l); printf(": %ld %.0f %.2e\n",profs[p].n,profs[p].e,profs[p].e/profs[p].n); }
  long nlong=0; double elong=0; for(int p=0;p<nprof;p++){ uint32_t key=profs[p].key; int c[8]; for(int l=K;l>=1;l--){c[l]=key%11;key/=11;} if(c[K]>0){ nlong+=profs[p].n; elong+=profs[p].e; } }
  printf("samples containing a %d-letter word: %ld (%.2f%%), balanced hits among them: %.0f (rate %.2e)\n",K,nlong,100.0*nlong/NS,elong,nlong?elong/nlong:0);
  return 0;
}
