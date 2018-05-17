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



class draftCog:
    def __init__(self, bot):
        self.bot = bot
        
        def turn_check(self):
            output = ""
    
            if len(self.bot.B_ban) < 2:
                if self.bot.AI_turn == 0:
                    output += "Ban a hero"
                    return output
                elif self.bot.AI_turn == 1:
                    chosen_hero = AI_ban(self.bot.A_side, self.bot.B_side, self.bot.A_ban, self.bot.B_ban)
                    if self.bot.side == 0:
                        self.bot.A_ban.append(chosen_hero)
                        output += "AI has banned " + chosen_hero + "\n"
                        turn_time()
                        output += turn_check()
                    elif self.bot.side == 1:
                        self.bot.B_ban.append(chosen_hero)
                        output += "AI has banned " + chosen_hero + "\n"
                        turn_time()
                        output += turn_check()
                        
            elif len(self.bot.B_side) < 5:
                if self.bot.AI_turn == 0:
                    output += "Pick a hero"
                    return output
                elif self.bot.AI_turn == 1:
                    chosen_hero = AI_pick(self.bot.A_side, self.bot.B_side, self.bot.A_ban, self.bot.B_ban)
                    if self.bot.side == 0:
                        self.bot.A_side.append(chosen_hero)
                        output += "AI has selected " + chosen_hero + "\n"
                        turn_time()
                        output += turn_check()
                    elif self.bot.side == 1:
                        self.bot.B_side.append(chosen_hero)
                        output += "AI has selected " + chosen_hero + "\n"
                        turn_time()
                        output += turn_check()
            elif len(self.bot.B_side) == 5:
                output += print_log(self.bot)        
            return output

        def turn_time(self):
            if len(self.bot.B_ban) < 2:
                self.bot.AI_turn = (self.bot.AI_turn+1)%2 
                
            elif len(self.bot.B_side) < 5:
                #If it's A's turn now
                if (len(self.bot.A_side)%2 == 0 or (len(self.bot.A_side)%2 == 1 and len(self.bot.B_side) > len(self.bot.A_side))):
                    if self.bot.side == 0:
                        self.bot.AI_turn = 1
                    else:
                        self.bot.AI_turn = 0
                        
                #If it's B's turn now
                else:
                    if self.bot.side == 1:
                        self.bot.AI_turn = 1
                    else:
                        self.bot.AI_turn = 0
            else:
                self.bot.AI_turn = 2

    @commands.command()
    async def start(self):
        """
        Starts the draft. Competitive 5v5 format
        """
        
        await self.bot.say("Draft format: (Ban) ABAB (Pick) ABBAABBAAB")
        if self.bot.side == 1:
            await self.bot.say("Player side: A")
        if self.bot.side == 0:
            await self.bot.say("Player side: B")
        
        self.bot.A_ban = []
        self.bot.B_ban = []
        self.bot.A_side = []
        self.bot.B_side = []
        
        self.bot.AI_turn = self.bot.side
        turn_time()
        output = turn_check()
        await self.bot.say(output)            
    
    @commands.command()
    async def pick(self, hero):
        """
        Picks a hero
        """
        hero = hero.title()
        if self.bot.AI_turn == 1:
            await self.bot.say("It's not your turn yet. Can't you be a little patient?")
        elif len(self.bot.B_ban) < 2:
            await self.bot.say("Stop cheating. It's ban phase.")
        elif (hero in self.bot.A_side or hero in self.bot.B_side):
            await self.bot.say("Hero has alreay been picked. Pick another hero.")
        elif (hero in self.bot.A_ban or hero in self.bot.B_ban):
            await self.bot.say("Hero has already been banned. Pick another hero.")
        elif (hero not in hero_list):
            await self.bot.say("Hero does not exist. Pick again.")
        else:
            if self.bot.side == 1:
                self.bot.A_side.append(hero)
                turn_time()
                await self.bot.say("Player has selected " + hero)
            elif self.bot.side == 0:
                self.bot.B_side.append(hero)
                turn_time()
                await self.bot.say("Player has selected " + hero)
            output = turn_check()
            await self.bot.say(output)
            
    @commands.command()
    async def ban(self, hero):
        """
        Bans a hero
        """
        hero = hero.title()
        if len(self.bot.B_ban) >= 2:
            await self.bot.say("Stop cheating. You're only supposed to ban a maximum of 2 heroes.")
        elif self.bot.AI_turn == 1:
            await self.bot.say("It's not your turn yet. Can't you be a little patient?")
        elif (hero in self.bot.A_ban or hero in self.bot.B_ban):
            await self.bot.say("Hero has already been banned. Ban another hero.")
        elif (hero not in hero_list):
            await self.bot.say("Hero does not exist. Ban again.")
        else:
            if self.bot.side == 1:
                self.bot.A_ban.append(hero)
                turn_time()
                await self.bot.say("Player has banned " + hero)
            elif self.bot.side == 0:
                self.bot.B_ban.append(hero)
                turn_time()
                await self.bot.say("Player has banned " + hero)
            output = turn_check()
            await self.bot.say(output)


def setup(bot):
    bot.add_cog(draftCog(bot))