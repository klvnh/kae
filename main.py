import discord 
from discord.ext import commands
import os
from dotenv import load_dotenv
import aiohttp

load_dotenv()
prefix = ["-"]

class Bot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix = prefix, case_insensitive = True, 
        strip_after_prefix=True, 
        activity = discord.Activity(name='your spotify songs!', type=discord.ActivityType.listening), 
        status = discord.Status.idle, 
        intents=discord.Intents.all(), 
        owner_ids = [675104167345258506, 766696711128743966])


    async def setup_hook(self):
        self.session = aiohttp.ClientSession()
        for filename in os.listdir('./cogs'):
            if filename.endswith('.py'):
                await self.load_extension(f'cogs.{filename[:-3]}')
                print(f"{filename[:-3]} has been loaded!")

    async def on_ready(self):
        print(self.user.id) 

if __name__ == '__main__':
    bot = Bot()
    bot.run(os.getenv('TOKEN'))