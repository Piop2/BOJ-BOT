# TODO class 써서 코드 깔끔시하게!!

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
from modules.routine.solved_problem import get_new_solved

USER_DATA_PATH = "data/user.json"
USER_DATA_BACKUP_PATH = "data/user.json.back"

role_log = get_logger("roleUpdate")


async def check_tier(bot: commands.Bot):
    try:
        with open(USER_DATA_PATH, "r") as f:
            user_data = json.load(f)
    except json.JSONDecodeError:
        role_log.warning("reading user.json failed. use backup file")
        with open(USER_DATA_BACKUP_PATH, "r") as f:
            user_data = json.load(f)
        with open(USER_DATA_PATH, "w") as f:
            json.dump(user_data, f, indent=4)

    guild = bot.get_guild(conf["local"]["server"])
    coro = []
    for member_id, user_data in user_data.items():
        member = guild.get_member(int(member_id))
        coro.append(_update_role(member=member, user_data=user_data))
    await asyncio.gather(*coro)
    role_log.info("updated all members' role")


def get_tier_role(**kwargs) -> int:
    if "user" in kwargs:
        tier = _get_tier(user=kwargs["user"])
    else:
        tier = kwargs["tier"]

    return conf["local"]["tier"][tier]


async def set_member(member: Member, user: User) -> None:
    with open(USER_DATA_PATH, "r") as f:
        user_data = json.load(f)

    user_data[str(member.id)] = {
        "solvedAcId": user.name,
        "latestTier": _get_tier(user=user),
        "solved": get_new_solved(user_id=user.name)
    }

    with open(USER_DATA_PATH, "w") as f:
        json.dump(user_data, f, indent=4)
    return


async def change_role(member: Member, new_role: int, old_role: int = None) -> None:
    await member.add_roles(Object(new_role))
    if old_role is not None:
        await member.remove_roles(Object(old_role))
    return


def _get_tier(user: User) -> str:
    return user.tier.split()[0]


async def _remove_role(member: Member, role_id: int) -> None:
    try:
        await member.remove_roles(Object(role_id))
    except Forbidden:
        role_log.warning(f"{member.name} does not have role ( id: {role_id} )")
    return


async def _update_role(member: Member, user_data: dict = None) -> None:
    user = solvedac.get_user(user_id=user_data["solvedAcId"])
    latest_tier = user_data["latestTier"]

    tier = _get_tier(user=user)
    if latest_tier == tier:
        role_log.info(f"{member.name} tier update: None")
        return

    old_role = get_tier_role(tier=latest_tier)
    new_role = get_tier_role(user=user)
    await change_role(member=member, old_role=old_role, new_role=new_role)
    await set_member(member=member, user=user)
    role_log.info(f"{member.name} tier update: {latest_tier} -> {tier}")
    return


async def remove_user(user: Member) -> None:
    with open(USER_DATA_PATH, "r") as f:
        user_data = json.load(f)
    user_role = get_tier_role(tier=user_data[str(user.id)]["latestTier"])
    await _remove_role(member=user, role_id=user_role)
    del user_data[str(user.id)]
    with open(USER_DATA_PATH, "w") as f:
        json.dump(user_data, f, indent=4)
    return
