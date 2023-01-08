""""
Copyright © Krypton 2019-2022 - https://github.com/kkrypt0nn (https://krypton.ninja)
Description:
🐍 A simple template to start to code your own and personalized discord bot in Python programming language.

Version: 5.4.1
"""

import platform

import discord
from discord.ext import commands
from discord.ext.commands import Context

from helpers import checks


class General(commands.Cog, name="general"):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(
        name="help",
        description="List all commands the bot has loaded."
    )
    @checks.not_blacklisted()
    async def help(self, context: Context) -> None:
        prefix = self.bot.config["prefix"]
        if context.author.id in self.bot.config["owners"]:
            embed = discord.Embed(
                title="Help", description="List of available commands:", color=0x6930C3)
            for i in self.bot.cogs:
                cog = self.bot.get_cog(i.lower())
                commands = cog.get_commands()
                data = []
                for command in commands:
                    description = command.description.partition('\n')[0]
                    data.append(f"{prefix}{command.name} - {description}")
                help_text = "\n".join(data)
                embed.add_field(name=i.capitalize(),
                                value=f'```{help_text}```', inline=False)
            await context.send(embed=embed)
        # check if user has permission to manage channels
        elif context.author.guild_permissions.manage_channels:
            embed = discord.Embed(
                title="Help", description="List of available commands:", color=0x6930C3)
            for i in self.bot.cogs:
                if i.lower() == "owner":
                    continue
                cog = self.bot.get_cog(i.lower())
                commands = cog.get_commands()
                data = []
                for command in commands:
                    description = command.description.partition('\n')[0]
                    data.append(f"{prefix}{command.name} - {description}")
                help_text = "\n".join(data)
                embed.add_field(name=i.capitalize(),
                                value=f'```{help_text}```', inline=False)
            await context.send(embed=embed)
        else:
            embed = discord.Embed(
                title="Help", description="List of available commands:", color=0x6930C3)
            for i in self.bot.cogs:
                if i.lower() == "owner":
                    continue
                if i.lower() == "moderation":
                    continue
                if i.lower() == "giveaways":
                    continue
                cog = self.bot.get_cog(i.lower())
                commands = cog.get_commands()
                data = []
                for command in commands:
                    description = command.description.partition('\n')[0]
                    data.append(f"{prefix}{command.name} - {description}")
                help_text = "\n".join(data)
                embed.add_field(name=i.capitalize(),
                                value=f'```{help_text}```', inline=False)
            await context.send(embed=embed)

    @commands.hybrid_command(
        name="botinfo",
        description="Get some useful (or not) information about the bot."
    )
    @checks.not_blacklisted()
    async def botinfo(self, context: Context) -> None:
        """
        Get some useful (or not) information about the bot.

        :param context: The hybrid command context.
        """
        guild = self.bot.get_guild(1057268363929333800)
        embed = discord.Embed(
            title=f"Developed for {guild} server",
            description="Used [Krypton's](https://krypton.ninja) template",
            color=0x6930C3
        )
        embed.set_author(
            name="Bot Information"
        )
        embed.add_field(
            name="Owner:",
            value="Edgers#2088",
            inline=True
        )
        embed.add_field(
            name="Python Version:",
            value=f"{platform.python_version()}",
            inline=True
        )
        embed.add_field(
            name="Prefix:",
            value=f"/ (Slash Commands) or {self.bot.config['prefix']} for normal commands",
            inline=False
        )
        embed.set_footer(

            text=f"Created: {self.bot.user.created_at.strftime('%d/%m/%Y %H:%M %p')}"
        )
        await context.send(embed=embed)

    @commands.hybrid_command(
        name="serverinfo",
        description="Get some useful (or not) information about the server.",
    )
    @checks.not_blacklisted()
    async def serverinfo(self, context: Context) -> None:
        """
        Get some useful (or not) information about the server.

        :param context: The hybrid command context.
        """

        embed = discord.Embed(
            title=f"**{context.guild}**",
            description="About:",
            color=0x6930C3
        )
        embed.set_author(
            name="Server Information"
        )
        if context.guild.icon is not None:
            embed.set_thumbnail(
                url=context.guild.icon.url
            )
        embed.add_field(
            name="Server ID",
            value=context.guild.id
        )
        embed.add_field(
            name="Server Owner",
            value=context.guild.owner
        )
        embed.add_field(
            name="Member Count",
            value=context.guild.member_count
        )
        embed.add_field(
            name="Text Channels",
            value=f"{len(context.guild.text_channels)}"
        )
        embed.add_field(
            name="Voice Channels",
            value=f"{len(context.guild.voice_channels)}"
        )
        embed.add_field(
            name=f"Roles",
            value=f"{len(context.guild.roles)}"
        )
        embed.set_footer(
            text=f"Created at: {context.guild.created_at.strftime('%d/%m/%Y %H:%M %p')}"
        )
        await context.send(embed=embed)

    @commands.hybrid_command(
        name="ping",
        description="Check if the bot is alive.",
    )
    @checks.not_blacklisted()
    async def ping(self, context: Context) -> None:
        """
        Check if the bot is alive.

        :param context: The hybrid command context.
        """
        embed = discord.Embed(
            title="🏓 Pong!",
            description=f"The bot latency is {round(self.bot.latency * 1000)}ms.",
            color=0x6930C3
        )
        await context.send(embed=embed)

    # @commands.hybrid_command(
    #    name="invite",
    #    description="Get the invite link of the bot to be able to invite it.",
    # )
    # @checks.not_blacklisted()
    # async def invite(self, context: Context) -> None:
    #    """
    #    Get the invite link of the bot to be able to invite it.
    #
    #    :param context: The hybrid command context.
    #    """
    #    embed = discord.Embed(
    #        description=f"Invite me by clicking [here](https://discordapp.com/oauth2/authorize?&client_id={self.bot.config['application_id']}&scope=bot+applications.commands&permissions={self.bot.config['permissions']}).",
    #        color=0xD75BF4
    #    )
    #    try:
    #        # To know what permissions to give to your bot, please see here: https://discordapi.com/permissions.html and remember to not give Administrator permissions.
    #        await context.author.send(embed=embed)
    #        await context.send("I sent you a private message!")
    #    except discord.Forbidden:
    #        await context.send(embed=embed)

    # @commands.hybrid_command(
    #    name="server",
    #    description="Get the invite link of the discord server of the bot for some support.",
    # )
    # @checks.not_blacklisted()
    # async def server(self, context: Context) -> None:
    #    """
    #    Get the invite link of the discord server of the bot for some support.
    #
    #    :param context: The hybrid command context.
    #    """
    #    embed = discord.Embed(
    #        description=f"Join the support server for the bot by clicking [here](https://discord.gg/mTBrXyWxAF).",
    #        color=0xD75BF4
    #    )
    #    try:
    #        await context.author.send(embed=embed)
    #        await context.send("I sent you a private message!")
    #    except discord.Forbidden:
    #        await context.send(embed=embed)

    # @commands.hybrid_command(
    #    name="bitcoin",
    #    description="Get the current price of bitcoin.",
    # )
    # @checks.not_blacklisted()
    # async def bitcoin(self, context: Context) -> None:
    #    """
    #    Get the current price of bitcoin.
    #
    #    :param context: The hybrid command context.
    #    """
    #    # This will prevent your bot from stopping everything when doing a web request - see: https://discordpy.readthedocs.io/en/stable/faq.html#how-do-i-make-a-web-request
    #    async with aiohttp.ClientSession() as session:
    #        async with session.get("https://api.coindesk.com/v1/bpi/currentprice/BTC.json") as request:
    #            if request.status == 200:
    #                data = await request.json(
    #                    content_type="application/javascript")  # For some reason the returned content is of type JavaScript
    #                embed = discord.Embed(
    #                    title="Bitcoin price",
    #                    description=f"The current price is {data['bpi']['USD']['rate']} :dollar:",
    #                    color=0x79b3b9
    #                )
    #            else:
    #                embed = discord.Embed(
    #                    title="Error!",
    #                    description="There is something wrong with the API, please try again later",
    #                    color=0xE02B2B
    #                )
    #            await context.send(embed=embed)


async def setup(bot):
    await bot.add_cog(General(bot))
