"""
# Command
: /problem problem_id

# Param
int problem_id: BOJ 에 등록된 문제 id
"""
from discord import app_commands
from discord.ext import commands
from discord import Interaction

from utils.logger import get_logger
from solvedac.api.search_suggestion import search_suggestion
from cogs.problem import send_problem
from cogs.problem import send_problem_img
from cogs.user import send_user

search_log = get_logger("cmd.search")


class Search(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="search", description="search solved.ac")
    @app_commands.describe(keyword="search keyword")
    async def search(self, interaction: Interaction, keyword: str) -> None:
        img = False
        search_log.info(f"search command used: {interaction.user.id}, {keyword}")
        try:
            keyword = int(keyword)
            if img:
                await send_problem_img(problem_id=keyword, interaction=interaction)
            else:
                await send_problem(problem_id=keyword, interaction=interaction)
        except ValueError:
            await send_user(user_id=keyword, interaction=interaction)

    @search.autocomplete('keyword')
    async def search_autocomplete(self, interaction: Interaction, current: str) -> list[app_commands.Choice]:
        if current == "":
            return []
        suggestions = search_suggestion(query=current)
        problems = {f'{i["id"]}': f'{i["id"]}. {i["title"]}' for i in suggestions["problems"]}
        users = {i["handle"]: f'User {i["handle"]}' for i in suggestions["users"]}
        suggestions = {**problems, **users}
        search_log.info(f"search suggestions found: {interaction.user.id}, {current}")
        return [app_commands.Choice(name=value, value=key) for key, value in suggestions.items() if True]

    @search.error
    async def search_handler(self, ctx, error):
        search_log.error(error)
        await ctx.followup.send(content="예상치 못한 오류 발생", ephemeral=True)
        return


async def setup(bot) -> None:
    await bot.add_cog(Search(bot=bot))
    return
