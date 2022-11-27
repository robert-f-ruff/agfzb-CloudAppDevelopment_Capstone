from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
from .models import CarDealer, CarModel
from .restapis import get_dealers_from_cf, get_dealer_by_id_from_cf, get_dealer_reviews_from_cf, post_request
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from datetime import datetime
import logging
import json

DEALERSHIP_URL = "https://us-south.functions.appdomain.cloud/api/v1/web/7bb49de3-b231-4e7e-a14f-acaa6e6b6c4d/dealership-package/get-dealership.json"
REVIEW_URL = "https://us-south.functions.appdomain.cloud/api/v1/web/7bb49de3-b231-4e7e-a14f-acaa6e6b6c4d/dealership-package/get-review.json"

# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create your views here.


# Create an `about` view to render a static about page
def about(request):
    return render(request, 'djangoapp/about.html')


# Create a `contact` view to return a static contact page
def contact(request):
    return render(request, 'djangoapp/contact.html')
    

# Create a `login_request` view to handle sign in request
def login_request(request):
    context = {}
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('djangoapp:index')
        else:
            return render(request,'djangoapp/index.html', context)
    else:
        return render(request, 'djangoapp/login.html', context)


# Create a `logout_request` view to handle sign out request
def logout_request(request):
    logout(request)
    return redirect('djangoapp:index')


# Create a `registration_request` view to handle sign up request
def registration_request(request):
    context = {}
    if request.method == 'GET':
        return render(request, 'djangoapp/registration.html', context)
    elif request.method == 'POST':
        user_name = request.POST['username']
        first_name = request.POST['firstname']
        last_name = request.POST['lastname']
        password = request.POST['password']
        if User.objects.filter(username=user_name).count() == 0:
            user = User.objects.create_user(username=user_name, first_name=first_name, last_name=last_name, password=password)
            login(request, user)
            return redirect('djangoapp:index')
        else:
            return render(request, 'djangoapp/registration.html', context)

# Update the `get_dealerships` view to render the index page with a list of dealerships
def get_dealerships(request):
    if request.method == "GET":
        context = {}
        # Get dealers from the URL
        dealerships = get_dealers_from_cf(DEALERSHIP_URL)
        context["dealerships"] = dealerships
        # Show the list of dealerships
        return render(request, 'djangoapp/index.html', context)


# Create a `get_dealer_details` view to render the reviews of a dealer
def get_dealer_details(request, dealer_id):
    if request.method == "GET":
        context = {}
        dealer = get_dealer_by_id_from_cf(DEALERSHIP_URL, id=dealer_id)
        context["dealer"] = dealer
        # Get reviews from the URL
        reviews = get_dealer_reviews_from_cf(REVIEW_URL, dealer_id=dealer_id)
        # Show the list of reviews
        context["reviews"] = reviews
        return render(request, 'djangoapp/dealer_details.html', context)

# Create a `add_review` view to submit a review
def add_review(request, dealer_id):
    context = {}
    if request.method == "GET":
        cars = CarModel.objects.filter(dealer_id = dealer_id)
        context["cars"] = cars
        dealer = get_dealer_by_id_from_cf(DEALERSHIP_URL, id=dealer_id)
        context["dealer"] = dealer
        return render(request, 'djangoapp/add_review.html', context)
    if request.method == "POST":
        url = "https://us-south.functions.appdomain.cloud/api/v1/web/7bb49de3-b231-4e7e-a14f-acaa6e6b6c4d/dealership-package/post-review.json"
        review = {}
        review["name"] = request.user.first_name + ' ' + request.user.last_name
        review["dealership"] = dealer_id
        review["review"] = request.POST["review"]
        if request.POST["purchasecheck"] == "on":
            review["purchase"] = True
        else:
            review["purchase"] = False
        if review["purchase"]:
            review["purchase_date"] = request.POST["purchasedate"]
            car = CarModel.objects.get(id=request.POST["car"])
            review["car_make"] = car.make.name
            review["car_model"] = car.name
            review["car_year"] = car.year.strftime("%Y")
        json_payload = {"review": review}
        result = post_request(url, json_payload)
        return redirect("djangoapp:dealer_details", dealer_id=dealer_id)
