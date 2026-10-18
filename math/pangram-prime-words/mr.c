/* Deterministic Miller-Rabin for 64-bit n (the 12 prime bases 2..37 are
   deterministic for all n < 3.3e24, hence for all 64-bit n).  Compiled to a
   shared library and called from Python via ctypes on whole numpy arrays. */
#include <stdint.h>
#include <stddef.h>
typedef unsigned __int128 u128;
static uint64_t mulmod(uint64_t a, uint64_t b, uint64_t m){ return (uint64_t)((u128)a*b % m); }
static uint64_t powmod(uint64_t a, uint64_t e, uint64_t m){
    uint64_t r = 1; a %= m;
    while(e){ if(e&1) r = mulmod(r,a,m); a = mulmod(a,a,m); e >>= 1; }
    return r;
}
int is_prime_u64(uint64_t n){
    if(n < 2) return 0;
    static const uint64_t small[] = {2,3,5,7,11,13,17,19,23,29,31,37};
    for(int i=0;i<12;i++){ if(n==small[i]) return 1; if(n%small[i]==0) return 0; }
    uint64_t d = n-1; int s = 0; while((d&1)==0){ d>>=1; s++; }
    for(int i=0;i<12;i++){
        uint64_t a = small[i];
        uint64_t x = powmod(a,d,n);
        if(x==1 || x==n-1) continue;
        int comp = 1;
        for(int r=1;r<s;r++){ x = mulmod(x,x,n); if(x==n-1){ comp=0; break; } }
        if(comp) return 0;
    }
    return 1;
}
void is_prime_batch(const uint64_t* n, size_t k, uint8_t* out){
    for(size_t i=0;i<k;i++) out[i] = (uint8_t)is_prime_u64(n[i]);
}
