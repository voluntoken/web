#!/bin/bash
sudo pip install virtualenv
virtualenv voluntokenvenv
source voluntokenvenv/bin/activate
pip install Django
pip install djangorestframework
pip install django-rest-auth
pip install Pillow