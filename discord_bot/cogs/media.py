import discord
import random
import os
from discord.ext import commands
from serpapi import GoogleSearch


class Media(commands.Cog):
    @commands.command(name="image", help="Searches and displays an image")
    async def show_image(self, ctx, *args):

        query = " ".join(args)

        params = {
            "api_key": os.environ.get("SERPAPI_API"),
            "engine": "google",
            "q": query,
            "google_domain": "google.com",
            "hl": "en",
            "num": "10",
            "tbm": "isch",
        }
        # search google api and get random image
        search = GoogleSearch(params)
        results = search.get_dict()
        random_image = random.choice(results["images_results"])

        # create embed
        embed = discord.Embed(title=random_image["title"], color=discord.Color.blue(), url=random_image["link"])
        embed.set_image(url=(random_image["thumbnail"]))

        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Media(bot))
