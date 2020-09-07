import json
import pandas as pd
import requests


def get_neighbourhoods():
 
    # Get the dataset metadata by passing package_id to the package_search endpoint
    # For example, to retrieve the metadata for this dataset:
    
    url = "https://ckan0.cf.opendata.inter.prod-toronto.ca/api/3/action/package_show"
    params = { "id": "4def3f65-2a65-4a4f-83c4-b2a4aed72d46"}
    package = requests.get(url, params = params).json()
    print(package["result"])
    
    # Get the data by passing the resource_id to the datastore_search endpoint
    # See https://docs.ckan.org/en/latest/maintaining/datastore.html for detailed parameters options
    # For example, to retrieve the data content for the first resource in the datastore:
    
    for idx, resource in enumerate(package["result"]["resources"]):
        if resource["datastore_active"]:
            url = "https://ckan0.cf.opendata.inter.prod-toronto.ca/api/3/action/datastore_search"
            p = { "id": resource["id"] }
            data = requests.get(url, params = p).json()
            neighbourhoods_df = pd.DataFrame(data["result"]["records"])
            break
    
    return neighbourhoods_df

neighbourhoods_df = get_neighbourhoods()
