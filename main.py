from discord import Activity
from discord import Intents
from discord import Status
from discord.ext import commands

from config.config import conf
from utils.logger import get_logger


root_log = get_logger("root")


class Bot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix="!", intents=Intents.default(), sync_command=True)

        self.initial_extension = ["cogs.problem"]

    async def setup_hook(self):
        for ext in self.initial_extension:
            await self.load_extension(ext)
        await self.tree.sync()
        root_log.info("load all extensions")
        return

    async def on_ready(self):
        root_log.info(f"activity set: name={self.activity.name} type={self.activity.type}")
        root_log.info(f"status set: {self.status}")
        root_log.info("ready")
        await self.change_presence(activity=Activity(name="문제 풀이", type=2), status=Status.do_not_disturb)
        return


if __name__ == "__main__":
    token = conf["bot"]["token"]
    Bot().run(token=token)
