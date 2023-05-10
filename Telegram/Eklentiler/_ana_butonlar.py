# Bu araç @keyiflerolsun tarafından | @KekikAkademi için yazılmıştır.

from pyrogram import Client, filters
from pyrogram.types import Message, CallbackQuery

# Ana Butonlar
start_mesajı = "** Botu /kelimeara aranacak_kelime Şeklinde Kullanmaya Başlayabilirsiniz**"


@Client.on_message(filters.command(["start"], ["!", ".", "/"]))
async def start_buton(client: Client, message: Message):
    # < Başlangıç
    ilk_mesaj = await message.reply(
        "⌛️ `Hallediyorum..`", quote=True, disable_web_page_preview=True
    )
    # ------------------------------------------------------------- Başlangıç >

    await ilk_mesaj.delete()
    await message.reply(
        start_mesajı, quote=True
    )



