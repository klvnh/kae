import discord
from discord.ext import commands
from discord import app_commands

async def setup(bot):
    await bot.add_cog(Slash(bot))

class Slash(commands.Cog):

    """Slash Events"""

    def __init__(self, bot):
        self.bot = bot
        

    @app_commands.command(name='Hello', brief='A default slash command.')
    async def hello_slash(self, interaction):
        await interaction.response.send_message('Hello')