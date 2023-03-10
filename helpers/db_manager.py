""""
Copyright © Krypton 2019-2022 - https://github.com/kkrypt0nn (https://krypton.ninja)
Description:
🐍 A simple template to start to code your own and personalized discord bot in Python programming language.

Version: 5.4.1
"""

import os

import aiosqlite

DATABASE_PATH = f"{os.path.realpath(os.path.dirname(__file__))}/../database/database.db"


async def is_blacklisted(user_id: int) -> bool:
    """
    This function will check if a user is blacklisted.

    :param user_id: The ID of the user that should be checked.
    :return: True if the user is blacklisted, False if not.
    """
    async with aiosqlite.connect(DATABASE_PATH) as db:
        async with db.execute("SELECT * FROM blacklist WHERE user_id=?", (user_id,)) as cursor:
            result = await cursor.fetchone()
            return result is not None


async def add_user_to_blacklist(user_id: int) -> int:
    """
    This function will add a user based on its ID in the blacklist.

    :param user_id: The ID of the user that should be added into the blacklist.
    """
    async with aiosqlite.connect(DATABASE_PATH) as db:
        await db.execute("INSERT INTO blacklist(user_id) VALUES (?)", (user_id,))
        await db.commit()
        rows = await db.execute("SELECT COUNT(*) FROM blacklist")
        async with rows as cursor:
            result = await cursor.fetchone()
            return result[0] if result is not None else 0


async def remove_user_from_blacklist(user_id: int) -> int:
    """
    This function will remove a user based on its ID from the blacklist.

    :param user_id: The ID of the user that should be removed from the blacklist.
    """
    async with aiosqlite.connect(DATABASE_PATH) as db:
        await db.execute("DELETE FROM blacklist WHERE user_id=?", (user_id,))
        await db.commit()
        rows = await db.execute("SELECT COUNT(*) FROM blacklist")
        async with rows as cursor:
            result = await cursor.fetchone()
            return result[0] if result is not None else 0


async def add_warn(user_id: int, server_id: int, moderator_id: int, reason: str) -> int:
    """
    This function will add a warn to the database.

    :param user_id: The ID of the user that should be warned.
    :param reason: The reason why the user should be warned.
    """
    async with aiosqlite.connect(DATABASE_PATH) as db:
        rows = await db.execute("SELECT id FROM warns WHERE user_id=? AND server_id=? ORDER BY id DESC LIMIT 1",
                                (user_id, server_id,))
        async with rows as cursor:
            result = await cursor.fetchone()
            warn_id = result[0] + 1 if result is not None else 1
            await db.execute("INSERT INTO warns(id, user_id, server_id, moderator_id, reason) VALUES (?, ?, ?, ?, ?)",
                             (warn_id, user_id, server_id, moderator_id, reason,))
            await db.commit()
            return warn_id


async def remove_warn(warn_id: int, user_id: int, server_id: int) -> int:
    """
    This function will remove a warn from the database.

    :param warn_id: The ID of the warn.
    :param user_id: The ID of the user that was warned.
    :param server_id: The ID of the server where the user has been warned
    """
    async with aiosqlite.connect(DATABASE_PATH) as db:
        await db.execute("DELETE FROM warns WHERE id=? AND user_id=? AND server_id=?", (warn_id, user_id, server_id,))
        await db.commit()
        rows = await db.execute("SELECT COUNT(*) FROM warns WHERE user_id=? AND server_id=?", (user_id, server_id,))
        async with rows as cursor:
            result = await cursor.fetchone()
            return result[0] if result is not None else 0


async def get_warnings(user_id: int, server_id: int) -> list:
    """
    This function will get all the warnings of a user.

    :param user_id: The ID of the user that should be checked.
    :param server_id: The ID of the server that should be checked.
    :return: A list of all the warnings of the user.
    """
    async with aiosqlite.connect(DATABASE_PATH) as db:
        rows = await db.execute(
            "SELECT user_id, server_id, moderator_id, reason, strftime('%s', created_at), id FROM warns WHERE user_id=? AND server_id=?",
            (user_id, server_id,))
        async with rows as cursor:
            result = await cursor.fetchall()
            result_list = []
            for row in result:
                result_list.append(row)
            return result_list


async def get_balance(user_id: int, server_id: int) -> int:
    """
    This function will get the balance of a user.

    :param user_id: The ID of the user that should be checked.
    :param server_id: The ID of the server that should be checked.
    :return: The balance of the user.
    """
    async with aiosqlite.connect(DATABASE_PATH) as db:
        rows = await db.execute(
            "SELECT user_id, server_id, balance FROM economy WHERE user_id=? AND server_id=?",
            (user_id, server_id,))
        async with rows as cursor:
            result = await cursor.fetchone()
            return result[2] if result is not None else 0


async def add_balance(user_id: int, server_id: int, amount: int) -> int:
    """
    This function will add Tokens to the balance of a user.

    :param user_id: The ID of the user that should be checked.
    :param server_id: The ID of the server that should be checked.
    :param amount: The amount of Tokens that should be added to the balance.
    :return: The new balance of the user.
    """
    async with aiosqlite.connect(DATABASE_PATH) as db:
        rows = await db.execute("SELECT balance FROM economy WHERE user_id=? AND server_id=?", (user_id, server_id,))
        async with rows as cursor:
            result = await cursor.fetchone()
            if result is None:
                await db.execute("INSERT INTO economy(user_id, server_id, balance) VALUES (?, ?, ?)",
                                 (user_id, server_id, amount,))
            else:
                await db.execute("UPDATE economy SET balance=? WHERE user_id=? AND server_id=?",
                                 (result[0] + amount, user_id, server_id,))
            await db.commit()
            rows = await db.execute("SELECT balance FROM economy WHERE user_id=? AND server_id=?",
                                    (user_id, server_id,))
            async with rows as cursor:
                result = await cursor.fetchone()
                return result[0] if result is not None else 0


async def remove_balance(user_id: int, server_id: int, amount: int) -> int:
    """
    This function will remove Tokens from the balance of a user.

    :param user_id: The ID of the user that should be checked.
    :param server_id: The ID of the server that should be checked.
    :param amount: The amount of Tokens that should be removed from the balance.
    :return: The new balance of the user.
    """
    async with aiosqlite.connect(DATABASE_PATH) as db:
        rows = await db.execute("SELECT balance FROM economy WHERE user_id=? AND server_id=?", (user_id, server_id,))
        async with rows as cursor:
            result = await cursor.fetchone()
            if result is None:
                await db.execute("INSERT INTO economy(user_id, server_id, balance) VALUES (?, ?, ?)",
                                 (user_id, server_id, 0,))
            else:
                await db.execute("UPDATE economy SET balance=? WHERE user_id=? AND server_id=?",
                                 (result[0] - amount, user_id, server_id,))
            await db.commit()
            rows = await db.execute("SELECT balance FROM economy WHERE user_id=? AND server_id=?",
                                    (user_id, server_id,))
            async with rows as cursor:
                result = await cursor.fetchone()
                return result[0] if result is not None else 0


async def get_level(user_id: int, server_id: int) -> int:
    """
    This function will get the level of a user.

    :param user_id: The ID of the user that should be checked.
    :param server_id: The ID of the server that should be checked.
    :return: The level of the user.
    """
    async with aiosqlite.connect(DATABASE_PATH) as db:
        rows = await db.execute(
            "SELECT user_id, server_id, level FROM levels WHERE user_id=? AND server_id=?",
            (user_id, server_id,))
        async with rows as cursor:
            result = await cursor.fetchone()
            return result[2] if result is not None else 0


async def add_level(user_id: int, server_id: int, amount: int) -> int:
    """
    This function will add levels to the level of a user.

    :param user_id: The ID of the user that should be checked.
    :param server_id: The ID of the server that should be checked.
    :param amount: The amount of levels that should be added to the level.
    :return: The new level of the user.
    """
    async with aiosqlite.connect(DATABASE_PATH) as db:
        rows = await db.execute("SELECT level FROM levels WHERE user_id=? AND server_id=?", (user_id, server_id,))
        async with rows as cursor:
            result = await cursor.fetchone()
            if result is None:
                await db.execute("INSERT INTO levels(user_id, server_id, level) VALUES (?, ?, ?)",
                                 (user_id, server_id, amount,))
            else:
                await db.execute("UPDATE levels SET level=? WHERE user_id=? AND server_id=?",
                                 (result[0] + amount, user_id, server_id,))
            await db.commit()
            rows = await db.execute("SELECT level FROM levels WHERE user_id=? AND server_id=?",
                                    (user_id, server_id,))
            async with rows as cursor:
                result = await cursor.fetchone()
                return result[0] if result is not None else 0


async def remove_level(user_id: int, server_id: int, amount: int) -> int:
    """
    This function will remove levels from the level of a user.

    :param user_id: The ID of the user that should be checked.
    :param server_id: The ID of the server that should be checked.
    :param amount: The amount of levels that should be removed from the level.
    :return: The new level of the user.
    """
    async with aiosqlite.connect(DATABASE_PATH) as db:
        rows = await db.execute("SELECT level FROM levels WHERE user_id=? AND server_id=?", (user_id, server_id,))
        async with rows as cursor:
            result = await cursor.fetchone()
            if result is None:
                await db.execute("INSERT INTO levels(user_id, server_id, level) VALUES (?, ?, ?)",
                                 (user_id, server_id, 0,))
            else:
                await db.execute("UPDATE levels SET level=? WHERE user_id=? AND server_id=?",
                                 (result[0] - amount, user_id, server_id,))
            await db.commit()
            rows = await db.execute("SELECT level FROM levels WHERE user_id=? AND server_id=?",
                                    (user_id, server_id,))
            async with rows as cursor:
                result = await cursor.fetchone()
                return result[0] if result is not None else 0


async def get_xp(user_id: int, server_id: int) -> int:
    """
    This function will get the XP of a user.

    :param user_id: The ID of the user that should be checked.
    :param server_id: The ID of the server that should be checked.
    :return: The XP of the user.
    """
    async with aiosqlite.connect(DATABASE_PATH) as db:
        rows = await db.execute(
            "SELECT user_id, server_id, xp FROM levels WHERE user_id=? AND server_id=?",
            (user_id, server_id,))
        async with rows as cursor:
            result = await cursor.fetchone()
            return result[2] if result is not None else 0


async def add_xp(user_id: int, server_id: int, amount: int) -> int:
    """
    This function will add XP to the XP of a user.

    :param user_id: The ID of the user that should be checked.
    :param server_id: The ID of the server that should be checked.
    :param amount: The amount of XP that should be added to the XP.
    :return: The new XP of the user.
    """
    async with aiosqlite.connect(DATABASE_PATH) as db:
        rows = await db.execute("SELECT xp FROM levels WHERE user_id=? AND server_id=?", (user_id, server_id,))
        async with rows as cursor:
            result = await cursor.fetchone()
            if result is None:
                await db.execute("INSERT INTO levels(user_id, server_id, xp) VALUES (?, ?, ?)",
                                 (user_id, server_id, amount,))
            else:
                await db.execute("UPDATE levels SET xp=? WHERE user_id=? AND server_id=?",
                                 (result[0] + amount, user_id, server_id,))
            await db.commit()
            rows = await db.execute("SELECT xp FROM levels WHERE user_id=? AND server_id=?",
                                    (user_id, server_id,))
            async with rows as cursor:
                result = await cursor.fetchone()
                return result[0] if result is not None else 0


async def remove_xp(user_id: int, server_id: int, amount: int) -> int:
    """
    This function will set XP of a user to 0.

    :param user_id: The ID of the user that should be checked.
    :param server_id: The ID of the server that should be checked.
    :param amount: The amount of XP that should be removed from the XP.
    :return: The new XP of the user.
    """
    async with aiosqlite.connect(DATABASE_PATH) as db:
        rows = await db.execute("SELECT xp FROM levels WHERE user_id=? AND server_id=?", (user_id, server_id,))
        async with rows as cursor:
            result = await cursor.fetchone()
            if result is None:
                await db.execute("INSERT INTO levels(user_id, server_id, xp) VALUES (?, ?, ?)",
                                 (user_id, server_id, 0,))
            else:
                await db.execute("UPDATE levels SET xp=? WHERE user_id=? AND server_id=?",
                                 (result[0] - amount, user_id, server_id,))
            await db.commit()
            rows = await db.execute("SELECT xp FROM levels WHERE user_id=? AND server_id=?",
                                    (user_id, server_id,))
            async with rows as cursor:
                result = await cursor.fetchone()
                return result[0] if result is not None else 0


async def get_level_leaderboard(server_id: int, limit: int = 10) -> list:
    """
    This function will get the leaderboard of a server.

    :param server_id: The ID of the server that should be checked.
    :param limit: The amount of users that should be returned.
    :return: A list of users.
    """
    async with aiosqlite.connect(DATABASE_PATH) as db:
        rows = await db.execute("SELECT user_id, level FROM levels WHERE server_id=? ORDER BY level DESC LIMIT ?",
                                (server_id, limit,))
        async with rows as cursor:
            result = await cursor.fetchall()
            return result if result is not None else []


async def get_invite_leaderboard(server_id: int, limit: int = 10) -> list:
    """
    This function will get the leaderboard of a server.

    :param server_id: The ID of the server that should be checked.
    :param limit: The amount of users that should be returned.
    :return: A list of users.
    """
    async with aiosqlite.connect(DATABASE_PATH) as db:
        rows = await db.execute(
            "SELECT inviter_id, normal, leave, fake FROM totals WHERE guild_id=? ORDER BY (normal - (leave + fake)) DESC LIMIT ?",
            (server_id, limit,))
        async with rows as cursor:
            result = await cursor.fetchall()
            return result if result is not None else []


async def add_giveaway(giveaway_id: int, message_id: int, channel_id: int, guild_id: int, prize: str, time: int,
                       winners: int,
                       provider: str, message: str, finished: bool) -> None:
    """
    This function will add a giveaway to the database.

    :param giveaway_id: The ID of the giveaway.
    :param message_id: The ID of the message.
    :param channel_id: The ID of the channel that the giveaway is in.
    :param guild_id: The ID of the guild that the giveaway is in.
    :param prize: The prize of the giveaway.
    :param time: The duration of the giveaway.
    :param winners: The amount of winners of the giveaway.
    :param provider: The provider the giveaway.
    :param message: The description of the giveaway.
    :param finished: If the giveaway is finished.
    """
    async with aiosqlite.connect(DATABASE_PATH) as db:
        await db.execute(
            "INSERT INTO giveaways(giveaway_id, message_id, channel_id, guild_id, prize, time, winners, provider, message, finished) "
            "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (giveaway_id, message_id, channel_id, guild_id, prize, time, winners, provider, message, finished,))
        await db.commit()


async def add_participants(giveaway_id: int, user_id: int, entry: int) -> None:
    """
    This function will add a participant to a giveaway.

    :param giveaway_id: The ID of the giveaway.
    :param user_id: The ID of the user that should be added.
    :param entry: The amount of entries the user has.
    """
    async with aiosqlite.connect(DATABASE_PATH) as db:
        await db.execute("INSERT INTO participants(giveaway_id, user_id, entry) VALUES (?, ?, ?)",
                         (giveaway_id, user_id, entry))
        await db.commit()


async def get_participants(giveaway_id: int) -> list:
    """
    This function will get the participants of a giveaway.

    :param giveaway_id: The ID of the giveaway.
    :return: A list of participants.
    """
    async with aiosqlite.connect(DATABASE_PATH) as db:
        rows = await db.execute("SELECT user_id FROM participants WHERE giveaway_id=?", (giveaway_id,))
        async with rows as cursor:
            result = await cursor.fetchall()
            return result if result is not None else []


async def get_giveaways() -> list:
    """
    This function will get all giveaways from the database.

    :return: A list of giveaways.
    """
    async with aiosqlite.connect(DATABASE_PATH) as db:
        rows = await db.execute("SELECT * FROM giveaways")
        async with rows as cursor:
            result = await cursor.fetchall()
            return result if result is not None else []


async def get_giveaway(giveaway_id: int) -> list:
    """
    This function will get a giveaway from the database.

    :param giveaway_id: The ID of the giveaway.
    :return: A list of giveaways.
    """
    async with aiosqlite.connect(DATABASE_PATH) as db:
        rows = await db.execute("SELECT * FROM giveaways WHERE giveaway_id=?", (giveaway_id,))
        async with rows as cursor:
            result = await cursor.fetchall()
            return result if result is not None else []


async def get_guild_id(giveaway_id: int) -> int:
    """
    This function will get the guild ID of a giveaway.

    :param giveaway_id: The ID of the giveaway.
    :return: The guild ID of the giveaway.
    """
    async with aiosqlite.connect(DATABASE_PATH) as db:
        rows = await db.execute("SELECT guild_id FROM giveaways WHERE giveaway_id=?", (giveaway_id,))
        async with rows as cursor:
            result = await cursor.fetchone()
            return result[0] if result is not None else 0


async def is_in_giveaway(giveaway_id: int, user_id: int) -> bool:
    """
    This function will check if a user is in a giveaway.

    :param giveaway_id: The ID of the giveaway.
    :param user_id: The ID of the user that should be checked.
    :return: If the user is in the giveaway.
    """
    async with aiosqlite.connect(DATABASE_PATH) as db:
        rows = await db.execute("SELECT user_id FROM participants WHERE giveaway_id=? AND user_id=?",
                                (giveaway_id, user_id,))
        async with rows as cursor:
            result = await cursor.fetchone()
            return result is not None


async def is_finished(giveaway_id: int) -> bool:
    """
    This function will check if a giveaway is finished.

    :param giveaway_id: The ID of the giveaway.
    :return: If the giveaway is finished.
    """
    async with aiosqlite.connect(DATABASE_PATH) as db:
        rows = await db.execute("SELECT finished FROM giveaways WHERE giveaway_id=?", (giveaway_id,))
        async with rows as cursor:
            result = await cursor.fetchone()
            return result is not None


async def finish_giveaway(giveaway_id: int) -> None:
    """
    This function will finish a giveaway.

    :param giveaway_id: The ID of the giveaway.
    """
    async with aiosqlite.connect(DATABASE_PATH) as db:
        await db.execute("UPDATE giveaways SET finished=? WHERE giveaway_id=?", (1, giveaway_id,))
        await db.commit()


async def reroll(giveaway_id: int) -> None:
    """
    This function will reroll a giveaway.

    :param giveaway_id: The ID of the giveaway.
    """
    async with aiosqlite.connect(DATABASE_PATH) as db:
        await db.execute("UPDATE participants SET is_winner=? WHERE giveaway_id=?", (False, giveaway_id,))
        await db.commit()


async def get_winners(giveaway_id: int) -> list:
    """
    This function will get the winners of a giveaway.

    :param giveaway_id: The ID of the giveaway.
    :return: A list of winners.
    """
    async with aiosqlite.connect(DATABASE_PATH) as db:
        rows = await db.execute("SELECT user_id FROM participants WHERE giveaway_id=? AND is_winner=?",
                                (giveaway_id, 0))
        async with rows as cursor:
            result = await cursor.fetchall()
            return result if result is not None else []


async def set_winner(giveaway_id: int, user_id: int) -> None:
    """
    This function will set a winner for a giveaway.

    :param giveaway_id: The ID of the giveaway.
    :param user_id: The ID of the user that should be set as winner.
    """
    async with aiosqlite.connect(DATABASE_PATH) as db:
        await db.execute("UPDATE participants SET is_winner=? WHERE giveaway_id=? AND user_id=?",
                         (1, giveaway_id, user_id))
        await db.commit()


async def get_provider(giveaway_id: int) -> int:
    """
    This function will get the provider of a giveaway.

    :param giveaway_id: The ID of the giveaway.
    :return: The provider of the giveaway.
    """
    async with aiosqlite.connect(DATABASE_PATH) as db:
        rows = await db.execute("SELECT provider FROM giveaways WHERE giveaway_id=?", (giveaway_id,))
        async with rows as cursor:
            result = await cursor.fetchone()
            return result[0] if result is not None else []


async def drop_giveaways_table() -> None:
    """
    This function will drop the giveaways table.
    """
    async with aiosqlite.connect(DATABASE_PATH) as db:
        await db.execute("DROP TABLE giveaways")
        await db.commit()
    with open("schema.sql", "r") as f:
        schema = f.read()
    async with aiosqlite.connect(DATABASE_PATH) as db:
        await db.executescript(schema)
        await db.commit()


async def drop_participants_table() -> None:
    """
    This function will drop the participants table.
    """
    async with aiosqlite.connect(DATABASE_PATH) as db:
        await db.execute("DROP TABLE participants")
        await db.commit()
        with open("schema.sql", "r") as f:
            schema = f.read()
        async with aiosqlite.connect(DATABASE_PATH) as db:
            await db.executescript(schema)
            await db.commit()


# async def invite_setup(guild_id: int, inviter_id: int, invite_id: int, uses: int) -> None:
#     """
#     This function will add an invite to the database.
#
#     :param guild_id: The ID of the guild.
#     :param inviter_id: The ID of the inviter.
#     :param invite_id: The code of the invite.
#     :param uses: The number of uses of the invite.
#     """
#     async with aiosqlite.connect(DATABASE_PATH) as db:
#         await db.execute("INSERT OR IGNORE INTO invites(guild_id, code, uses) VALUES(?, ?, ?)",
#                          (guild_id, invite_id, uses))
#         await db.execute(
#             "INSERT OR IGNORE INTO totals(guild_id, inviter_id, normal, leave, fake) VALUES(?, ?, ?, ?, ?)",
#             (guild_id, inviter_id, 0, 0, 0))
#         await db.commit()


async def invite_create(guild_id: int, inviter_id: int, code: str, uses: int) -> None:
    """
    This function will add a use to an invite.
    :param guild_id: The ID of the guild.
    :param inviter_id: The ID of the inviter.
    :param code: The code of the invite.
    :param uses: The number of uses of the invite.
    """
    async with aiosqlite.connect(DATABASE_PATH) as db:
        await db.execute("INSERT OR IGNORE INTO invites(guild_id, code, inviter_id, uses) VALUES(?, ?, ?, ?)",
                         (guild_id, code, inviter_id, uses))
        await db.execute(
            "INSERT OR IGNORE INTO totals(guild_id, inviter_id, normal, leave, fake) VALUES(?, ?, ?, ?, ?)",
            (guild_id, inviter_id, uses, 0, 0))
        await db.commit()


async def invite_delete(guild_id: int, code: str) -> None:
    """
    This function will add a use to an invite.
    :param guild_id: The ID of the guild.
    :param code: The code of the invite.
    """
    async with aiosqlite.connect(DATABASE_PATH) as db:
        await db.execute("DELETE FROM invites WHERE guild_id = ? AND code = ?", (guild_id, code))
        await db.commit()


async def invite_use(guild_id: int, inviter_id: int) -> None:
    """
    This function will add a use to an invite.
    :param guild_id: The ID of the guild.
    :param inviter_id: The ID of the inviter.
    """
    async with aiosqlite.connect(DATABASE_PATH) as db:
        await db.execute("UPDATE invites SET uses = uses + 1 WHERE guild_id = ? AND inviter_id = ?",
                         (guild_id, inviter_id))
        await db.execute("UPDATE totals SET normal = normal + 1 WHERE guild_id = ? AND inviter_id = ?",
                         (guild_id, inviter_id))
        await db.commit()


async def invite_fake(guild_id: int, inviter_id: int) -> None:
    """
    This function will add a fake use to an invite.
    :param guild_id: The ID of the guild.
    :param inviter_id: The ID of the inviter.
    """
    async with aiosqlite.connect(DATABASE_PATH) as db:
        await db.execute("UPDATE invites SET uses = uses + 1 WHERE guild_id = ? AND inviter_id = ?",
                         (guild_id, inviter_id))
        await db.execute("UPDATE totals SET fake = fake + 1 WHERE guild_id = ? AND inviter_id = ?",
                         (guild_id, inviter_id))
        await db.commit()


async def invite_leave(guild_id: int, inviter_id: int) -> None:
    """
    This function will add a leave use to an invite.
    :param guild_id: The ID of the guild.
    :param inviter_id: The ID of the inviter.
    """
    async with aiosqlite.connect(DATABASE_PATH) as db:
        await db.execute("UPDATE totals SET leave = leave + 1 WHERE guild_id = ? AND inviter_id = ?",
                         (guild_id, inviter_id))
        await db.commit()


async def get_normal(guild_id: int, inviter_id: int) -> int:
    """
    This function will get the number of normal invites of a member.
    :param guild_id: The ID of the guild.
    :param inviter_id: The ID of the inviter.
    :return: The number of normal invites of the member.
    """
    async with aiosqlite.connect(DATABASE_PATH) as db:
        rows = await db.execute("SELECT normal FROM totals WHERE guild_id = ? AND inviter_id = ?",
                                (guild_id, inviter_id))
        async with rows as cursor:
            result = await cursor.fetchone()
            return result[0] if result is not None else 0


async def get_fake(guild_id: int, inviter_id: int) -> int:
    """
    This function will get the number of fake invites of a member.
    :param guild_id: The ID of the guild.
    :param inviter_id: The ID of the inviter.
    :return: The number of fake invites of the member.
    """
    async with aiosqlite.connect(DATABASE_PATH) as db:
        rows = await db.execute("SELECT fake FROM totals WHERE guild_id = ? AND inviter_id = ?",
                                (guild_id, inviter_id))
        async with rows as cursor:
            result = await cursor.fetchone()
            return result[0] if result is not None else 0


async def get_leave(guild_id: int, inviter_id: int) -> int:
    """
    This function will get the number of leave invites of a member.
    :param guild_id: The ID of the guild.
    :param inviter_id: The ID of the inviter.
    :return: The number of leave invites of the member.
    """
    async with aiosqlite.connect(DATABASE_PATH) as db:
        rows = await db.execute("SELECT leave FROM totals WHERE guild_id = ? AND inviter_id = ?",
                                (guild_id, inviter_id))
        async with rows as cursor:
            result = await cursor.fetchone()
            return result[0] if result is not None else 0


async def user_joined(guild_id: int, inviter_id, member_id: int) -> None:
    """
    This function will add a user to the database.
    :param guild_id: The ID of the guild.
    :param inviter_id: The ID of the inviter.
    :param member_id: The ID of the member.
    """
    async with aiosqlite.connect(DATABASE_PATH) as db:
        await db.execute("INSERT INTO joined(guild_id, inviter_id, member_id) VALUES(?, ?, ?)",
                         (guild_id, inviter_id, member_id))
        await db.commit()


async def user_left(guild_id: int, member_id: int) -> None:
    """
    This function will remove a user from the database.
    :param guild_id: The ID of the guild.
    :param member_id: The ID of the member.
    """
    async with aiosqlite.connect(DATABASE_PATH) as db:
        await db.execute("DELETE FROM joined WHERE guild_id = ? AND member_id = ?", (guild_id, member_id))
        await db.commit()


async def get_inviter(guild_id: int, member_id: int) -> int:
    """
    This function will get the inviter of a member.
    :param guild_id: The ID of the guild.
    :param member_id: The ID of the member.
    :return: The ID of the inviter.
    """
    async with aiosqlite.connect(DATABASE_PATH) as db:
        rows = await db.execute("SELECT inviter_id FROM joined WHERE guild_id = ? AND member_id = ?",
                                (guild_id, member_id))
        async with rows as cursor:
            result = await cursor.fetchone()
            return result[0] if result is not None else None
