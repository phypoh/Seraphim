#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#==============================================================================
# Created on Tue Aug  1 21:00:09 2017
# 
# @author: phypoh
#==============================================================================

import os 
import discord
from discord.ext import commands
from API import hero_list, pull_all
from AI_algos import AI_ban, AI_pick
from utils import print_log, reset_draft

bot = commands.Bot(command_prefix='!')

bot.API_rates = pull_all()


#bot.A_ban = []
#bot.B_ban = []
#bot.A_side = []
#bot.B_side = []
#bot.side = 1

ids = set()
draft_dict = {}

@bot.event
async def on_ready():
    bot.load_extension("timeCog")
    print("timeCog loaded")
    
    bot.load_extension("extraCog")
    print("extraCog loaded")
    
    bot.load_extension("apiCog")
    print("apiCog loaded")
    
    bot.load_extension("auxdraftCog")
    print("auxdraftCog loaded")
    
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')


@bot.command()
async def hello():
    await bot.say("Hello! I'm Seraphim.")

@bot.command()
async def unload(cog):
    bot.unload_extension(cog)
    await bot.say(cog + " unloaded.")

@bot.command()
async def load(cog):
    bot.load_extension(cog)
    await bot.say(cog + " loaded.")
    
@bot.command()
async def reload(cog):
    bot.unload_extension(cog)
    bot.load_extension(cog)
    await bot.say(cog + " reloaded.")



#==============================================================================
# Main Draft UI
#==============================================================================
@bot.command(pass_context=True)
async def start(ctx):
    """
    Starts the draft. Competitive 5v5 format
    """
    global ids
    global draft_dict
    id = ctx.message.author.id

    # Clears the draft data since you are starting a new draft
    data = id_to_dict_clear(id)

    await bot.say("Draft format: (Ban) ABAB (Pick) ABBAABBAAB")
    if data["side"] == 1:
        await bot.say("Player side: A")
    if data["side"] == 0:
        await bot.say("Player side: B")
    
    data["AI_turn"] = data["side"]
    turn_time(id)
    output = turn_check(id)

    await bot.say(output)

def id_to_dict(id):
    """
    Helper function to access draft data based on user id.
    """
    global ids
    global draft_dict

    # If id isn't in draft_dict, set it up.
    if id not in ids:
        ids.add(id)
        return id_to_dict_clear(id)
    else:
        return draft_dict[id]

def id_to_dict_clear(id):
    """
    Clears the values of the dict based on id.
    """
    global ids
    global draft_dict

    draft_dict[id] = {
        "A_ban": [],
        "B_ban": [],
        "A_side": [],
        "B_side": [],
        "side": 1,
        "AI_turn": 1
    }
    return draft_dict[id]

def turn_check(id):
    global ids
    global draft_dict

    data = id_to_dict(id)

    output = ""

    if len(data["B_ban"]) < 2:  # TODO
        if data["AI_turn"] == 0:
            output += "Ban a hero"
            return output
        elif data["AI_turn"] == 1:
            chosen_hero = AI_ban(data["A_side"], data["B_side"], data["A_ban"], data["B_ban"])
            if data["side"] == 0:
                data["A_ban"].append(chosen_hero)
                output += "AI has banned " + chosen_hero + "\n"
                turn_time(id)
                output += turn_check(id)
            elif data["side"] == 1:
                data["B_ban"].append(chosen_hero)
                output += "AI has banned " + chosen_hero + "\n"
                turn_time(id)
                output += turn_check(id)
                
    elif len(data["B_side"]) < 5:
        if data["AI_turn"] == 0:
            output += "Pick a hero"
            return output
        elif data["AI_turn"] == 1:
            chosen_hero = AI_pick(data["A_side"], data["B_side"], data["A_ban"], data["B_ban"])
            if data["side"] == 0:
                data["A_side"].append(chosen_hero)
                output += "AI has selected " + chosen_hero + "\n"
                turn_time(id)
                output += turn_check(id)
            elif data["side"] == 1:
                data["B_side"].append(chosen_hero)
                output += "AI has selected " + chosen_hero + "\n"
                turn_time(id)
                output += turn_check(id)
    elif len(data["B_side"]) == 5:
        output += print_log(bot)

    return output
     
def turn_time(id):
    global ids
    global draft_dict

    data = id_to_dict(id)

    if len(data["B_ban"]) < 2:
        data["AI_turn"] = (data["AI_turn"]+1)%2
        
    elif len(data["B_side"]) < 5:
        #If it's A's turn now
        if (len(data["A_side"])%2 == 0 or (len(data["A_side"])%2 == 1 and len(data["B_side"]) > len(data["A_side"]))):
            if data["side"] == 0:
                data["AI_turn"] = 1
            else:
                data["AI_turn"] = 0
                
        #If it's B's turn now
        else:
            if data["side"] == 1:
                data["AI_turn"] = 1
            else:
                data["AI_turn"] = 0
    else:
        data["AI_turn"] = 2
    

@bot.command(pass_context=True)
async def pick(ctx, *, hero):
    """
    Picks a hero
    """
    global ids
    global draft_dict

    id = ctx.message.author.id
    data = id_to_dict(id)

    hero = hero.title()
    if data["AI_turn"] == 1:
        await bot.say("It's not your turn yet. Can't you be a little patient?")
    elif len(data["B_ban"]) < 2:
        await bot.say("Stop cheating. It's ban phase.")
    elif (hero in data["A_side"] or hero in data["B_side"]):
        await bot.say("Hero has already been picked. Pick another hero.")
    elif (hero in data["A_ban"] or hero in data["B_ban"]):
        await bot.say("Hero has already been banned. Pick another hero.")
    elif (hero not in hero_list):
        await bot.say("Hero does not exist. Pick again.")
    else:
        if data["side"] == 1:
            data["A_side"].append(hero)
            turn_time(id)
            await bot.say(f"{ctx.message.author.nick} has selected {hero}")
        elif bot.side == 0:
            data["B_side"].append(hero)
            turn_time(id)
            await bot.say(f"{ctx.message.author.nick} has selected {hero}")
        output = turn_check(id)
        await bot.say(output)
        
@bot.command(pass_context=True)
async def ban(ctx, *, hero):
    """
    Bans a hero
    """
    global ids
    global draft_dict

    id = ctx.message.author.id
    data = id_to_dict(id)

    hero = hero.title()
    if len(data["B_ban"]) >= 2:
        await bot.say("Stop cheating. You're only supposed to ban a maximum of 2 heroes.")
    elif data["AI_turn"] == 1:
        await bot.say("It's not your turn yet. Can't you be a little patient?")
    elif (hero in data["A_ban"] or hero in data["B_ban"]):
        await bot.say("Hero has already been banned. Ban another hero.")
    elif (hero not in hero_list):
        await bot.say("Hero does not exist. Ban again.")
    else:
        if data["side"] == 1:
            data["A_ban"].append(hero)
            turn_time(id)
            await bot.say(f"{ctx.message.author.nick} has banned {hero}")
        elif bot.side == 0:
            data["B_ban"].append(hero)
            turn_time(id)
            await bot.say(f"{ctx.message.author.nick} has banned {hero}")
        output = turn_check(id)
        await bot.say(output)

bot.run(os.getenv('BOT_TOKEN'))


