import os
import discord

def main():
  TOKEN = os.environ.get("DISCORD_TOKEN")
  GUILD = os.environ.get("DISCORD_GUILD")
  client = discord.Client()

  @client.event
  async def on_ready():
    for guild in client.guilds:
      if guild.name == GUILD:
          break

    print(
        f'{client.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})'
    )

  client.run(TOKEN)
