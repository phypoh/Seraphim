#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 20 00:01:38 2018

@author: phypoh
"""

#Testing

import requests
import json
from API import hero_list, API_rates #, pickrates, banrates
from API import pull_hero


"""
Choose your AI algorithm here.
"""
def AI_pick(A_side, B_side, A_ban, B_ban):
    #return auto_highest(A_side, B_side, A_ban, B_ban)
    #return account_roles(A_side, B_side, A_ban, B_ban)
    return synergy_counter_role(A_side, B_side, A_ban, B_ban)

def AI_ban(A_side, B_side, A_ban, B_ban):
    return ban_second_highest(A_side, B_side, A_ban, B_ban)

"""
Picking algorithms

"""

def auto_highest(A_side, B_side, A_ban = [], B_ban = []):
    for hero in API_rates:
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
        for hero in API_rates:
            if (hero["name"] in A_side) or (hero["name"] in B_side) or (hero["name"] in A_ban) or (hero["name"] in B_ban):
                pass
            else:
                num = API_rates.index(hero)
                
                taken = 1
                while (taken == 1):                    
                    num +=1
                    output = API_rates[num]["name"]
                    if output in A_ban or output in B_ban or output in A_side or output in B_side:
                        taken = 1
                    else:
                        taken = 0
                break
    return output

def account_roles(A_side, B_side, A_ban = [], B_ban = []):
    """
    Accounts for roles in 5v5. Warning: Does not account for lane position
    """
    team_roles = {"Carry" : 3, "Captain" : 1, "Jungler" : 1}
    
    if len(A_side)%2 == 0 or (len(A_side)%2 == 1 and len(B_side) > len(A_side)) :
        #A side
        for name in A_side:
            data = [hero for hero in API_rates if hero['name'] == name]
            roles = data[0]["roles"]
            for role in roles:            
                team_roles[role] -= 1/len(roles)
        print("A side", team_roles)

    else:
        #B side
        for name in B_side:
            data = [hero for hero in API_rates if hero['name'] == name]
            roles = data[0]["roles"]
            for role in roles:            
                team_roles[role] -= 1/len(roles)
        print("B side", team_roles)
        
    for hero in API_rates:
        if (hero["name"] in A_side) or (hero["name"] in B_side) or (hero["name"] in A_ban) or (hero["name"] in B_ban) :
            pass
        else:
            for role in hero["roles"]:
                if team_roles[role] > 0:
                    print(hero["roles"])
                    return hero["name"]
                else:
                    pass
    return "NIL"

def synergy_counter_role(A_side, B_side, A_ban = [], B_ban = []):
    """
    Accounts for synergy of heroes, counters, as well as roles
    """
    
    #Decide which team
    if len(A_side)%2 == 0 or (len(A_side)%2 == 1 and len(B_side) > len(A_side)):
        team_side = "A"
        print("AI is on A Side")
        my_team = A_side
        enemy_team = B_side
    else:
        team_side = "B"
        my_team = B_side
        enemy_team = A_side
        print("AI is on B Side")
    
    #Role accounting 
    team_roles = {"Carry" : 3, "Captain" : 1, "Jungler" : 1}
    for name in my_team:
        data = [hero for hero in API_rates if hero['name'] == name]
        roles = data[0]["roles"]
        for role in roles:            
            team_roles[role] -= 1/len(roles)
    print(team_roles)

    candidates = []
    #Obtain eligible candidates by roles
    for hero in API_rates:
        if (hero["name"] in A_side) or (hero["name"] in B_side) or (hero["name"] in A_ban) or (hero["name"] in B_ban) :
            pass
        else:
            for role in hero["roles"]:
                if team_roles[role] > 0:
                    candidates.append(hero["name"])
                    break
                else:
                    pass 
    
    nominees = get_nominees(candidates, my_team, enemy_team)
    return nominees[0]["name"]


def get_nominees(candidates, my_team, enemy_team):
    nominees = []
    
    candidate_threshold = 10
    for candidate in candidates[:candidate_threshold]:
        nominees.append({"name": candidate, "synergy": 1, "counter":1, "overall": 1})
    
    #Add synergy and counter indexes
    for teammate in my_team:
        hero_data = pull_hero(teammate)
        synergy_data = hero_data["playingWith"]
        synergy_rates = [hero for hero in synergy_data if hero['key'] in candidates[:candidate_threshold]]
        
        for nominee in nominees:
            match_row = [hero for hero in synergy_rates if hero['key'] == nominee["name"]]
            nominee["synergy"] *= match_row[0]["winRate"]/100

     #Add synergy and counter indexes
    for enemy in enemy_team:
        hero_data = pull_hero(enemy)
        counter_data = hero_data["playingAgainst"]
        counter_rates = [hero for hero in counter_data if hero['key'] in candidates[:candidate_threshold]]
        
        for nominee in nominees:
            match_row = [hero for hero in counter_rates if hero['key'] == nominee["name"]]
            nominee["counter"] *= (1-match_row[0]["winRate"]/100)

    #Calculate overall index
    for nominee in nominees:
        nominee["overall"] = nominee["synergy"]*nominee["counter"]
                            
    nominees = sorted(nominees, key=lambda k: k['overall'], reverse = True) 
    for nominee in nominees:
        print(nominee["name"], nominee["overall"])
    #print(nominees)
    
    return nominees
        
        
        
        
    



"""
Possible future algorithms:
    To take note: synergy, counters, tiers

    Check API_rates for two heroes together, and API_rates for two heroes against each other?
    or check API_rates for which 

    Personal preferences
    Ban counters to what you intend to pick — eg if you wanna pick Fort ban Vox if he has the highest winrate vs Fort?
"""
