# Bu araç @keyiflerolsun tarafından | @KekikAkademi için yazılmıştır.

from pyrogram import Client, __version__
from pyrogram.errors import ApiIdInvalid, AccessTokenInvalid
from dotenv import load_dotenv
from Tabanım.taban import Amil
import os, sys
from pyrogram.types import BotCommand

taban = Amil(
    baslik="Lugatim",
    aciklama="Lugatim Başlatıldı..",
    banner="Lugatim",
    girinti=3,
)

konsol = taban.konsol


def hata(yazi: str) -> None:
    konsol.print(yazi, style="bold red")


def bilgi(yazi: str) -> None:
    konsol.print(yazi, style="blue")


def basarili(yazi: str) -> None:
    konsol.print(yazi, style="bold green", width=70, justify="center")


def onemli(yazi: str) -> None:
    konsol.print(yazi, style="bold cyan")


if sys.version_info[0] < 3 or sys.version_info[1] < 6:
    hata(
        """En az python 3.6 sürümüne sahip olmanız gerekir.
              Birden fazla özellik buna bağlıdır. Bot kapatılıyor."""
    )
    quit(1)

if (taban.bellenim_surumu.split("-")[-1] != "aws") and (
    not os.path.exists("ayar.env")
):  # Heroku Geçmek için aws
    hata("\n\tLütfen ayar.env dosyanızı oluşturun..\n")
    quit(1)

load_dotenv("ayar.env")

if AYAR_KONTROL := os.environ.get(
    "___________LUTFEN_______BU_____SATIRI_____SILIN__________", None
):
    hata(
        "\n\tLütfen ayar.env dosyanızı düzenlediğinize emin olun /veya\n\tilk hashtag'de belirtilen satırı kaldırın..\n"
    )
    quit(1)

API_ID = str(os.environ.get("API_ID", str))
API_HASH = str(os.environ.get("API_HASH", str))
BOT_TOKEN = str(os.environ.get("BOT_TOKEN", str))
LOG_ID = str(os.environ.get("LOG_ID", str))
SESSION_ADI = str(os.environ.get("SESSION_ADI", str))
BOT_KULLANICI_ADI = str(os.environ.get("BOT_KULLANICI_ADI", str))

try:
    LugatimBot = Client(
        api_id=API_ID,
        api_hash=API_HASH,
        name=SESSION_ADI,
        bot_token=BOT_TOKEN,
        plugins=dict(root="Telegram/Eklentiler"),
    )
except ValueError:
    hata("\n\tLütfen ayar.env dosyanızı DÜZGÜNCE! oluşturun..\n")
    quit(1)

DESTEK_KOMUT = {}

tum_eklentiler = [
    f"📂 {dosya.replace('.py','')}"
    for dosya in os.listdir("./Telegram/Eklentiler/")
    if dosya.endswith(".py") and not dosya.startswith("_")
]


def baslangic() -> None:
    try:
        LugatimBot.start()
    except ApiIdInvalid:
        hata("\n\tayar.env dosyasındaki API Bilgileri Geçersiz..\n")
        quit(1)
    except AccessTokenInvalid:
        hata("\n\tBot Token Geçersiz..\n")
        quit(1)
    # Set new commands
    LugatimBot.set_bot_commands([
        BotCommand("start", "Botu Başlat"),
        BotCommand("kelimeara", "Kelime Arama Komutu")])

    surum = f"{str(sys.version_info[0])}.{str(sys.version_info[1])}"
    konsol.print(
        f"[gold1]@{SESSION_ADI}[/] [yellow]:bird:[/] [bold red]Python: [/][i]{surum}[/]",
        width=70,
        justify="center",
    )
    basarili(
        f"{SESSION_ADI} [magenta]v[/] [blue]{__version__}[/] [red]Pyrogram[/] tabanında [magenta]{len(tum_eklentiler)} eklentiyle[/] çalışıyor...\n"
    )

    LugatimBot.stop()
