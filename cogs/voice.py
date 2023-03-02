import platform

import discord
from discord.ext import commands
from discord.ext.commands import Context

from helpers import checks


class Voice(commands.Cog, name="voice"):
    temp_channels = []

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_voice_state_update(self, member: discord.Member, before: discord.VoiceState,
                                    after: discord.VoiceState):
        channel_name = f"{member.display_name}'s 1 on 1"

        if member.bot:
            return

        if after.channel is None:
            pass
        elif after.channel.name == "Create 1 on 1":
            temp_channel = await after.channel.clone(name=channel_name)
            await member.move_to(temp_channel)
            self.temp_channels.append(temp_channel.id)

        if before.channel is None:
            pass
        elif before.channel.id in self.temp_channels:
            if after.channel is None or after.channel is not None:
                if len(before.channel.members) == 0:
                    await before.channel.delete()
                    self.temp_channels.remove(before.channel.id)


async def setup(bot):
    await bot.add_cog(Voice(bot))
