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
    destination = Destination.objects.filter(user_id=current_user)
    plan = Destination.objects.all() #need to figure out quiry for .exclude becasue all of yours weren't working.
    context = {
        "destinations": destination,
        "plans": plan,
    }

    return render(request, 'beltapp/travels.html', context)

def add(request):
    return render(request, 'beltapp/add.html')

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
    a_trip = Destination.objects.get(id=id)
    new_user = User.objects.get(id=request.session['user_id'])
    new_trip = Destination.objects.create(users=new_user)
    return render(request, 'beltapp/travels.html')

def destination(request, id):
    trip = Destination.objects.get(id=id)
    traveler = trip.users.all()
    context = {
        "trips": trip,
        "travelers": traveler,
    }
    return render(request, 'beltapp/destination.html', context)
