"""
# Command
: /connect user_id

# Param
str user_id: 유저 ID
"""
from discord import app_commands
from discord.ext import commands
from discord import Interaction
from discord import Object

import solvedac
from modules.role import set_member
from modules.role import change_role
from modules.role import get_tier_role
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
        except solvedac.UserNotExistError:
            await interaction.response.send_message(
                f"ERROR user id '{user_id}' does not exist", ephemeral=False
            )
            connect_log.warning(f"user does not exist: {user_id}")
            return

        await set_member(member=interaction.user, user=user)
        await change_role(member=interaction.user, new_role=get_tier_role(user=user))

        await interaction.response.send_message(f"USER ( {user.name} ) connected!")
        return

    @login.error
    async def login_handler(self, ctx, error):
        connect_log.error(error)
        await ctx.response.send_message(content="예상치 못한 오류 발생", ephemeral=True)
        return


async def setup(bot) -> None:
    await bot.add_cog(Login(bot=bot))
    return
