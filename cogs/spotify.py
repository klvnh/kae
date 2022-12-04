import discord
from discord.ext import commands
from views.spotify_select import Spotify_Select_View
import datetime
from discord import app_commands


class Spotify(commands.Cog):
    def __init__(self, bot):

        """Spotify Events"""
        self.bot = bot
        self.playing_cache = {}


    @commands.Cog.listener()
    async def on_presence_update(self, before, after):
        if before.bot:
            return


        before_spotify = discord.utils.find(
            lambda activity: isinstance(activity, discord.Spotify),
            before.activities)


        after_spotify = discord.utils.find(
            lambda activity: isinstance(activity, discord.Spotify),
            after.activities)


        before_activity = discord.utils.find(
            lambda activity: isinstance(activity, discord.Activity),
            before.activities)


        after_activity = discord.utils.find(
            lambda activity: isinstance(activity, discord.Activity),
            after.activities)    
        
        # check any other changes and return.
        if before.status != after.status or before_activity != after_activity:
            return

        # when user stops listening.
        if after_spotify is None or before_spotify is None and after_spotify is None:
            self.bot.dispatch("websocket_update", "STOPPED")
            return

        # when user starts listening.
        if before_spotify is None and after_spotify is not None:
            self.bot.dispatch("websocket_update", "STARTED")

        # when user changes songs.
        if before_spotify is not None and after_spotify is not None:
            self.bot.dispatch("websocket_update", "SKIPPED")

        if before_spotify is None:
            return
        else:
            try:
                if self.playing_cache[before.id]['song'] == before_spotify.title:
                    if self.playing_cache[before.id]['song'] != before_spotify.title:
                        self.playing_cache[after.id] = {'song': after_spotify.title, 'guild_id': after.guild.id}
                        print('bad', self.playing_cache)
                    else:
                        print('good', self.playing_cache)
                        return
            except:
                self.playing_cache[before.id] = {'song': after_spotify.title, 'guild_id': after.guild.id}
                print('just started', self.playing_cache)

        minutes = int(round(after_spotify.duration.total_seconds()) / 60)
        format = ' '.join(after_spotify.artists)
        embed = discord.Embed(color = 0x2F3136, timestamp=datetime.datetime.now())
        embed.set_author(name='NOW PLAYING.' + ('\u2800' * 19))
        embed.set_footer(text=f'{after.name}#{after.discriminator}', icon_url=after.avatar.url)
        embed.add_field(name=after_spotify.title, value=format, inline=False)
        embed.add_field(name='Duration', value=f"Est. {minutes} minute(s)", inline=False)
        embed.set_thumbnail(url=after_spotify.album_cover_url)
        for channel in after.guild.text_channels:
            if channel.name.startswith('np'):
                await channel.send(embed=embed, view=Spotify_Select_View(after_spotify.track_url))
        

    @app_commands.command(description='Sets the current channel as the now playing channel.')
    async def set_channel(self, interaction):
        self.bot.ids.append(interaction.channel.id)
        await interaction.response.send_message(f'{interaction.channel.mention} has been set as channel.')

async def setup(bot):
    await bot.add_cog(Spotify(bot))