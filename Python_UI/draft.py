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
from AI_algos import AI_pick, AI_ban
from API import hero_list, API_rates #, pickrates, banrates

print("List of heroes:", hero_list)


def turn_pick(AI_turn, A_side, B_side, A_ban = [], B_ban = []):
    if AI_turn == 0:
        output = input("Pick a hero. ")
        if (output in A_side or output in B_side):
            print("Hero has already been chosen. Pick another hero. ")
            output = turn_pick(AI_turn, A_side, B_side, A_ban, B_ban)
        elif (output in A_ban or output in B_ban):
            print("Hero has already been banned. Pick another hero. ")
            output = turn_pick(AI_turn, A_side, B_side, A_ban, B_ban)
        elif (output not in hero_list):
            print("Hero does not exist. Pick again. ")
            output = turn_pick(AI_turn, A_side, B_side, A_ban, B_ban)
    elif AI_turn == 1:
        output = AI_pick(A_side, B_side, A_ban, B_ban)
        print("AI has chosen", output)
    return output


def turn_ban(AI_turn, A_side, B_side, A_ban, B_ban):
    if AI_turn == 0:
        output = input("Ban a hero. ")
        if (output in A_side or output in B_side):
            print("Hero has already been chosen. Ban another hero. ")
            output = turn_ban(AI_turn, A_side, B_side, A_ban, B_ban)
        elif (output in A_ban or output in B_ban):
            print("Hero has already been banned. Pick another hero. ")
            output = turn_ban(AI_turn, A_side, B_side, A_ban, B_ban)
        elif (output not in hero_list):
            print("Hero does not exist. Ban again. ")
            output = turn_ban(AI_turn, A_side, B_side, A_ban, B_ban)
    elif AI_turn == 1:
        output = AI_ban(A_side, B_side, A_ban, B_ban)
        print("AI has banned", output)
    return output

def ranked_5v5(side):
    """
    5v5 pick and ban draft. side variable is either A or B, depending on what the player is.
    Format: Double ban then 1-2-2-2-2-1
    """
    if side != 0 and side != 1:
        print("Error. Pick a side: A (0) or B (1) for player.")
        return [], []

    AI_turn = side
    
    A_side = []
    B_side = []
    A_ban = []
    B_ban = []

    """
    Ban Phase
    """
    while len(B_ban) < 2:
        A_chosen = turn_ban(AI_turn, A_side, B_side, A_ban, B_ban)
        A_ban.append(A_chosen)
        
        AI_turn = (AI_turn+1)%2
        
        B_chosen = turn_ban(AI_turn, A_side, B_side, A_ban, B_ban)
        B_ban.append(B_chosen)
    
        AI_turn = (AI_turn+1)%2
    
    """
    Pick Phase
    """
    while len(B_side) < 4:
        A_chosen = turn_pick(AI_turn, A_side, B_side, A_ban, B_ban)
        A_side.append(A_chosen)
        
        AI_turn = (AI_turn+1)%2
        
        B_chosen = turn_pick(AI_turn, A_side, B_side, A_ban, B_ban)
        B_side.append(B_chosen)
        
        B_chosen = turn_pick(AI_turn, A_side, B_side, A_ban, B_ban)
        B_side.append(B_chosen)
        
        AI_turn = (AI_turn+1)%2
        
        A_chosen = turn_pick(AI_turn, A_side, B_side, A_ban, B_ban)
        A_side.append(A_chosen)
        
    A_chosen = turn_pick(AI_turn, A_side, B_side, A_ban, B_ban)
    A_side.append(A_chosen)
    
    AI_turn = (AI_turn+1)%2
    
    B_chosen = turn_pick(AI_turn, A_side, B_side, A_ban, B_ban)
    B_side.append(B_chosen)

    return A_ban, B_ban, A_side, B_side

def pick_5v5(side):
    """
    5v5 pick draft, no bans. side variable is either A or B, depending on what the player is.
    """
    if side != 0 and side != 1:
        print("Error. Pick a side: A (0) or B (1) for player.")
        return [], []

    AI_turn = side
    
    A_side = []
    B_side = []
    
    while len(B_side) < 4:
        A_chosen = turn_pick(AI_turn, A_side, B_side)
        A_side.append(A_chosen)
        
        AI_turn = (AI_turn+1)%2
        
        B_chosen = turn_pick(AI_turn, A_side, B_side)
        B_side.append(B_chosen)
        
        B_chosen = turn_pick(AI_turn, A_side, B_side)
        B_side.append(B_chosen)
        
        AI_turn = (AI_turn+1)%2
        
        A_chosen = turn_pick(AI_turn, A_side, B_side)
        A_side.append(A_chosen)
        
    A_chosen = turn_pick(AI_turn, A_side, B_side)
    A_side.append(A_chosen)
    
    AI_turn = (AI_turn+1)%2
    
    B_chosen = turn_pick(AI_turn, A_side, B_side)
    B_side.append(B_chosen)

    return [], [], A_side, B_side

