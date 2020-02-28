#!/usr/bin/env python
# coding: utf-8

# In[11]:


import pyrebase
import pandas as pd
from time import time, sleep
import numpy as np

from flask import Flask, request, current_app, jsonify


# In[2]:


config= {
    "apiKey": "AIzaSyAm8ABmhDYIl0wwj6PeLQCQyM1t3qvhfzU",
    "authDomain": "wine-c0b8f.firebaseapp.com",
    "databaseURL": "https://wine-c0b8f.firebaseio.com",
    "projectId": "wine-c0b8f",
    "storageBucket": "wine-c0b8f.appspot.com",
    "messagingSenderId": "158435355979",
    "appId": "1:158435355979:web:a34d401a62ffa62fae8cce",
    "measurementId": "G-XHP6NB48HW"
  }
firebase = pyrebase.initialize_app(config)


# In[3]:


db = firebase.database()
storage = firebase.storage()


# In[4]:


def upload():
    wine = pd.read_csv("winemag-data-130k-v2.csv")
    del wine['Unnamed: 0']
    wine = wine.fillna(0)
    wine.price =wine.price.astype(float)
    wine.points =wine.points.astype(float)
    for i in range(1000):
        data = wine.iloc[i]
        data = data.to_dict()


        id = int(time())
        sleep (1)
        db.child("wine").child(id).set(data)


# In[5]:


def image(request):
    req = request.json
    storage.child("{}".format(time())).put(req)
    return jsonify({'sucesso': True})
    


# In[6]:


def first_15():
    first_15 = db.child("wine").order_by_child("points").limit_to_first(15).get()
    return first_15.val()


# In[7]:


def province(request):
    req = request.json
    db.child("wine").order_by_child("province").equal_to(req).get()
    return jsonify({'sucesso': True})


# In[8]:


def delete(id):
    wine = db.child('wine').child(id).get()
    if not wine:
        return 'Vinho não encontrado.', 400
    db.child('wine').child(id).remove()
    return jsonify({'sucesso': True})


# In[9]:


def update_wine(id, request):
    wine = db.child('wine').child(id).get()
    if not wine:
        return 'Vinho não encontrado.', 400
    req = request.json
    db.child('wine').child(id).update(req)
    return jsonify({'sucesso': True})


# In[26]:


def wine(request):
    if request.path == '/' or request.path == '':
        if request.method == 'POST':
            return upload()
        else:
            return 'Método não suportado.', 400
    if request.path.startswith('/'):
        id = request.path.lstrip('/')
        if request.method == 'GET' and id == "first_15":
            return first_15()
        elif request.method == 'GET' and type(id) == str:
            return province(request)
        elif request.method == 'PUT' and type(id) == str:
            return image(request)
        elif request.method == 'DELETE' and id is not None:
            return delete(id)
        elif request.method == 'PUT' and type(id) == int:
            return update_wine(id, request)
        else:
            return 'Método não suportado.', 400
        
    return 'URL não encontrada.', 400


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




