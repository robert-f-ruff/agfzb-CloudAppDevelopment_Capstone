/**
  *
  * main() will be run when you invoke this action
  *
  * @param Cloud Functions actions accept a single parameter, which must be a JSON object.
  *
  * @return The output of this action, which must be a JSON object.
  *
  */
 const { CloudantV1 } = require('@ibm-cloud/cloudant');
 const { IamAuthenticator } = require('ibm-cloud-sdk-core');
 
 async function main(params) {
       const authenticator = new IamAuthenticator({ apikey: params.IAM_API_KEY })
       const cloudant = CloudantV1.newInstance({
           authenticator: authenticator
       });
       cloudant.setServiceUrl(params.COUCH_URL);
       try {
            if (params.state) {
                let dealershipsList = await cloudant.postFind({ db: 'dealerships', selector: {state: params.state} })
                result = { 'dealerships': dealershipsList.result.docs }
            } else if (params.id) {
                let dealership = await cloudant.postFind({ db: 'dealerships', selector: {id: parseInt(params.id)} })
                result = { 'dealerships': dealership.result.docs }
            } else {
                let dealershipsList = await cloudant.postAllDocs({ db: 'dealerships', includeDocs: true });
                result = { 'dealerships': dealershipsList.result.rows }
            }
            return result;
       } catch (error) {
           return { error: error.description };
       }
 }