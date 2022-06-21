import os
import random
import discord
from discord.ext import commands

def main():
  TOKEN = os.environ.get("DISCORD_TOKEN")
  GUILD = os.environ.get("DISCORD_GUILD")

  intents = discord.Intents.default()
  intents.members = True
  intents.messages = True
  bot = commands.Bot(command_prefix='!',intents=intents)

  @bot.event
  async def on_ready():
    guild = discord.utils.find(lambda g: g.name == GUILD, bot.guilds)

    print(
        f'{bot.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})'
    )

  @bot.event
  async def on_member_join(member):
    guild = discord.utils.find(lambda g: g.name == GUILD, bot.guilds)

    await member.create_dm()
    await member.dm_channel.send(
        f'Hi {member.name}, welcome to {guild.name}'
    )

  @bot.event
  async def on_message(message):
    # guard if message is written by the bot
    if message.author.id == bot.user.id:
      return

    possible_greetings = ["hello", "hey", "hi"]

    if message.content in possible_greetings:
      await message.channel.send(f'Hey <@{message.author.id}>')
    await bot.process_commands(message)

  @bot.command(name="helper", help='bot comes to your aid')
  async def on_message(ctx):
    response = "I am here to help!"
    await ctx.send(response)

  @bot.command(name='roll_dice', help='Simulates rolling dice.')
  async def roll(ctx, number_of_dice : int, number_of_sides : int): 
    max_dice = 100

    if number_of_dice > max_dice:
      await ctx.send(f'Maximum number of dice capped at {max_dice} dice!')
      return 

    dice = [
        str(random.choice(range(1, number_of_sides + 1)))
        for _ in range(number_of_dice)
    ]
    await ctx.send(', '.join(dice))

  bot.run(TOKEN)
