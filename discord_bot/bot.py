import os
import discord

def main():
  TOKEN = os.environ.get("DISCORD_TOKEN")
  GUILD = os.environ.get("DISCORD_GUILD")

  intents = discord.Intents.default()
  intents.members = True
  client = discord.Client(intents=intents)

  @client.event
  async def on_ready():
    guild = discord.utils.find(lambda g: g.name == GUILD, client.guilds)

    print(
        f'{client.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})'
    )

  @client.event
  async def on_member_join(member):
    await member.create_dm()
    await member.dm_channel.send(
        f'Hi {member.name}, welcome to my Discord server!'
    )

  client.run(TOKEN)
