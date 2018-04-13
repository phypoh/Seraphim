#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr  9 09:51:10 2018

@author: phypoh
"""


#==============================================================================
# MISC COMMANDS
#==============================================================================

import discord
from discord.ext import commands
from API import pull_hero, pull_all


class apiCog:
    def __init__(self, bot):
        self.bot = bot
        
    @commands.command()
    async def update(self):
        self.bot.API_rates = pull_all()
        await self.bot.say("API updated. Cheers, VGpro")
    
    @commands.command()
    async def rates(self, ratename):
        output = ""
        if ratename == "win":
            num = "winRate"
            output = "Win Rates: \n"
        elif ratename == "ban":
            num = "banRate"
            output = "Ban Rates: \n"
        elif ratename == "pick":
            num = "pickRate"
            output = "Pick Rates: \n"
        
        to_print = sorted(self.bot.API_rates, key=lambda k: k[num], reverse = True)
        for rate in to_print:
            output += rate["name"] + ": " + str(rate[num]) + "% \n"
        await self.bot.say(output)
    
    @commands.command()
    async def synergy(self, hero):
        hero = hero.capitalize()
        synergy = pull_hero(hero)["playingWith"]
        synergy = sorted(synergy, key=lambda k: k["winRate"], reverse = True)
        output = ""
        for teammate in synergy:
            output += teammate["key"] + ": " + str(teammate["winRate"]) + "% \n"
        await self.bot.say(output)
        
    @commands.command()
    async def synratios(self,hero, decimal= 3):
        synergy = pull_hero(hero)["playingWith"]
        all_heroes = self.bot.API_rates
        synergy_list = []
        output = ""
        for teammate in synergy:
            overall_rate = next(item for item in all_heroes if item["name"] == teammate["key"])
            synergy_list.append([teammate["key"], teammate["winRate"]/overall_rate["winRate"]])
        for row in synergy_list:
            output += row[0] + ": " + str(row[1])[:decimal + 2] + " \n"
        await self.bot.say(output)
        


def setup(bot):
    bot.add_cog(apiCog(bot))