import discord
from discord.ext import commands
from discord import app_commands
import datetime

async def setup(bot):
    await bot.add_cog(Slash(bot))

class Slash(commands.Cog):

    """Slash Events"""

    def __init__(self, bot):
        self.bot = bot
        

    @app_commands.command(name='hello', description='A default slash command.')
    async def hello_slash(self, interaction):
        await interaction.response.send_message(f'Hello {interaction.user.id}, Invoked at {datetime.datetime.now()}')