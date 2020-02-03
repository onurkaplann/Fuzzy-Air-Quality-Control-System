# -*- coding: utf-8 -*-
"""
Created on Wed Dec 11 17:54:06 2019

@author: Onur
"""
import skfuzzy as fuzz
import pymysql as mysql
import numpy as np
import matplotlib.pyplot as plt
from array import array

conn = mysql.connect(user="root",passwd="",host="127.0.0.1",port=3306,database="fuzzy")
cursor = conn.cursor()
sql_query = "SELECT * FROM fuzzy.kocaeli_izmit_mthm"

PM10_L = []
NO2_L  = []
CO_L   = []
HKİ_defuz_L = []
HKİ_result_L = []

try :
    cursor.execute(sql_query)
    results = cursor.fetchall()
    for record in results :
        PM10_L.append(int(record[2]))
        NO2_L.append(int(record[3]))
        CO_L.append(int(record[4]))     
        
except Exception as e :
    print("Exception : ",e)

conn.close()

"""
PM10 = np.array(PM10)
NO2 = np.array(NO2)
CO = np.array(CO)
"""

PM10 = np.arange(0,531,1)
NO2 = np.arange(0,2011,1)
CO = np.arange(0,32011,1)
HKİ = np.arange(0,501,1)

#pm10_low = fuzz.trapmf(PM10,[0,0,40,75])
pm10_low = fuzz.trimf(PM10,[0,0,75])
pm10_medium = fuzz.trimf(PM10,[40,150,260])
pm10_high = fuzz.trimf(PM10,[180,530,530])
#pm10_high = fuzz.trapmf(PM10,[180,260,530,530])

#no2_low = fuzz.trapmf(NO2,[0,0,50,150])
no2_low = fuzz.trimf(NO2,[0,0,150])
no2_medium = fuzz.trimf(NO2,[50,275,550])
no2_high = fuzz.trimf(NO2,[300,2010,2010])
#no2_high = fuzz.trapmf(NO2,[300,550,2010,2010])

#co_low = fuzz.trapmf(CO,[0,0,4000,7750])
co_low = fuzz.trimf(CO,[0,0,7750])
co_medium = fuzz.trimf(CO,[4000,10000,16000])
co_high = fuzz.trimf(CO,[12000,32010,32010])
#co_high = fuzz.trapmf(CO,[12000,16000,32010,32010])

#hki_good = fuzz.trapmf(HKİ,[0,0,40,60])
hki_good = fuzz.trimf(HKİ,[0,0,60])
hki_medium = fuzz.trimf(HKİ,[40,75,110])
hki_delicate = fuzz.trimf(HKİ,[90,130,170])
hki_unhealty = fuzz.trimf(HKİ,[130,175,220])
hki_bad = fuzz.trimf(HKİ,[180,250,320])
hki_dangerous = fuzz.trimf(HKİ,[280,500,500])
#hki_dangerous = fuzz.trapmf(HKİ,[280,320,500,500])

"""
fig, (ax0, ax1, ax2, ax3) = plt.subplots(nrows=4, figsize=(8, 8))
    
ax0.plot(PM10,pm10_low,'b',linewidth=1.5, label='Düşük')
ax0.plot(PM10,pm10_medium,'g',linewidth=1.5, label='Orta')
ax0.plot(PM10,pm10_high,'r',linewidth=1.5, label='Yüksek')
ax0.set_title('PM10')
ax0.legend()

ax1.plot(NO2,no2_low,'b',linewidth=1.5, label='Düşük')
ax1.plot(NO2,no2_medium,'g',linewidth=1.5, label='Orta')
ax1.plot(NO2,no2_high,'r',linewidth=1.5, label='Yüksek')
ax1.set_title('NO2')
ax1.legend()

ax2.plot(CO,co_low,'b',linewidth=1.5, label='Düşük')
ax2.plot(CO,co_medium,'g',linewidth=1.5, label='Orta')
ax2.plot(CO,co_high,'r',linewidth=1.5, label='Yüksek')
ax2.set_title('CO')
ax2.legend()

ax3.plot(HKİ,hki_good,'b',linewidth=1.5, label='İyi')
ax3.plot(HKİ,hki_medium,'g',linewidth=1.5, label='Orta')
ax3.plot(HKİ,hki_delicate,'r',linewidth=1.5, label='Hassas')
ax3.plot(HKİ,hki_unhealty,'p',linewidth=1.5, label='Sağlıksız')
ax3.plot(HKİ,hki_bad,'y',linewidth=1.5, label='Kötü')
ax3.plot(HKİ,hki_dangerous,'o',linewidth=1.5, label='Tehlikeli')
ax3.set_title('HKİ')
ax3.legend()

for ax in (ax0, ax1, ax2, ax3):
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.get_xaxis().tick_bottom()
    ax.get_yaxis().tick_left()

plt.tight_layout()
"""
temp=0
for i in range(len(PM10_L)):
    
    pm10_level_low = fuzz.interp_membership(PM10,pm10_low,PM10_L[i])
    pm10_level_medium = fuzz.interp_membership(PM10,pm10_medium,PM10_L[i])
    pm10_level_high = fuzz.interp_membership(PM10,pm10_high,PM10_L[i])
    
    no2_level_low = fuzz.interp_membership(NO2,no2_low,NO2_L[i])
    no2_level_medium = fuzz.interp_membership(NO2,no2_medium,NO2_L[i])
    no2_level_high = fuzz.interp_membership(NO2,no2_high,NO2_L[i])
    
    co_level_low = fuzz.interp_membership(CO,co_low,CO_L[i])
    co_level_medium = fuzz.interp_membership(CO,co_medium,CO_L[i])
    co_level_high = fuzz.interp_membership(CO,co_high,CO_L[i])
    
    ######################### KURAL 1 ##############################################
    ar11 = np.fmax(pm10_level_low,no2_level_low)
    active_rule1 = np.fmax(ar11,co_level_low)
    #######################################################################
    
    ######################## KURAL 2 ###############################################
    ar211 =np.fmin(pm10_level_low,no2_level_low)
    ar21 = np.fmin(ar211,co_level_medium)
    
    ar221 =np.fmin(pm10_level_low,no2_level_medium)
    ar22 = np.fmin(ar221,co_level_low)
    
    ar231=np.fmin(pm10_level_medium,no2_level_low)
    ar23 = np.fmin(ar231,co_level_low)
    
    ar24= np.fmax(ar21,ar22)
    active_rule2 = np.fmax(ar24,ar23)
    #######################################################################
    
    ######################## KURAL 3 ###############################################
    ar3111=np.fmin(pm10_level_low,no2_level_medium)
    ar311=np.fmin(ar3111,co_level_medium)
    ar3121=np.fmin(pm10_level_medium,no2_level_low)
    ar312=np.fmin(ar3121,co_level_medium)
    
    ar3131=np.fmin(pm10_level_medium,no2_level_medium)
    ar313=np.fmin(ar3131,co_level_low)
    
    ar314=np.fmax(ar311,ar312)
    ar31 =  np.fmax(ar314,ar313)
    
    ar3211 =np.fmin(pm10_level_low,no2_level_low)
    ar321 = np.fmin(ar3211,co_level_high)
    
    ar3221 =np.fmin(pm10_level_low,no2_level_high)
    ar322 = np.fmin(ar3221,co_level_low)
    
    ar3231 =np.fmin(pm10_level_high,no2_level_low)
    ar323 = np.fmin(ar3231,co_level_low)
    
    ar324=np.fmax(ar321,ar322)
    ar32 =  np.fmax(ar324,ar323)
    
    active_rule3 = np.fmax(ar31,ar32)
    #######################################################################
    
    ######################## KURAL 4 ###############################################
    
    ar4111=np.fmin(pm10_level_low,no2_level_medium)
    ar411=np.fmin(ar4111,co_level_high)
    
    ar4121=np.fmin(pm10_level_low,no2_level_high)
    ar412=np.fmin(ar4121,co_level_medium)
    
    ar4131=np.fmin(pm10_level_medium,no2_level_low)
    ar413=np.fmin(ar4131,co_level_high)
    
    ar414= np.fmax(ar411,ar412)
    ar41 = np.fmax(ar414,ar413)
    
    ar4211=np.fmin(pm10_level_medium,no2_level_high)
    ar421=np.fmin(ar4211,co_level_low)
    
    ar4221=np.fmin(pm10_level_high,no2_level_medium)
    ar422=np.fmin(ar4221,co_level_low)
    
    ar42 = np.fmax(ar421,ar422)
    
    ar4311=np.fmin(pm10_level_high,no2_level_low)
    ar431 = np.fmin(ar4311,co_level_medium)
    
    ar4321=np.fmin(pm10_level_medium,no2_level_medium)
    ar432 =np.fmin(ar4321,co_level_medium)
    
    ar43 = np.fmax(ar431,ar432)
    
    ar44=np.fmax(ar41,ar42)
    active_rule4 = np.fmax(ar44,ar43)
    #######################################################################
    
    ######################## KURAL 5 ###############################################
    
    ar5111=np.fmin(pm10_level_medium,no2_level_medium)
    ar511=np.fmin(ar5111,co_level_high)
    
    ar5121=np.fmin(pm10_level_medium,no2_level_high)
    ar512=np.fmin(ar5121,co_level_medium)
    
    ar5131=np.fmin(pm10_level_high,no2_level_medium)
    ar513=np.fmin(ar5131,co_level_medium)
    
    ar514=np.fmax(ar511,ar512)
    ar51 = np.fmax(ar514,ar513)
    
    
    ar5211=np.fmin(pm10_level_low,no2_level_high)
    ar521=np.fmin(ar5211,co_level_high)
    
    ar5221=np.fmin(pm10_level_high,no2_level_low)
    ar522=np.fmin(ar5221,co_level_high)
    
    ar5231=np.fmin(pm10_level_high,no2_level_high)
    ar523=np.fmin(ar5231,co_level_low)
    
    ar524=np.fmax(ar521,ar522)
    ar52 = np.fmax(ar524,ar523)
    
    active_rule5 = np.fmax(ar51,ar52)
    #######################################################################
    
    ######################## KURAL 6 ###############################################
    
    ar6111=np.fmin(pm10_level_medium,no2_level_high)
    ar611=np.fmin(ar6111,co_level_high)
    
    ar6121=np.fmin(pm10_level_high,no2_level_medium)
    ar612=np.fmin(ar6121,co_level_high)
    
    ar61 = np.fmax(ar611,ar612)
    
    ar6211= np.fmin(pm10_level_high,no2_level_high)
    ar621= np.fmin(ar6211,co_level_medium)
    
    ar6221=np.fmin(pm10_level_high,no2_level_high)
    ar622=np.fmin(ar6221,co_level_high)
    
    ar62 = np.fmax(ar621,ar622)
    
    active_rule6 = np.fmax(ar61,ar62)
    #######################################################################
    
    hki_activation_good = np.fmin(active_rule1,hki_good)
    hki_activation_medium = np.fmin(active_rule2,hki_medium)
    hki_activation_delicate = np.fmin(active_rule3,hki_delicate)
    hki_activation_unhealty = np.fmin(active_rule4,hki_unhealty)
    hki_activation_bad = np.fmin(active_rule5,hki_bad)
    hki_activation_dangerous = np.fmin(active_rule6,hki_dangerous)
    
    HKİ0 = np.zeros_like(HKİ)

    """
    fig, rule = plt.subplots(figsize=(8, 8))
    
    rule.fill_between(HKİ,HKİ0,hki_activation_good,facecolor='b',alpha=0.7)
    rule.plot(HKİ,hki_good,'b',linewidth=0.5,linestyle='--')
    rule.fill_between(HKİ,HKİ0,hki_activation_medium,facecolor='g',alpha=0.7)
    rule.plot(HKİ,hki_medium,'g',linewidth=0.5,linestyle='--')
    rule.fill_between(HKİ,HKİ0,hki_activation_delicate,facecolor='r',alpha=0.7)
    rule.plot(HKİ,hki_delicate,'r',linewidth=0.5,linestyle='--')
    rule.fill_between(HKİ,HKİ0,hki_activation_unhealty,facecolor='b',alpha=0.7)
    rule.plot(HKİ,hki_unhealty,'b',linewidth=0.5,linestyle='--')
    rule.fill_between(HKİ,HKİ0,hki_activation_bad,facecolor='g',alpha=0.7)
    rule.plot(HKİ,hki_bad,'g',linewidth=0.5,linestyle='--')
    rule.fill_between(HKİ,HKİ0,hki_activation_dangerous,facecolor='r',alpha=0.7)
    rule.plot(HKİ,hki_dangerous,'r',linewidth=0.5,linestyle='--')
    rule.set_title('Output membership activity')
    
    
    rule.spines['top'].set_visible(False)
    rule.spines['right'].set_visible(False)
    rule.get_xaxis().tick_bottom()
    rule.get_yaxis().tick_left()
    
    plt.tight_layout()
    """

    hki_activation1 = np.fmax(hki_activation_good,hki_activation_medium)
    hki_activation2 = np.fmax(hki_activation_delicate,hki_activation_unhealty)
    hki_activation3 = np.fmax(hki_activation_bad,hki_activation_dangerous)
    hki_activation4 = np.fmax(hki_activation1,hki_activation2)
    
    aggregated = np.fmax(hki_activation3,hki_activation4)
    
    HKİ_defuz = fuzz.defuzz(HKİ,aggregated,'centroid')
    hki_result = fuzz.interp_membership(HKİ, aggregated, HKİ_defuz)

    """
    fig, result = plt.subplots(figsize=(8, 8))
    
    result.plot(HKİ, hki_good, 'b', linewidth=0.5, linestyle='--', )
    result.plot(HKİ, hki_medium, 'g', linewidth=0.5, linestyle='--')
    result.plot(HKİ, hki_delicate, 'r', linewidth=0.5, linestyle='--')
    result.plot(HKİ, hki_unhealty, 'b', linewidth=0.5, linestyle='--', )
    result.plot(HKİ, hki_bad, 'g', linewidth=0.5, linestyle='--')
    result.plot(HKİ, hki_dangerous, 'r', linewidth=0.5, linestyle='--')
    
    result.fill_between(HKİ, HKİ0, aggregated, facecolor='Orange', alpha=0.7)
    result.plot([HKİ_defuz, HKİ_defuz], [0, hki_result], 'k', linewidth=1.5, alpha=0.9)
    result.set_title('Aggregated membership and result (line)')
    
    rule.spines['top'].set_visible(False)
    rule.spines['right'].set_visible(False)
    rule.get_xaxis().tick_bottom()
    rule.get_yaxis().tick_left()
    
    plt.tight_layout()
    """
    HKİ_defuz_L.append(HKİ_defuz)
    HKİ_result_L.append(hki_result)  
    print("HKİ:",HKİ_defuz)
    temp += 1
    if(temp%(4200)==0):
        print(".")
    

hki_avg = sum(HKİ_defuz_L)/len(HKİ_defuz_L)
print("ortalama: ",hki_avg)
print("Max hki --> ",max(HKİ_defuz_L))
print("Min hki --> ",min(HKİ_defuz_L))
"""
#for i in range(len(HKİ_defuz_L)):
fig, grafik = plt.subplots(figsize=(8, 8))
grafik.plot(HKİ_defuz_L,HKİ_result_L,'b',linewidth=1.5, label='HKİ')
grafik.set_title('HKİ')
grafik.legend()

fig, grafik2 = plt.subplots(figsize=(8, 8))
grafik2.plot(HKİ_result_L,HKİ_defuz_L,'r',linewidth=1.5, label='HKİ')
grafik2.set_title('HKİ')
grafik2.legend()
"""
"""
fig, plt2 = plt.subplots(figsize=(20, 20))
plt2.scatter(HKİ_defuz_L,HKİ_result_L,s=1)

print("Max hki --> ",max(HKİ_defuz_L))
print("Min hki --> ",min(HKİ_defuz_L))
"""

