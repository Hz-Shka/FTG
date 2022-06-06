# -*- coding: utf-8 -*-

# meta Developer: @Ne_TegayMenya

import random
import telethon
import logging
from .. import loader, utils
from random import randint, choice


def register(cb):
    cb(EditMod())

@loader.tds
class EditMod(loader.Module):
    """✏️Изменяет сообщение, Поддерживает HTML.
        ❤P.S. Это первый модуль Хз-Шки❤"""
    strings = {'name': 'EditText'}

    async def izcmd(self, message):
        """Ответ на сооб. + .iz {text} — Изменяет сообщение, Поддерживает HTML. Пример:
        	.iz <b>Привет</b> – "<b>" делает текст жирным. """
        args = utils.get_args_raw(message)
        if message.is_reply:
            if args:
                reply = await message.get_reply_message()
                await message.delete()
                await reply.edit(f"{args}")
                return
            if not args:
                await message.edit(f'<b>Неверно указаны аргументы.</b>')
                return
        if not message.is_reply:
            await message.edit(f'<b>💩Что изменять то?\nИзменять можно только в ответ на сообщение(своё)</b>')
            
            
    async def hcmd(self, message):
        """.h {text} — Изменяет сообщение, Поддерживает HTML. Пример:
        	.h <b>Как дела?</b> – "<b>" делает текст жирным. """
        args = utils.get_args_raw(message)
        if not message.is_reply:
            if args:
                await message.delete()
                await message.client.send_message(message.chat_id, f"{args}")
            if not args:
                await message.edit(f'<b>Привет, ты гей❤</b>')
        if message.is_reply:
            await message.edit(f'<b>Создатель модуля – <a href="t.me/Ne_TegayMenya">👑Хз-Шка👑</a>\nА так же он гей💩\nЮзай ".iz"</b>')