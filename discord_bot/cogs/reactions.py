from discord.ext import commands
import discord


class Reactions(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.select_role_channel_name = "select-role"
        self.emoji_dict = {"Nerd": "🥸", "Snek": "🐍", "Gamer": "🕹"}
        self.select_role_channel_id = None
        self.select_role_message_id = None

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

    @commands.Cog.listener()
    async def on_ready(self):
        guild = self.bot.find_guild()

        # checks if select-role channel already exists
        channel = next((channel for channel in guild.channels if channel.name == self.select_role_channel_name), None)

        if channel == None:
            await self.create_select_role_channel(guild)
            await self.send_select_role_message(guild)
        else:
            # assign select_role ids
            self.select_role_channel_id = channel.id
            self.select_role_message_id = channel.last_message_id

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        guild = discord.utils.get(self.bot.guilds, id=payload.guild_id)
        member = discord.utils.get(guild.members, id=payload.user_id)

        if payload.channel_id == self.select_role_channel_id and payload.message_id == self.select_role_message_id:
            for key, value in self.emoji_dict.items():
                if value == str(payload.emoji):
                    role = discord.utils.get(guild.roles, name=key)
                    await member.add_roles(role)

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        guild = discord.utils.get(self.bot.guilds, id=payload.guild_id)
        member = discord.utils.get(guild.members, id=payload.user_id)

        if payload.channel_id == self.select_role_channel_id and payload.message_id == self.select_role_message_id:
            for key, value in self.emoji_dict.items():
                if value == str(payload.emoji):
                    role = discord.utils.get(guild.roles, name=key)
                    await member.remove_roles(role)


def setup(bot):
    bot.add_cog(Reactions(bot))
