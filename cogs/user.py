"""
# Commmand
: /user user_id

# Param
str user_id: 유저 ID
"""
from discord import app_commands
from discord.ext import commands
from discord import Embed
from discord import File
from discord import Interaction

import solvedac
from utils.logger import get_logger

problem_log = get_logger("cmd.user")


class SearchUser(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="user", description="search BOJ user with ID")
    @app_commands.describe(user_id="user ID on BOJ")
    async def search(self, interaction: Interaction, user_id: str) -> None:
        try:
            user = solvedac.search_user(user_id=user_id)
        except solvedac.SolvedAcApiError.UserApiError.UserNotExistError:
            await interaction.response.send_message(
                f"ERROR user id '{user_id}' does not exist", ephemeral=False
            )
            problem_log.warning(f"user does not exist: {user_id}")
            return

        tier_icon = File(
            f"resource/rank/{user.tier}.png", filename=f"level_{user.tier}.png"
        )

        embed = Embed(description=user.bio)
        embed.set_author(name=user.name, url=user.url, icon_url=user.image_url)
        embed.set_thumbnail(url=f"attachment://level_{user.tier}.png")
        embed.set_image(url=user.background.image_url)
        embed.set_footer(text=user.badge.name, icon_url=user.badge.image_url)
        embed.add_field(name="클래스", value=str(user.class_))
        embed.add_field(name="랭크", value=f"#{user.rank}", inline=True)
        embed.add_field(
            name="소속", value=", ".join([org.name for org in user.organizations])
        )
        embed.add_field(name="레이팅", value=user.rating, inline=True)
        embed.add_field(name="푼 문제", value=user.solved_count, inline=True)
        embed.add_field(name="최대 연속 풀이", value=user.max_streak, inline=True)
        embed.add_field(name="기여 문제 수", value=user.vote_count, inline=True)
        embed.add_field(name="라이벌 수", value=user.rival_count, inline=True)

        await interaction.response.send_message(
            embed=embed, file=tier_icon, ephemeral=False
        )
        problem_log.info(f"user found: {user_id}")
        return


async def setup(bot) -> None:
    await bot.add_cog(SearchUser(bot=bot))
    return
