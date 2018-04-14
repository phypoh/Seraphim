#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 20 00:01:38 2018

@author: phypoh
"""

#Testing
import os
import requests
import json


def pull_all():
    link = os.getenv('API_LINK')
    response = requests.get(link)
    data = response.json()
    data = sorted(data, key=lambda k: k['winRate'], reverse = True)
    return data
    

def pull_heroes():
    all_heroes = {}
    for hero in hero_list:
        link = os.getenv('API_LINK')
        link += hero
        response = requests.get(link)
        data = response.json()
        all_heroes[hero] = data
    return all_heroes

def pull_hero(hero):
    return all_heroes[hero]


API_rates = pull_all()
hero_list = [x["name"] for x in API_rates]
all_heroes = pull_heroes()
print("API initialized")






