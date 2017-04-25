# -*- coding: utf-8 -*-
"""
Created on Wed Sep  7 00:21:20 2016

@author: Nick
"""
import csv
import pandas as pd
from yahoo_finance import Currency
import httplib
import oandapy
import time
from datetime import datetime


rates_csv = {}
remove_this = 'UTC-0000'


accountID = "" # your account ID
OANDA = oandapy.API(environment= "practice", access_token="") # enter your credentials 

GBPTOUSD = Currency('GBPUSD')
USDTOEUR = Currency('USDEUR')
EURTOGBP = Currency('GBPEUR')



def bid_refresh(exchange):
    exchange.refresh()
    return exchange.get_bid()

def ask_refresh(exchange):
    exchange.refresh()
    return exchange.get_ask()


def csv_return():
    GBPTOUSD.refresh()
    time = GBPTOUSD.get_trade_datetime()
    time = time.replace(" ","")
    time = time[:-9]
    refreshed = time,GBPTOUSD.get_bid(),GBPTOUSD.get_ask()
    func_data = [refreshed]
    df = pd.DataFrame(func_data)
    csv_data = df.to_csv(index=False, header=False)
    return csv_data
    


def check_arb(x,y,z):
    x.refresh()
    y.refresh()
    z.refresh()
    x = float(GBPTOUSD.get_bid())
    y= float(USDTOEUR.get_bid())
    z = float(EURTOGBP.get_ask())
    arb = (((1*y)/z)*x)
    return arb
def buy_EUR(amount):
    OANDA.create_order(accountID, instrument="EUR_USD", units=amount, side='buy', type='market')
def buy_USD(amount):
    OANDA.create_order(accountID, instrument="GBP_USD", units=(amount*EUR)/GBP, side='sell', type='market')
def sell_EURtoGBP(amount):
    OANDA.create_order(accountID, instrument="GBP_EUR", units=(amount*EUR), side='sell', type='market')        
def execute_arb():
    buy_EUR(1500)
    time.sleep(2)
    sell_EURtoGBP(1500)
    time.sleep(2)
    buy_USD(1500)

start = time.time()    
def mainFunction():
    while True: 
        arb = check_arb(GBPTOUSD,USDTOEUR,EURTOGBP)
        if arb>1.0005:
            execute_arb()
            print "arbitrage executed"
            print arb
            time.sleep(5)
            
        if arb<1.0005:
            print "no arbitrage availible"
            print arb
            time.sleep(10)

mainFunction()
            

    


    

        
