import os
import discord

def main():
  TOKEN = os.environ.get("DISCORD_TOKEN")
  client = discord.Client()

  @client.event
  async def on_ready():
      print(f'{client.user} has connected to Discord!')

  client.run(TOKEN)
