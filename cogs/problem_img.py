"""
# Commmand
: /problem_img problem_id

# Param
int problem_id: BOJ 에 등록된 문제 id
"""
from discord import app_commands
from discord.ext import commands
from discord import Embed
from discord import Interaction
from discord import File

import solvedac
from utils.logger import get_logger
from modules.image import make_problem_thumbnail

problem_log = get_logger("cmd.problem")


class SearchProblemImg(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="problem_img", description="search BOJ problem with ID")
    @app_commands.describe(problem_id="problem ID registered on BOJ")
    async def search(self, interaction: Interaction, problem_id: int) -> None:
        try:
            problem = solvedac.search_problem(problem_id=problem_id)
        except solvedac.SolvedAcApiError.ProblemApiError.ProblemNotExistError:
            await interaction.response.send_message(
                f"ERROR problem id '{problem_id}' does not exist", ephemeral=False
            )
            problem_log.warning(f"problem does not exist: {problem_id}")
            return

        try:
            make_problem_thumbnail(problem=problem)
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


async def setup(bot) -> None:
    await bot.add_cog(SearchProblemImg(bot=bot))
    return
