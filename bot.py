"""
Copyright © Krypton 2019-2022 - https://github.com/kkrypt0nn (https://krypton.ninja)
Description:
🐍 A simple template to start to code your own and personalized discord bot in Python programming language.

Version: 5.4.1
"""

import asyncio
import json
import os
import platform
import random
import sys

import aiosqlite
import discord
from discord.ext import commands, tasks
from discord.ext.commands import Bot, Context, HelpCommand
from datetime import datetime

import exceptions

from helpers.db_manager import get_level, add_level, add_balance, get_xp, add_xp, invite_setup, invite_create, \
    invite_delete, get_balance

if not os.path.isfile(f"{os.path.realpath(os.path.dirname(__file__))}/config.json"):
    sys.exit("'config.json' not found! Please add it and try again.")
else:
    with open(f"{os.path.realpath(os.path.dirname(__file__))}/config.json") as file:
        config = json.load(file)

DATABASE_PATH = f"{os.path.realpath(os.path.dirname(__file__))}/../database/database.db"

intents = discord.Intents.all()

bot = Bot(command_prefix=commands.when_mentioned_or(
    config["prefix"]), intents=intents, help_command=None)


async def init_db():
    async with aiosqlite.connect(f"{os.path.realpath(os.path.dirname(__file__))}/database/database.db") as db:
        with open(f"{os.path.realpath(os.path.dirname(__file__))}/database/schema.sql") as file:
            await db.executescript(file.read())
        await db.commit()


"""
Create a bot variable to access the config file in cogs so that you don't need to import it every time.

The config is available using the following code:
- bot.config # In this file
- self.bot.config # In cogs
"""
bot.config = config


@bot.event
async def on_ready() -> None:
    """
    The code in this even is executed when the bot is ready
    """
    print(f"Logged in as {bot.user.name}")
    print(f"discord.py API version: {discord.__version__}")
    print(f"Python version: {platform.python_version()}")
    print(f"Running on: {platform.system()} {platform.release()} ({os.name})")
    print("-------------------")
    status_task.start()
    if config["sync_commands_globally"]:
        print("Syncing commands globally...")
        await bot.tree.sync()


@tasks.loop(minutes=1.0)
async def status_task() -> None:
    """
    Set up the game status task of the bot
    """
    statuses = ["Making developer", "Raising error", "Deleting user database...", "Refusing to execute commands"]
    await bot.change_presence(activity=discord.Game(random.choice(statuses)))


@bot.event
async def on_message(message: discord.Message) -> None:
    """
    The code in this event is executed every time someone sends a message, with or without the prefix

    :param message: The message that was sent.
    """
    if message.author == bot.user or message.author.bot:
        return
    await bot.process_commands(message)
    author = message.author
    guild = message.guild
    context = await bot.get_context(message)
    async with aiosqlite.connect("database/database.db"):
        if any(role.id == 1057365599522652221 for role in author.roles):  # Gold
            xp = random.randint(1, 25) * 1.75
        elif any(role.id == 1057365535748272248 or 1057346657315991592 for role in author.roles):  # Silver and Booster
            xp = random.randint(1, 25) * 1.5
        elif any(role.id == 1057365194315137057 for role in author.roles):  # Bronze
            xp = random.randint(1, 25) * 1.25
        elif any(role.id == 1057346908286373938  # Donor
                 or 1057346904821866666
                 or 1057346901348982914
                 or 1057346896080937020
                 or 1057346882860498974
                 or 1057346875293958196
                 or 1057346686005031073
                 or 1057346862870429726
                 for role in author.roles):
            xp = random.randint(1, 25) * 1.1
        else:
            xp = random.randint(1, 25)

        current_xp = await get_xp(author.id, guild.id)
        current_level = await get_level(author.id, guild.id)
        if current_level == 0:
            xp_req = 100
        else:
            xp_req = (current_level / 0.07) ** 2
        if current_xp + xp >= xp_req:
            embed = discord.Embed(
                title="Level up!",
                description=f"{author.mention} has leveled up to level {current_level + 1}!\nHere's a **1** Token!",
                color=0x6930C3
            )
            await add_level(author.id, guild.id, 1)
            current_level += 1
            if current_level == 1:
                new_role = discord.utils.get(context.guild.roles, name="Lv 1+")
                await context.author.add_roles(new_role)
            elif current_level == 5:
                old_role = discord.utils.get(context.guild.roles, name="Lv 1+")
                new_role = discord.utils.get(context.guild.roles, name="Lv 5+")
                await context.author.remove_roles(old_role)
                await context.author.add_roles(new_role)
            elif current_level == 10:
                old_role = discord.utils.get(context.guild.roles, name="Lv 5+")
                new_role = discord.utils.get(context.guild.roles, name="Lv 10+")
                await context.author.remove_roles(old_role)
                await context.author.add_roles(new_role)
            elif current_level == 15:
                old_role = discord.utils.get(context.guild.roles, name="Lv 10+")
                new_role = discord.utils.get(context.guild.roles, name="Lv 15+")
                await context.author.remove_roles(old_role)
                await context.author.add_roles(new_role)
            elif current_level == 25:
                old_role = discord.utils.get(context.guild.roles, name="Lv 15+")
                new_role = discord.utils.get(context.guild.roles, name="Lv 25+")
                await context.author.remove_roles(old_role)
                await context.author.add_roles(new_role)
            elif current_level == 50:
                old_role = discord.utils.get(context.guild.roles, name="Lv 25+")
                new_role = discord.utils.get(context.guild.roles, name="Lv 50+")
                await context.author.remove_roles(old_role)
                await context.author.add_roles(new_role)
            elif current_level == 100:
                old_role = discord.utils.get(context.guild.roles, name="Lv 50+")
                new_role = discord.utils.get(context.guild.roles, name="Lv 100+")
                await context.author.remove_roles(old_role)
                await context.author.add_roles(new_role)
            await add_xp(author.id, guild.id, xp)
            await add_balance(author.id, guild.id, 1)
            await message.channel.send(embed=embed)
        else:
            await add_xp(author.id, guild.id, xp)


async def setup():
    async with aiosqlite.connect("database/database.db"):
        for guild in bot.guilds:
            invites = await guild.invites()
            for invite in invites:
                await invite_create(guild.id, invite.inviter.id, invite.id, invite.uses)


async def update_totals(member: discord.Member) -> None:
    """
    Update the total users and total bots in the database
    """
    invites = await member.guild.invites()

    c = datetime.today().strftime('%Y-%m-%d').split('-')
    c_y = int(c[0])
    c_m = int(c[1])
    c_d = int(c[2])

    async with aiosqlite.connect(DATABASE_PATH) as db:
        async with db.execute("SELECT code, uses FROM invites WHERE guild_id = ?", member.guild.id) as cursor:
            async for invite_id, old_uses in cursor:
                for invite in invites:
                    if invite.id == invite_id and invite.uses - old_uses > 0:
                        if not (
                                c_y == member.created_at.year and c_m == member.created_at.month and c_d - member.created_at.day < 7):
                            await db.execute("UPDATE invites SET uses = uses + 1 WHERE guild_id = ? AND code = ?",
                                             (invite.guild.id, invite.id))
                            await db.execute(
                                "INSERT OR IGNORE INTO joined (guild_id, inviter_id, joined_id) VALUES (?, ?, ?)",
                                (invite.guild.id, invite.inviter.id, member.id))
                            await db.execute(
                                "UPDATE totals SET normal = normal + 1 WHERE guild_id = ? AND inviter_id = ?",
                                (invite.guild.id, invite.inviter.id))
                            # add 1 Token per 10 normal - (fake + left)
                            cur = await db.execute(
                                "SELECT normal, left, fake FROM totals WHERE guild_id = ? AND inviter_id = ?",
                                (member.guild.id, member.id))
                            res = await cur.fetchone()
                            normal, left, fake = res
                            total = normal - (left + fake)
                            if total % 10 == 0:
                                await add_balance(member.id, member.guild.id, 1)
                                balance = await get_balance(member.id, member.guild.id)
                                try:
                                    await member.send(f"You got **1** Token for 10 users invited!\nYou now have **{balance}** Tokens.")
                                except:
                                    pass
                        else:
                            await db.execute(
                                "UPDATE totals SET normal = normal + 1, fake = fake + 1 WHERE guild_id = ? AND inviter_id = ?",
                                (invite.guild.id, invite.inviter.id))

                        return


@bot.event
async def on_member_join(member: discord.Member) -> None:
    async with aiosqlite.connect(DATABASE_PATH) as db:
        await update_totals(member)
        await db.commit()


@bot.event
async def on_member_remove(member: discord.Member) -> None:
    async with aiosqlite.connect(DATABASE_PATH) as db:
        cur = await db.execute("SELECT inviter_id FROM joined WHERE guild_id = ? AND joined_id = ?",
                               (member.guild.id, member.id))
        result = await cur.fetchone()
        if result is None:
            return

        inviter_id = result[0]

        await db.execute("DELETE FROM joined WHERE guild_id = ? AND joined_id = ?", (member.guild.id, member.id))
        await db.execute("DELETE FROM totals WHERE guild_id = ? AND inviter_id = ?", (member.guild.id, member.id))
        await db.execute("UPDATE totals SET left = left + 1 WHERE guild_id = ? AND inviter_id = ?",
                         (member.guild.id, inviter_id))
        await db.commit()


@bot.event
async def on_invite_create(invite: discord.Invite) -> None:
    async with aiosqlite.connect("database/database.db"):
        await invite_create(invite.guild.id, invite.inviter.id, invite.id, invite.uses)


@bot.event
async def on_invite_delete(invite: discord.Invite) -> None:
    async with aiosqlite.connect("database/database.db"):
        await invite_delete(invite.guild.id, invite.id)


@bot.event
async def on_command_completion(context: Context) -> None:
    """
    The code in this event is executed every time a normal command has been *successfully* executed
    :param context: The context of the command that has been executed.
    """
    full_command_name = context.command.qualified_name
    split = full_command_name.split(" ")
    executed_command = str(split[0])
    if context.guild is not None:
        print(
            f"Executed {executed_command} command in {context.guild.name} (ID: {context.guild.id}) by {context.author} (ID: {context.author.id})")
    else:
        print(
            f"Executed {executed_command} command by {context.author} (ID: {context.author.id}) in DMs")


@bot.event
async def on_command_error(context: Context, error) -> None:
    """
    The code in this event is executed every time a normal valid command catches an error
    :param context: The context of the normal command that failed executing.
    :param error: The error that has been faced.
    """
    if isinstance(error, commands.CommandOnCooldown):
        minutes, seconds = divmod(error.retry_after, 60)
        hours, minutes = divmod(minutes, 60)
        hours = hours % 24
        embed = discord.Embed(
            title="Hey, please slow down!",
            description=f"You can use this command again in {f'{round(hours)} hours' if round(hours) > 0 else ''} {f'{round(minutes)} minutes' if round(minutes) > 0 else ''} {f'{round(seconds)} seconds' if round(seconds) > 0 else ''}.",
            color=0xE02B2B
        )
        await context.send(embed=embed)
    elif isinstance(error, exceptions.UserBlacklisted):
        """
        The code here will only execute if the error is an instance of 'UserBlacklisted', which can occur when using
        the @checks.not_blacklisted() check in your command, or you can raise the error by yourself.
        """
        embed = discord.Embed(
            title="Error!",
            description="You are blacklisted from using the bot.",
            color=0xE02B2B
        )
        await context.send(embed=embed)
    elif isinstance(error, exceptions.UserNotOwner):
        """
        Same as above, just for the @checks.is_owner() check.
        """
        embed = discord.Embed(
            title="Error!",
            description="You are not the owner of the bot!",
            color=0xE02B2B
        )
        await context.send(embed=embed)
    elif isinstance(error, commands.MissingPermissions):
        embed = discord.Embed(
            title="Error!",
            description="You are missing the permission(s) `" + ", ".join(
                error.missing_permissions) + "` to execute this command!",
            color=0xE02B2B
        )
        await context.send(embed=embed)
    elif isinstance(error, commands.BotMissingPermissions):
        embed = discord.Embed(
            title="Error!",
            description="I am missing the permission(s) `" + ", ".join(
                error.missing_permissions) + "` to fully perform this command!",
            color=0xE02B2B
        )
        await context.send(embed=embed)
    elif isinstance(error, commands.MissingRequiredArgument):
        embed = discord.Embed(
            title="Error!",
            # We need to capitalize because the command arguments have no capital letter in the code.
            description=str(error).capitalize(),
            color=0xE02B2B
        )
        await context.send(embed=embed)
    raise error


async def load_cogs() -> None:
    """
    The code in this function is executed whenever the bot will start.
    """
    for file in os.listdir(f"{os.path.realpath(os.path.dirname(__file__))}/cogs"):
        if file.endswith(".py"):
            extension = file[:-3]
            try:
                await bot.load_extension(f"cogs.{extension}")
                print(f"Loaded extension '{extension}'")
            except Exception as e:
                exception = f"{type(e).__name__}: {e}"
                print(f"Failed to load extension {extension}\n{exception}")


asyncio.run(init_db())
asyncio.run(load_cogs())
bot.run(config["token"])
