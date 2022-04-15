# meta developer: @Ne_TegayMenya

from .. import loader
from asyncio import sleep

@loader.tds
class HzOnlineMod(loader.Module):
    """Вечный онлайн By Hz-Shka."""
    strings = {'name': 'HzOnline'}

    async def client_ready(self, client, db):
        self.db = db

    async def hzonlinecmd(self, message):
        """Включить/выключить вечный онлайн."""
        if not self.db.get("Eternal Online", "status"):
            self.db.set("Eternal Online", "status", True)
            await message.edit("Вечный онлайн: включен.\n👩‍💻<b>By Hz-Shka</b>")
            while self.db.get("Eternal Online", "status"):
                await message.client(__import__("telethon").functions.account.UpdateStatusRequest(offline=False))
                await sleep(60)

        else:
            self.db.set("Eternal Online", "status", False)
            await message.edit("Вечный онлайн: выключен.\n👩‍💻<b>By Hz-Shka</b>")
