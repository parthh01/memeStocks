
import os 

TRADIER_API_KEY = os.getenv("TRADIER_API_KEY")
headers = {'Authorization': "Bearer {}".format(TRADIER_API_KEY), 'Accept': 'application/json'}
BASE_URL = "https://sandbox.tradier.com"
