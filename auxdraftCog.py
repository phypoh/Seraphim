#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 25 22:28:07 2018

@author: phypoh
"""

import discord
from discord.ext import commands

from API import hero_list, pull_all
from AI_algos import AI_ban, AI_pick
from utils import print_log, reset_draft

class auxdraftCog:
    """
    Auxillary Draft functions
    """
    
    def __init__(self, bot):
        self.bot = bot
        
    @commands.command()
    async def log(self):
        output = print_log(self.bot)
        await self.bot.say(output)
        
    @commands.command()
    async def reset(self):
        """
        Resets draft
        """
        self.bot = reset_draft(self.bot)
        await self.bot.say("Draft entries have been reset.")
    
    @commands.command()
    async def side(self,letter):
        """
        Sets a side for the draft
        """
        letter = letter.capitalize()
        if letter == "A":
            self.bot.side = 1
            await self.bot.say("Side has been set to A for player.")
    
        elif letter == "B":
            self.bot.side = 0
            await self.bot.say("Side has been set to B for player.")    
        else:
            await self.bot.say("Input unclear. Set side to either A or B")
            
    @commands.command()
    async def myside(self):
        """
        Checks what's your current side of the draft.
        """
        
        if self.bot.side == 1:
            await self.bot.say("Player is on A side.")
        elif self.bot.side == 0:
            await self.bot.say("Player is on B side.")
    
    
    
    @commands.command()
    async def heroes(self):
        """
        Prints a list of heroes
        """
        heroes = sorted(hero_list)
        output = "List of heroes: \n"
        for hero in heroes:
            output += hero + ", "

        await self.bot.say(output)

def setup(bot):
    bot.add_cog(auxdraftCog(bot))
        