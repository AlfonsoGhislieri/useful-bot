import discord
import os
from bot import Bot
from dotenv import load_dotenv

load_dotenv()


def main():
    TOKEN = os.getenv("DISCORD_TOKEN")
    intents = discord.Intents().all()
    bot = Bot(command_prefix="!", intents=intents)

    for file in os.listdir("./discord_bot/cogs"):
        if file.endswith("py"):
            cog_name = file.split(".")[0]
            bot.load_extension(f"cogs.{cog_name}")
            print(f"loaded cog: {cog_name}")

    bot.run(TOKEN)


main()
