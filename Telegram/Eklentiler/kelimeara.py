# Bu araç @keyiflerolsun tarafından | @KekikAkademi için yazılmıştır.

from pyrogram import Client, filters
from pyrogram.types import Message
from Lugatim import Lugatim
from Telegram import konsol

@Client.on_message(filters.command(["kelimeara"], ["!", ".", "/"]))
async def kelime_ara(client: Client, message: Message):
    aranacak_kelime = message.text.split(" ")
    if len(aranacak_kelime) < 2:
        await message.reply("**⚠️ Lütfen bir kelime yazınız.**")
        return
    aranacak_kelime = aranacak_kelime[1]
    konsol.log(f"[bold green]Sorgulanan Kelime[/]: [bold purple]{aranacak_kelime}")
    lugat = Lugatim()
    kelimeLugatleri = lugat.arama_yap(aranacak_kelime)
    if kelimeLugatleri == []:
        await message.reply("**⚠️ Kelime Bulunamadı**")
    else:
        kelime_cevap = await message.reply(
            "⌛️ `Hallediyorum..`", quote=True, disable_web_page_preview=True
        )
        mesaj = ""
        for kelimeLugati in kelimeLugatleri:
            mesaj += f"**{kelimeLugati.kelime}**\n\n"
            mesaj += f"**•** {kelimeLugati.anlam}\n"
            mesaj += "\n"
            await kelime_cevap.edit(
                mesaj,
            )