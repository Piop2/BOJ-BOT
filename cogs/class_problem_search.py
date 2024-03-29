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

from modules.send.problem import send_problem
from modules.send.problem import send_problem_img
import solvedac
from utils.logger import get_logger

class_log = get_logger("cmd.class_problem")


class SearchClassProblem(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.instance: dict[int, dict[str: any]] = {}

    @app_commands.command(name="class", description="search Class Problems with ID")
    @app_commands.describe(class_id="class ID registered on solved.ac(1~10)")
    async def search(self, interaction: Interaction, class_id: int) -> None:
        img = False
        class_log.info(f"class command used: {interaction.user.id}, {class_id}, {img}")
        if interaction.user.id in self.instance:
            try:
                await self.instance[interaction.user.id]["interaction"].delete_original_response()
            except:
                pass
        self.instance[interaction.user.id] = {"interaction": interaction, "page": 0, "first": True,
                                              "img": img, "class_id": class_id}
        await interaction.response.defer(ephemeral=True)
        try:
            self.instance[interaction.user.id]["class_problem"] = solvedac.get_class_problem(class_id=class_id)
            class_log.info(f"class problem found: {class_id}")
        except solvedac.ClassNotExistError:
            await interaction.followup.send(
                f"ERROR class id '{class_id}' does not exist"
            )
            class_log.warning(f"class problem does not exist: {class_id}")
            return
        solved = self.bot.user_data[str(interaction.user.id)]
        if solved:
            solved = solved["solved"]
            self.instance[interaction.user.id]["class_problem"] = \
                [[i.id in solved, i] for i in self.instance[interaction.user.id]["class_problem"]]
        else:
            self.instance[interaction.user.id]["class_problem"] = \
                [[False, i] for i in self.instance[interaction.user.id]["class_problem"]]
        await self.set_ui(interaction.user.id)

    async def set_ui(self, id: int):
        class_icon = File(
            f"resource/class/{3*self.instance[id]['class_id']+1}.png",
            filename=f"{3*self.instance[id]['class_id']+1}.png"
        )
        self.instance[id]['selects'] = Select(
            options=[
                SelectOption(label=f"{i[1].id}. {i[1].title}", value=i[1].id)
                for i in self.instance[id]['class_problem']
                [self.instance[id]['page']*25:self.instance[id]['page']*25+25]
            ]
        )
        self.instance[id]['button1'] = Button(label="다음 페이지", style=ButtonStyle.primary)
        self.instance[id]['button2'] = Button(label="이전 페이지", style=ButtonStyle.danger)
        self.instance[id]['embed'] = Embed(title=f"Class {self.instance[id]['class_id']}",
                                           description='\n'.join([f"[{':green_circle: ' if i[0] else ''}"
                                                                  f"{i[1].id}. {i[1].title}]({i[1].url})"
                                                                  for i in self.instance[id]['class_problem']
                                                                  [self.instance[id]['page']*25:
                                                                   self.instance[id]['page']*25+25]])
                                                       + f'\n\n{self.instance[id]["page"]+1}/'
                                                         f'{len(self.instance[id]["class_problem"])//25+1}페이지')
        self.instance[id]['embed'].set_thumbnail(url=f"attachment://{3*self.instance[id]['class_id']+1}.png")

        async def select_callback(interaction: Interaction) -> None:
            class_log.info(f"select menu selected: {interaction.user.id}, "
                           f"{self.instance[interaction.user.id]['selects'].values[0]}")
            if self.instance[interaction.user.id]['img']:
                await send_problem_img(int(self.instance[interaction.user.id]['selects'].values[0]),
                                       interaction=interaction, ephemeral=True)
            else:
                await interaction.response.defer(ephemeral=True)
                embed, file, problem_id = await send_problem(int(
                    self.instance[interaction.user.id]['selects'].values[0]), interaction=interaction)
                if self.bot.user_data[str(interaction.user.id)]:
                    if problem_id in self.bot.user_data[str(interaction.user.id)]["solved"]:
                        embed.colour = 4429174
                    else:
                        embed.colour = 13389362
                await interaction.followup.send(embed=embed, file=file, ephemeral=True)

        async def button1_callback(interaction: Interaction):
            class_log.info(f"button1 clicked: {interaction.user.id}")
            self.instance[interaction.user.id]['page'] += 1
            await self.set_ui(interaction.user.id)
            await interaction.response.defer()

        async def button2_callback(interaction: Interaction):
            class_log.info(f"button2 clicked: {interaction.user.id}")
            self.instance[interaction.user.id]['page'] -= 1
            await self.set_ui(interaction.user.id)
            await interaction.response.defer()

        self.instance[id]['selects'].callback = select_callback
        self.instance[id]['button1'].callback = button1_callback
        self.instance[id]['button2'].callback = button2_callback
        self.instance[id]['view'] = View()
        self.instance[id]['view'].add_item(self.instance[id]['selects'])
        if self.instance[id]['page'] != len(self.instance[id]['class_problem'])//25:
            self.instance[id]['view'].add_item(self.instance[id]['button1'])
        if self.instance[id]['page'] != 0:
            self.instance[id]['view'].add_item(self.instance[id]['button2'])

        if self.instance[id]['first']:
            await self.instance[id]["interaction"].followup.send(embed=self.instance[id]['embed'],
                                                                 view=self.instance[id]['view'],
                                                                 file=class_icon)
            class_log.info(f"class problem sent: {id}, {self.instance[id]['class_id']}")
            self.instance[id]['first'] = False
        else:
            await self.instance[id]["interaction"].edit_original_response(embed=self.instance[id]['embed'],
                                                                          view=self.instance[id]['view'])
            class_log.info(f"class problem edited: {id}, {self.instance[id]['class_id']}")

    @search.error
    async def search_handler(self, ctx, error):
        class_log.error(error)
        await ctx.followup.send(content="예상치 못한 오류 발생")
        return


async def setup(bot) -> None:
    await bot.add_cog(SearchClassProblem(bot=bot))
    return
