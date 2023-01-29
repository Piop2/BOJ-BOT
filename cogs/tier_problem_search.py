"""
# Command
: /tier tier_name

# Param
str tier_name: solved.ac 에 있는 티어 이름
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
from solvedac.utils.rank import get_rank_id
from utils.logger import get_logger

problem_log = get_logger("cmd.tier_problem")


class SearchTierProblem(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.instance: dict[int, dict[str: any]] = {}

    @app_commands.command(name="tier", description="search Tier Problems with Tier Name")
    @app_commands.describe(tier_name="tier Name registered on solved.ac(ex.Bronze V)",
                           img="whether to send image or not")
    async def search(self, interaction: Interaction, tier_name: str, img: bool = False) -> None:
        if interaction.user.id in self.instance:
            await self.instance[interaction.user.id]["interaction"].delete_original_response()
        tier_id = get_rank_id(tier_name)
        self.instance[interaction.user.id] = {"interaction": interaction, "page": 0, "first": True,
                                              "img": img, "tier_id": tier_id, "tier_name": tier_name}
        await interaction.response.defer(ephemeral=True)
        try:
            self.instance[interaction.user.id]["tier_problem"] = solvedac.get_tier_problem(tier_id=tier_id)
        except solvedac.TierNotExistError:
            await interaction.followup.send(
                f"ERROR tier '{tier_name}' does not exist"
            )
            problem_log.warning(f"Tier problem does not exist: {tier_name}")
            return
        await self.set_ui(interaction.user.id)
        problem_log.info(f"tier problem found: {tier_name}")

    @search.autocomplete('tier_name')
    async def search_autocomplete(self, interaction: Interaction, current: str) -> list[app_commands.Choice[str]]:
        tiers = ['Bronze V', 'Bronze IV', 'Bronze III', 'Bronze II', 'Bronze I',
                 'Silver V', 'Silver IV', 'Silver III', 'Silver II', 'Silver I',
                 'Gold V', 'Gold IV', 'Gold III', 'Gold II', 'Gold I',
                 'Platinum V', 'Platinum IV', 'Platinum III', 'Platinum II', 'Platinum I',
                 'Diamond V', 'Diamond IV', 'Diamond III', 'Diamond II', 'Diamond I',
                 'Ruby V', 'Ruby IV', 'Ruby III', 'Ruby II', 'Ruby I']
        return [
            app_commands.Choice(name=tier_name, value=tier_name)
            for tier_name in tiers if current.lower() in tier_name.lower()
        ]

    async def set_ui(self, id: int):
        tier_icon = File(
            f"resource/rank/{self.instance[id]['tier_id']}.png", filename=f"{self.instance[id]['tier_id']}.png"
        )
        self.instance[id]['selects'] = Select(
            options=[
                SelectOption(label=f"{i.id}. {i.title}", value=i.id)
                for i in self.instance[id]['tier_problem'][self.instance[id]['page']*25:self.instance[id]['page']*25+25]
            ]
        )
        self.instance[id]['button1'] = Button(label="다음 페이지", style=ButtonStyle.primary)
        self.instance[id]['button2'] = Button(label="이전 페이지", style=ButtonStyle.danger)
        self.instance[id]['embed'] = Embed(title=f"{self.instance[id]['tier_name']}",
                                           description='\n'.join([f"[{i.id}. {i.title}]({i.url})"
                                                                  for i in self.instance[id]['tier_problem']
                                                                  [self.instance[id]['page']*25:
                                                                   self.instance[id]['page']*25+25]])
                                                       + f'\n\n{self.instance[id]["page"]+1}/'
                                                         f'{len(self.instance[id]["tier_problem"])//25+1}페이지')
        self.instance[id]['embed'].set_thumbnail(url=f"attachment://{self.instance[id]['tier_id']}.png")

        async def select_callback(interaction: Interaction) -> None:
            if self.instance[interaction.user.id]['img']:
                await send_problem_img(int(self.instance[interaction.user.id]['selects'].values[0]),
                                       interaction=interaction, ephemeral=True)
            else:
                await send_problem(int(self.instance[interaction.user.id]['selects'].values[0]),
                                   interaction=interaction, ephemeral=True)

        async def button1_callback(interaction: Interaction):
            self.instance[interaction.user.id]['page'] += 1
            await self.set_ui(interaction.user.id)
            await interaction.response.defer()

        async def button2_callback(interaction: Interaction):
            self.instance[interaction.user.id]['page'] -= 1
            await self.set_ui(interaction.user.id)
            await interaction.response.defer()

        self.instance[id]['selects'].callback = select_callback
        self.instance[id]['button1'].callback = button1_callback
        self.instance[id]['button2'].callback = button2_callback
        self.instance[id]['view'] = View()
        self.instance[id]['view'].add_item(self.instance[id]['selects'])
        if self.instance[id]['page'] != 0:
            self.instance[id]['view'].add_item(self.instance[id]['button2'])
        if self.instance[id]['page'] != len(self.instance[id]['tier_problem'])//25:
            self.instance[id]['view'].add_item(self.instance[id]['button1'])

        if self.instance[id]['first']:
            await self.instance[id]['interaction'].followup.send(embed=self.instance[id]['embed'],
                                                                 view=self.instance[id]['view'],
                                                                 file=tier_icon, ephemeral=False)
            self.instance[id]['first'] = False
        else:
            await self.instance[id]['interaction'].edit_original_response(embed=self.instance[id]['embed'],
                                                                          view=self.instance[id]['view'])

    @search.error
    async def search_handler(self, ctx, error):
        problem_log.error(error)
        await ctx.followup.send(content="예상치 못한 오류 발생", ephemeral=True)
        return


async def setup(bot) -> None:
    await bot.add_cog(SearchTierProblem(bot=bot))
    return
