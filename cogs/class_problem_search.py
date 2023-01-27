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

from cogs.problem import send_problem
from cogs.problem import send_problem_img
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
        self.img: bool

    @app_commands.command(name="class", description="search Class Problems with ID")
    @app_commands.describe(class_id="class ID registered on solved.ac(1~10)", img="whether to send image or not")
    async def search(self, interaction: Interaction, class_id: int, img: bool = False) -> None:
        self.img = img
        self.interaction = interaction
        self.class_id = class_id
        await self.interaction.response.defer()
        try:
            self.class_problem = solvedac.get_class_problem(class_id=self.class_id)
        except solvedac.ClassNotExistError:
            await interaction.followup.send(
                f"ERROR class id '{self.class_id}' does not exist", ephemeral=False
            )
            problem_log.warning(f"class problem does not exist: {self.class_id}")
            return
        await self.setui()
        problem_log.info(f"class problem found: {self.class_id}")


    async def setui(self):
        class_icon = File(
            f"resource/class/{3*self.class_id+1}.png", filename=f"{3*self.class_id+1}.png"
        )
        self.selects = Select(
            options=[
                SelectOption(label=f"{i.id}. {i.title}", value=i.id)
                for i in self.class_problem[self.page*25:self.page*25+25]
            ]
        )
        self.button1 = Button(label="다음 페이지", style=ButtonStyle.primary)
        self.button2 = Button(label="이전 페이지", style=ButtonStyle.danger)
        self.embed = Embed(title=f"Class {self.class_id}",
            description='\n'.join([f"[{i.id}. {i.title}]({i.url})" for i in self.class_problem[self.page*25:self.page*25+25]])+f'\n\n{self.page+1}/{len(self.class_problem)//25+1}페이지')
        self.embed.set_thumbnail(url=f"attachment://{3*self.class_id+1}.png")

        async def select_callback(interaction: Interaction) -> None:
            if self.img:
                await send_problem_img(int(self.selects.values[0]), interaction)
            else:
                await send_problem(int(self.selects.values[0]), interaction)

        async def button1_callback(interaction: Interaction):
            self.page += 1
            await self.setui()
            await interaction.response.defer()

        async def button2_callback(interaction: Interaction):
            self.page -= 1
            await self.setui()
            await interaction.response.defer()

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
            await self.interaction.followup.send(embed=self.embed, view=self.view, file=class_icon, ephemeral=False)
            self.first = False
        else:
            await self.interaction.edit_original_response(embed=self.embed, view=self.view)


    @search.error
    async def search_handler(self, ctx, error):
        problem_log.error(error)
        await ctx.followup.send(content="예상치 못한 오류 발생", ephemeral=True)
        return


async def setup(bot) -> None:
    await bot.add_cog(SearchClassProblem(bot=bot))
    return
