""""
Copyright © Krypton 2019-2022 - https://github.com/kkrypt0nn (https://krypton.ninja)
Description:
🐍 A simple template to start to code your own and personalized discord bot in Python programming language.

Version: 5.4.1
"""
import random
import time as pyTime
from math import floor

import aiosqlite
import discord
import humanfriendly
from discord import app_commands
from discord.ext import commands
from discord.ext.commands import Context

from helpers import db_manager


async def is_level_5(user, guild):
    if await db_manager.get_level(user, guild) < 5:
        return False
    return True


async def has_enough_tokens(user, guild, amount):
    if await db_manager.get_balance(user, guild) < amount:
        return False
    return True


async def is_participant(user, giveaway_id):
    if await db_manager.is_in_giveaway(user, giveaway_id):
        return True
    return False


async def get_winners(giveaway_id, winners):
    participants = await db_manager.get_participants(giveaway_id)
    winners_list = []
    if winners_list is None:
        return None
    else:
        for i in range(winners):
            if len(participants) == 0:
                break
            if len(participants) == 1:
                winners_list.append(participants[0])
                break
            else:
                winner = random.choice(participants)
                participants = [x for x in participants if x != winner]
                winners_list.append(winner)
    #for winner in winners_list:
    #    await db_manager.set_winner(giveaway_id, winner)

    provider = await db_manager.get_provider(giveaway_id)
    if provider == '1058058094439039127':
        return winners_list
    else:
        guild_id = await db_manager.get_guild_id(giveaway_id)
        participants = await db_manager.get_participants(giveaway_id)
        await db_manager.add_balance(await db_manager.get_provider(giveaway_id), guild_id, len(participants))
        return winners_list


class JoinGiveaway(discord.ui.View):
    def __init__(self, time, giveaway_id, guild, epochEnd, bot):
        super().__init__(timeout=time)
        self.giveaway_id = giveaway_id
        self.guild = guild
        self.time = epochEnd
        self.bot = bot

    async def on_timeout(self):
        for child in self.children:
            child.disabled = True
            giveaway = await db_manager.get_giveaway(self.giveaway_id)
            for i in giveaway:
                giveaway_id = i[0]
                prize = i[3]
                winners = i[5]
                provider = i[6]
                description = i[7]

            winners_list = await get_winners(giveaway_id, winners)
            if winners_list is None:
                return
            elif len(winners_list) == 1:
                winners_list = str(winners_list[0])
                winners_list = winners_list.replace("[", "").replace("(", "").replace(")", ">").replace("'",
                                                                                                        "").replace(",",
                                                                                                                    "").replace(
                    "]", "")
                winners_list = "<@" + winners_list
            else:
                winners_list = [str(t) for t in winners_list]
                winners_list = [t.replace("(", "").replace(")", ">").replace(",", "").replace("'", "") for t in
                                winners_list]
                winners_list = ", <@".join(winners_list)
                winners_list = "<@" + winners_list

            embed = discord.Embed(
                title=f"Giveaway has ended.\n**{prize}**",
                description=f"{description}\n**Winner(s):** {winners_list}\n**Provided by:** <@{provider}>",
                color=0x2f3136
            )

            embed.set_footer(text=f"Giveaway ID: {giveaway_id}")
            await db_manager.finish_giveaway(giveaway_id)
            await self.message.edit(embed=embed, view=self)

    @discord.ui.button(label="🎉", style=discord.ButtonStyle.blurple, custom_id="join_1")
    async def join_1(self, interaction: discord.Interaction, button: discord.ui.Button):
        if await db_manager.get_giveaway(self.giveaway_id):
            if not await db_manager.is_finished(self.giveaway_id):
                await interaction.response.send_message("This giveaway has ended.", ephemeral=True)
                return
            if not await db_manager.is_in_giveaway(self.giveaway_id, interaction.user.id) is False:
                await interaction.response.send_message("You are already in this giveaway!",
                                                        ephemeral=True)
                return
            if not await is_level_5(interaction.user.id, self.guild):
                await interaction.response.send_message("You need to be at least level 5 to join giveaways.",
                                                        ephemeral=True)
                return
            if not await has_enough_tokens(interaction.user.id, self.guild, 1):
                await interaction.response.send_message("You don't have enough Tokens to join this giveaway.",
                                                        ephemeral=True)
                return
            if interaction.user.id == await db_manager.get_provider(self.giveaway_id):
                await interaction.response.send_message("You can't join your own giveaway.",
                                                        ephemeral=True)
                return
            await db_manager.remove_balance(interaction.user.id, interaction.guild.id, 1)
            await db_manager.add_participants(self.giveaway_id, interaction.user.id, 1)
            await interaction.response.send_message("You have joined the giveaway using **1** Token!", ephemeral=True)
        else:
            await interaction.response.send_message("This giveaway has ended.", ephemeral=True)
            return

    @discord.ui.button(label="🎉🎉", style=discord.ButtonStyle.blurple, custom_id="join_2")
    async def join_2(self, interaction: discord.Interaction, button: discord.ui.Button):
        if await db_manager.get_giveaway(self.giveaway_id):
            if not await db_manager.is_finished(self.giveaway_id):
                await interaction.response.send_message("This giveaway has ended.", ephemeral=True)
                return
            if not await db_manager.is_in_giveaway(self.giveaway_id, interaction.user.id) is False:
                await interaction.response.send_message("You are already in this giveaway!",
                                                        ephemeral=True)
                return
            if not await is_level_5(interaction.user.id, self.guild):
                await interaction.response.send_message("You need to be at least level 5 to join giveaways.",
                                                        ephemeral=True)
                return
            if not await has_enough_tokens(interaction.user.id, self.guild, 2):
                await interaction.response.send_message("You don't have enough Tokens to join this giveaway.",
                                                        ephemeral=True)
                return
            if interaction.user.id == await db_manager.get_provider(self.giveaway_id):
                await interaction.response.send_message("You can't join your own giveaway.",
                                                        ephemeral=True)
                return
            await db_manager.remove_balance(interaction.user.id, interaction.guild.id, 2)
            await db_manager.add_participants(self.giveaway_id, interaction.user.id, 1)
            await db_manager.add_participants(self.giveaway_id, interaction.user.id, 2)
            await interaction.response.send_message("You have joined the giveaway using **2** Tokens!", ephemeral=True)
        else:
            await interaction.response.send_message("This giveaway has ended.", ephemeral=True)
            return

    @discord.ui.button(label="🎉🎉🎉", style=discord.ButtonStyle.blurple, custom_id="join_3")
    async def join_3(self, interaction: discord.Interaction, button: discord.ui.Button):
        if await db_manager.get_giveaway(self.giveaway_id):
            if not await db_manager.is_finished(self.giveaway_id):
                await interaction.response.send_message("This giveaway has ended.", ephemeral=True)
                return
            if not await db_manager.is_in_giveaway(self.giveaway_id, interaction.user.id) is False:
                await interaction.response.send_message("You are already in this giveaway!",
                                                        ephemeral=True)
                return
            if not await is_level_5(interaction.user.id, self.guild):
                await interaction.response.send_message("You need to be at least level 5 to join giveaways.",
                                                        ephemeral=True)
                return
            if not await has_enough_tokens(interaction.user.id, self.guild, 3):
                await interaction.response.send_message("You don't have enough Tokens to join this giveaway.",
                                                        ephemeral=True)
                return
            if interaction.user.id == await db_manager.get_provider(self.giveaway_id):
                await interaction.response.send_message("You can't join your own giveaway.",
                                                        ephemeral=True)
                return
            await db_manager.remove_balance(interaction.user.id, interaction.guild.id, 3)
            await db_manager.add_participants(self.giveaway_id, interaction.user.id, 1)
            await db_manager.add_participants(self.giveaway_id, interaction.user.id, 2)
            await db_manager.add_participants(self.giveaway_id, interaction.user.id, 3)
            await interaction.response.send_message("You have joined the giveaway using **3** Tokens!", ephemeral=True)
        else:
            await interaction.response.send_message("This giveaway has ended.", ephemeral=True)
            return


class Giveaways(commands.Cog, name="giveaways"):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_group(
        name="giveaway",
        description="Manage giveaways.",
    )
    @commands.has_permissions(manage_channels=True)
    async def giveaway(self, context: Context) -> None:
        """
        This is the main command for the giveaway group.

        :param context: The hybrid command context.
        """
        if context.invoked_subcommand is None:
            embed = discord.Embed(
                title="Balance",
                description="You need to specify a subcommand.\n\n**Subcommands:**\n`start` - .\n`finish` - .\n`reroll` - .\n`delete` - .",
                color=0xE02B2B
            )
            await context.send(embed=embed)

    @giveaway.command(
        base="giveaway",
        name="start",
        description="Start a giveaway.",
    )
    @commands.has_permissions(manage_channels=True)
    @app_commands.describe(prize="The prize of the giveaway.", duration="The duration of the giveaway.",
                           winners="The number of winners of the giveaway.", provider="The provider of the giveaway.",
                           description="The description of the giveaway.")
    async def start(self, context: Context, prize: str, duration: str, winners: str, provider: discord.Member,
                    description: str):
        """
        This command starts a giveaway.

        :param context: The hybrid command context.
        :param prize: The prize of the giveaway.
        :param duration: The duration of the giveaway.
        :param winners: The number of winners of the giveaway.
        :param provider: The provider of the giveaway.
        :param description: The description of the giveaway.
        """
        if not context.author.guild_permissions.manage_channels:
            embed = discord.Embed(
                title="Giveaway",
                description="You don't have the permission to create giveaway.",
                color=0xE02B2B
            )
            await context.send(embed=embed)
            return
        if winners == 0:
            winners = 1
        time = humanfriendly.parse_timespan(duration)
        epochEnd = floor(pyTime.time() + time)
        giveaway_id = floor(pyTime.time() * 2)
        async with aiosqlite.connect("database/database.db"):
            await db_manager.add_giveaway(giveaway_id, context.channel.id, context.guild.id, prize, epochEnd, winners,
                                          provider.id, description, finished=False)
        embed = discord.Embed(
            title=f"Giveaway! 🎉\n**{prize}**",
            description=f"{description}\n**Ends **<t:{int(epochEnd)}:R>\n**Total number of winners:** {winners}\n**Provided by:** {provider.mention}",
            color=0x2BE0E0
        )
        embed.add_field(
            name="How to participate?",
            value="Enter giveaway using your Tokens.\nYou need to be at least level 5.",
            inline=False
        )
        embed.add_field(
            name="To enter with 1 Token",
            value="Press 🎉",
            inline=False
        )
        embed.add_field(
            name="To enter with 2 Tokens",
            value="Press 🎉🎉",
            inline=False
        )
        embed.add_field(
            name="To enter with 3 Tokens",
            value="Press 🎉🎉🎉",
            inline=False
        )
        embed.set_footer(text=f"Giveaway ID: {giveaway_id}")
        message = f"Giveaway started!\nGiveaway ID: {giveaway_id}"
        channel = self.bot.get_channel(context.channel.id)

        view = JoinGiveaway(time, giveaway_id, context.guild.id, epochEnd, self.bot)
        msg = await channel.send(embed=embed, view=view)
        view.message = msg

        # await channel.send(embed=embed)
        await context.send(message, ephemeral=True)

    @giveaway.command(
        base="giveaway",
        name="finish",
        description="Finish a giveaway."
    )
    @commands.has_permissions(manage_channels=True)
    @app_commands.describe(giveaway_id="The ID of the giveaway.")
    async def finish(self, context: Context, giveaway_id: int):
        """
        This command finishes a giveaway.

        :param context: The hybrid command context.
        :param giveaway_id: The ID of the giveaway.
        """
        if not await db_manager.get_giveaway(giveaway_id):
            embed = discord.Embed(
                title="Giveaway",
                description="This giveaway doesn't exist.",
                color=0xE02B2B
            )
            await context.send(embed=embed)
            return
        if not await db_manager.is_finished(giveaway_id):
            embed = discord.Embed(
                title="Giveaway",
                description="This giveaway has already been finished.",
                color=0xE02B2B
            )
            await context.send(embed=embed)
            return

        view = JoinGiveaway(0, giveaway_id, context.guild.id, 0, self.bot)
        await view.on_timeout()

        await context.send("Giveaway finished", ephemeral=True)

    @giveaway.command(
        base="giveaway",
        name="reroll",
        description="Reroll a giveaway."
    )
    @commands.has_permissions(manage_channels=True)
    @app_commands.describe(giveaway_id="The ID of the giveaway.")
    async def reroll(self, context: Context, giveaway_id: int):
        """
        This command rerolls a giveaway.

        :param context: The hybrid command context.
        :param giveaway_id: The ID of the giveaway.
        """
        if not await db_manager.get_giveaway(giveaway_id):
            embed = discord.Embed(
                title="Giveaway",
                description="This giveaway doesn't exist.",
                color=0xE02B2B
            )
            await context.send(embed=embed)
            return
        if not await db_manager.is_finished(giveaway_id):
            embed = discord.Embed(
                title="Giveaway",
                description="This giveaway hasn't been finished yet.",
                color=0xE02B2B
            )
            await context.send(embed=embed)
            return
        winners = await db_manager.get_winners(giveaway_id)

        if not winners:
            embed = discord.Embed(
                title="Giveaway",
                description="There are no winners in this giveaway.",
                color=0xE02B2B
            )
            await context.send(embed=embed)
            return
        await db_manager.reroll(giveaway_id)
        winners = [str(t) for t in winners]
        winners = [t.replace("(", "").replace(")", ">").replace(",", "").replace("'", "") for t in
                   winners]
        winners = ", <@".join(winners)
        winners = "<@" + winners
        embed = discord.Embed(
            title="Giveaway",
            description="Giveaway has been rerolled.\nNew winners:\n" + "\n".join(winners),
            color=0x2BE0E0
        )
        await context.send(embed=embed, ephemeral=True)


async def setup(bot):
    await bot.add_cog(Giveaways(bot))
