import math
c=299792458.0; g=9.80665; c2=c*c
T80=80*365.25*86400
for h in (1,1.7,0.33):
    f=g*h/c2; print(h,f,"80y",f*T80, "per yr",f*365.25*86400,"per day",f*86400)
for gg in (9.780,9.832,9.83): print(gg, gg*1.7/c2*T80)
f17=g*1.7/c2; print("1us",1e-6/f17/(365.25*86400),"yr; 1s",1/f17/(365.25*86400))
print("Chou pred",9.80*0.33/c2,(4.1e-17-9.80*0.33/c2)/1.6e-17, "h from meas", 4.1e-17*c2/9.80, 1.6e-17*c2/9.80)
print("79yr 33cm", 9.80*0.33/c2*79*365.25*86400)
print("Bothwell pred per mm",9.80*1e-3/c2, 9.8e-20/(9.80*1e-3/c2), 2.3e-20/(9.80*1e-3/c2),(1.090e-19-9.8e-20)/2.3e-20)
GM=3.986004418e14; R=6.371e6; print("Earth",GM/(R*c2),GM/(R*c2)*T80)
GMs=1.32712440018e20; AU=1.495978707e11; print("Sun",GMs/(AU*c2),GMs/(AU*c2)*T80)
print("v",1/(2*c2),100/(2*c2))
print("=== solar nu ===")
L=3.828e26; Q=26.731; MeV=1.602176634e-13
# energy to photons per 2 nu: average nu energy loss ~0.6 MeV total => 26.1
rate=2*L/(26.1*MeV); print("nu/s",rate,"flux at AU",rate/(4*math.pi*(AU*100)**2))
Qcalc=(4*1.00782503223-4.00260325413)*931.49410372; print("Q",Qcalc)
fl=6.54e10; print("per s", fl*5000, fl*1e4, "per day",fl*5000*86400, fl*1e4*86400)
tot=5.98e10+4.93e9+1.44e8+2.78e8+2.05e8+5.46e6+5.29e6+7.98e3; print("tot SSM",tot, 5.98e10/tot)
# electrons
ne=70e3*0.549*6.02214076e23; print("ne",ne)
for s in (11.6e-46,3.3e-46): r=5.98e10*s*ne; print("rate",r,r*86400)
# Borexino scaling
mC9H12=9*12.011+12*1.008; e_per=9*6+12; ne_bx=1e8/mC9H12*6.02214076e23*e_per; print("ne bx",ne_bx)
for cpd in (134,134+48.3+2.43): x=cpd*ne/ne_bx; print(cpd,x,x*365.25,x*365.25*80)
print("per neutrino prob 20cm", 3.34e23*1.16e-45*20, "e density", 0.549*6.022e23*1.0)
# ratio K40 betas / interactions
print(3.4e8/0.094, 3.4e8/0.13)
# KCL
print("1e35 vs", 2*L/(26.1*MeV)/1e35)
# coherent recoil
E=0.420; M=15.9949*931.494
print("Tmax keV",2*E**2/(M+2*E)*1e6,"eV")
print("pp nu-e Tmax", 2*E**2/(0.511+2*E))
