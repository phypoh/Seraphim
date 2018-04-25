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


bot.A_ban = []
bot.B_ban = []
bot.A_side = []
bot.B_side = []
bot.side = 1

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
@bot.command()
async def start():
    """
    Starts the draft. Competitive 5v5 format
    """
    
    await bot.say("Draft format: (Ban) ABAB (Pick) ABBAABBAAB")
    if bot.side == 1:
        await bot.say("Player side: A")
    if bot.side == 0:
        await bot.say("Player side: B")
    
    bot.A_ban = []
    bot.B_ban = []
    bot.A_side = []
    bot.B_side = []
    
    bot.AI_turn = bot.side
    turn_time()
    output = turn_check()
    await bot.say(output)

def turn_check():
    output = ""

    if len(bot.B_ban) < 2:
        if bot.AI_turn == 0:
            output += "Ban a hero"
            return output
        elif bot.AI_turn == 1:
            chosen_hero = AI_ban(bot.A_side, bot.B_side, bot.A_ban, bot.B_ban)
            if bot.side == 0:
                bot.A_ban.append(chosen_hero)
                output += "AI has banned " + chosen_hero + "\n"
                turn_time()
                output += turn_check()
            elif bot.side == 1:
                bot.B_ban.append(chosen_hero)
                output += "AI has banned " + chosen_hero + "\n"
                turn_time()
                output += turn_check()
                
    elif len(bot.B_side) < 5:
        if bot.AI_turn == 0:
            output += "Pick a hero"
            return output
        elif bot.AI_turn == 1:
            chosen_hero = AI_pick(bot.A_side, bot.B_side, bot.A_ban, bot.B_ban)
            if bot.side == 0:
                bot.A_side.append(chosen_hero)
                output += "AI has selected " + chosen_hero + "\n"
                turn_time()
                output += turn_check()
            elif bot.side == 1:
                bot.B_side.append(chosen_hero)
                output += "AI has selected " + chosen_hero + "\n"
                turn_time()
                output += turn_check()
    elif len(bot.B_side) == 5:
        output += print_log()        
    return output
     
def turn_time():
    if len(bot.B_ban) < 2:
        bot.AI_turn = (bot.AI_turn+1)%2 
        
    elif len(bot.B_side) < 5:
        #If it's A's turn now
        if (len(bot.A_side)%2 == 0 or (len(bot.A_side)%2 == 1 and len(bot.B_side) > len(bot.A_side))):
            if bot.side == 0:
                bot.AI_turn = 1
            else:
                bot.AI_turn = 0
                
        #If it's B's turn now
        else:
            if bot.side == 1:
                bot.AI_turn = 1
            else:
                bot.AI_turn = 0
    else:
        bot.AI_turn = 2
        
    

@bot.command()
async def pick(hero):
    """
    Picks a hero
    """
    hero = hero.title()
    if bot.AI_turn == 1:
        await bot.say("It's not your turn yet. Can't you be a little patient?")
    elif len(bot.B_ban) < 2:
        await bot.say("Stop cheating. It's ban phase.")
    elif (hero in bot.A_side or hero in bot.B_side):
        await bot.say("Hero has alreay been picked. Pick another hero.")
    elif (hero in bot.A_ban or hero in bot.B_ban):
        await bot.say("Hero has already been banned. Pick another hero.")
    elif (hero not in hero_list):
        await bot.say("Hero does not exist. Pick again.")
    else:
        if bot.side == 1:
            bot.A_side.append(hero)
            turn_time()
            await bot.say("Player has selected " + hero)
        elif bot.side == 0:
            bot.B_side.append(hero)
            turn_time()
            await bot.say("Player has selected " + hero)
        output = turn_check()
        await bot.say(output)
        
@bot.command()
async def ban(hero):
    """
    Bans a hero
    """
    hero = hero.title()
    if len(bot.B_ban) >= 2:
        await bot.say("Stop cheating. You're only supposed to ban a maximum of 2 heroes.")
    elif bot.AI_turn == 1:
        await bot.say("It's not your turn yet. Can't you be a little patient?")
    elif (hero in bot.A_ban or hero in bot.B_ban):
        await bot.say("Hero has already been banned. Ban another hero.")
    elif (hero not in hero_list):
        await bot.say("Hero does not exist. Ban again.")
    else:
        if bot.side == 1:
            bot.A_ban.append(hero)
            turn_time()
            await bot.say("Player has banned " + hero)
        elif bot.side == 0:
            bot.B_ban.append(hero)
            turn_time()
            await bot.say("Player has banned " + hero)
        output = turn_check()
        await bot.say(output)

bot.run(os.getenv('BOT_TOKEN'))


