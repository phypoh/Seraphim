#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#==============================================================================
# Created on Tue Aug  1 21:00:09 2017
# 
# @author: phypoh
#==============================================================================


# https://discordapp.com/oauth2/authorize?client_id=341929737557508096&scope=bot
import os
#import datetime  
import discord
from discord.ext import commands
import random
from API import hero_list, pull_all
from AI_algos import AI_ban, AI_pick

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
    print("TimeCog loaded")
    
    bot.load_extension("extraCog")
    print("extraCog loaded")
    
    bot.load_extension("apiCog")
    print("apiCog loaded")
    
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
    await bot.say("Draft format: (Ban) ABAB (Pick) ABBAABBAAB")
    if bot.side == 1:
        await bot.say("Player side: A")
    if bot.side == 0:
        await bot.say("Player side: B")
    reset_draft()
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
    hero = hero.capitalize()
    if bot.AI_turn == 1:
        await bot.say("It's not your turn yet. Can't you be a little patient?")
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
    hero = hero.capitalize()
    if len(bot.B_ban) >= 2:
        await bot.say("Stop cheating. You're only supposed to ban a maximum of 2 heroes.")
    if bot.AI_turn == 1:
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
    


#==============================================================================
# AUXILLARIES
#==============================================================================


@bot.command()
async def log():
    output = print_log()
    await bot.say(output)
    
def print_log():
    output = "A Bans: "
    for ban in bot.A_ban:
        output += ban + " "

    output += "\nB Bans: "
    for ban in bot.B_ban:
        output += ban + " "

    output += "\nA Picks: "
    for pick in bot.A_side:
        output += pick + " "

    output += "\nB Picks: "
    for pick in bot.B_side:
        output += pick + " "        
    return output
    
@bot.command()
async def reset():
    reset_draft()
    await bot.say("Draft entries have been reset.")

def reset_draft():
    bot.A_ban = []
    bot.B_ban = []
    bot.A_side = []
    bot.B_side = []


@bot.command()
async def side(letter):
    letter = letter.capitalize()
    if letter == "A":
        bot.side = 1
        await bot.say("Side has been set to A for player.")

    elif letter == "B":
        bot.side = 0
        await bot.say("Side has been set to B for player.")    
    else:
        await bot.say("Input unclear. Set side to either A or B")
        
@bot.command()
async def see_side():
    if bot.side == 1:
        await bot.say("Player is on A side.")
    elif bot.side == 0:
        await bot.say("Player is on B side.")



@bot.command()
async def heroes():
    output = print_heroes()
    await bot.say(output)

def print_heroes():
    heroes = sorted(hero_list)
    output = "List of heroes: \n"
    for hero in heroes:
        output += hero + ", "
    return output

bot.run(os.getenv('BOT_TOKEN'))


