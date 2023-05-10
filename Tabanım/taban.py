from pyfiglet import Figlet
import os, platform, requests, datetime, pytz
from rich.console import Console
from requests.exceptions import ConnectionError
from signal import signal, SIGINT
from desktop_notifier import DesktopNotifier
from contextlib import suppress
from pathlib    import Path
from notifypy import Notify
import sys





class Amil:
    """
    KekikTaban : @KekikAkademi Projelerinin Standart Terminal Tabanı.

    Kullanım
    ----------
        taban = KekikTaban(
            baslik   = "@KekikAkademi Userbot",
            aciklama = "kekikUserbot Başlatıldı..",
            banner   = "kekikUserbot",
            girinti  = 1
        )

    Methodlar
    ----------
        taban.konsol:
            Rich Konsol

        taban.logo_yazdir():
            Konsolu Temizler ve İstenilen Renkte Logoyu Yazdırır..

        taban.bilgi_yazdir():
            Üst Bilgiyi Yazdırır..

        taban.log_salla(sol:str, orta:str, sag:str):
            Sol orta ve sağ şeklinde ekranda hizalanmış tek satır log verir..

        taban.hata_salla(hata:Exception):
            Yakalanan Exception'ı ekranda gösterir..
    """

    def __repr__(self) -> str:
        return f"{__class__.__name__} Sınıfı -- @KekikAkademi projelerinde standart terminal tabanı olması amacıyla kodlanmıştır.."

    konsol: Console = Console(log_path=False, highlight=False)

    try:
        kullanici_adi = os.getlogin()
    except OSError:
        import pwd

        kullanici_adi = pwd.getpwuid(os.geteuid())[0]

    bilgisayar_adi = platform.node()
    oturum = kullanici_adi + "@" + bilgisayar_adi  # Örn.: "kekik@Administrator"

    isletim_sistemi = platform.system()
    bellenim_surumu = platform.release()
    cihaz = isletim_sistemi + " | " + bellenim_surumu  # Örn.: "Windows | 10"

    tarih = datetime.datetime.now(pytz.timezone("Turkey")).strftime("%d-%m-%Y")
    saat = datetime.datetime.now(pytz.timezone("Turkey")).strftime("%H:%M")
    zaman = tarih + " | " + saat

    try:
        global_ip = requests.get("http://ip-api.com/json").json()["query"]
    except ConnectionError:
        global_ip = requests.get("https://api.ipify.org").text

    ust_bilgi = f"[bright_red]{cihaz}[/]\t\t[bright_yellow]{zaman}[/]\n\n"
    ust_bilgi += f"[turquoise2]{oturum}[/]\n"
    ust_bilgi += f"[yellow2]{global_ip}[/]\n"

    def __init__(
        self,
        baslik: str,
        aciklama: str,
        banner: str,
        genislik: int = 70,
        girinti: int = 0,
        stil: str = "stop",
        bildirim: bool = False,
    ) -> None:
        "Varsayılan Olarak; konsolu temizler, logoyu ve üst bilgiyi yazdırır.."

        self.genislik = genislik
        self.pencere_basligi = baslik
        self.bildirim_metni = aciklama
        self.logo = Figlet(font=stil).renderText(f"{' ' * girinti}{banner}")

        self.temizle

        if bildirim:
            self.bildirim

        self.konsol.print(self.logo, width=genislik, style="green")
        self.konsol.print(self.ust_bilgi, width=genislik, justify="center")
        
        self.son_versiyon()
        signal(SIGINT, self.sinyal_yakala)
        sys.excepthook = self.hata_yakala

    def logo_yazdir(self, renk: str = "turquoise2") -> None:
        "Konsolu Temizler ve İstenilen Renkte Logoyu Yazdırır.."

        self.temizle
        self.konsol.print(self.logo, width=self.genislik, style=renk)

    def bildirim_gonder(self,programAdi:str,bildirimMetni:str) -> None:
        bildirimci = Notify()
        bildirimci.title = programAdi
        bildirimci.message = bildirimMetni
        bildirimci.send()
    def bilgi_yazdir(self):
        "Üst Bilgiyi Yazdırır.."

        self.konsol.print(self.ust_bilgi, width=self.genislik, justify="center")

    def log_salla(self, sol: str, orta: str, sag: str) -> None:
        "Sol orta ve sağ şeklinde ekranda hizalanmış tek satır log verir.."

        sol = f"{sol[:13]}[bright_blue]~[/]" if len(sol) > 14 else sol
        orta = f"{orta[:19]}[bright_blue]~[/]" if len(orta) > 20 else orta
        sag = f"{sag[:14]}[bright_blue]~[/]" if len(sag) > 15 else sag
        bicimlendir = "[bold red]{:14}[/] [green]||[/] [yellow]{:20}[/] {:>2}[green]||[/] [magenta]{:^16}[/]".format(
            sol, orta, "", sag
        )
        self.konsol.log(bicimlendir)

    def hata_salla(self, hata: Exception) -> None:
        "Yakalanan Exception'ı ekranda gösterir.."

        bicimlendir = f"\t  [bold yellow2]{str(type(hata).__name__)}[/] [bold magenta]||[/] [bold grey74]{str(hata)}[/][bold deep_pink4]{str(hata.__traceback__.tb_frame.f_code.co_filename)}|{str(hata.__traceback__.tb_lineno)}[/]"
        self.konsol.print(f"{bicimlendir}", width=self.genislik, justify="center")

    def son_versiyon(self) -> None:
        os.system("git pull --rebase")

    def sinyal_yakala(self,signal, frame):
        self.cikis_yap()

    def bellek_temizle(self) -> None:
        with suppress(Exception):
            [alt_dizin.unlink() for alt_dizin in Path(".").rglob("*.py[coi]")]
            [alt_dizin.rmdir()  for alt_dizin in Path(".").rglob("__pycache__")]
            [rmtree(alt_dizin)  for alt_dizin in Path(".").rglob("*.build")]
            [alt_dizin.unlink() for alt_dizin in Path(".").rglob("*.bak")]
    def cikis_yap(self,_print=True):
        if _print:
            self.konsol.print("\n\n")
            self.konsol.log("[bold purple]Çıkış Yapıldı..")
        self.bellek_temizle()
        exit()

    # programdaki tüm hataları yakala ve ekrana yazdır
    def hata_yakala(self, exctype, value, traceback) -> None:
        "Programdaki Tüm Hataları Yakalar ve Ekrana Yazdırır.."
        self.hata_salla(value)
    @property
    def temizle(self) -> None:
        if self.isletim_sistemi == "Windows":
            os.system("cls")
        else:
            os.system("clear")

    @property
    def win_baslik(self) -> None:
        if self.isletim_sistemi == "Windows":
            try:
                import ctypes
            except ModuleNotFoundError:
                os.system("pip install ctypes")
                import ctypes

            ctypes.windll.kernel32.SetConsoleTitleW(f"{self.pencere_basligi}")

    @property
    def bildirim(self) -> None:
        if platform.machine() == "aarch64":
            return
        elif self.kullanici_adi == "gitpod":
            return
        elif self.bellenim_surumu.split("-")[-1] == "aws":
            return
        bildirimci = Notify()
        bildirimci.title = self.pencere_basligi
        bildirimci.message = self.bildirim_metni
        bildirimci.send()

    def bilgi_yazdircik(self, yazi: str) -> None:
        self.konsol.print(yazi, style="blue")

    def basarili_is(self, yazi: str) -> None:
        self.konsol.print(f"✅{yazi}", style="bold green", width=70, justify="center")

    def onemli_yazdir(self, yazi: str) -> None:
        self.konsol.print(yazi, style="bold cyan")
