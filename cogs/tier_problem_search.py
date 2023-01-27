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
from cogs.problem_search import SearchProblem

import solvedac
from solvedac.utils.rank import get_rank_id
from utils.logger import get_logger

problem_log = get_logger("cmd.tier_problem")


class SearchTierProblem(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.page = 0
        self.first = True
        self.embed: Embed
        self.view: View
        self.selects: Select
        self.button1: Button
        self.button2: Button
        self.tier_problem: list
        self.tier_id: int
        self.tier_name: str
        self.interaction: Interaction
        self.response: Interaction.InteractionResponse

    @app_commands.command(name="tier", description="search Tier Problems with Tier Name")
    @app_commands.describe(tier_name="tier Name registered on solved.ac(ex.Bronze V)")
    async def search(self, interaction: Interaction, tier_name: str) -> None:
        self.interaction = interaction
        self.tier_id = get_rank_id(tier_name)
        self.tier_name = tier_name
        await self.interaction.response.defer()
        try:
            self.tier_problem = solvedac.get_tier_problem(tier_id=self.tier_id)
        except solvedac.TierNotExistError:
            await interaction.followup.send(
                f"ERROR tier '{self.tier_name}' does not exist", ephemeral=False
            )
            problem_log.warning(f"Tier problem does not exist: {self.tier_name}")
            return
        await self.setui()
        problem_log.info(f"tier problem found: {self.tier_name}")


    @search.autocomplete('tier_name')
    async def search_autocomplete(self, interaction: Interaction, current: str) -> list[app_commands.Choice[str]]:
        tiers = ['Bronze V', 'Bronze IV', 'Bronze III', 'Bronze II', 'Bronze I', 'Silver V', 'Silver IV',
                 'Silver III', 'Silver II', 'Silver I', 'Gold V', 'Gold IV', 'Gold III', 'Gold II', 'Gold I', 'Platinum V',
                 'Platinum IV', 'Platinum III', 'Platinum II', 'Platinum I', 'Diamond V', 'Diamond IV', 'Diamond III',
                 'Diamond II', 'Diamond I', 'Ruby V', 'Ruby IV', 'Ruby III', 'Ruby II', 'Ruby I']
        return [
            app_commands.Choice(name=tier_name, value=tier_name)
            for tier_name in tiers if current.lower() in tier_name.lower()
        ]


    async def setui(self):
        tier_icon = File(
            f"resource/rank/{self.tier_id}.png", filename=f"{self.tier_id}.png"
        )
        self.selects = Select(
            options=[
                SelectOption(label=f"{i.id}. {i.title}", value=i.id)
                for i in self.tier_problem[self.page*25:self.page*25+25]
            ]
        )
        self.button1 = Button(label="다음 페이지", style=ButtonStyle.primary)
        self.button2 = Button(label="이전 페이지", style=ButtonStyle.danger)
        self.embed = Embed(title=f"{self.tier_name}",
                           description='\n'.join([f"[{i.id}. {i.title}]({i.url})" for i in self.tier_problem[self.page*25:self.page*25+25]])+f'\n\n{self.page+1}/{len(self.tier_problem)//25+1}페이지')
        self.embed.set_thumbnail(url=f"attachment://{self.tier_id}.png")

        async def select_callback(interaction: Interaction) -> None:
            await SearchProblem.send_message(int(self.selects.values[0]), interaction)

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
        if self.page != 0:
            self.view.add_item(self.button2)
        if self.page != len(self.tier_problem)//25:
            self.view.add_item(self.button1)


        if self.first == True:
            await self.interaction.followup.send(embed=self.embed, view=self.view, file=tier_icon, ephemeral=False)
            self.first = False
        else:
            await self.interaction.edit_original_response(embed=self.embed, view=self.view)


    @search.error
    async def search_handler(self, ctx, error):
        problem_log.error(error)
        await ctx.followup.send(content="예상치 못한 오류 발생", ephemeral=True)
        return


async def setup(bot) -> None:
    await bot.add_cog(SearchTierProblem(bot=bot))
    return
