# meta developer: @Ne_TegayMenya

from .. import loader, utils 


@loader.tds
class MuteMod(loader.Module):
    """Мут by Hz-Shka."""
    strings = {'name': 'HzMute'}

    async def client_ready(self, client, db):
        self.db = db

    async def hzmutecmd(self, message):
        """Включить/выключить мут. Используй: .hzmute <@ или реплай>."""
        if message.chat:
            chat = await message.get_chat()
            if not chat.admin_rights and not chat.creator:
                return await message.edit("<b>Я не админ здесь.</b>")
            else:
                if chat.admin_rights.delete_messages == False:
                    return await message.edit("<b>У меня нет нужных прав.</b>")
        args = utils.get_args_raw(message)
        reply = await message.get_reply_message()
        chatid = str(message.chat_id)
        mutes = self.db.get("Hzmute", "mutes", {})
        if not args and not reply: return await message.edit("<b>Нет аргументов или реплая.</b>")
        try:
            if args: 
                if args.isnumeric(): user = await message.client.get_entity(int(args))
                else: user = await message.client.get_entity(args)
            else: user = await message.client.get_entity(reply.sender_id)
        except ValueError: await message.edit("<b>Я не нашел чела которого хочешь наказать.</b>")
        if chatid not in mutes:
            mutes.setdefault(chatid, [])
        if str(user.id) not in mutes[chatid]:
            mutes[chatid].append(str(user.id))
            self.db.set("Hzmute", "mutes", mutes)
            await message.edit("<b>Ай-Ай-Ай, нельзя себя так вести.</b>")
        else:
            mutes[chatid].remove(str(user.id))
            if len(mutes[chatid]) == 0:
                mutes.pop(chatid)
            self.db.set("Hzmute", "mutes", mutes)
            await message.edit("<b>Ладно, прощаю, живи...</b>")

    async def setmutecmd(self, message):
        """Настройки мута. Используй: .setmute <hzclear/hzclearall (по желанию)>."""
        try:
            args = utils.get_args_raw(message)
            mutes = self.db.get("Hzmute", "mutes", {})
            chatid = str(message.chat_id)
            ls = mutes[chatid]
            users = ""
            if args == "hzclear":
                mutes.pop(chatid)
                self.db.set("Hzmute", "mutes", mutes)
                return await message.edit("<b>Мут-список очищен.</b>")
            if args == "hzclearall":
                self.db.set("Hzmute", "mutes", {})
                return await message.edit("<b>Мут-список очищен во всех чатах.</b>")
            for _ in ls:
                user = await message.client.get_entity(int(_))
                users += f"• <a href=\"tg://user?id={int(_)}\">{user.first_name}</a> <b>| [</b><code>{_}</code><b>]</b>\n"
            await message.edit(f"<b>В этом чате в муте: {len(ls)}</b>\n\n{users}")
        except KeyError: return await message.edit("<b>Мут-список чист.</b>")

    async def watcher(self, message):
        try:
            mutes = self.db.get("Hzmute", "mutes", {})
            chatid = str(message.chat_id)
            if chatid not in str(mutes): return
            ls = mutes[chatid]
            for _ in ls:
                if message.sender_id == int(_):
                    await message.client.delete_messages(message.chat_id, message.id)
        except: pass