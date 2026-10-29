from access import get_secret
import requests
import os
import time
import math
import hmac
import json
import hashlib
import pandas as pd
from dotenv import load_dotenv
load_dotenv
from endpoints import ORDERS,TICKERS,PRODUCTS
class DeltaClient:
    def __init__(self):
        self.secrets = get_secret()
        self.prod_url = os.getenv('PROD_URL')
        self.orders = ORDERS
        self.products = PRODUCTS
        self.headers={'Accept':'application/json'}

    def get_current_price(self,symbol):
        r = requests.get(f'{self.prod_url}{TICKERS}/{symbol}',
                         params={},
                         headers=self.headers)
        data = r.json()
        return data['result']['close']

    def get_signature(self,secret,message):
        message = bytes(message,'UTF-8')
        secret = bytes(secret,'UTF-8')
        hash = hmac.new(secret,message,hashlib.sha256)
        return hash.hexdigest()

    def get_tickers_by_contracts(self,asset,expiry_date,contract_types):
        r = requests.get(self.prod_url+'/v2/tickers',
                         params={'contract_types':contract_types,
                                 'underlying_asset_symbols':asset,
                                 'expiry_date':expiry_date},
                        headers={
                            'Accept':'application/json'
                        },
                        timeout=50)
        df = pd.DataFrame(r.json()['result'])
        df = df[['product_id','symbol','strike_price']]
        return df

    def place_market_order(self,product_id):
        method='POST'
        timestamp=str(int(time.time()))
        path = self.orders
        url = f'{self.prod_url}{path}'
        query_string=''
        payload = json.dumps(
            {
                'order_type':'market_order',
                'size':1,
                'side':'sell',
                'product_id':int(product_id)
            }
        )
        signature_data = method+timestamp+path+query_string+payload
        signature = self.get_signature(self.secrets[1],signature_data)
        req_headers = {
            'api-key':self.secrets[0],
            'timestamp':timestamp,
            'signature':signature,
            'User-Agent':'pavan-btc-algo',
            'Content-Type':'application/json'
        }
        response = requests.request(
            method,
            url,
            data=payload,
            params={},
            timeout=(3,27),
            headers=req_headers
        )
        return response.json()

    def place_basket_order(self,product_ids):
        call_sell = self.place_market_order(product_ids[0])
        put_sell = self.place_market_order(product_ids[1])
        print(call_sell)
        print(put_sell)
        return (call_sell['success'],put_sell['success'])

    def decide_strike_price(self):
        ltp = self.get_current_price('BTCUSD')
        strike_price = math.floor(ltp/100)*100
        print({'ltp':ltp,'strike_price':strike_price})
        return strike_price

    def get_products_by_symbol(self,symbol:str):
        r = requests.get(f'{self.prod_url}{PRODUCTS}/{symbol}',
                                 params={},
                                 headers=self.headers)
        data = r.json()
        return data

