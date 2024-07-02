from fyers_api import fyersModel
from fyers_api import accessToken
import tkinter as tk
from tkinter import ttk
from tkinter import *
import requests
import pandas as pd
import time

app_id='RES3PU5SCE-100'
secret_id='HATLQJ7BFE'
redirect_uri='https://trade.fyers.in/api-login/redirect-uri/index.html'

session=accessToken.SessionModel(client_id=app_id,secret_key=secret_id,
redirect_uri=redirect_uri, response_type='code', grant_type='authorization_code')
session.set_token(input(f"\nGo To This Link And Copy The Authorization Code And Paste Below And Press Enter:\n\n{session.generate_authcode()}\n\nAuthorization code: "))
response = session.generate_token()
access_token = response["access_token"]
fyers = fyersModel.FyersModel(client_id=app_id, token=access_token)

win = tk.Tk()
win.title("Order Placer For BankNifty")
win.geometry("315x170")

with requests.get("https://public.fyers.in/sym_details/NSE_FO.csv") as rq:
    with open("instrument.csv", 'wb') as file:
        file.write(rq.content)
df=pd.read_csv("instrument.csv",names=[0,1,2,3,4,5,6,7,8,9,10,11,12,13])
df=df[df[13]=='BANKNIFTY']

def check(a,b):
    if a.get()==1:
        b.set('0')
    elif a.get()==0:
        b.set('1')

QTYtext = ttk.Label(win,text='QTY.',font= ('Goudy old style', 10)).place(x=15,y=20)
QTY = ttk.Entry(win,width=10)
QTY.place(x=15,y=45)


SPRICEtext = ttk.Label(win,text='STRIKE PRICE',font= ('Goudy old style', 10)).place(x=115,y=20)
SPRICE = ttk.Entry(win,width=10)
SPRICE.place(x=115,y=45)

def CEf():
    check(var7,var8)
var7 = tk.IntVar()
CEB = ttk.Checkbutton(win,text='CE',variable = var7,command=CEf).place(x=215,y=45)

def PEf():
    check(var8,var7)
var8 = tk.IntVar()
PEB = ttk.Checkbutton(win,text='PE',variable = var8,command=PEf).place(x=260,y=45)

def CBf():
    check(var5,var6)
var5 = tk.IntVar()
CB = ttk.Checkbutton(win,text='CURRENT EXPIRY',variable = var5,command=CBf).place(x=50,y=85)
var5.set('1')

def NBf():
    check(var6,var5)
var6 = tk.IntVar()
NB = ttk.Checkbutton(win,text='NEXT EXPIRY',variable = var6,command=NBf).place(x=170,y=85)

#buttons
def button2f():
    if int(QTY.get())%25!=0:
        print('Please give the quantity in the multiple of 25')
        return True
    
    if var7.get()==1:
        pc='CE'
    elif var8.get()==1:
        pc='PE' 
    elif var7.get()==0 and var8.get()==0:
        print("Please select CE or PE")
        return True
    
    try:
        if var5.get()==1:
            symbol=(df[df[1].str.contains(SPRICE.get()) & df[1].str.contains(pc)][9].iloc[0])
        elif var6.get()==1:
            symbol=(df[df[1].str.contains(SPRICE.get()) & df[1].str.contains(pc)][9].iloc[1])
    except:
        print('Please give correct strike price')
        return True
    
    print(fyers.place_order({
        "symbol":symbol,
        "qty":int(QTY.get()),
        "type":2,
        "side":1,
        "productType":"MARGIN",
        "limitPrice":0,
        "stopPrice":0,
        "validity":"DAY",
        "disclosedQty":0,
        "offlineOrder":"False",
        "stopLoss":0,
        "takeProfit":0
    }))
    ltpd=fyers.quotes({"symbols":symbol})
    ltpi=0
    while (ltpd['s']!='ok') or (ltpd['d'][0]['s']!='ok'):
        ltpd= fyers.quotes({"symbols":symbol})
        ltpi+=1
        if ltpi==9:
            print("API error for sl order")
            break
    ltp=ltpd['d'][0]['v']['lp']
    time.sleep(4)
    print(fyers.place_order({
        "symbol":symbol,
        "qty":int(QTY.get()),
        "type":4,
        "side":-1,
        "productType":"MARGIN",
        "limitPrice":round((ltp-20),2),
        "stopPrice":round((ltp-19.95),2),
        "validity":"DAY",
        "disclosedQty":0,
        "offlineOrder":"False",
        "stopLoss":0,
        "takeProfit":0
    }))
    SPRICE.delete('0','end')
    QTY.delete('0','end')
    var7.set('0')
    var8.set('0')
    if var6.get()==1:
        var6.set('0')
        var5.set('1')
    
button2 = ttk.Button(win,text="BUY",command=button2f)
button2.place(x=115,y=120)

win.mainloop()