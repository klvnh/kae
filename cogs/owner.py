import discord
from discord.ext import commands
import traceback
from discord.ext import tasks
from PIL import Image, ImageDraw, ImageFont
import datetime 
from io import BytesIO
import random

async def setup(bot):
    await bot.add_cog(owner(bot))

class owner(commands.Cog):

    """Owner Events"""

    def __init__(self, bot):
        self.bot = bot
        self._last_result = None
        self.steps.start()

    def cog_unload(self):
        self.steps.cancel()

    async def cog_check(self, ctx):
        return await self.bot.is_owner(ctx.author)

    @commands.command(hidden=True)
    async def sync(self, ctx):
        embed = discord.Embed()
        await self.bot.tree.sync()
        embed.add_field(name="Success", value="Successfully synced all commands!")
        await ctx.send(embed=embed)

    @commands.command()
    async def reload(self, ctx):
        paginator = commands.Paginator(prefix='', suffix='')
        for extension in list(self.bot.extensions.keys()):
            try:
                await self.bot.reload_extension(extension)
                paginator.add_line(f"> Succesfully reloaded: ``{extension}``")
            except Exception as e:
                er = getattr(e, 'original', e)
                paginator.add_line(f'\U0001f6ab Failed to load extension: ``{extension}``')
                error = ''.join(traceback.format_exception(type(er), er, er.__traceback__))
                paginator.add_line('`'*3 + f'\n{error}' + '`'*3)

        for page in paginator.pages:
            await ctx.send(page)

    @tasks.loop(seconds=10)
    async def steps(self):
        channel = self.bot.get_channel(1051145679382253628)
        random_steps = str(random.randint(15000, 19500))
        im = Image.open('./template/image.png')
        draw = ImageDraw.Draw(im)
        font1 = ImageFont.truetype(font='./template/font_pro.ttf', size=50)
        font2 = ImageFont.truetype(font='./template/font_round.ttf', size=120)
        font3 = ImageFont.truetype(font='./template/font_pro.ttf', size=40)
        format = (random_steps[:2] + ',' + random_steps[2:])
        month = datetime.datetime.now().strftime("%b")
        day = datetime.datetime.now().strftime("%d")
        year = datetime.datetime.now().strftime("%Y")
        if day[0] == '0':
                day = day[1]
        draw.text((10, 2), 'TOTAL', font=font3, fill=(154,153,159,255))
        draw.text((10, 41), format, font=font2)
        draw.text((355, 108), 'steps', font=font1, fill=(154,153,159,255))
        draw.text((10, 180), f'{month} {day}, {year}', font=font3, fill=(154,153,159,255))
        buffer = BytesIO()
        im.save(buffer, format="PNG")
        buffer.seek(0)
        await channel.send(file=discord.File(buffer, filename="some_image.png"))


    @steps.before_loop
    async def before_steps(self):
        print('waiting...')
        await self.bot.wait_until_ready()