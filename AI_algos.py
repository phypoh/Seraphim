#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 20 00:01:38 2018

@author: phypoh
"""

#Testing

import requests
import json
from API import hero_list, hero_range, API_rates #, pickrates, banrates
from API import pull_hero


"""
Choose your AI algorithm here.
"""
def AI_pick(A_side, B_side, A_ban, B_ban):
    #return auto_highest(A_side, B_side, A_ban, B_ban)
    #return account_roles(A_side, B_side, A_ban, B_ban)
    return Elim_Index(A_side, B_side, A_ban, B_ban)

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
    
    if len(A_side)%2 == 0 or (len(A_side)%2 == 1 and len(B_side) > len(A_side)):
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

#==============================================================================
# AUXILIARY FUNCTIONS
#==============================================================================

def count_roles(my_team, role_data):
    team_roles = {"Carry" : 3, "Captain" : 1, "Jungler" : 1}
    for name in my_team:
        data = [hero for hero in role_data if hero['name'] == name]
        roles = data[0]["roles"]
        for role in roles:            
            team_roles[role] -= 1/len(roles)
    #print(team_roles)
    return team_roles
    
def count_range(my_team, range_data):
    team_range = {"melee" : 3, "ranged" : 3}
    for name in my_team:
        if range_data[name] == "both":
            team_range["melee"] -= 0.5
            team_range["ranged"] -= 0.5
        else:
            team_range[range_data[name]] -= 1
    return team_range

def eliminate_banned_picked(heroes, A_side, B_side, A_ban, B_ban):
    to_eliminate = A_side + B_side + A_ban + B_ban
    for hero in to_eliminate:
        try:
            heroes.remove(hero)
        except ValueError:
            pass
    return heroes

def eliminate_by_role(heroes, team_roles):
    for hero in API_rates:
        viable = 0
        for role in hero["roles"]:
            if team_roles[role] > 0:
                viable = 1
                #print(hero["name"], "viable")
                break
        if viable == 0:
            #print(hero["name"], "remove")
            try:
                heroes.remove(hero["name"])
            except ValueError:
                pass
    return heroes
    
def eliminate_by_range(heroes, team_range, range_data):
    for mode in team_range:
        if team_range[mode] <= 0:
            for hero in heroes:
                if range_data[hero] == mode:
                    try:
                        heroes.remove(hero)
                    except ValueError:
                        pass
            break
    return heroes
                        
        
#==============================================================================
# INDEX PROCESSORS
#==============================================================================

def synergy_multiplier(index, winrate):
    multiplier = winrate/50
    index *= multiplier
    return index

def counter_multiplier(index, winrate):
    multiplier = (100-winrate)/50
    index *= multiplier
    return index


#==============================================================================
# CURRENT ALGO
#==============================================================================

def Elim_Index(A_side, B_side, A_ban = [], B_ban = []):
    """
    Synergy Counter Roles Range
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
    
    #Role and range accounting 
    team_roles = count_roles(my_team, API_rates)
    team_range = count_range(my_team, hero_range)

    #Elimination process
    candidates = list(hero_list)
    candidates = eliminate_banned_picked(candidates, A_side, B_side, A_ban, B_ban)
    candidates = eliminate_by_role(candidates, team_roles)
    candidates = eliminate_by_range(candidates, team_range, hero_range)
    
    
    nominees = SC_index_calc(candidates, my_team, enemy_team)
    return nominees[0]["name"]


def SC_index_calc(candidates, my_team, enemy_team):
    candidate_threshold = 10
    nominees = []
    
    for candidate in candidates[:candidate_threshold]:
        nominees.append({"name": candidate, "synergy": 1, "counter":1, "overall": 1})
    
    if len(my_team)> 0:
        for teammate in my_team:
            hero_data = pull_hero(teammate)["playingWith"]
            hero_data = [hero for hero in hero_data if hero['key'] in candidates[:candidate_threshold]]
            
            for nominee in nominees:
                match_row = [hero for hero in hero_data if hero['key'] == nominee["name"]]
                winrate = match_row[0]["winRate"]
                nominee["synergy"] = synergy_multiplier(nominee["synergy"], winrate)
    
    if len(enemy_team)> 0:
        for enemy in my_team:
            hero_data = pull_hero(enemy)["playingAgainst"]
            hero_data = [hero for hero in hero_data if hero['key'] in candidates[:candidate_threshold]]
            
            for nominee in nominees:
                match_row = [hero for hero in hero_data if hero['key'] == nominee["name"]]
                winrate = match_row[0]["winRate"]
                nominee["counter"] = counter_multiplier(nominee["counter"], winrate)
    
    for nominee in nominees:
        nominee["overall"] = nominee["synergy"]*nominee["counter"]
    
    nominees = sorted(nominees, key=lambda k: k["overall"], reverse = True) 
    for nominee in nominees:
        print(nominee["name"], nominee["synergy"], nominee["counter"], nominee["overall"])
    #print(nominees)
    
    return nominees
        


#==============================================================================
# OLD ALGO
#==============================================================================

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
