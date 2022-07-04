import discord
import os
from discord_bot.bot import Bot


def main():
    TOKEN = os.environ.get("DISCORD_TOKEN")
    intents = discord.Intents.default()
    intents.members = True
    intents.messages = True
    intents.reactions = True
    bot = Bot(command_prefix="!", intents=intents)
    bot.run(TOKEN)
