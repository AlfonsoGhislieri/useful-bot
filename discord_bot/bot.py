import os
from discord.ext import commands
import discord
from dotenv import load_dotenv

load_dotenv()


class Bot(commands.Bot):
    def __init__(self, command_prefix, intents):
        super().__init__(command_prefix=command_prefix, intents=intents)
        self.active_guild = os.getenv("DISCORD_GUILD")

    def find_guild(self):
        return discord.utils.get(self.guilds, name=self.active_guild)

    async def on_ready(self):
        guild = self.find_guild()

        print(f"{self.user} is connected to the following guild:\n" f"{guild.name}(id: {guild.id})")

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
