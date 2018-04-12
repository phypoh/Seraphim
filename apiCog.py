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


def setup(bot):
    bot.add_cog(apiCog(bot))