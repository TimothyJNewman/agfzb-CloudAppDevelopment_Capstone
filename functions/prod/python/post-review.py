#
#
# main() will be run when you invoke this action
#
# @param Cloud Functions actions accept a single parameter, which must be a JSON object.
#
# @return The output of this action, which must be a JSON object.
#
#
from cloudant.client import Cloudant
from cloudant.error import CloudantException
import requests


def main(dict):
    
    requiredFields = [
        "id", 
        "name", 
        "dealership", 
        "review", 
        "purchase", 
        "another", 
        "purchase_date", 
        "car_make", 
        "car_model", 
        "car_year"
        ]

    formattedJSON = {}
    for key in dict["review"].keys():
        if key in requiredFields:
            formattedJSON[key] = dict["review"][key]
        
    return {"doc": formattedJSON}
    