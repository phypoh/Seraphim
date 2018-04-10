#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 20 00:01:38 2018

@author: phypoh
"""

#Testing

import requests
import json
import pandas as pd
from draft import ranked_5v5
from draft import pick_5v5

A_ban, B_ban, A_side, B_side = ranked_5v5(1)
print("\nBanned heroes: ")
print("A Side: ", A_ban)
print("B Side: ", B_ban)

print("\nChosen heroes: ")
print("A Side: ", A_side)
print("B Side: ", B_side)