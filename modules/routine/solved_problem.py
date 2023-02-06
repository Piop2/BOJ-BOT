import asyncio
import discord
from discord.ext import commands

from modules.send.problem import send_problem
from solvedac import get_user_solved
from config.config import conf
from utils.logger import get_logger

solved_log = get_logger("solved_problem")


class SolvedProblem:
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.user_data = self.bot.user_data

    async def check_solved_problem(self):
        channel = self.bot.get_channel(conf["local"]["solved_channel"])
        for member_id in self.user_data.keys():
            await asyncio.wait_for(self._send_solved(member_id=member_id, channel=channel), timeout=100)
        solved_log.info("sent all members' solved problem")

    async def _send_solved(self, member_id: int, channel: discord.channel.TextChannel) -> None:
        old_solved = self.user_data[str(member_id)]["solved"]
        await self.update_solved(member_id=member_id)
        new_solved = list(set(self.user_data[str(member_id)]["solved"]) - set(old_solved))

        if len(new_solved) > 0:
            await channel.send(f"<@{member_id}>님! {len(new_solved)}문제 풀으셨네요! 수고하셨습니다")
            for problem in new_solved:
                await send_problem(channel=channel, problem_id=problem)
        solved_log.info(f"send {member_id}'s solved problem")
        return

    async def update_solved(self, member_id: int) -> None:
        new_solved = self.get_new_solved(user_id=self.user_data[str(member_id)]["solvedAcId"])
        self.user_data.update_user(user_id=member_id, solved=new_solved)

        solved_log.info(f"updated {member_id}'s solved problem")
        return

    @staticmethod
    def get_new_solved(user_id: str) -> list[int, ...]:
        new_solved = get_user_solved(user_id=user_id)
        problem_numbers = []

        for i in new_solved:
            problem_numbers.append(i.id)

        return problem_numbers
