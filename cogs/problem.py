"""
# Commmand
: /problem problem_id

# Param
int problem_id: BOJ에 등록된 문제 id
"""
from discord import app_commands
from discord import Interaction
from discord.ext import commands

from boj.api.problem import search_problem
from boj.error import BOJApiError


class SearchProblem(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="problem", description="search boj problem with id")
    @app_commands.describe(problem_id="problem ID registered on BOJ")
    async def search(self, interaction: Interaction, problem_id: int) -> None:
        try:
            problem = search_problem(problem_id=problem_id)
        except BOJApiError.ProblemApiError.ProblemNotExistError:
            await interaction.response.send_message(f"ERROR problem id '{problem_id}' does not exist", ephemeral=False)
        else:
            await interaction.response.send_message(f"{problem.problem_id}.{problem.title_ko}: {problem.rank}", ephemeral=False)
        return


async def setup(bot) -> None:
    await bot.add_cog(SearchProblem(bot=bot))
    return
