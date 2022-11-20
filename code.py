#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov 19 13:06:51 2022

@author: giuseppecangemi
"""

import pandas_datareader.data as pdr
import pandas as pd
import datetime as dt
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import seaborn as sns


df = pd.read_excel(r"/Users/giuseppecangemi/Desktop/ftse/ftse.xlsx").iloc[:4607]
#iloc4605 per far coincidere lo starting_date con df2 (btp)
df = df[::-1]

#rappresento graficamente il prezzo di chiusura del FTSEMIB
fig, ax = plt.subplots()
ax.plot('Data', 'Ultimo', data=df)
ax.xaxis.set_major_locator(mdates.YearLocator())
ax.set_ylabel("Prezzo Chiusura")
ax.set_title("Serie Storica Prezzo Chiusura FTSEMIB")
for label in ax.get_xticklabels(which='major'):
    label.set(rotation=30, horizontalalignment='right')

df["returns"] = df["Ultimo"] - df["Ultimo"].shift(1)

#plotto i returns del FTSEMIB
plt.plot(df["returns"])
#plotto la distribuzione dei ritorni (FTSEMIB) (segue una normale)
sns.histplot(df["returns"], kde=True, label="Distribuzione dei Returns Giornalieri")
plt.legend()
plt.title("FTSEMIB")

#######################################
#######################################
df2 = pd.read_excel("/Users/giuseppecangemi/Desktop/ftse/btp.xlsx")
df2 = df2[::-1]
df2["returns"] = df2["Ultimo"] - df2["Ultimo"].shift(1)
#rappresento graficamente il rendimento di chiusura del BTP
fig, ax = plt.subplots()
ax.plot('Data', 'Ultimo', data=df2)
ax.xaxis.set_major_locator(mdates.YearLocator())
ax.set_ylabel("Prezzo Chiusura")
ax.set_title("Serie Storica Prezzo Chiusura FTSEMIB")
for label in ax.get_xticklabels(which='major'):
    label.set(rotation=30, horizontalalignment='right')
    
#plotto i returns del BTP
plt.plot(df2["returns"])
#plotto la distribuzione dei ritorni (BTP) (segue una normale)
sns.histplot(df2["returns"], kde=True, label="Distribuzione dei Returns Giornalieri")
plt.legend()
plt.title("BTP")    

#######################################################
# Faccio merge per eliminare i dati con differente data
#######################################################

df_merged = df.merge(df2.drop_duplicates(), on=['Data'], 
                   how='left', indicator=True)
df_merged = df_merged.dropna()


df_merged["rend_ftse"] = (df_merged["Ultimo_x"] - df_merged["Ultimo_x"].shift(1))/df_merged["Ultimo_x"]
df_merged["rend_btp"] = (df_merged["Ultimo_y"] - df_merged["Ultimo_y"].shift(1))/df_merged["Ultimo_y"]

#Distribuzione returns giornalieri intero campione:
plt.plot()
sns.histplot(df_merged["rend_btp"], alpha=0.6, kde=False, bins=80, label="Rendimento BTP")
sns.histplot(df_merged["rend_ftse"], alpha=0.6, kde=False, bins=80, label="Rendimento FTSE")
plt.legend()
plt.title("Distribuzione returns giornalieri intero campione")

rend_x_all = df_merged["rend_ftse"][np.logical_not(np.isnan(df_merged["rend_ftse"]))]
rend_y_all = df_merged["rend_btp"][np.logical_not(np.isnan(df_merged["rend_btp"]))]

#returns btp e ftsemib dal 2004 al 2022
plt.plot(rend_x_all, label="FTSEMIB")
plt.plot(rend_y_all, color="orange", alpha=0.7, label="BTP")
plt.axhline(0, color="black", linestyle="--")
plt.title("Returns giornalieri FTSEMIB-BTP dal 2004 al 2022")
plt.legend()
#correlazione rendimenti intero campione: 24%
corr = np.corrcoef(rend_x_all, rend_y_all)
corr 


prezzo_ftse  = df_merged["Ultimo_x"].dropna()
prezzo_btp  = df_merged["Ultimo_y"].dropna()

data = list()
for i, row in df_merged.iterrows():
    if row["Ultimo_y"] and row["Ultimo_x"] is not None:
        data.append(df_merged["Data"][i])


#mostro graficamente andamento dei due differenti assets:
fig, ax = plt.subplots()
ax.plot(data, prezzo_ftse, label="FTSEMIB")
ax.set_ylabel("FTSEMIB", fontsize=12)
ax.legend(loc="upper left")
ax.xaxis.set_major_locator(mdates.YearLocator())
ax2=ax.twinx()
ax2.plot(prezzo_btp, color="orange", label="BTP")
ax2.set_ylabel("BTP",fontsize=12)
ax2.legend()
ax.set_title("Quotazioni FTSEMIB e BTP dal 2004 al 2022")
for label in ax.get_xticklabels(which='major'):
    label.set(rotation=30, horizontalalignment='right')


#######################################
#######################################

#Ultimo anno!
df_2022 = df_merged.loc[4380:]
df_2022 = df_2022[::-1]
#mostro graficamente andamento dei due differenti assets:
fig, ax = plt.subplots()
ax.plot(df_2022["Data"], df_2022["Ultimo_x"], label="FTSEMIB")
ax.set_ylabel("FTSEMIB", fontsize=12)
ax.legend(loc="upper left")
ax.xaxis.set_major_locator(mdates.MonthLocator())
ax2=ax.twinx()
ax2.plot(df_2022["Data"], df_2022["Ultimo_y"], color="orange", label="BTP")
ax2.set_ylabel("BTP",fontsize=12)
ax2.legend()
ax.set_title("Quotazioni FTSEMIB e Rendimenti BTP nel 2022")
for label in ax.get_xticklabels(which='major'):
    label.set(rotation=30, horizontalalignment='right')


rend_x = (df_2022["Ultimo_x"] - df_2022["Ultimo_x"].shift(1))/df_2022["Ultimo_x"]
rend_y = (df_2022["Ultimo_y"] - df_2022["Ultimo_y"].shift(1))/df_2022["Ultimo_y"]
rend_x = rend_x.dropna()
rend_y = rend_y.dropna()
#returns btp e ftsemib nel 2022
plt.plot(rend_x, label="FTSEMIB")
plt.plot(rend_y, color="orange", label="BTP")
plt.axhline(0, color="black", linestyle="--")
plt.title("Returns giornalieri FTSEMIB-BTP nel 2022")
plt.legend()

#Distribuzione returns giornalieri ultimo anno:
plt.plot()
sns.histplot(rend_x, alpha=0.8, kde=False, bins=80, label="Rendimento BTP")
sns.histplot(rend_y, alpha=0.5, kde=False, bins=80, label="Rendimento FTSE")
plt.legend()
plt.title("Distribuzione returns giornalieri ultimo anno")



rend_x = rend_x[np.logical_not(np.isnan(rend_x))]
print(rend_x)
rend_x = pd.Series(rend_x)
rend_y = rend_y[np.logical_not(np.isnan(rend_y))]
print(rend_y)
rend_y = pd.Series(rend_y)



dataframe = { 'Rendimenti FTSEMIB': rend_x, 'Rendimenti BTP': rend_y }
dataframe = pd.DataFrame(dataframe)

#correlazione rendimenti ultimo anno: poca correlazione 
corr = np.corrcoef(rend_x, rend_y)
corr 

correlation = np.corrcoef(dataframe)
plt.matshow(correlation)
plt.show()
            
#######################################
####################################### 
#CALCOLO L'INDICE DI CORRELAZIONE SETTIMANALE NELL'ULTIMO ANNO.

for i in rend_x:
    for j in rend_y:
        print("Coppia: " + str(i) + "/" + str(j))
        break

#CREO LISTE CORRELAZIONE 2D
start = 4606
end = 4602
corr_list = list()
for i in range(len(rend_x)):
    w_rend_x = rend_x.loc[end:start]
    w_rend_y = rend_y.loc[end:start]
    print(np.corrcoef(w_rend_x, w_rend_y))
    corr_list.append(np.corrcoef(w_rend_x, w_rend_y))
    start -= 5
    end -= 5
#CREO ARRAY CORRELAZIONE 1D
count = 0
arr_corr = list()
for i in range(len(corr_list)):
    c = corr_list[count][1]
    arr_corr.append(c[0])
    count += 1
#ISTOGRAMMA DELLA DISTRIBUZIONE DELLA CORRELAZIONE NEL 2022
sns.histplot(arr_corr, bins=10)



#######################################
####################################### 
#CALCOLO L'INDICE DI CORRELAZIONE SETTIMANALE INTERO CAMPIONE.

#CREO LISTE CORRELAZIONE 2D
start = 4606
end = 4602
corr_list_all = list()
for i in range(len(rend_x)):
    w_rend_x_all = rend_x_all.loc[end:start]
    w_rend_y_all = rend_y_all.loc[end:start]
    print(np.corrcoef(w_rend_x_all, w_rend_y_all))
    corr_list_all.append(np.corrcoef(w_rend_x_all, w_rend_y_all))
    start -= 5
    end -= 5
#CREO ARRAY CORRELAZIONE 1D
count = 0
arr_corr_all = list()
for i in range(len(corr_list_all)):
    c = corr_list_all[count][1]
    arr_corr_all.append(c[0])
    count += 1
#ISTOGRAMMA DELLA DISTRIBUZIONE DELLA CORRELAZIONE intero campione
sns.histplot(arr_corr_all, bins=15)

#confronto le due frequenze
sns.histplot(arr_corr_all, bins=15, label="Distribuzione Correlazione Settimanale Intero Campione")
sns.histplot(arr_corr, bins=15, label = "Distribuzione Correlazione Settimanale nel 2022")
plt.legend()

#creo plot
plt.plot(arr_corr_all)    
plt.plot(arr_corr)     


