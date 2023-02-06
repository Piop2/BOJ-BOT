import asyncio
from discord.ext import commands

from modules.routine.role import Role
from modules.routine.solved_problem import SolvedProblem
from config.config import conf
from utils.logger import get_logger

routine_log = get_logger("routine")


class Routine:
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.role = Role(bot=self.bot)
        self.solved_problem = SolvedProblem(bot=self.bot)

    async def routine(self):
        while True:
            await self.role.check_tier()
            await self.solved_problem.check_solved_problem()
            self.bot.user_data.save_backup_file()
            routine_log.info("routine finished")
            await asyncio.sleep(conf["local"]["update_timer"])
