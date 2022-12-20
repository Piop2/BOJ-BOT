import json
import asyncio
from discord import Member
from discord import Object
from discord.ext import commands
from discord.errors import Forbidden

import solvedac
from solvedac.user import User
from config.config import conf
from utils.logger import get_logger

USER_DATA_PATH = "data/user.json"

connect_log = get_logger("cmd.connect")


async def set_member(member: Member, user_id: str) -> None:
    with open(USER_DATA_PATH, "r") as f:
        user_data = json.load(f)
        user_data[member.id] = user_id

    with open(USER_DATA_PATH, "w") as f:
        json.dump(user_data, f, indent=4)
    return


async def reset_role(member: Member) -> None:
    for role_id in conf["local"]["tier"].values():
        try:
            await member.remove_roles(Object(role_id))
        except Forbidden:
            pass
        else:
            return
    return


async def update_role(member: Member, user_id: str = None, user: User = None) -> None:
    await reset_role(member=member)

    if user_id is not None:
        user = solvedac.search_user(user_id=user_id)
    elif user is None:
        connect_log.error("update_role should get 1 param: user_id or user")

    role_name = user.tier.split()[0]
    role_id = conf["local"]["tier"][role_name]
    await member.add_roles(Object(role_id))
    return


async def check_tier(bot: commands.Bot):
    while True:
        with open(USER_DATA_PATH, "r") as f:
            user_data = json.load(f)

        guild = bot.get_guild(conf["local"]["server"])
        coro = []
        for member_id, user_id in user_data.items():
            member = guild.get_member(int(member_id))
            coro.append(update_role(member=member, user_id=user_id))
        await asyncio.gather(*coro)
        connect_log.info("update all members' role")

        await asyncio.sleep(conf["local"]["update_timer"])
