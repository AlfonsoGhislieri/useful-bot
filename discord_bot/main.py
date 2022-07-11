import discord
import os
from discord_bot.bot import Bot


def main():
    TOKEN = os.environ.get("DISCORD_TOKEN")
    intents = discord.Intents().all()
    bot = Bot(command_prefix="!", intents=intents)

    for file in os.listdir("./discord_bot/cogs"):
        if file.endswith("py"):
            cog_name = file.split(".")[0]
            bot.load_extension(f"discord_bot.cogs.{cog_name}")
            print(f"loaded cog: {cog_name}")

    bot.run(TOKEN)
