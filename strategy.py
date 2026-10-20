from dotenv import load_dotenv  
from access import get_secret
load_dotenv()
import os
from delta import DeltaClient

dc = DeltaClient()

dc.get_tickers_by_contracts('BTC','20-10-2026')