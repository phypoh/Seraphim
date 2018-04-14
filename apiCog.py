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
    def orderbool(self, order):
        if order in {"ascending", "a", "Ascending", "A"}:
            return False
        else:
            return True

    @commands.command()
    async def update(self):
        self.bot.API_rates = pull_all()
        await self.bot.say("API updated. Cheers, VGpro")
    
    @commands.command()
    async def rates(self, ratename):
        """
        Type !rates win, !rates ban, or !rates pick for the following rates
        """
        
    async def rates(self, ratename=None, order="descending"):
        output = ""
        if ratename is None:
            await self.bot.say("Usage: rates [win/ban/pick]")
        elif ratename == "win":
            num = "winRate"
            output = "Win Rates: \n"
        elif ratename == "ban":
            num = "banRate"
            output = "Ban Rates: \n"
        elif ratename == "pick":
            num = "pickRate"
            output = "Pick Rates: \n"

        reversebool = self.orderbool(order)
        to_print = sorted(self.bot.API_rates, key=lambda k: k[num], reverse=reversebool)
        for rate in to_print:
            output += rate["name"] + ": " + str(rate[num]) + "% \n"
        await self.bot.say(output)
    
    @commands.command()
    async def synergy(self, hero):
        """
        Winrates of two heroes combined.
        """
    async def synergy(self, hero, order="descending"):
        hero = hero.capitalize()
        reversebool = self.orderbool(order)
        synergy = pull_hero(hero)["playingWith"]
        synergy = sorted(synergy, key=lambda k: k["winRate"], reverse=reversebool)
        output = ""
        for teammate in synergy:
            output += teammate["key"] + ": " + str(teammate["winRate"]) + "% \n"
        await self.bot.say(output)
        
    @commands.command()
    async def sr(self,hero, decimal= 3):
        """
        Synergy Ratios. (teammate & hero)/teammate winrates
        """
        
    async def sr(self, hero, order="descending", decimal=3):
        hero = hero.capitalize()
        reversebool = self.orderbool(order)
        synergy = pull_hero(hero)["playingWith"]
        all_heroes = self.bot.API_rates
        synergy_list = []
        output = ""
        for teammate in synergy:
            overall_rate = next(item for item in all_heroes if item["name"] == teammate["key"])
            synergy_list.append([teammate["key"], teammate["winRate"]/overall_rate["winRate"]])
        synergy_list = sorted(synergy_list, key=lambda k: k[1], reverse=reversebool)
        for row in synergy_list:
            output += row[0] + ": " + str(row[1])[:decimal + 2] + " \n"
        await self.bot.say(output)
    
    @commands.command()
    async def srh(self,hero, order="descending", decimal= 3):
        """
        Synergy Ratios. (teammate & hero)/hero winrates
        """
        reversebool = self.orderbool(order)
        synergy = pull_hero(hero)["playingWith"]
        winrate = pull_hero(hero)["winRate"]
        output = ""
        synergy_list = []
        for teammate in synergy:
            synergy_list.append([teammate["key"], teammate["winRate"]/winrate])
        synergy_list = sorted(synergy_list, key=lambda k: k[1], reverse=reversebool)
        for row in synergy_list:
            output += row[0] + ": " + str(row[1])[:decimal + 2] + " \n"
        await self.bot.say(output)
        


def setup(bot):
    bot.add_cog(apiCog(bot))