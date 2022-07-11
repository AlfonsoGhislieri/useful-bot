from discord.ext import commands
import random


class Chance(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(
        name="roll_dice",
        help="Simulates rolling dice, default is 1 d6. Number of sides (optional) Number of dice (optional) \n Eg: !roll_dice 16 2 (rolls 2 16 sided dice)",
    )
    async def roll_dice(self, ctx, number_of_sides: int = 6, number_of_dice: int = 1):
        max_dice = 100
        min_sides = 2

        if number_of_dice > max_dice:
            return await ctx.send(f"Maximum number of dice capped at {max_dice} dice!")

        if number_of_sides < min_sides:
            return await ctx.send(f"Minimum number of sides must be {min_sides}!")
        dice = [str(random.choice(range(1, number_of_sides + 1))) for _ in range(number_of_dice)]
        await ctx.send(", ".join(dice))

    @commands.command(name="flip_coin", help="Flips a coin.")
    async def flip_coin(self, ctx):
        res = random.choice(["Heads", "Tails"])
        await ctx.send(res)


def setup(bot):
    bot.add_cog(Chance(bot))
