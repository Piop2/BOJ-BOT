import asyncio
from discord import Member
from discord import Object
from discord.ext import commands
from discord.errors import Forbidden

import solvedac
from solvedac.user import User
from config.config import conf
from utils.logger import get_logger

role_log = get_logger("roleUpdate")


class Role:
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.user_data = self.bot.user_data

    async def check_tier(self):
        guild = self.bot.get_guild(conf["local"]["server"])
        coro = []
        for member_id in self.user_data.keys():
            member = guild.get_member(int(member_id))
            coro.append(self.update_role(member=member))
        await asyncio.gather(*coro)
        role_log.info("updated all members' role")

    def get_tier_role(self, **kwargs) -> int:
        if "user" in kwargs:
            tier = self._get_user_tier(user=kwargs["user"])
        else:
            tier = kwargs["tier"]

        return conf["local"]["tier"][tier]

    async def set_member(self, member: Member, user: User) -> None:
        self.user_data[str(member.id)] = {"solvedAcId": user.name, "latestTier": self._get_user_tier(user=user),
                                          "solved": self.bot.routine.solved_problem.get_new_solved(user_id=user.name)}
        return

    @staticmethod
    async def change_role(member: Member, new_role: int, old_role: int = None) -> None:
        await member.add_roles(Object(new_role))
        if old_role is not None:
            await member.remove_roles(Object(old_role))
        return

    @staticmethod
    def _get_user_tier(user: User) -> str:
        return user.tier.split()[0]

    @staticmethod
    async def _remove_role(member: Member, role_id: int) -> None:
        try:
            await member.remove_roles(Object(role_id))
        except Forbidden:
            role_log.warning(f"{member.name} does not have role ( id: {role_id} )")
        return

    async def update_role(self, member: Member) -> None:
        print(self.user_data[str(member.id)])
        user = solvedac.get_user(user_id=self.user_data[str(member.id)]["solvedAcId"])
        latest_tier = self.user_data[str(member.id)]["latestTier"]

        tier = self._get_user_tier(user=user)
        if latest_tier == tier:
            role_log.info(f"{member.name} tier update: None")
            return

        old_role = self.get_tier_role(tier=latest_tier)
        new_role = self.get_tier_role(user=user)
        await self.change_role(member=member, old_role=old_role, new_role=new_role)
        await self.set_member(member=member, user=user)
        role_log.info(f"{member.name} tier update: {latest_tier} -> {tier}")
        return
