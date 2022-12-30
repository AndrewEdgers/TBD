""""
Copyright © Krypton 2019-2022 - https://github.com/kkrypt0nn (https://krypton.ninja)
Description:
🐍 A simple template to start to code your own and personalized discord bot in Python programming language.

Version: 5.4.1
"""
import aiosqlite
import discord
from discord.ext import commands
from discord.ext.commands import Context

from helpers import checks, db_manager
from helpers.db_manager import get_level, get_xp


class Interaction(commands.Cog, name="interaction"):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_group(
        name="balance",
        description="Get the balance of a user.",
    )
    @checks.not_blacklisted()
    async def balance(self, context: Context) -> None:
        """
        Lets you add or remove a user from not being able to use the bot.

        :param context: The hybrid command context.
        """
        if context.invoked_subcommand is None:
            embed = discord.Embed(
                title="Balance",
                description="You need to specify a subcommand.\n\n**Subcommands:**\n`add` - Add a user to the blacklist.\n`remove` - Remove a user from the blacklist.",
                color=0xE02B2B
            )
            await context.send(embed=embed)

    @balance.command(
        base="balance",
        name="show",
        description="Show the balance of a user.",
    )
    @checks.not_blacklisted()
    async def balance_show(self, context: Context):
        """
        This is a command to check your balance.

        :param context: The application command context.
        """
        async with aiosqlite.connect("database/database.db"):
            balance = await db_manager.get_balance(context.author.id, context.guild.id)
            if balance is None:
                embed = discord.Embed(
                    title="Balance",
                    description="You don't have any Tokens yet.",
                    color=0xe08621
                )
                await context.send(embed=embed)
            else:
                embed = discord.Embed(
                    title="Balance",
                    description=f"You have **{balance}** Tokens.",
                    color=0x6930C3
                )
                await context.send(embed=embed)

    @balance.command(
        base="balance",
        name="add",
        description="Add Tokens to a user."
    )
    @checks.is_owner()
    @checks.not_blacklisted()
    async def balance_add(self, context: Context, user: discord.Member, amount: int):
        """
        This is a command to add tokens to a user.

        :param context: The application command context.
        :param user: The user to add tokens to.
        :param amount: The amount of tokens to add.
        """
        async with aiosqlite.connect("database/database.db"):
            member = context.guild.get_member(user.id) or await context.guild.fetch_member(user.id)
            total = await db_manager.add_balance(
                user.id, context.guild.id, amount)
            embed = discord.Embed(
                title="Balance",
                description=f"You have added **{amount}** coins to {member.mention}.\n\n{member.mention} now has **{total}** coins.",
                color=0x6930C3
            )
            await context.send(embed=embed)
            try:
                await member.send(f"You got **{amount}** Tokens!\nYou now have **{total}** Tokens.")
            except:
                # Couldn't send a message in the private messages of the user
                await context.send(f"{member.mention}, you got **{amount}** Tokens!\nYou now have **{total}** Tokens.")

    @balance.command(
        base="balance",
        name="remove",
        description="Remove Tokens from a user."
    )
    @checks.is_owner()
    @checks.not_blacklisted()
    async def balance_remove(self, context: Context, user: discord.Member, amount: int):
        """
        This is a command to remove tokens from a user.

        :param context: The application command context.
        :param user: The user to remove tokens from.
        :param amount: The amount of tokens to remove.
        """
        async with aiosqlite.connect("database/database.db"):
            member = context.guild.get_member(user.id) or await context.guild.fetch_member(user.id)
            total = await db_manager.remove_balance(
                user.id, context.guild.id, amount)
            embed = discord.Embed(
                title="Balance",
                description=f"You have removed **{amount}** coins to {member.mention}.\n\n{member.mention} now has **{total}** coins.",
                color=0x6930C3
            )
            await context.send(embed=embed)
            try:
                await member.send(f"You got **{amount}** Tokens!\nYou now have **{total}** Tokens.")
            except:
                # Couldn't send a message in the private messages of the user
                await context.send(f"{member.mention}, you got **{amount}** Tokens!\nYou now have **{total}** Tokens.")

    @balance.command(
        base="balance",
        name="get",
        description="Get the balance of a specific user."
    )
    @commands.has_permissions(manage_channels=True)
    @checks.not_blacklisted()
    async def balance_get(self, context: Context, user: discord.Member):
        """
        This is a command to get the balance of a specific user.

        :param context: The application command context.
        :param user: The user to get the balance from.
        """
        async with aiosqlite.connect("database/database.db"):
            member = context.guild.get_member(user.id) or await context.guild.fetch_member(user.id)
            balance = await db_manager.get_balance(user.id, context.guild.id)
            embed = discord.Embed(
                title="Balance",
                description=f"{member.mention} has **{balance}** Tokens.",
                color=0x6930C3
            )
            await context.send(embed=embed)

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

    @commands.hybrid_command(
        name="xprequired",
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
            level = await db_manager.get_level(context.author.id, context.guild.id)
            if level is None:
                embed = discord.Embed(
                    title="XP Required",
                    description="You need **100** XP to level up.",
                    color=0x6930C3
                )
                await context.send(embed=embed)
            else:
                current_level = await get_level(author.id, guild.id)
                current_xp = await get_xp(author.id, guild.id)
                xp_req = round(((current_level / 0.07) ** 2) - current_xp)
                embed = discord.Embed(
                    title="XP Required",
                    description=f"You need {xp_req} XP to level up.",
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
            leaderboard = await db_manager.get_leaderboard(context.guild.id)
            embed = discord.Embed(
                title="**Leaderboard**",
                description="Here is top 10 users of the server.",
                color=0x6930C3
            )
            for i in range(10):
                try:
                    member = context.guild.get_member(leaderboard[i][0]) or await context.guild.fetch_member(
                        leaderboard[i][0])
                    embed.add_field(
                        name=f"{i + 1}. {member}",
                        value=f"Level: {leaderboard[i][1]}",
                        inline=False
                    )
                except IndexError:
                    break
            await context.send(embed=embed)


async def setup(bot):
    await bot.add_cog(Interaction(bot))
