#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 20 00:01:38 2018

@author: phypoh
"""

#Testing

import requests
import json
from API import hero_list, winrates #, pickrates, banrates



def auto_highest(A_side, B_side, A_ban = [], B_ban = []):
    for hero in winrates:
        if (hero["name"] in A_side) or (hero["name"] in B_side) or (hero["name"] in A_ban) or (hero["name"] in B_ban) :
            pass
        else:
            return hero["name"]
    return "NIL"

def ban_second_highest(A_side, B_side, A_ban = [], B_ban = []):
    """
    If AI takes A side, employs a passive ban on the second highest winrate hero
    so it can secure the highest winrate hero. Else, employ auto_highest ban
    
    """
    
    if len(A_ban) > len(B_ban):
        output = auto_highest(A_side, B_side, A_ban, B_ban)
    else:
        for hero in winrates:
            if (hero["name"] in A_side) or (hero["name"] in B_side) or (hero["name"] in A_ban) or (hero["name"] in B_ban):
                pass
            else:
                num = winrates.index(hero)
                
                taken = 1
                while (taken == 1):                    
                    num +=1
                    output = winrates[num]["name"]
                    if output in A_ban or output in B_ban or output in A_side or output in B_side:
                        taken = 1
                    else:
                        taken = 0
                break
    return output



"""

Possible future algorithms:
    To take note: synergy, counters, tiers

    Check winrates for two heroes together, and winrates for two heroes against each other?
    or check winrates for which 

    Personal preferences
    Ban counters to what you intend to pick — eg if you wanna pick Fort ban Vox if he has the highest winrate vs Fort?
"""
