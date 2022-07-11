import os
from discord.ext import commands
import random
import discord
from serpapi import GoogleSearch


class Bot(commands.Bot):
    def __init__(self, command_prefix, intents):
        super().__init__(command_prefix=command_prefix, intents=intents)
        self.active_guild = os.environ.get("DISCORD_GUILD")
        self.select_role_channel_name = "select-role"
        self.emoji_dict = {"Nerd": "🥸", "Snek": "🐍", "Gamer": "🕹"}
        self.select_role_channel_id = None
        self.select_role_message_id = None
        self.add_commands()

    def find_guild(self):
        return discord.utils.get(self.guilds, name=self.active_guild)

    def create_select_role_embed(self):
        embed_description = ""
        for emoji in self.emoji_dict:
            embed_description += f"{emoji} - {self.emoji_dict[emoji]}\n"

        return discord.Embed(
            title="React to this message to get your role",
            description=embed_description,
            color=discord.Color.green(),
        )

    async def send_select_role_message(self, guild):
        # find newly created channel and seed starting message
        channel = next(x for x in guild.channels if x.name == self.select_role_channel_name)

        message = await channel.send(embed=self.create_select_role_embed())
        self.select_role_message_id = message.id

        # add emoji reactions to message
        for emoji in self.emoji_dict.values():
            await message.add_reaction(emoji)

    async def create_select_role_channel(self, guild):
        overwrites = {guild.default_role: discord.PermissionOverwrite(send_messages=False, add_reactions=False)}

        channel = await guild.create_text_channel(name=self.select_role_channel_name, overwrites=overwrites)
        self.select_role_channel_id = channel.id

    async def on_ready(self):
        guild = self.find_guild()

        # checks if select-role channel already exists
        channel = next((channel for channel in guild.channels if channel.name == self.select_role_channel_name), None)

        if channel == None:
            await self.create_select_role_channel(guild)
            await self.send_select_role_message(guild)
        else:
            # assign select_role ids
            self.select_role_channel_id = channel.id
            self.select_role_message_id = channel.last_message_id

        print(f"{self.user} is connected to the following guild:\n" f"{guild.name}(id: {guild.id})")

    async def on_raw_reaction_add(self, payload):
        guild = discord.utils.get(self.guilds, id=payload.guild_id)
        member = discord.utils.get(guild.members, id=payload.user_id)

        if payload.channel_id == self.select_role_channel_id and payload.message_id == self.select_role_message_id:
            for key, value in self.emoji_dict.items():
                if value == str(payload.emoji):
                    role = discord.utils.get(guild.roles, name=key)
                    await member.add_roles(role)

    async def on_raw_reaction_remove(self, payload):
        guild = discord.utils.get(self.guilds, id=payload.guild_id)
        member = discord.utils.get(guild.members, id=payload.user_id)

        if payload.channel_id == self.select_role_channel_id and payload.message_id == self.select_role_message_id:
            for key, value in self.emoji_dict.items():
                if value == str(payload.emoji):
                    role = discord.utils.get(guild.roles, name=key)
                    await member.remove_roles(role)

    async def on_member_join(self, member):
        guild = self.find_guild()

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
