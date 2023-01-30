__version__ = "1.0.0"

from discord import Activity
from discord import ActivityType
from discord import Intents
from discord import Status
from discord import Object
from discord.ext import commands
import pygame.font

from modules.routine.routine import routine
from config.config import conf
from utils.logger import get_logger

root_log = get_logger("root")


class Bot(commands.Bot):
    def __init__(self):
        intents = Intents.default()
        intents.members = True
        super().__init__(
            command_prefix="!", intents=intents, sync_command=True
        )

        self.all_cogs = ["cogs.search",
                         "cogs.connect",
                         "cogs.class_problem_search",
                         "cogs.tier_problem_search"]

    async def setup_hook(self):
        for ext in self.all_cogs:
            await self.load_extension(ext)
        await self.tree.sync()
        await self.tree.sync(guild=Object(id=conf["local"]["server"]))
        root_log.info(f"load all extensions")
        return

    async def on_ready(self):
        presence = conf["presence"]
        activity_name = presence["activity"]["name"]
        match presence["activity"]["type"]:
            case 1:
                activity_type = ActivityType.unknown
            case 2:
                activity_type = ActivityType.playing
            case 3:
                activity_type = ActivityType.streaming
            case 4:
                activity_type = ActivityType.listening
            case 5:
                activity_type = ActivityType.watching
            case 6:
                activity_type = ActivityType.custom
            case 7:
                activity_type = ActivityType.competing
            case _:
                activity_type = ActivityType.unknown

        match presence["status"]["type"]:
            case 1:
                status_type = Status.online
            case 2:
                status_type = Status.offline
            case 3:
                status_type = Status.idle
            case 4:
                status_type = Status.do_not_disturb
            case 5:
                status_type = Status.invisible
            case _:
                status_type = Status.online

        root_log.info(f"version: {__version__}")
        root_log.info(f"activity set: name={activity_name} type={activity_type}")
        root_log.info(f"status set: type={status_type}")
        root_log.info("ready")
        await self.change_presence(
            activity=Activity(name=activity_name, type=activity_type),
            status=status_type,
        )

        await routine(bot=self)
        return


if __name__ == "__main__":
    pygame.font.init()
    Bot().run(token=conf["token"])
