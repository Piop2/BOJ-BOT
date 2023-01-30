import asyncio
from discord.ext import commands

from modules.routine.role import check_tier
from modules.routine.solved_problem import check_solved_problem
from config.config import conf
from utils.logger import get_logger

routine_log = get_logger("routine")


async def routine(bot: commands.Bot):
    await check_tier(bot=bot)
    await check_solved_problem(bot=bot)
    routine_log.info("routine finished")
    await asyncio.sleep(conf["local"]["update_timer"])
