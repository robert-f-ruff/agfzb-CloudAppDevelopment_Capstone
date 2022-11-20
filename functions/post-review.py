#
#
# main() will be run when you invoke this action
#
# @param Cloud Functions actions accept a single parameter, which must be a JSON object.
#
# @return The output of this action, which must be a JSON object.
#
#
import sys
from ibmcloudant.cloudant_v1 import Document, CloudantV1
from ibm_cloud_sdk_core import ApiException
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
import requests

def main(dict):
    databaseName = "reviews"

    try:
        authenticator = IAMAuthenticator(apikey=dict["IAM_API_KEY"])
        client = CloudantV1(authenticator=authenticator)
        client.set_service_url(dict["COUCH_URL"])
        new_review = Document.from_dict(dict["review"])
        response = client.post_document(db=databaseName, document=new_review).get_result()
    except ApiException as ae:
        return {"error": ae.code + " " + ae.message}
    except (requests.exceptions.RequestException, ConnectionResetError) as err:
        return {"error": err}

    if response["ok"]:
        
        result = {
        'headers':{'Content-Type':'application/json'},
        'body':{'message':"Data Inserted"}
        }
        return result