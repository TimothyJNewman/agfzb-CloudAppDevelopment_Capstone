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
    results = []
    result = {}
    for elem in result_collection:
        if (elem["doc"]["dealership"] == dict["dealerId"]):
            for key in elem["doc"].keys():
                if (key != "_id" and key != "_rev"):
                    result[key] = elem["doc"][key]
            results.append(result)
    return {"entries": results}
