/* Exact cover of the 26 letters by dictionary words (bitset Algorithm X).
   usage: xcover <wordfile> <max_solutions> <budget> [full_mask] [max_consonants_per_word]
   wordfile lines: "<mask> <cost>" (decimal). Branches on the uncovered letter
   with the fewest available words.  Prints each solution as a list of
   0-based word indices, then "nodes=... solutions=...".
   Words with cost > remaining budget are unavailable (used for the
   'minimum number of foreign clusters' search). */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
typedef uint64_t u64;
static int N, W;                 /* words, 64-bit words per bitset */
static u64 *bits_letter[26];     /* words containing letter b */
static u64 *bits_costle;         /* [k][W]: words with cost <= k */
static uint32_t *wmask; static int *wcost; static int maxcost;
static long long nodes = 0, nsol = 0, maxsol; static int full = (1<<26)-1;
static int cap = 26;             /* max consonants per word: prune if the uncovered
                                    consonants exceed cap * uncovered vowels */
static const int VOW = (1<<0)|(1<<4)|(1<<8)|(1<<14)|(1<<20)|(1<<24);   /* a e i o u y */
static int chosen[64];
static u64 *stack;               /* avail bitsets per depth */
static void rec(int depth, int covered, int left){
    nodes++;
    if(covered == full){
        nsol++;
        for(int i=0;i<depth;i++) printf("%d ", chosen[i]);
        printf("\n");
        return;
    }
    u64 *avail = stack + (size_t)depth*W;
    {   int unc = full & ~covered;
        int nv = __builtin_popcount(unc & VOW), ncn = __builtin_popcount(unc & ~VOW);
        if(nv == 0 || ncn > cap * nv) return; }
    int best=-1, bestc=1<<30;
    for(int b=0;b<26;b++){
        if((covered>>b & 1) || !(full>>b & 1)) continue;   /* letters outside `full` are never needed */
        int c=0; u64 *lb = bits_letter[b];
        for(int i=0;i<W;i++) c += __builtin_popcountll(avail[i] & lb[i]);
        if(c < bestc){ bestc=c; best=b; if(c==0) return; }
    }
    u64 *lb = bits_letter[best];
    for(int i=0;i<W;i++){
        u64 x = avail[i] & lb[i];
        while(x){
            int t = __builtin_ctzll(x); x &= x-1;
            int w = i*64+t;
            if(wcost[w] > left) continue;
            /* new avail: remove words sharing a letter with w, and words too costly */
            u64 *nav = stack + (size_t)(depth+1)*W;
            memcpy(nav, avail, (size_t)W*8);
            for(int b=0;b<26;b++) if(wmask[w]>>b & 1){ u64 *q=bits_letter[b]; for(int j=0;j<W;j++) nav[j] &= ~q[j]; }
            int nl = left - wcost[w];
            if(nl < maxcost){ u64 *q = bits_costle + (size_t)nl*W; for(int j=0;j<W;j++) nav[j] &= q[j]; }
            chosen[depth] = w;
            rec(depth+1, covered | (int)wmask[w], nl);
            if(nsol >= maxsol) return;
        }
    }
}
int main(int argc, char**argv){
    if(argc<4){ fprintf(stderr,"usage\n"); return 1; }
    FILE*f=fopen(argv[1],"r"); maxsol=atoll(argv[2]); int budget=atoi(argv[3]);
    if(argc>4) full=atoi(argv[4]);
    if(argc>5) cap=atoi(argv[5]);
    int cap=1<<16; wmask=malloc(cap*4); wcost=malloc(cap*4); N=0; maxcost=0;
    unsigned long long m; int c;
    while(fscanf(f,"%llu %d",&m,&c)==2){ if(N==cap){cap*=2; wmask=realloc(wmask,cap*4); wcost=realloc(wcost,cap*4);} wmask[N]=(uint32_t)m; wcost[N]=c; if(c>maxcost)maxcost=c; N++; }
    fclose(f);
    W=(N+63)/64;
    for(int b=0;b<26;b++){ bits_letter[b]=calloc(W,8); }
    bits_costle=calloc((size_t)(maxcost+1)*W,8);
    for(int w=0;w<N;w++){
        for(int b=0;b<26;b++) if(wmask[w]>>b&1) bits_letter[b][w/64] |= 1ULL<<(w%64);
        for(int k=wcost[w];k<=maxcost;k++) bits_costle[(size_t)k*W + w/64] |= 1ULL<<(w%64);
    }
    stack=calloc((size_t)30*W,8);
    for(int i=0;i<W;i++) stack[i]=~0ULL;
    if(N%64) stack[W-1] = (1ULL<<(N%64))-1;
    if(budget < maxcost){ u64*q=bits_costle+(size_t)budget*W; for(int j=0;j<W;j++) stack[j]&=q[j]; }
    rec(0,0,budget);
    printf("nodes=%lld solutions=%lld\n", nodes, nsol);
    return 0;
}
