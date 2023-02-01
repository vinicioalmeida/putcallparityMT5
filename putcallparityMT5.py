import MetaTrader5 as mt5
import pandas as pd
import numpy as np
import time
from threading import Thread
from datetime import datetime

mt5.initialize()

def putcall(ativo,call,put,k):
    r=0.1375      
    t=24/252      
    cost=20             
    lot=100           
    deviation=2        

    mt5.initialize()
    mt5.symbol_select(ativo,True)
    mt5.symbol_select(call,True)
    mt5.symbol_select(put,True)

    scan=0
    abre=0
    tentativain=0
    
    while scan < 1:
        time.sleep(1)
        lasttickativo=mt5.symbol_info_tick(ativo)
        lasttickcall=mt5.symbol_info_tick(call)
        lasttickput=mt5.symbol_info_tick(put)
        precob=lasttickativo.bid
        precoa=lasttickativo.ask
        callb=lasttickcall.bid
        calla=lasttickcall.ask
        putb=lasttickput.bid
        puta=lasttickput.ask
        uLEE=(callb+k*np.exp(-r*t))-(puta+precoa) 
        uLDE=(putb+precob)-(calla+k*np.exp(-r*t)) 

        if uLEE>0:
            print('vende call, compra ativo e put')
            request = {
            "action": mt5.TRADE_ACTION_DEAL,
            "symbol": call,
            "volume": float(lot),
            "type": mt5.ORDER_TYPE_SELL,
            "price": callb,
            "deviation": deviation,
            "magic": 123456,
            "comment": "venda",
            "type_time": mt5.ORDER_TIME_GTC,
            "type_filling": mt5.ORDER_FILLING_RETURN
            }
            result = mt5.order_send(request)
            callbe=result[4]
            print(result)
            request = {
            "action": mt5.TRADE_ACTION_DEAL,
            "symbol": put,
            "volume": float(lot),
            "type": mt5.ORDER_TYPE_BUY,
            "price": puta,
            "deviation": deviation,
            "magic": 123456,
            "comment": "compra",
            "type_time": mt5.ORDER_TIME_GTC,
            "type_filling": mt5.ORDER_FILLING_RETURN
            }
            result = mt5.order_send(request)
            putae=result[4]
            print(result)
            request = {
            "action": mt5.TRADE_ACTION_DEAL,
            "symbol": ativo,
            "volume": float(lot),
            "type": mt5.ORDER_TYPE_BUY,
            "price": precoa,
            "deviation": deviation,
            "magic": 123456,
            "comment": "compra",
            "type_time": mt5.ORDER_TIME_GTC,
            "type_filling": mt5.ORDER_FILLING_RETURN
            }
            result = mt5.order_send(request)
            precoae=result[4]
            print(result)
            abre=1
            scan=1      
        else:
            if uLDE>0:
                request = {
                "action": mt5.TRADE_ACTION_DEAL,
                "symbol": call,
                "volume": float(lot),
                "type": mt5.ORDER_TYPE_BUY,
                "price": calla,
                "deviation": deviation,
                "magic": 123456,
                "comment": "compra",
                "type_time": mt5.ORDER_TIME_GTC,
                "type_filling": mt5.ORDER_FILLING_RETURN
                }
                result = mt5.order_send(request)
                callae=result[4]
                print(result)
                request = {
                "action": mt5.TRADE_ACTION_DEAL,
                "symbol": put,
                "volume": float(lot),
                "type": mt5.ORDER_TYPE_SELL,
                "price": putb,
                "deviation": deviation,
                "magic": 123456,
                "comment": "venda",
                "type_time": mt5.ORDER_TIME_GTC,
                "type_filling": mt5.ORDER_FILLING_RETURN
                }
                result = mt5.order_send(request)
                putbe=result[4]
                print(result)
                request = {
                "action": mt5.TRADE_ACTION_DEAL,
                "symbol": ativo,
                "volume": float(lot),
                "type": mt5.ORDER_TYPE_SELL,
                "price": precob,
                "deviation": deviation,
                "magic": 123456,
                "comment": "venda",
                "type_time": mt5.ORDER_TIME_GTC,
                "type_filling": mt5.ORDER_FILLING_RETURN
                }
                result = mt5.order_send(request)
                precobe=result[4]
                print(result) 
                print('compra call, vende ativo e put')
                abre=-1
                scan=1          
            else:
                print('Sem oportunidade de abrir')
                abre=0
                scan=0
                tentativain=tentativain+1
                print(tentativain)
 
    stop=0
    tentativaout=0
    while stop<1:
        lasttickativo=mt5.symbol_info_tick(ativo)
        lasttickcall=mt5.symbol_info_tick(call)
        lasttickput=mt5.symbol_info_tick(put)
        precob=lasttickativo.bid
        precoa=lasttickativo.ask
        callb=lasttickcall.bid
        calla=lasttickcall.ask
        putb=lasttickput.bid
        puta=lasttickput.ask
        uLEE=(callb+k*np.exp(-r*t))-(puta+precoa) 
        uLDE=(putb+precob)-(calla+k*np.exp(-r*t)) 
        if abre>0: 
            if (callbe+putb+precob)>(calla+putae+precoae+cost):
                print('ENCERRADO - compra call, vende ativo e put')
                request = {
                "action": mt5.TRADE_ACTION_DEAL,
                "symbol": call,
                "volume": float(lot),
                "type": mt5.ORDER_TYPE_BUY,
                "price": calla,
                "deviation": deviation,
                "magic": 123456,
                "comment": "compra",
                "type_time": mt5.ORDER_TIME_GTC,
                "type_filling": mt5.ORDER_FILLING_RETURN
                }
                result = mt5.order_send(request)
                print(result)
                request = {
                "action": mt5.TRADE_ACTION_DEAL,
                "symbol": put,
                "volume": float(lot),
                "type": mt5.ORDER_TYPE_SELL,
                "price": putb,
                "deviation": deviation,
                "magic": 123456,
                "comment": "venda",
                "type_time": mt5.ORDER_TIME_GTC,
                "type_filling": mt5.ORDER_FILLING_RETURN
                }
                result = mt5.order_send(request)
                print(result)
                request = {
                "action": mt5.TRADE_ACTION_DEAL,
                "symbol": ativo,
                "volume": float(lot),
                "type": mt5.ORDER_TYPE_SELL,
                "price": precob,
                "deviation": deviation,
                "magic": 123456,
                "comment": "venda",
                "type_time": mt5.ORDER_TIME_GTC,
                "type_filling": mt5.ORDER_FILLING_RETURN
                }
                result = mt5.order_send(request)
                print(result) 
                print('compra call, vende ativo e put')
                stop=1
            else:
                print('AINDA ABERTA - nada a fazer')
                stop=0
                tentativaout=tentativaout+1
                print(tentativaout)
        if abre<0: 
            if (putbe+precobe+callb)>(callae+puta+precoa+cost):
                print('ENCERRADO - vende call, compra ativo e put')
                request = {
                "action": mt5.TRADE_ACTION_DEAL,
                "symbol": call,
                "volume": float(lot),
                "type": mt5.ORDER_TYPE_SELL,
                "price": callb,
                "deviation": deviation,
                "magic": 123456,
                "comment": "venda",
                "type_time": mt5.ORDER_TIME_GTC,
                "type_filling": mt5.ORDER_FILLING_RETURN
                }
                result = mt5.order_send(request)
                print(result)
                request = {
                "action": mt5.TRADE_ACTION_DEAL,
                "symbol": put,
                "volume": float(lot),
                "type": mt5.ORDER_TYPE_BUY,
                "price": puta,
                "deviation": deviation,
                "magic": 123456,
                "comment": "compra",
                "type_time": mt5.ORDER_TIME_GTC,
                "type_filling": mt5.ORDER_FILLING_RETURN
                }
                result = mt5.order_send(request)
                print(result)
                request = {
                "action": mt5.TRADE_ACTION_DEAL,
                "symbol": ativo,
                "volume": float(lot),
                "type": mt5.ORDER_TYPE_BUY,
                "price": precoa,
                "deviation": deviation,
                "magic": 123456,
                "comment": "compra",
                "type_time": mt5.ORDER_TIME_GTC,
                "type_filling": mt5.ORDER_FILLING_RETURN
                }
                result = mt5.order_send(request)
                print(result)
                stop=1
            else:
                print('AINDA ABERTA - nada a fazer')
                stop=0
                tentativaout=tentativaout+1
                print(tentativaout)


pc1=['PETR4','PETRB34','PETRN34',24.51]
pc2=['BOVA11','BOVAB108','BOVAN108',108.00]
pc3=['VALE3','VALEB951','VALEN951',94.91]
pc4=['BBDC4','BBDCB159','BBDCN159',15.44]
pc=pc1+pc2+pc3+pc4

if __name__ == '__main__':
    Thread(target = putcall,args=(pc[0],pc[1],pc[2],pc[3])).start()
    Thread(target = putcall,args=(pc[4],pc[5],pc[6],pc[7])).start()
    Thread(target = putcall,args=(pc[8],pc[9],pc[10],pc[11])).start()
    Thread(target = putcall,args=(pc[12],pc[13],pc[14],pc[15])).start()
    
mt5.shutdown()
