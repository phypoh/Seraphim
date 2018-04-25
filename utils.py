"""
Utility functions
"""


def print_log(bot):
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