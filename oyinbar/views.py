from multiprocessing import context
import pyrebase 
import os
from . import settings
from django.shortcuts import render
from django.contrib import auth
import firebase_admin
from firebase_admin import db
from firebase_admin import credentials

cred = credentials.Certificate(os.path.join(settings.STATICFILES_DIRS[0], 'oyinbar-b689f-firebase-adminsdk-bgwzi-bddaa82efa.json'))                        

firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://oyinbar-b689f-default-rtdb.europe-west1.firebasedatabase.app'
})

ref = db.reference()

config = {
    'apiKey': "AIzaSyA4sIWJwl3TEu-om8nW-JmAQnmv8eqEQwE",
    'authDomain': "oyinbar-b689f.firebaseapp.com",
    'projectId': "oyinbar-b689f",
    'storageBucket': "oyinbar-b689f.appspot.com",
    'messagingSenderId': "220543843416",
    'appId': "1:220543843416:web:1efb95b280ec33fbb05e2d",
    'measurementId': "G-CH439G06CF",
    "databaseURL": "https://oyinbar-b689f-default-rtdb.europe-west1.firebasedatabase.app"
}

firebase = pyrebase.initialize_app(config)
authe = firebase.auth()
database = firebase.database()

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
    print(user['idToken'])
    session_id=user['idToken']
    request.session['uid'] = str(session_id)
    return render(request, "main.html",{"e":email})

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
    
    data = {"first_name": fname, 
            "second_name": sname,
            "status": "1"}  
    
    users_ref = ref.child('users').child(uid).child("details")
    users_ref.set(data)
    return render(request, "login.html")

def indexView(request):
    product_ref = ref.child('games')
    products_list = product_ref.get()
    print(products_list)
    context = {
        'products_list': products_list,
    }
    return render(request, 'main.html', context)
    
