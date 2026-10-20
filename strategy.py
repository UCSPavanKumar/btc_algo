from dotenv import load_dotenv  
from access import get_secret
load_dotenv()

import os
from delta import DeltaClient

dc = DeltaClient()

data = dc.get_tickers_by_contracts('BTC','21-10-2026')
print(data)
dc.place_market_order('158961')