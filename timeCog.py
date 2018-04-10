#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#==============================================================================
# Created on Tue Aug  1 21:00:09 2017
# 
# @author: phypoh
#==============================================================================


# https://discordapp.com/oauth2/authorize?client_id=341929737557508096&scope=bot

import datetime  
import discord
from discord.ext import commands

class timeCog:
    def __init__(self, bot):
        self.bot = bot
    
#==============================================================================
#     @commands.command()
#     async def nowSGT(self):
#         time = datetime.datetime.now().strftime('%H:%M')
#         output = "The time now is " + time + " SGT"
#         await self.bot.say(output)
#     
#     @commands.command()
#     async def nowCEST(self):
#         time = datetime.datetime.now() + datetime.timedelta(hours=-6)
#         time = time.strftime('%H:%M')
#         output = "The time now is " + time + " CEST"
#         await self.bot.say(output)
#     
#==============================================================================
    @commands.command()
    async def toSGT(self, time_input):
        time = datetime.datetime.strptime(time_input, '%H:%M') + datetime.timedelta(hours=6)
        output = time.strftime('%I:%M %p') + "SGT"
        await self.bot.say(output)


    @commands.command()
    async def nowSGT(self):
        time = datetime.datetime.now().strftime('%I:%M %p')
        output = "The time now is " + time + " SGT"
        await self.bot.say(output)

    @commands.command()
    async def nowCEST(self):
        time = datetime.datetime.now() + datetime.timedelta(hours=-6)
        time = time.strftime('%I:%M %p')
        output = "The time now is " + time + " CEST"
        await self.bot.say(output)


def setup(bot):
    bot.add_cog(timeCog(bot))