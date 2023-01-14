"""
# Command
: /problem problem_id

# Param
int problem_id: BOJ 에 등록된 문제 id
"""
from discord import app_commands
from discord.ext import commands
from discord import Embed
from discord import File
from discord import Interaction

import solvedac
from utils.logger import get_logger
from modules.draw.problem import make_thumbnail

problem_log = get_logger("cmd.problem")


class SearchProblem(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="problem", description="search BOJ problem with ID")
    @app_commands.describe(problem_id="problem ID registered on BOJ")
    async def search(self, interaction: Interaction, problem_id: int) -> None:
        try:
            problem = solvedac.search_problem(problem_id=problem_id)
        except solvedac.ProblemNotExistError:
            await interaction.response.send_message(
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

        await interaction.response.send_message(
            embed=embed, file=rank_icon, ephemeral=False
        )
        problem_log.info(f"problem found: {problem_id}")
        return

    @app_commands.command(name="problem-img", description="search BOJ problem with ID")
    @app_commands.describe(problem_id="problem ID registered on BOJ")
    async def search_img(self, interaction: Interaction, problem_id: int) -> None:
        try:
            problem = solvedac.search_problem(problem_id=problem_id)
        except solvedac.ProblemNotExistError:
            await interaction.response.send_message(
                f"ERROR problem id '{problem_id}' does not exist", ephemeral=False
            )
            problem_log.warning(f"problem does not exist: {problem_id}")
            return

        try:
            make_thumbnail(problem=problem)
            file = File("temp/problem_thumbnail.png", filename="test_thumbnail.png")

            embed = Embed(title="보러 가기", url=problem.url)
            embed.set_image(url="attachment://test_thumbnail.png")

            await interaction.response.send_message(
                embed=embed, file=file, ephemeral=False
            )
            problem_log.info(f"problem found: {problem_id}")
        except Exception as e:
            problem_log.error(e)
        return

    @search.error
    async def search_handler(self, ctx, error):
        problem_log.error(error)
        await ctx.response.send_message(content="예상치 못한 오류 발생", ephemeral=True)
        return

    @search_img.error
    async def search_img_handler(self, ctx, error):
        problem_log.error(error)
        await ctx.response.send_message(content="예상치 못한 오류 발생", ephemeral=True)
        return


async def setup(bot) -> None:
    await bot.add_cog(SearchProblem(bot=bot))
    return
