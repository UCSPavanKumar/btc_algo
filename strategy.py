from dotenv import load_dotenv  
from access import get_secret
load_dotenv()
import os

from delta_rest_client import DeltaRestClient
secrets = get_secret()
print(secrets)
delta_client = DeltaRestClient(
    base_url=os.getenv("PROD_URL"),
    api_key=secrets[0],
    api_secret=secrets[1]

)

response = delta_client.get_balances(asset_id=1)
print(response)