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


async def get_leaderboard(server_id: int, limit: int = 10) -> list:
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
