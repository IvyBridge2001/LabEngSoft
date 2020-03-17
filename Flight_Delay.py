#Data cleaning
print('Processing started...')
import sys
import pandas as pd
import glob as gl
import os.path
from datetime import datetime

#Constants
origin1 = 'ICAO Aeródromo Origem'
origin2 = 'ICAO Aerodromo Origem'
origin3 = 'sg_icao_origem'
destination1 = 'ICAO Aeródromo Destino'
destination2 = 'ICAO Aerodromo Destino'
destination3 = 'sg_icao_destino'
departPreview1 = 'Partida Prevista'
departPreview2 = 'dt_partida_prevista'
departActual1 = 'Partida Real'
departActual2 = 'dt_partida_real'
count = 0

def process(df,pathx,filex,origin,dest,deptPrev,deptAct):
    try:
        df = df.rename(columns={origin:"Origin",dest: "Dest",deptPrev:"Depart Prev",deptAct: "Depart Act"})
        df = df[["Origin","Dest","Depart Prev","Depart Act"]]
        df["Depart Prev"] = pd.to_datetime(df["Depart Prev"],format='%d/%m/%Y %H:%M')
        df["Depart Act"] = pd.to_datetime(df["Depart Act"], format='%d/%m/%Y %H:%M')
        df["Month"] = df["Depart Prev"].dt.month
        df["Day"] = df["Depart Prev"].dt.day
        df["Hour"] = df["Depart Prev"].dt.hour
        df["diff"] = df["Depart Act"] - df["Depart Prev"]
        df["diff"] = (df["diff"]).dt.total_seconds() / 60
        df = df.fillna({'diff': 1})
        df["Delayed"] = [1 if x > 15 else 0 for x in df["diff"]]
        df["Delayed"] = df["Delayed"].astype(float)
        df = df[["Origin","Dest","Month","Day","Hour","Delayed"]]
        df = pd.get_dummies(df, columns=['Origin','Dest'])
        pathy = pathx + '\processed\\' + filex
        df.to_csv(pathy)
        print(pathy+ 'successfully created at ' + str(datetime.now()))
    except Exceptio as e:
        print(e)

#def main(arg1):
def main():
    try:
        fileToClean = "C:\\Users\\danie\\Desktop\\all\\vra_012019.csv" #Tem que ter uma pasta chamada 'processed' dentro do diretório que contém o .csv
        print(fileToClean)
        df = pd.read_csv(fileToClean,sep=';',encoding='latin')
        print("ok")
        print(df.head)
        pathx, filex = os.path.split(fileToClean)
        if origin1 in df:
            print('Processing of file '+filex+'began at'+str(datetime.now()))
            process(df,pathx,filex,origin1,destination1,departPreview1,departActual1)
        elif origin2 in df:
            print('Processing of file '+filex+'began at'+str(datetime.now()))
            process(df,pathx,filex,origin2,destination2,departPreview1,departActual1)
        elif origin3 in df:
            print('Processing of file '+filex+'began at'+str(datetime.now()))
            process(df,pathx,filex,origin3,destination3,departPreview2,departActual2)
        print('Processing finished at ' + str(datetime.now()))
    except Exception as e:
        print(e)

if __name__ == "__main__":
    main()



