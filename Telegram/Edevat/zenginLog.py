# Bu araç @keyiflerolsun tarafından | @KekikAkademi için yazılmıştır.

from pyrogram import Client
from pyrogram.types import Message
import datetime, pytz
from Telegram import SESSION_ADI, LOG_ID, hata, taban

tarih = lambda: datetime.datetime.now(pytz.timezone("Turkey")).strftime("%d-%m-%Y")
saat = lambda: datetime.datetime.now(pytz.timezone("Turkey")).strftime("%H:%M:%S")


async def log_yolla(client: Client, message: Message):
    uye_id = message.from_user.id
    uye_nick = f"@{message.from_user.username}" if message.from_user.username else None
    uye_adi = f"{message.from_user.first_name or ''} {message.from_user.last_name or ''}".strip()
    komut = message.text

    if message.chat.type not in ["private", "bot"]:
        sohbet = await client.get_chat(message.chat.id)
        sohbet_adi = f"@{sohbet.username}" if sohbet.username else sohbet.title
    else:
        sohbet_adi = message.chat.type

    taban.log_salla(uye_nick or uye_adi, komut, sohbet_adi)

    with open(f"@{SESSION_ADI}.log", "a+", encoding="utf-8") as log_yaz:
        log_yaz.write(
            f"[{saat()} | {tarih()}]"
            + " {:20} || {:50} {:>2}|| {:^20}\n".format(
                uye_nick or uye_adi, komut, "", sohbet_adi
            )
        )

    try:
        await client.send_message(
            int(LOG_ID),
            f"**Kullanıcı :** __{message.from_user.mention}__\n\n**Komut :** `{komut}`\n\n**Sohbet :** __{sohbet_adi}__",
        )
    except ValueError:
        hata("\n\tLOG ID Geçersiz..\n")
        await message.reply("`LOG ID geçersiz olduğu için bot kapatıldı!`")
        quit(1)


async def buton_log_yolla(client: Client, callback_query):
    uye_id = callback_query.from_user.id
    uye_nick = (
        f"@{callback_query.from_user.username}"
        if callback_query.from_user.username
        else None
    )
    uye_adi = f"{callback_query.from_user.first_name or ''} {callback_query.from_user.last_name or ''}".strip()
    komut = callback_query.data
    if callback_query.message.chat.type not in ["private", "bot"]:
        sohbet = await client.get_chat(callback_query.message.chat.id)
        sohbet_adi = f"@{sohbet.username}" if sohbet.username else sohbet.title
    else:
        sohbet_adi = callback_query.message.chat.type

    taban.log_salla(uye_nick or uye_adi, komut, sohbet_adi)

    with open(f"@{SESSION_ADI}.log", "a+", encoding="utf-8") as log_yaz:
        log_yaz.write(
            f"[{saat()} | {tarih()}]"
            + " {:20} || {:50} {:>2}|| {:^20}\n".format(
                uye_nick or uye_adi, komut, "", sohbet_adi
            )
        )

    try:
        await client.send_message(
            int(LOG_ID),
            f"**Kullanıcı :** __{callback_query.from_user.mention}__\n\n**Komut :** `{komut}`\n\n**Sohbet :** __{sohbet_adi}__",
        )
    except ValueError:
        hata("\n\tLOG ID Geçersiz..\n")



async def hata_log(hata_: Exception, client: Client, message: Message = None):
    taban.hata_salla(hata_)
    if message:
        await message.edit(
            f"⚠️ **Hata Oluştu !**\n\n🚨 `{type(hata_).__name__}`\n\n🔖 __{hata_}__\n\n**Hata Satırı :** `{hata_.__traceback__.tb_lineno}`"
        )

    with open(f"@{SESSION_ADI}.log", "a+") as log_yaz:
        log_yaz.write(f"\n\t\t{type(hata_).__name__}\t»\t{hata_}\n\n")
        
    try:
        await client.send_message(
            int(LOG_ID.split(",")[0]),
            f"⚠️ **Hata Oluştu !**\n\n🚨 `{type(hata_).__name__}`\n\n🔖 __{hata_}__\n\n**Hata Satırı :** `{hata_.__traceback__.tb_lineno}`",
        )
    except ValueError:
        hata("\n\tLOG ID Geçersiz..\n")
        await message.reply("`LOG ID geçersiz olduğu için bot kapatıldı!`")
        quit(1)