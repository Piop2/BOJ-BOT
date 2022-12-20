"""
# Commmand
: /connect user_id

# Param
str user_id: 유저 ID
"""
from discord import app_commands
from discord.ext import commands
from discord import Interaction
from discord import Object

import solvedac
from modules.role import add_member
from modules.role import update_role
from config.config import conf
from utils.logger import get_logger

connect_log = get_logger("cmd.connect")


class Login(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="connect", description="connect to solved.ac")
    @app_commands.describe(user_id="user ID on BOJ")
    @app_commands.guilds(Object(id=conf["local"]["server"]))
    async def login(self, interaction: Interaction, user_id: str) -> None:
        try:
            user = solvedac.search_user(user_id=user_id)
        except solvedac.SolvedAcApiError.UserApiError.UserNotExistError:
            await interaction.response.send_message(
                f"ERROR user id '{user_id}' does not exist", ephemeral=False
            )
            connect_log.warning(f"user does not exist: {user_id}")
            return

        await add_member(member=interaction.user, user_id=user.name)
        await update_role(member=interaction.user, user=user)

        await interaction.response.send_message(f"user {user.name} connected!")
        return

    @login.error
    async def login_handler(self, ctx, error):
        connect_log.error(error)
        await ctx.response.send_message(content="예상치 못한 오류 발생", ephemeral=True)
        return


async def setup(bot) -> None:
    await bot.add_cog(Login(bot=bot))
    return