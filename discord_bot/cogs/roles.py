from discord.ext import commands
import discord


class Roles(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def valid_role(self, role):
        if role is None:
            return False
        else:
            return True

    def valid_permissions(self, ctx):
        admin = discord.utils.get(ctx.guild.roles, name="Admin")
        if ctx.message.author == ctx.guild.owner or admin in ctx.message.author.roles:
            return True
        else:
            return False

    def check_invalid_role_assignment(self, ctx, role):
        if not self.valid_permissions(ctx):
            return "Invalid permissions"

        if not self.valid_role(role):
            return "Role does not exist"

    @commands.command(name="add_role", help="Adds roles to user")
    async def add_role(self, ctx, role: str, member: discord.Member = None):
        member = member or ctx.message.author
        role = discord.utils.get(ctx.guild.roles, name=role.capitalize())

        invalid_role_assignment = self.check_invalid_role_assignment(ctx, role)
        if invalid_role_assignment:
            return await ctx.send(invalid_role_assignment)

        await member.add_roles(role)

    @commands.command(name="remove_role", help="Removes role from user")
    async def remove_role(self, ctx, role: str, member: discord.Member = None):
        member = member or ctx.message.author
        role = discord.utils.get(ctx.guild.roles, name=role.capitalize())

        invalid_role_assignment = self.check_invalid_role_assignment(ctx, role)
        if invalid_role_assignment:
            return await ctx.send(invalid_role_assignment)

        await member.remove_roles(role)


def setup(bot):
    bot.add_cog(Roles(bot))
