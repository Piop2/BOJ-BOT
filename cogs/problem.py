"""
# Command
: /problem problem_id

# Param
int problem_id: BOJ 에 등록된 문제 id
"""
from discord import Embed
from discord import File
from discord import Interaction

import solvedac
from utils.logger import get_logger
from modules.draw.problem import make_thumbnail

problem_log = get_logger("send.problem")


async def send_problem(problem_id: int, interaction: Interaction) -> None:
    await interaction.response.defer()

    try:
        problem = solvedac.get_problem(problem_id=problem_id)
    except solvedac.ProblemNotExistError:
        await interaction.followup.send(
            f"ERROR problem id '{problem_id}' does not exist", ephemeral=False
        )
        problem_log.warning(f"problem does not exist: {problem_id}")
        return

    rank_icon = File(
        f"resource/rank/{problem.level}.png", filename=f"level_{problem.level}.png"
    )

    embed = Embed(title=f"{problem.id}. {problem.title}", url=problem.url)
    embed.set_author(name=problem.rank)
    embed.set_thumbnail(url=f"attachment://level_{problem.level}.png")
    embed.set_footer(text="".join([f"#{i} " for i in problem.shorts]))

    await interaction.followup.send(
        embed=embed, file=rank_icon, ephemeral=False
    )
    problem_log.info(f"problem found: {problem_id}")
    return


async def send_problem_img(problem_id: int, interaction: Interaction) -> None:
    await interaction.response.defer()

    try:
        problem = solvedac.get_problem(problem_id=problem_id)
    except solvedac.ProblemNotExistError:
        await interaction.response.send_message(
            f"ERROR problem id '{problem_id}' does not exist", ephemeral=False
        )
        problem_log.warning(f"problem does not exist: {problem_id}")
        return

    make_thumbnail(problem=problem)
    file = File(fp="temp/problem_thumbnail.png", filename=f"problem_{problem_id}.png")
    embed = Embed(title="보러 가기", url=problem.url)
    embed.set_image(url=f"attachment://problem_{problem_id}.png")

    await interaction.followup.send(
        embed=embed, file=file, ephemeral=False
    )

    problem_log.info(f"problem found: {problem_id}")
    return
