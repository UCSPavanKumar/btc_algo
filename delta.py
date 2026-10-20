from access import get_secret
import requests
import os
from dotenv import load_dotenv
load_dotenv
class DeltaClient:
    def __init__(self):
        self.secrets = get_secret()
        self.prod_url = os.getenv('PROD_URL')


    def get_tickers_by_contracts(self,asset,expiry_date):
        r = requests.get(self.prod_url+'/v2/tickers',
                         params={'contract_types':'call_options',
                                 'underlying_asset_symbols':asset,
                                 'expiry_date':expiry_date},
                        headers={
                            'Accept':'application/json'
                        },
                        timeout=50)
        print(r.url)
        print(r.json())

