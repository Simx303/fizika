import math, time
import os
# import numpy as np
# import matplotlib.pyplot as plt


# Nustatymai
eina =True
timestep = 0.01 # delta t. dt
ratas = 0
FPS=10

# duomenys = np.empty((6,6))

# Konstantos
G = 6.67430e-11 # gravitacija
M = 0.0289644 #mase
R = 8.3144598 #r nr

# Erdve
ti=0 # laikrodis
r=6371 # km
rg=6375.4 # km standartinei gravitacijai
m_zeme=5.9722e24 # kg
g0=G*m_zeme/((rg*1000)**2)
# print(g0)

# oro pasi...
T_b = 288.15
rho_b = 1.2250 # tankis
P_b=101325 # Pa
h_b = 0

# Kunas
x = 0
y = 10000 # m
m_dry=3691 # tuscias kg
m_f=10912/2# degalai

a=0
m=m_f+m_dry

# VARIKLIS
Isp=322 # vakume
max_m_d=75 # kg/s
A_e=0.25*3.14*(1.2**2)# m^2

v_evac=Isp*g0
m_d=0 # GALIAA
Thrust=0 # N

# oro pasipriesinimas 
CD = 0.58 # koficientas.... nebegaliu. kamuolys 0.47
A = 0.25*3.14*(1.5**2) # skerspjuvio plotas (pi*r^2).
Fd=0
atmo=0


v0 = 0
vl=v0
v = v0

ending= 0

totalt = 0

#skrydzio duomenys .csv
h = open("./skr/s"+str(len(os.listdir('./skr')))+".csv", 'a')
h.write("t,y,v,a\n")

# kirsti kampa. optimizacija
#kk1=0.5*CD*A*rho_b
#kk2=-g0*M
#kk3=R*T_b
# v = math.sqrt((2*m*g0)/(rho_b*A*CD))

# sekti raketos pakopas.
stg = [0,0,0]

print(len(stg))

pradzia=time.time()
while eina:
    # Atmosfera. Gravitacija aukstyje.
    atmo=math.exp((-g0*M*(y-h_b))/(R*T_b))
    Fd=0.5*CD*A*rho_b*(v**2)*atmo
    grav = -g0 * ((r/(r+y))**2)

    # VARIKLISSS. is jungia jei be degalu. leidzia tik max
    if m_d>0 and m_f>max_m_d:
        m_f=m_f- m_d*timestep
        Thrust=(m_d * v_evac) - (A_e * P_b*atmo)
    else:
        Thrust=0
      
    m=m_dry+m_f

    a = grav + Fd/m + Thrust/m
    v = v + timestep*a
    y = y+timestep*v
    
    gforce = a/9.8
    print("".join([str(round(n,3)).ljust(12) for n in [ti,y,v,a/9.8,Fd,Thrust,m_f]]))
    # duomenys = np.append(duomenys,[[ti,y,v,a,Fd,Thrust]],axis=0)
    
    h.write(f"{ti},{y},{v},{a},{Thrust},{m_f}\n")
    # jei ismigo i zeme. >7m/s
    if y <= 0 and v<-7:
        print("".join([str(round(n,3)).ljust(12) for n in [ti,y,v,a/9.8,Fd,Thrust]]))
        print("CRASH!!!!")
        break
    elif y<2000-19 and len(stg)==3: # 1a pakopa. MAX_THROT kai aukstis < 1981m
        stg.pop()
        m_d = max_m_d
        print("FIRE")
    elif y<0 and len(stg)<=1: # jei paliete zeme. <7m/s
        break
    elif v>=-1 and len(stg)==2: # 2a pakopa. OFF_THROT kai greitis < 1m/s
        stg.pop()
        m_d = 0
      
    ratas=ratas+1;
    ti=ratas*timestep; # ir isnaujo...
h.close()
print(pradzia-time.time())
print(f"Trenksmas su: {str(0.5*m*v**2)}J") # K=0.5mv^2 blablabla

# plt.plot(duomenys[:,0],duomenys[:,1],label="Aukstis")
# plt.plot(duomenys[:,0],duomenys[:,2],label="Greitis")
# plt.plot(duomenys[:,0],duomenys[:,3],label="Pagreitis")
# plt.plot(duomenys[:,0],duomenys[:,4],label="Oro pasipriesinimas")
# plt.show()
