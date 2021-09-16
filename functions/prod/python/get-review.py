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
from cloudant.result import Result, ResultByKey
import requests


def main(dict):

    try:
        client = Cloudant.iam(
            account_name=dict["COUCH_USERNAME"],
            api_key=dict["IAM_API_KEY"],
            connect=True,
        )
        print("Databases: {0}".format(client.all_dbs()))
    except CloudantException as ce:
        print("unable to connect")
        return {"error": ce}
    except (requests.exceptions.RequestException, ConnectionResetError) as err:
        print("connection error")
        return {"error": err}
        
    databaseName = "reviews"
    my_database = client[databaseName]
    result_collection = Result(my_database.all_docs, include_docs=True)
    print(dict["dealerId"])
    result = {}
    for elem in result_collection:
        result["id"] = elem["doc"]["id"]
        result["name"] = elem["doc"]["name"]
        result["dealership"] = elem["doc"]["dealership"]
        result["review"] = elem["doc"]["review"]
        result["purchase"] = elem["doc"]["purchase"]
        #result["purchase_date"] = elem["doc"]["purchase_date"]
        #result["car_make"] = elem["doc"]["car_make"]
        #result["car_model"] = elem["doc"]["car_model"]
        #result["car_year"] = elem["doc"]["car_year"]
    print(result_collection[0][0]["doc"].keys())
    return {"dbs": result_collection[0]}
