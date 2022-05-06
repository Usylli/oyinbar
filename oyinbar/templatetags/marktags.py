import os
from django import template
from .. import settings
import firebase_admin
from firebase_admin import db
from firebase_admin import credentials
from firebase_admin import firestore

register = template.Library()

cred = credentials.Certificate(os.path.join(settings.STATICFILES_DIRS[0], 'serviceAccountKey.json'))                    
if (not len(firebase_admin._apps)):
    firebase_admin.initialize_app(cred)
db=firestore.client()

@register.simple_tag(takes_context = True)
def cookie(context, cookie_name):
    request = context['request']
    result = request.COOKIES.get(cookie_name,'') # I use blank as default value
    print(cookie_name, result)
    return result

@register.simple_tag(takes_context=True)
def get_email(context):
    request = context.get("request")
    access_token = request.COOKIES.get('access_token', None)
    email_doc = db.collection('users').document(access_token).get()
    email_dic = email_doc.to_dict()
    return email_dic['email']

@register.simple_tag(takes_context=True)
def total_price(context):
    request = context.get("request")
    access_token = request.COOKIES.get('access_token', None)
    user_doc = db.collection('users').document(access_token)
    games_docs = user_doc.collection('cart').get()
    games = []
    total = 0
    db.collection('users').document(access_token)
    for game_doc in games_docs:
        games.append(game_doc.to_dict())
    for game in games:
        total += game['price']
    return total

