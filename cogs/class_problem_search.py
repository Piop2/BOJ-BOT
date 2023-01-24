"""
# Command
: /class class_id

# Param
int class_id: solved.ac 에 등록된 class id
"""
from discord import app_commands
from discord.ext import commands
from discord import Embed
from discord import File
from discord.ui import Select
from discord import SelectOption
from discord.ui import Button, View
from discord import ButtonStyle
from discord import Interaction
from cogs.problem_search import SearchProblem

import solvedac
from utils.logger import get_logger

problem_log = get_logger("cmd.class_problem")


class SearchClassProblem(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.page = 0
        self.first = True
        self.embed: Embed
        self.view: View
        self.selects: Select
        self.button1: Button
        self.button2: Button
        self.class_problem: list
        self.class_id: int
        self.interaction: Interaction
        self.response: Interaction.InteractionResponse

    @app_commands.command(name="class", description="search Class Problems with ID")
    @app_commands.describe(class_id="class ID registered on solved.ac")
    async def search(self, interaction: Interaction, class_id: int) -> None:
        self.interaction = interaction
        self.class_id = class_id
        try:
            self.class_problem = solvedac.get_class_problem(class_id=self.class_id)
        except solvedac.ClassNotExistError:
            await interaction.response.send_message(
                f"ERROR class id '{self.class_id}' does not exist", ephemeral=False
            )
            problem_log.warning(f"class problem does not exist: {self.class_id}")
            return
        await self.setui()
        problem_log.info(f"class problem found: {self.class_id}")


    async def setui(self):
        class_icon = File(
            f"resource/class/{3*self.class_id+1}.png", filename=f"class{self.class_id}.png"
        )
        self.selects = Select(
            options=[
                SelectOption(label=f"{i.id}. {i.title}", value=i.id)
                for i in self.class_problem[self.page*25:self.page*25+25]
            ]
        )
        self.button1 = Button(label="다음 페이지", style=ButtonStyle.primary)
        self.button2 = Button(label="이전 페이지", style=ButtonStyle.primary)
        self.embed = Embed(title=f"Class {self.class_id}",
            description='\t'.join([f"{i.id}. {i.title}" for i in self.class_problem[self.page*25:self.page*25+25]])+f'\n\n{self.page+1}페이지')
        self.embed.set_thumbnail(url=f"attachment://class{self.class_id}.png")

        async def select_callback(interaction: Interaction) -> None:
            await self.interaction.response.send_message(f"{self.selects.values[0]}를 선택하셨습니다.")

        async def button1_callback(interaction: Interaction):
            self.page += 1
            await self.setui()

        async def button2_callback(interaction: Interaction):
            self.page -= 1
            await self.setui()

        self.selects.callback = select_callback
        self.button1.callback = button1_callback
        self.button2.callback = button2_callback
        self.view = View()
        self.view.add_item(self.selects)
        if self.page != len(self.class_problem)//25:
            self.view.add_item(self.button1)
        if self.page != 0:
            self.view.add_item(self.button2)

        if self.first == True:
            await self.interaction.response.send_message(embed=self.embed, view=self.view, file=class_icon, ephemeral=False)
            self.first = False
        else:
            await self.interaction.response.message.edit_message(embed=self.embed, view=self.view)


    @search.error
    async def search_handler(self, ctx, error):
        problem_log.error(error)
        await ctx.response.send_message(content="예상치 못한 오류 발생", ephemeral=True)
        return


async def setup(bot) -> None:
    await bot.add_cog(SearchClassProblem(bot=bot))
    return
