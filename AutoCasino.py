# meta Developer: @Ne_TegayMenya

from telethon import types 
from .. import loader, utils 
from typing import * 
import asyncio 
 
@loader.tds 
class AutoCasinoMod(loader.Module): 
    'Авто-Казино BFG.' 
 
    strings = { 
        'name':'AutoCasino' 
    } 
     
    start: int = 0 
    last: int = 0 
    loses: int = 0 
    is_started: bool = False 
    bot: str = '@bforgame_bot' 
    bot_id: int = 1721358063 
     
    async def casinocmd(self, m: types.Message): 
        '.casino <x> - начать с x ставки' 
        args: str = utils.get_args_raw(m) 
        if self.is_started: 
            return await utils.answer(m, 'Уже запущен! Для остановки юзай .casinostop') 
        try: 
            self.last = int(args) 
            self.start = int(args) 
            self.loses = 0 
        except: 
            return await utils.answer(m, 'Введи корректное число.') 
        self.is_started = True 
        await m.client.send_message(self.bot, "казино {} ".format(self.start)) 
        await utils.answer(m, 'Запущено! Начальная ставка {}.'.format(self.start)) 
 
    async def casinostopcmd(self, m: types.Message): 
        '.casinostop - остановить казино.' 
        if not self.is_started: 
            return await utils.answer(m, 'Не запущено! Для запуска юзай .casino <начальная ставка>.') 
        self.is_started = False 
        await utils.answer(m, 'Остановлено!') 
     
    async def watcher(self, m: types.Message): 
        if not isinstance(m, types.Message): 
            return 
        if not hasattr(m.peer_id, 'user_id'): 
            return 
        chat = m.peer_id.user_id 
        if chat == self.bot_id and not m.out and self.is_started: 
            if 'вы выиграли' in m.raw_text: 
                await asyncio.sleep(6) 
                self.loses = 0 
                self.last = self.start 
                await m.client.send_message(self.bot, "казино {} ".format(self.last)) 
            elif 'остаются' in m.raw_text: 
                await asyncio.sleep(6) 
                self.loses = 0 
                await m.client.send_message(self.bot, "казино {} ".format(self.last)) 
            elif 'вы проиграли' in m.raw_text or 'сгорели' in m.raw_text: 
                await asyncio.sleep(6) 
                if self.loses >= 15: 
                    self.loses = 0 
                    self.last = self.start 
                else: 
                    self.last *= 2 
                    self.loses += 1 
                await m.client.send_message(self.bot, "казино {} ".format(self.last)) 
            elif 'Недостаточно' in m.raw_text: 
                await asyncio.sleep(6) 
                self.last = self.start 
                self.loses = 0 
                await m.client.send_message(self.bot, "казино {} ".format(self.last))