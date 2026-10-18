/* Independent check of the free-regime count: stage DP over the 6 vowels.
   dp[S] = number of ways to choose words for the vowels processed so far
   whose consonant sets are pairwise disjoint with union S (S over 2^20).
   Input: for each vowel, a list of (consonant mask, multiplicity) of prime words.
   Output: dp_final[full] (unsigned 128-bit, printed in decimal). */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
typedef unsigned __int128 u128;
static void print128(u128 x){ char b[64]; int i=63; b[i]=0; if(!x){printf("0");return;} while(x){ b[--i]='0'+(int)(x%10); x/=10; } printf("%s", b+i); }
int main(int argc,char**argv){
    FILE*f=fopen(argv[1],"r"); const int NS=1<<20;
    uint64_t *dp=calloc(NS,8), *nd=calloc(NS,8); dp[0]=1;
    u128 full=0;
    for(int v=0;v<6;v++){
        int n; if(fscanf(f,"%d",&n)!=1) return 1;
        unsigned *tm=malloc(n*4); unsigned *tc=malloc(n*4);
        for(int i=0;i<n;i++){ unsigned long long m; unsigned c; fscanf(f,"%llu %u",&m,&c); tm[i]=(unsigned)m; tc[i]=c; }
        memset(nd,0,(size_t)NS*8);
        for(int S=0;S<NS;S++){ uint64_t d=dp[S]; if(!d) continue;
            for(int i=0;i<n;i++){ if(tm[i]&S) continue; nd[S|tm[i]] += d*tc[i]; } }
        uint64_t*t=dp; dp=nd; nd=t; free(tm); free(tc);
        fprintf(stderr,"stage %d done\n",v);
    }
    printf("count = "); print128((u128)dp[NS-1]); printf("\n");
    return 0;
}
