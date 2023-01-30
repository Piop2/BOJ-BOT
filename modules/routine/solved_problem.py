import json
import asyncio
from discord.ext import commands

from cogs.problem import send_problem
from solvedac import get_user_solved
from config.config import conf
from utils.logger import get_logger

USER_DATA_PATH = "data/user.json"
USER_DATA_BACKUP_PATH = "data/user.json.back"

solved_log = get_logger("solved_problem")


async def check_solved_problem(bot: commands.Bot):
    try:
        with open(USER_DATA_PATH, "r") as f:
            user_data = json.load(f)
    except json.JSONDecodeError:
        solved_log.warning("reading user.json failed. use backup file")
        with open(USER_DATA_BACKUP_PATH, "r") as f:
            user_data = json.load(f)
        with open(USER_DATA_PATH, "w") as f:
            json.dump(user_data, f, indent=4)

    channel = bot.get_channel(conf["local"]["solved_channel"])
    coro = []
    for member_id, user_data in user_data.items():
        coro.append(_send_solved(member_id=member_id, old_solved=user_data["solved"], channel=channel))
    await asyncio.gather(*coro)
    solved_log.info("sent all members' solved problem")


async def _send_solved(member_id: int, old_solved: list, channel) -> None:
    await update_solved(member_id=member_id)
    with open(USER_DATA_PATH, "r") as f:
        user_data = json.load(f)
    new_solved = list(set(user_data[str(member_id)]["solved"]) - set(old_solved))

    if len(new_solved) > 0:
        await channel.send(f"<@{member_id}>님! {len(new_solved)}문제 풀으셨네요! 수고하셨습니다")
        for problem in new_solved:
            await send_problem(channel=channel, problem_id=problem)
    solved_log.info(f"send {member_id}'s solved problem")
    return


async def update_solved(member_id: int) -> None:
    with open(USER_DATA_PATH, "r") as f:
        user_data = json.load(f)

    new_solved = get_new_solved(user_id=user_data[str(member_id)]["solvedAcId"])
    user_data[str(member_id)]["solved"] = new_solved

    with open(USER_DATA_PATH, "w") as f:
        json.dump(user_data, f, indent=4)

    solved_log.info(f"updated {member_id}'s solved problem")
    return


def get_new_solved(user_id: str) -> list[int, ...]:
    new_solved = get_user_solved(user_id=user_id)
    problem_numbers = []

    for i in new_solved:
        problem_numbers.append(i.id)

    return problem_numbers
