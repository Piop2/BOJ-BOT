"""
# Commmand
: /problem problem_id

# Param
int problem_id: BOJ 에 등록된 문제 id
"""
from discord import app_commands
from discord.ext import commands
from discord import Embed
from discord import Interaction

from boj.api.problem import search_problem
from boj.error import BOJApiError
from utils.logger import get_logger


problem_log = get_logger("cmd.problem")


class SearchProblem(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="problem", description="search BOJ problem with ID")
    @app_commands.describe(problem_id="problem ID registered on BOJ")
    async def search(self, interaction: Interaction, problem_id: int) -> None:
        try:
            problem = search_problem(problem_id=problem_id)
        except BOJApiError.ProblemApiError.ProblemNotExistError:
            await interaction.response.send_message(f"ERROR problem id '{problem_id}' does not exist", ephemeral=False)
            problem_log.warning(f"problem does not exist: {problem_id}")
            return

        embed = Embed(title=f"{problem.id}. {problem.title}", url=problem.url)
        embed.set_author(name=problem.rank , url=f"https://static.solved.ac/tier_small/{problem.level}.svg")
        embed.set_footer(text="".join([f"#{i} " for i in problem.shorts]))

        await interaction.response.send_message(embed = embed, ephemeral=False)
        problem_log.info(f"problem found: {problem_id}")
        return


async def setup(bot) -> None:
    await bot.add_cog(SearchProblem(bot=bot))
    return
