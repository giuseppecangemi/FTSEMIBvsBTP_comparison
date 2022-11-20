#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov 20 17:30:08 2022

@author: giuseppecangemi
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import seaborn as sns

#DATAFRAME PER IL 2022
#ftse
df_2022_ftse = pd.read_excel("/Users/giuseppecangemi/Desktop/ftse/2022_pazzo.xlsx")
df_2022_ftse = df_2022_ftse[::-1]

cap_invested = 10000 #assumo un capitale investito pari a 10k
#calcolo la frazione di ftse acquistabili con 10k
fraz_ftse = cap_invested/df_2022_ftse["Ultimo"][226]

#creo lista del valore giornaliero del ftse acquistato:
return_ftse_plot = list()
for i, row in df_2022_ftse.iterrows():
    return_ftse_plot.append(row["Ultimo"]*fraz_ftse)
    
plt.plot(return_ftse_plot, color="orange")

#btp
df_2022_btp = pd.read_excel("/Users/giuseppecangemi/Desktop/ftse/btp_future10y.xlsx")
df_2022_btp = df_2022_btp[::-1]

#calcolo la frazione di bond acquistabili con 10k
fraz_btp = cap_invested/df_2022_btp["Ultimo"][226]

#creo lista del valore giornaliero dei bonds acquistati:
return_btp_plot = list()
for i, row in df_2022_btp.iterrows():
    return_btp_plot.append(row["Ultimo"]*fraz_btp)
    
plt.plot(return_btp_plot, color="blue")

#calcolo profit-loss
profit_ftse = fraz_ftse*df_2022_ftse["Ultimo"][0]
profit_btp = fraz_btp*df_2022_btp["Ultimo"][0]

if profit_ftse > cap_invested:
    pl_ftse = round(cap_invested-profit_ftse)
    pl_ftse = "FTSE - Profit: " + str(pl_ftse)
    print("FTSE - Profit: " + str(cap_invested-profit_ftse))
elif profit_ftse < cap_invested:
    pl_ftse = round(profit_ftse - cap_invested)
    pl_ftse = "FTSE - Loss: " + str(pl_ftse)
    print("FTSE - Loss: " + str(profit_ftse - cap_invested))
    
if profit_btp > cap_invested:
    pl_btp = round(cap_invested-profit_btp)
    pl_btp = "BTP - Profit: " + str(pl_btp)
    print("BTP - Profit: " + str(cap_invested-profit_btp))
elif profit_btp < cap_invested:
    pl_btp = round(profit_btp - cap_invested)
    pl_btp = "BTP - Loss: " + str(pl_btp)
    print("BTP - Loss: " + str(profit_btp - cap_invested))

plt.plot(return_btp_plot, label="BTP Future 10y")
plt.plot(return_ftse_plot, color="orange", label = "FTSEMIB 40")
plt.axhline(10000, color="black", linestyle="--")
plt.legend()
plt.title("Contronto Profit-Loss (FTSEMIB-BTP) se investissimo 10k tra il 3Gen2022 e il 18Nov2022 \n" + pl_ftse + "/ " + pl_btp)

#CALCOLO LA CORRELAZIONE TRA FTSE-BTP RETURNS
#DF_MERGED PER CREARE DF CON STESSA DIMENSIONE
df_merged = df_2022_ftse.merge(df_2022_btp.drop_duplicates(), on=['Data'], 
                   how='left', indicator=True)
#df_merged = df_merged.dropna()
np.corrcoef(df_merged["Ultimo_x"], df_merged["Ultimo_y"])

######################################################
######################################################
#WHAT'S GOING ON IF WE CONSIDER A LARGER DATAFRAME?
# EX. 2009-2022
df = pd.read_excel(r"/Users/giuseppecangemi/Desktop/ftse/ftse.xlsx").iloc[:3367]
df = df[::-1]

fraz_ftse = cap_invested/df["Ultimo"][3366]
return_ftse = list()
for i, row in df.iterrows():
    return_ftse.append(row["Ultimo"]*fraz_ftse)
    
plt.plot(return_ftse)  

#######################
df2 = pd.read_excel("/Users/giuseppecangemi/Desktop/ftse/btp_all.xlsx")
df2 = df2[::-1]

#FACCIO MERGE PER CONSIDERARE SOLO I DATI CHE COINCIDONO CON IL DATAFRAME DEL FTSEMIB\\
    #CIOè COERENTE CON LE CHIUSURE SETTIMANALI (SABATO-DOMENICA)
df_merged = df.merge(df2.drop_duplicates(), on=['Data'], 
                   how='left', indicator=True)

fraz_btp = cap_invested/df_merged["Ultimo_y"][0]
return_btp = list()
for i, row in df_merged.iterrows():
    return_btp.append(row["Ultimo_y"]*fraz_btp)
    
plt.plot(return_btp)  

df_merged["return_ftse"] = return_ftse
df_merged["return_btp"] = return_btp

#######
#calcolo profit-loss dell'investimento come se dovessimo chiudere posizione al 18/11/22(FTSEMIB):
profit_ftse = fraz_ftse*df_merged["Ultimo_x"][3366]
profit_ftse

#calcolo profit-loss dell'investimento come se dovessimo chiudere posizione al 18/11/22 (BTP):
profit_btp = fraz_btp*df_merged["Ultimo_y"][3366]
profit_btp
#in realtà ha poco senso imho, ma replico l'analisi vista su linkedin
#######

#confronto due grafici (grafico incompleto)
plt.plot(return_btp, label="BTP Future 10y")
plt.plot(return_ftse, color="orange", label = "FTSEMIB 40")
plt.legend()
plt.title("Contronto Profitto (FTSEMIB-BTP) se investissimo 10k il 15Sett2009")

#confronto due grafici
fig, ax = plt.subplots()
ax.plot("Data", "return_ftse", data=df_merged, label="FTSEMIB40")
ax.plot("Data", "return_btp", data=df_merged, color="orange", label="Future BTP 10y")
ax.xaxis.set_major_locator(mdates.YearLocator())
ax.set_ylabel("Profit-Loss", size=14)
plt.axhline(10000, color="black", linestyle="--")
ax.set_title("Confronto Profit-Loss (FTSEMIB40-FutureBTP10y) se investissimo 10k tra il 15Set2009 e il 18Nov2022")
plt.legend()
#for label in ax.get_xticklabels(which='major'):
    #label.set(rotation=30, horizontalalignment='right')

len_profit_ftse = list()
for i, row in df_merged.iterrows():
    if row["return_ftse"] > 10000:
        len_profit_ftse.append(row["Data"])
print(len(len_profit_ftse))        
#581 giorni profittevoli        
        

len_profit_btp = list()
for i, row in df_merged.iterrows():
    if row["return_btp"] > 10000:
        len_profit_btp.append(row["Data"])
print(len(len_profit_btp))
#2536 giorni profittevoli

#distribuzione dei ritorni ftse!
l = list()
for i, row in df_merged.iterrows():
        l.append((row["Ultimo_x"]*fraz_ftse)-10000)
sns.histplot(l, kde=True)
plt.axvline(0, color="red", linestyle="--")
plt.title("Distribuzione Profit-Loss FTSEMIB 40")

#distribuzione dei ritorni btp!
k = list()
for i, row in df_merged.iterrows():
        k.append((row["Ultimo_y"]*fraz_btp)-10000)
sns.histplot(k, kde=True)
plt.axvline(0, color="red", linestyle="--")
plt.title("Distribuzione Profit-Loss Future BTP 10y")

#si potrebbe migliorare l'analisi calcolando l'integrale dell'area sottesa le curve. 

