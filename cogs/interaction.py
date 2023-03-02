from math import floor

import aiosqlite
import discord
from discord.ext import commands
from discord.ext.commands import Context

from helpers import checks, db_manager
from helpers.db_manager import get_level, get_xp, get_normal, get_leave, get_fake


class Interaction(commands.Cog, name="interaction"):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(
        name="balance",
        description="Show your current Token balance"
    )
    @checks.not_blacklisted()
    async def balance(self, context: Context):
        """
        This is a command to check your balance.
        :param context: The application command context.
        """
        async with aiosqlite.connect("database/database.db"):
            balance = await db_manager.get_balance(context.author.id, context.guild.id)
            if balance == 0:
                embed = discord.Embed(
                    title="Balance",
                    description="You don't have any Tokens yet.",
                    color=0xe08621
                )
                await context.send(embed=embed, ephemeral=True)
            else:
                embed = discord.Embed(
                    title="Balance",
                    description=f"You have **{balance}** Tokens.",
                    color=0x6930C3
                )
                await context.send(embed=embed, ephemeral=True)

    @commands.hybrid_command(
        name="level",
        description="Show your current level."
    )
    @checks.not_blacklisted()
    async def level(self, context: Context):
        """
        This is a command to show your current level.

        :param context: The application command context.
        """
        async with aiosqlite.connect("database/database.db"):
            level = await db_manager.get_level(context.author.id, context.guild.id)
            if level is None:
                embed = discord.Embed(
                    title="Level",
                    description="You are at level **0**.",
                    color=0x6930C3
                )
                await context.send(embed=embed)
            else:
                embed = discord.Embed(
                    title="Level",
                    description=f"You are level **{level}**.",
                    color=0x6930C3
                )
                await context.send(embed=embed)

    @commands.hybrid_group(
        naem="xp",
        description="Show the amount of XP required to level up."
    )
    @checks.not_blacklisted()
    async def xp(self, context: Context) -> None:
        """
        Lets you add or remove a user from not being able to use the bot.

        :param context: The hybrid command context.
        """
        if context.invoked_subcommand is None:
            embed = discord.Embed(
                title="XP",
                description="You need to specify a subcommand.\n\n**Subcommands:**\n`required` - Show the amount of XP required to level up.",
                color=0xE02B2B
            )
            await context.send(embed=embed)

    @xp.command(
        base="xp",
        name="required",
        description="Show the amount of XP required to level up."
    )
    @checks.not_blacklisted()
    async def xp_required(self, context: Context):
        """
        This is a command to show the amount of XP required to level up.

        :param context: The application command context.
        """
        author = context.author
        guild = context.guild
        async with aiosqlite.connect("database/database.db"):
            current_level = await db_manager.get_level(context.author.id, context.guild.id)
            if current_level == 0:
                current_xp = await get_xp(author.id, guild.id)
                xp_req = 100 - floor(current_xp)
                embed = discord.Embed(
                    title="XP Required",
                    description=f"You need **{xp_req}** XP to level up.",
                    color=0x6930C3
                )
                await context.send(embed=embed)
            else:
                current_level = await get_level(author.id, guild.id)
                current_xp = await get_xp(author.id, guild.id)
                xp_req = floor(((current_level / 0.07) ** 2) - floor(current_xp))
                embed = discord.Embed(
                    title="XP Required",
                    description=f"You need **{xp_req}** XP to level up.",
                    color=0x6930C3
                )
                await context.send(embed=embed)

    @commands.hybrid_command(
        name="leaderboard",
        description="Show the leaderboard of the server."
    )
    @checks.not_blacklisted()
    async def leaderboard(self, context: Context):
        """
        This is a command to show the leaderboard of the server.

        :param context: The application command context.
        """
        async with aiosqlite.connect("database/database.db"):
            leaderboard = await db_manager.get_level_leaderboard(context.guild.id)
            level = discord.Embed(
                title="**Level Leaderboard**",
                description="Here is top 10 users of the server based on level.",
                color=0x6930C3
            )
            for i in range(10):
                try:
                    member = context.guild.get_member(leaderboard[i][0]) or await context.guild.fetch_member(
                        leaderboard[i][0])
                    level.add_field(
                        name=f"{i + 1}. {member}",
                        value=f"Level: {leaderboard[i][1]}",
                        inline=False
                    )
                except IndexError:
                    break
                except discord.errors.NotFound:
                    return await context.send(f"Could not find member with ID {leaderboard[i][0]}", ephemeral=True)
            leaderboard = await db_manager.get_invite_leaderboard(context.guild.id)
            invite = discord.Embed(
                title="**Invite Leaderboard**",
                description="Here is top 10 users of the server based on invites.",
                color=0x6930C3
            )
            for i in range(10):
                try:
                    total = leaderboard[i][1] - (leaderboard[i][2] + leaderboard[i][3])
                    member = context.guild.get_member(leaderboard[i][1]) or await context.guild.fetch_member(
                        leaderboard[i][0])
                    invite.add_field(
                        name=f"{i + 1}. {member}",
                        value=f"Invites: {total}",
                        inline=False
                    )
                except IndexError:
                    break
                except discord.errors.NotFound:
                    return await context.send(f"Could not find member with ID {leaderboard[i][1]}", ephemeral=True)
                await context.send(embeds=[level, invite])

    @commands.hybrid_command(
        name="invites",
        description="Show the amount of invites you have."
    )
    @checks.not_blacklisted()
    async def invites(self, context: Context):
        """
        This is a command to show the amount of invites you have.

        :param context: The application command context.
        """
        async with aiosqlite.connect("database/database.db"):
            normal = await get_normal(context.guild.id, context.author.id)
            left = await get_leave(context.guild.id, context.author.id)
            fake = await get_fake(context.guild.id, context.author.id)
            if ((normal and left and fake) == 0) or ((normal and left and fake) is None):
                embed = discord.Embed(
                    title="Invites",
                    description="You have no invites.",
                    color=0x6930C3
                )
                await context.send(embed=embed)
            else:

                total = normal - (left + fake)
                embed = discord.Embed(
                    title="Invites",
                    description=f"You have **{total}** invites.\nInvited members left: {left}\nFake accounts invited: {fake}",
                    color=0x6930C3
                )
                await context.send(embed=embed)
                if fake < 0:
                    embed.set_footer(
                        text="For account to count as real it must be at least week old."
                    )


async def setup(bot):
    await bot.add_cog(Interaction(bot))
