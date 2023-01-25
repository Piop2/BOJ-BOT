"""
# Command
: /connect user_id

# Param
str user_id: 유저 ID
"""
from discord import app_commands
from discord.ext import commands
from discord import Interaction, Embed
from discord.ui import Button, View
from discord import ButtonStyle
from discord import Object
import random

import solvedac
from modules.routine.role import set_member
from modules.routine.role import change_role
from modules.routine.role import get_tier_role
from config.config import conf
from utils.logger import get_logger

connect_log = get_logger("cmd.connect")


class Login(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.interaction: Interaction

    @app_commands.command(name="connect", description="connect to solved.ac")
    @app_commands.describe(user_id="user ID on BOJ")
    @app_commands.guilds(Object(id=conf["local"]["server"]))
    async def connect(self, interaction: Interaction, user_id: str) -> None:
        self.interaction = interaction
        await interaction.response.defer()

        try:
            user = solvedac.get_user(user_id=user_id)
        except solvedac.UserNotExistError:
            await interaction.followup.send(
                f"ERROR user id '{user_id}' does not exist", ephemeral=True
            )
            connect_log.warning(f"user does not exist: {user_id}")
            return

        key = ''.join(random.sample('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890!@#$%^&*', 50))
        embed = Embed(title=f'{user.name}님의 유저 등록 절차를 시작합니다', description=f'1. solved.ac에 로그인하고 본인의 프로필 페이지로 가주세요\n'
                                                 f'2. 프로필 편집 버튼을 누르 상태메시지를 적는 칸에 아래의 코드롤 복사해서 넣어주세요\n``{key}``\n'
                                                 f'3. 등록 확인 버튼을 눌러주세요')
        button1 = Button(style=ButtonStyle.green, label='등록 확인')
        button2 = Button(style=ButtonStyle.red, label='취소')
        attempt = 1
        async def button1_callback(interaction: Interaction):
            nonlocal attempt
            if await self.check_certification(key=key, user_id=user_id):
                embed = Embed(title=f'{user.name}님의 유저 등록이 완료되었습니다', description=f'{user.name}님과 {interaction.user.name}님은 이제 하나입니다!\n'
                                                                                 f'프로필의 상태메시지는 원래대로 돌려놓으셔도 좋습니다.')
                await set_member(member=interaction.user, user=user)
                await change_role(member=interaction.user, new_role=get_tier_role(user=user))
                await self.interaction.edit_original_response(embed=embed, view=None)
            else:
                if attempt > 5:
                    embed = Embed(title='등록이 최소되었습니다', description='등록을 너무 많이 시도하셨습니다\n등록 절차를 강제로 중단합니다.')
                    await self.interaction.edit_original_response(embed=embed, view=None)
                else:
                    embed = Embed(title=f'{user.name}님의 유저 등록에 실패했습니다', description=f'{attempt}번째 시도는 실패하셨습니다. 다시 시도해주세요\n'
                                                                                 f'1. solved.ac에 로그인하고 본인의 프로필 페이지로 가주세요\n'
                                                                                 f'2. 프로필 편집 버튼을 누르 상태메시지를 적는 칸에 아래의 코드롤 복사해서 넣어주세요\n``{key}``\n'
                                                                                 f'3. 등록 확인 버튼을 눌러주세요')
                    attempt += 1
                    await self.interaction.edit_original_response(embed=embed)

        async def button2_callback(interaction: Interaction):
            embed = Embed(title='등록을 취소하셨습니다', description='등록절차가 중단되었습니다')
            await self.interaction.edit_original_response(embed=embed, view=None)

        button1.callback = button1_callback
        button2.callback = button2_callback
        view = View()
        view.add_item(button1)
        view.add_item(button2)
        await interaction.followup.send(embed=embed, ephemeral=True, view=view)
        return


    async def check_certification(self, key: str, user_id: str) -> bool:
        user = solvedac.get_user(user_id=user_id)
        if key in user.bio:
            return True
        else:
            return False


    @connect.error
    async def cnt_handler(self, ctx, error):
        connect_log.error(error)
        await ctx.response.send_message(content="예상치 못한 오류 발생", ephemeral=True)
        return


async def setup(bot) -> None:
    await bot.add_cog(Login(bot=bot))
    return
