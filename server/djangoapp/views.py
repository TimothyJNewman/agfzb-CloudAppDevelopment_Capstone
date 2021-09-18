from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
from .models import CarMake, CarModel, CarDealer
from .restapis import get_dealers_from_cf, get_dealer_reviews_from_cf, post_request
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from datetime import datetime
import logging
import json

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
        password = request.POST['psw']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('djangoapp:index')
        else:
            context['message'] = "Invalid username or password."
            return render(request, 'djangoapp/user_login_bootstrap.html', context)
    else:
        return render(request, 'djangoapp/user_login_bootstrap.html', context)


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
        # Check if user exists
        username = request.POST['username']
        password = request.POST['psw']
        first_name = request.POST['firstname']
        last_name = request.POST['lastname']
        user_exist = False
        try:
            User.objects.get(username=username)
            user_exist = True
        except:
            logger.error("New user")
        if not user_exist:
            user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name,
                                            password=password)
            login(request, user)
            return redirect("djangoapp:index")
        else:
            context['message'] = "User already exists."
            return render(request, 'djangoapp/registration.html', context)

# Update the `get_dealerships` view to render the index page with a list of dealerships
def get_dealerships(request):
    context = {}
    if request.method == "GET":
        url = "https://c9702308.eu-gb.apigw.appdomain.cloud/api/dealership"
        # Get dealers from the URL
        dealerships = get_dealers_from_cf(url)
        #return HttpResponse(' '.join([dealer.short_name for dealer in dealerships]))
        context = {"dealership_list": dealerships}
        return render(request, 'djangoapp/index.html', context)

# Create a `get_dealer_details` view to render the reviews of a dealer
def get_dealer_details(request, dealer_id):
    context = {}
    if request.method == "GET":
        url = "https://c9702308.eu-gb.apigw.appdomain.cloud/api/reviews"
        # Get dealers from the URL
        dealer_reviews = get_dealer_reviews_from_cf(url, dealer_id)
        #return HttpResponse(' '.join([dealer.short_name for dealer in dealer_reviews]))
        context = {"reviews_list":dealer_reviews, "dealer_id": dealer_id}
        return render(request, 'djangoapp/dealer_details.html', context)

# Create a `add_review` view to submit a review
def add_review(request, dealer_id):
    context = {}
    if request.user.is_authenticated:
        if request.method == "GET":
            car_model = CarModel.objects.all().filter(dealerId=dealer_id)
            context["cars"] = car_model
            context["dealer_id"] = dealer_id
            return render(request, 'djangoapp/add_review.html', context)
        elif request.method == 'POST':
            car_model = CarModel.objects.get(id=request.POST['car'])
            review = {
                "id":1,
                "name":request.user.first_name+" "+request.user.last_name,
                "dealership":dealer_id,
                "review":request.POST['content'],
                "purchase":request.POST['purchasecheck'],
                "purchase_date":request.POST['purchasedate'],
                "car_make":car_model.carMake.name,
                "car_model":car_model.carType,
                "car_year":car_model.year.strftime("%Y")
            }
            json_payload = {"review": review}
            post_request("https://c9702308.eu-gb.apigw.appdomain.cloud/api/reviews", json_payload)
            return redirect("djangoapp:dealer_details", dealer_id=dealer_id)


