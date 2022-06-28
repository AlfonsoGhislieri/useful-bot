import os
from discord.ext import commands
import random
import discord
from serpapi import GoogleSearch


class Bot(commands.Bot):
    def __init__(self, command_prefix, intents):
        super().__init__(command_prefix=command_prefix, intents=intents)
        self.active_guild = os.environ.get("DISCORD_GUILD")
        self.add_commands()

    async def on_ready(self):
        guild = discord.utils.find(lambda g: g.name == self.active_guild, self.guilds)

        print(f"{self.user} is connected to the following guild:\n" f"{guild.name}(id: {guild.id})")

    async def on_member_join(self, member):
        guild = discord.utils.find(lambda g: g.name == self.active_guild, self.guilds)

        await member.create_dm()
        await member.dm_channel.send(f"Hi {member.name}, welcome to {guild.name}")

    async def on_message(self, message):
        # guard if message is written by the bot
        if message.author.id == self.user.id:
            return

        possible_greetings = ["hello", "hey", "hi"]

        if message.content.lower() in possible_greetings:
            await message.channel.send(f"{message.content.capitalize()} <@{message.author.id}>")
        await self.process_commands(message)

    def add_commands(self):
        @self.command(name="helper", help="bot comes to your aid")
        async def on_message(ctx):
            response = "I am here to help!"
            await ctx.send(response)

        @self.command(name="add_role", help="Adds roles to user")
        async def add_role(ctx, role, member: discord.Member = None):
            member = member or ctx.message.author
            admin = discord.utils.get(ctx.guild.roles, name="Admin")

            if member == ctx.guild.owner or admin in member.roles:
                role = discord.utils.get(ctx.guild.roles, name=role.capitalize())
                if role is None:
                    await ctx.send("Role does not exist")

                await member.add_roles(role)
            else:
                await ctx.send("Invalid permissions")

        @self.command(name="remove_role", help="Removes role from user")
        async def remove_roll(ctx, role, member: discord.Member = None):
            member = member or ctx.message.author
            admin = discord.utils.get(ctx.guild.roles, name="Admin")

            if member == ctx.guild.owner or admin in member.roles:
                role = discord.utils.get(ctx.guild.roles, name=role.capitalize())
                if role is None:
                    await ctx.send("Role does not exist")

                await member.remove_roles(role)
            else:
                await ctx.send("Invalid permissions")

        @self.command(
            name="roll_dice",
            help="Simulates rolling dice, default is 1 d6. Number of sides (optional) Number of dice (optional) \n Eg: !roll_dice 16 2 (rolls 2 16 sided dice)",
        )
        async def roll_dice(ctx, number_of_sides: int = 6, number_of_dice: int = 1):
            max_dice = 100
            min_sides = 2

            if number_of_dice > max_dice:
                return await ctx.send(f"Maximum number of dice capped at {max_dice} dice!")

            if number_of_sides < min_sides:
                return await ctx.send(f"Minimum number of sides must be {min_sides}!")
            dice = [str(random.choice(range(1, number_of_sides + 1))) for _ in range(number_of_dice)]
            await ctx.send(", ".join(dice))

        @self.command(name="flip_coin", help="Flips a coin.")
        async def flip_coin(ctx):
            res = random.choice(["Heads", "Tails"])
            await ctx.send(res)

        @self.command(name="image", help="Searches and displays an image")
        async def show_image(ctx, *args):

            query = " ".join(args)

            params = {
                "api_key": os.environ.get("SERPAPI_API"),
                "engine": "google",
                "q": query,
                "google_domain": "google.com",
                "hl": "en",
                "num": "10",
                "tbm": "isch",
            }
            # search google api and get random image
            search = GoogleSearch(params)
            results = search.get_dict()
            random_image = random.choice(results["images_results"])

            # create embed
            embed = discord.Embed(title=random_image["title"], color=discord.Color.blue(), url=random_image["link"])
            embed.set_image(url=(random_image["thumbnail"]))

            await ctx.send(embed=embed)
