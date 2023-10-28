#This task completes incomplete address, the output returns the full address with Google address format.
#Google api doc : https://developers.google.com/maps/documentation/places/web-service/autocomplete
import googlemaps

mykey = 'Enter your key'
gmaps = googlemaps.Client(key = mykey)

import pandas as pd

#Data must provide CSV format
data = pd.read_csv(r"your_file_path.csv")

#The data contains "Billing Street" text on the header
#Each rows will contain dirty data(incomplete) address
series = data['Billing Street']
data = series.values.tolist()

import sys

#Google API
import json
import requests
from urllib.parse import urlencode



def get_autocomplete(address_name):
    #specify returned data type
    data_type = 'json'
    #provided by Google developers
    endpoint = f"https://maps.googleapis.com/maps/api/place/autocomplete/{data_type}"
    #input parameters then encode them
    params = {"input": address_name, "key": mykey}
    url_params = urlencode(params)
    url = f"{endpoint}?{url_params}"

    r = requests.get(url)
    if r.status_code not in range(200, 299):
        return sys.exit("Error message")
    return r.json()


list = []
for i in range(len(data)):
    output = get_autocomplete(data[i])
    if (output['status'] == "OK"):
        print(output['predictions'])
        list.append(output['predictions'][0]['description'])
    else:
        list.append("ZERO_RESULTS")


export = pd.DataFrame(list)
export.to_csv(r"export_path.csv", index=False, header=False)
