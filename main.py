from discord import Activity
from discord import Intents
from discord import Status
from discord.ext import commands

from config.config import conf


class Bot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix="!", intents=Intents.default(), sync_command=True)

        self.initial_extension = []

    async def on_ready(self):
        await self.change_presence(activity=Activity(name="문제 풀이", type=2), status=Status.do_not_disturb)
        return

    async def setup_hook(self):
        for ext in self.initial_extension:
            await self.load_extension(ext)
        return


if __name__ == "__main__":
    token = conf["bot"]["token"]
    Bot().run(token)
