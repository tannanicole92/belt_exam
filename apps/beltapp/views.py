from __future__ import unicode_literals
from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from .models import User, Destination
import datetime
import bcrypt
import re
from django.db.models import Count
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9\.\+_-]+@[a-zA-Z0-9\._-]+\.[a-zA-Z]*$')

def index(request):
    return render(request, 'beltapp/index.html')

def register(request):
    return render(request, 'beltapp/register.html')

def exists(request):
    data = {'email': request.POST['email'], 'password': request.POST['password']}
    results = User.objects.login(data)
    if len(results) > 0:
        for error in results:
            messages.add_message(request, messages.ERROR, error)
        return redirect('/')
    else:
        request.session['email'] = request.POST['email']
        request.session['first_name'] = User.objects.get(email=data['email']).first_name
        request.session['user_id'] = User.objects.get(email=data['email']).id
        return redirect('/travels')

def create(request):
    data = {'first_name': request.POST['first_name'], 'last_name': request.POST['last_name'], 'email': request.POST['email'], 'password': request.POST['password'], 'passwordcon': request.POST['passwordcon']}
    results = User.objects.register(data)
    if len(results) > 0:
        for error in results:
            messages.add_message(request, messages.ERROR, error)
        return redirect('/')
    else:
        pw = bcrypt.hashpw(data['password'].encode('utf8'), bcrypt.gensalt())
        User.objects.create(first_name=data['first_name'],last_name=data['last_name'], email=data['email'], password=pw)
        request.session['first_name'] = User.objects.get(email=data['email']).first_name
        request.session['user_id'] = User.objects.get(email=data['email']).id
        return redirect('/travels')

def logout(request):
    del request.session['user_id']
    return redirect('/')

def travels(request):
    current_user = User.objects.get(id=request.session['user_id'])
    plan = Destination.objects.all().exclude(user_id=request.session['user_id']).exclude(users=request.session['user_id'])
    context = {
        "current_user": current_user,
        "plans": plan,
    }

    return render(request, 'beltapp/travels.html', context)

def add(request):
    current_user = User.objects.get(id=request.session['user_id'])
    context = {
    "current_user": current_user,
    }
    return render(request, 'beltapp/add.html', context)

def deletetrip(request, id, user_id):
    id = id
    a_user = User.objects.get(id=request.session['user_id'])
    user_id = a_user
    a_trip = Destination.objects.filter(id=id)
    a_trip.delete()
    return redirect('/portfolio/'+ str(user_id.id))

def portfolio(request, user_id):
    a_user = User.objects.get(id=user_id)
    current_user = User.objects.get(id=request.session['user_id'])
    joined_trip = Destination.objects.filter(users__id=user_id)
    journeys = Destination.objects.filter(user_id=user_id)
    context = {
    "a_user": a_user,
    "current_user": current_user,
    "journeys": journeys,
    "joined_trips": joined_trip,
    }
    return render(request, 'beltapp/portfolio.html', context)

def add_trip(request):
    print request.POST
    data = {'name': request.POST['name'], 'description': request.POST['description'], 'start_date': request.POST['start_date'], 'end_date': request.POST['end_date']}
    results = Destination.objects.create_trip(data)
    if len(results) > 0:
        for error in results:
            messages.add_message(request, messages.ERROR, error)
        return redirect('/add')
    else:
        new_user = User.objects.get(id=request.session['user_id'])
        new_trip = Destination.objects.create(name = data['name'], description=data['description'], start_date=data['start_date'], end_date=data['end_date'], user_id=new_user)
        return redirect('/destination/'+str(new_trip.id))

def join(request, id):
    trip_id = int(id)
    a_trip = Destination.objects.get(id=trip_id)
    new_user = User.objects.get(id=request.session['user_id'])
    new_trip = a_trip.users.add(new_user)
    return redirect('/travels')

def leaving(request, id, user_id):
    trip_id = int(id)
    user_id = user_id
    a_trip = Destination.objects.get(id=trip_id)
    new_user = User.objects.get(id=request.session['user_id'])
    new_trip = a_trip.users.remove(new_user)
    return redirect('/portfolio/'+str(user_id))

def joining(request, id, user_id):
    trip_id = int(id)
    user_id = user_id
    a_trip = Destination.objects.get(id=trip_id)
    new_user = User.objects.get(id=request.session['user_id'])
    new_trip = a_trip.users.add(new_user)
    return redirect('/portfolio/'+str(user_id))

def leaves(request, id, user_id):
    trip_id = int(id)
    user_id = user_id
    a_trip = Destination.objects.get(id=trip_id)
    new_user = User.objects.get(id=request.session['user_id'])
    new_trip = a_trip.users.remove(new_user)
    return redirect('/destination/'+str(trip_id))

def joiners(request, id, user_id):
    trip_id = int(id)
    user_id = user_id
    a_trip = Destination.objects.get(id=trip_id)
    new_user = User.objects.get(id=request.session['user_id'])
    new_trip = a_trip.users.add(new_user)
    return redirect('/destination/'+str(trip_id))

def destination(request, id):
    trip = Destination.objects.filter(id=id)
    current_user = User.objects.get(id=request.session['user_id'])
    context = {
        "trips": trip,
        "current_user": current_user,
    }
    return render(request, 'beltapp/destination.html', context)
