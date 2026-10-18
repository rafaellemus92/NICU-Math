import math
NA=6.02214076e23; c=299792458.0; hbar_eVs=6.582119569e-16; hbarc=197.3269804
u=931.49410372; mp=938.27208816; mn=939.56542052; me=0.51099895
mH1=1.00782503223; mn_u=1.00866491606; O16=15.99491461957
print("=== Glucose ===")
p=6*6+12+6*8; n=6*6+6*8; print("p,n",p,n,"u",2*p+n,"d",p+2*n,"tot",3*(p+n))
M=72+12*mH1+6*O16; print("mono mass",M, "MeV",M*u)
qm=276*2.16+264*4.70; Mm=M*u; print("quark MeV",qm, qm/Mm*100)
for mu,md in [(2.16-.07,4.70-.07),(2.16+.07,4.70+.07)]:
    print(" range", (276*mu+264*md)/Mm*100)
print("e frac",96*me/Mm*100)
nucsum=96*mp+84*mn; print("nucleon sum",nucsum,"QCD",nucsum-qm,(nucsum-qm)/Mm*100)
B12=(6*mH1+6*mn_u-12)*u; B16=(8*mH1+8*mn_u-O16)*u; print("B12",B12,"B16",B16,"tot",6*B12+6*B16,(6*B12+6*B16)/Mm*100)
free=96*mp+84*mn+96*me; print("free-M",free-Mm)
# oxidation
E=2805.0e3; print("ratio dH",E/(M*1e-3*c**2), "eV/molec", E/NA/1.602176634e-19)
print("dG", 2870e3/(M*1e-3*c**2), 2910e3/(M*1e-3*c**2))
print("2000 kcal mass ng", 2000*4184/c**2*1e12)
# per nucleon
print("p",9.02/mp*100,"n",11.56/mn*100)
print("=== RQ ===")
print(16/23, 1-16/23, 63/77, 1-63/77)
print("met water glu",6*18.015/180.156,"palm",16*18.015/256.43)
# buck
def buck(T): return 0.61121*math.exp((18.678-T/234.5)*(T/(257.14+T)))  # kPa
def absh(T,RH=1): 
    e=buck(T)*1000*RH; return e*0.018015/(8.314462*(T+273.15))*1000
print("abs hum 37",absh(37),"34",absh(34),"20@50%",absh(20,.5))
V=0.5*12*60*24/1000; print("V m3/day",V, V*(absh(37)-absh(20,.5)), V*(absh(34)-absh(20,.5)))
print("=== K40/C14 ===")
yr=365.25*86400
Katoms=140*0.000117/39.0983*NA; lam=math.log(2)/(1.248e9*yr); A=Katoms*lam
print("K40 atoms",Katoms,"mg",Katoms/NA*39.964*1000,"lam",lam,"A",A,"Bq/gK",A/140)
sa=1.176e-12*NA/12.011*math.log(2)/(5700*yr); print("C14 Bq/g",sa, sa*16000, sa*12600)
anu=A*0.8928+sa*16000; nu=A*0.1072; print("anu/s",anu,"/day",anu*86400,"nu/s",nu,"/day",nu*86400,"tot",anu+nu,(anu+nu)*86400)
print("HPS 5000", (5000*0.8928+sa*16000+5000*.1072)*86400)
print("K40 beta- per day",A*0.8928*86400)
print("=== DNA C14 ===")
for Cbp in (19,20):
    Cn=2*3.055e9*Cbp; n14=Cn*1.176e-12; dec=n14*math.log(2)/5700
    print(Cbp,"C/nucleus",Cn,"14C",n14,"dec/yr",dec,"bodyday 3e12",dec*3e12/365.25,"per s",dec*3e12/yr,"80y",dec*3e12*80,"3.72e13*80",dec*3.72e13*80, dec/40)
