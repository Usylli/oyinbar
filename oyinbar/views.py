from ast import Constant
import os
from django.http import HttpResponseRedirect
from django.urls import reverse
import pyrebase
from . import settings
from django.shortcuts import render
from django.contrib import auth
import oyinbar.settings as settings
from firebase_admin import initialize_app
import firebase_admin
from firebase_admin import db
from firebase_admin import credentials
from firebase_admin import firestore
from django.template import RequestContext
from django.shortcuts import redirect

cred = credentials.Certificate(os.path.join(settings.STATICFILES_DIRS[0], 'serviceAccountKey.json'))                    
if (not len(firebase_admin._apps)):
    firebase_admin.initialize_app(cred)
    
firebaseConfig = {
  "apiKey": "AIzaSyA4sIWJwl3TEu-om8nW-JmAQnmv8eqEQwE",
  "authDomain": "oyinbar-b689f.firebaseapp.com",
  "databaseURL": "https://oyinbar-b689f-default-rtdb.europe-west1.firebasedatabase.app",
  "projectId": "oyinbar-b689f",
  "storageBucket": "oyinbar-b689f.appspot.com",
  "messagingSenderId": "220543843416",
  "appId": "1:220543843416:web:1efb95b280ec33fbb05e2d",
  "measurementId": "G-CH439G06CF"
};
firebase = pyrebase.initialize_app(firebaseConfig)

db=firestore.client()

authe = firebase.auth()

def signIn(request):
    return render(request, "login.html")

def postsign(request):
    email = request.POST.get('email')
    passw = request.POST.get("pass")
    try:
        user = authe.sign_in_with_email_and_password(email,passw)
    except:
        message = "invalid crediantials"
        return render(request,"login.html",{"msg":message})
    games_docs = db.collection('games').get()
    games = []
    for game_doc in games_docs:
        games.append(game_doc.to_dict())
    context = {
        'products_list': games,
        "e":email
    }
    user = db.collection('users').where("email", "==", email).get()
    print(user[0].id)
    print(games)
    response = HttpResponseRedirect(reverse('index'), context)
    response.set_cookie('access_token', user[0].id)
    return response

def logout(request):
    auth.logout(request)
    return render(request, 'login.html')

def signUp(request): 
     
    return render(request, "Register.html")

def postsignup(request):
    fname = request.POST.get('fname')
    sname = request.POST.get('sname')
    email = request.POST.get('email')
    password = request.POST.get('password')
    rpassword = request.POST.get('rpassword')
    
    user = authe.create_user_with_email_and_password(email, password)
    uid = user['localId']
    print(user)
    
    data = {"email": email,
            "first_name": fname, 
            "second_name": sname,
            "status": "1"}  
    
    db.collection('users').document(uid).set(data)
    return render(request, "login.html")

def indexView(request):
    games_docs = db.collection('games').get()
    games = []
    for game_doc in games_docs:
        games.append(game_doc.to_dict())
    print(games)
    context = {
        'products_list': games,
    }
    return render(request, 'main.html', context)

def add_cart(request, game_id):
    token = request.COOKIES.get('access_token', '')
    games_docs = db.collection('games').get()
    games = []
    for game_doc in games_docs:
        games.append(game_doc.to_dict())
    data={
        'id': game_id,
        'desc': games[game_id]['desc'],
        'name': games[game_id]['name'],
        'price': games[game_id]['price'],
        'img': games[game_id]['img']
    }
    db.collection('users').document(token).collection('cart').document(str(game_id)).set(data)
    return redirect(indexView)

def delete_from_cart(request, game_id):
    token = request.COOKIES.get('access_token', '')
    db.collection('users').document(token).collection('cart').document(str(game_id)).delete()
    return redirect(cartView)

def cartView(request):
    token = request.COOKIES.get('access_token', '')
    user_doc = db.collection('users').document(token)
    games_docs = user_doc.collection('cart').get()
    games = []
    for game_doc in games_docs:
        games.append(game_doc.to_dict())
    context = {
        'products_list': games,
    }
    return render(request, 'cart.html', context)

def profileView(request):
    token = request.COOKIES.get('access_token', '')
    user_doc = db.collection('users').document(token).get()
    user_dict = user_doc.to_dict()
    context = {
        'user': user_dict
    }
    return render(request, 'profile.html', context)

def logout(request):
    response = HttpResponseRedirect(reverse('index'))
    response.delete_cookie('access_token')
    return response
    
