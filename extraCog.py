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
import random


class extraCog:
    def __init__(self, bot):
        self.bot = bot
        self.bot.data = {}
        
    @commands.command()
    async def ping(self):
        await self.bot.say("Pong")
    
    @commands.command()
    async def pong(self):
        await self.bot.say("Ping")
    
    @commands.command()
    async def potato(self):
        choose = ["Tacchan", "Onii Sama", "Raccoon"]
        output = random.choice(choose) + " is potato"
        await self.bot.say(output)
        
    @commands.command(pass_context=True)
    async def server(self, ctx):
        await self.bot.say(ctx.message.server.id)

    @commands.command(pass_context=True)
    async def push(self, ctx, store):
        self.bot.data[ctx.message.server.id] = store
        output = "Value " + store + " stored under " + str(ctx.message.server.id)
        await self.bot.say(output)

    @commands.command(pass_context=True)
    async def pull(self, ctx):
        output = self.bot.data[ctx.message.server.id]
        await self.bot.say(output)



def setup(bot):
    bot.add_cog(extraCog(bot))