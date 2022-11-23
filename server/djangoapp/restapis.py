import requests
import json
import os
from .models import CarDealer, DealerReview
from requests.auth import HTTPBasicAuth
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson.natural_language_understanding_v1 \
import Features, SentimentOptions
from dotenv import load_dotenv


def get_request(url, **kwargs):
    print(kwargs)
    print("GET from {} ".format(url))
    try:
        # Call get method of requests library with URL and parameters
        response = requests.get(url, headers={'content-type': 'application/json'}, params=kwargs)
    except:
        # If any error occurs
        print("Network exception occurred")
    status_code = response.status_code
    print("With status {} ".format(status_code))
    json_data = json.loads(response.text)
    return json_data

def post_request(url, json_payload, **kwargs):
    try:
        # Call post method of requests library with URL and parameters
        response = requests.post(url, json=json_payload, params=kwargs)
    except:
        # If any error occurs
        print("Network exception occurred")
    json_data = json.loads(response.text)
    return json_data

def get_dealers_from_cf(url, **kwargs):
    results = []
    # Call get_request with a URL parameter
    json_result = get_request(url)
    if json_result:
        # Get the row list in JSON as dealers
        dealers = json_result["dealerships"]
        # For each dealer object
        for dealer in dealers:
            # Create a CarDealer object
            dealer_obj = CarDealer(address=dealer["address"], city=dealer["city"], full_name=dealer["full_name"],
                                   id=dealer["id"], lat=dealer["lat"], long=dealer["long"],
                                   short_name=dealer["short_name"],
                                   st=dealer["st"], zip=dealer["zip"])
            results.append(dealer_obj)

    return results

def get_dealers_by_state_from_cf(url, **kwargs):
    results = []
    # Call get_request with a URL parameter
    json_result = get_request(url, state=kwargs["state"])
    if json_result:
        # Get the row list in JSON as dealers
        dealers = json_result["dealerships"]
        # For each dealer object
        for dealer in dealers:
            # Create a CarDealer object
            dealer_obj = CarDealer(address=dealer["address"], city=dealer["city"], full_name=dealer["full_name"],
                                   id=dealer["id"], lat=dealer["lat"], long=dealer["long"],
                                   short_name=dealer["short_name"],
                                   st=dealer["st"], zip=dealer["zip"])
            results.append(dealer_obj)

    return results

def get_dealer_reviews_from_cf(url, **kwargs):
    results = []
    # Call get_request with a URL parameter
    json_result = get_request(url, dealerId=kwargs["dealer_id"])
    if json_result:
        # Get the row list in JSON as dealers
        reviews = json_result["reviews"]
        # For each review object
        for review in reviews:
            # Create a DealerReview object
            review_obj = DealerReview(dealership=int(review["dealership"]), name=review["name"], purchase=review["purchase"], review=review["review"],
                                      purchase_date=review["purchase_date"], car_make=review["car_make"], car_model=review["car_model"], car_year=review["car_year"],
                                      sentiment=analyze_review_sentiments(review["review"]), id=review["id"])
            results.append(review_obj)

    return results


def analyze_review_sentiments(text):
    load_dotenv()
    authenticator = IAMAuthenticator(apikey=os.environ['nlu_api_key'])
    natural_language_understanding = NaturalLanguageUnderstandingV1(
        version='2022-04-07',
        authenticator=authenticator
    )

    natural_language_understanding.set_service_url('https://api.us-south.natural-language-understanding.watson.cloud.ibm.com/instances/02aca5a6-a39d-4a2b-bf4d-bc2b97db6c67')

    response = natural_language_understanding.analyze(
        text=text,
        features=Features(sentiment=SentimentOptions(document=True))).get_result()
    
    return response['sentiment']['document']['label'].title()
