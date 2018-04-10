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
    

def pull_hero(hero):
   link = os.getenv('API_LINK')
   link += hero
   response = requests.get(link)
   data = response.json()
   #print(data)
   return data

#pull_hero("Adagio")
API_rates = pull_all()
hero_list = [x["name"] for x in API_rates]


hero_range =  {
 'Adagio': 'ranged',
 'Alpha': 'melee',
 'Ardan': 'melee',
 'Baptiste': 'melee',
 'Baron': 'ranged',
 'Blackfeather': 'melee',
 'Catherine': 'melee',
 'Celeste': 'ranged',
 'Churnwalker': 'melee',
 'Flicker': 'melee',
 'Fortress': 'melee',
 'Glaive': 'melee',
 'Grace': 'melee',
 'Grumpjaw': 'melee',
 'Gwen': 'ranged',
 'Idris': 'both',
 'Joule': 'melee',
 'Kestrel': 'ranged',
 'Koshka': 'melee',
 'Krul': 'melee',
 'Lance': 'melee',
 'Lorelai': 'ranged',
 'Lyra': 'ranged',
 'Ozo': 'melee',
 'Petal': 'ranged',
 'Phinn': 'melee',
 'Reim': 'melee',
 'Reza': 'melee',
 'Ringo': 'ranged',
 'Rona': 'melee',
 'SAW': 'ranged',
 'Samuel': 'ranged',
 'Skaarf': 'ranged',
 'Skye': 'ranged',
 'Taka': 'melee',
 'Tony': 'melee',
 'Varya': 'ranged',
 'Vox': 'ranged'}






