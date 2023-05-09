# Bu araç @keyiflerolsun tarafından | @KekikAkademi için yazılmıştır.

from .core    import konsol, Lugatim
from argparse import ArgumentParser

argumanlar = ArgumentParser()
argumanlar.add_argument(
    "kelime",
    type    = str,
    nargs   = "*",
    help    = "«Arama Yapılacak Kelime veya Kelime Grubu»",
)
argumanlar.add_argument(
    "-t",
    "--tum",
    action  = "store_true",
    default = False,
    help    = "Tüm olası sonuçları göster",
)


def basla():
    args = argumanlar.parse_args()

    arama_metni = " ".join(args.kelime)
    lugat = Lugatim()
    if not arama_metni:
        return konsol.print("[bold red]Lütfen Kelime veya Kelime Grubu Girin..")

    lugat.tablo(arama_metni, args.tum)