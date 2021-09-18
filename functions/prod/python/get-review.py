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
            #account_name=dict["COUCH_USERNAME"],
            #api_key=dict["IAM_API_KEY"],
            account_name="dde8132b-8051-43bb-8826-e3e668959555-bluemix",
            api_key="EFhAv_KvwaGMZlmbnP9UkM9Gj-jjm1m8iJwdEmlTtba8",
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
    for elem in result_collection:
        if (elem["doc"]["dealership"] == int(dict["dealerId"])):
            resultObj = {}
            for key in elem["doc"].keys():
                if (key != "_id" and key != "_rev"):
                    resultObj[key] = elem["doc"][key]
            results.append({"doc":resultObj})
            
    if (len(results) == 0):
        raise CloudantException("404 Error: dealerId does not exist")
    
    return {"rows": results}