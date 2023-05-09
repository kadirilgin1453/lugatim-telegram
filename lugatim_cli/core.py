# Bu araç @keyiflerolsun tarafından | @KekikAkademi için yazılmıştır.

from Kekik.cli    import konsol
from httpx        import Client as Session
from httpx        import Timeout
from urllib.parse import quote
from parsel       import Selector
from pydantic     import BaseModel, validator
from rich.table   import Table
from rich         import box

class KelimeHatasi(Exception):
    pass

class SozlukAnlam(BaseModel):
    kelime : str
    anlam  : str

    @validator("kelime")
    def kelime_uzunlugu(cls, deger):
        if len(deger) < 1:
            raise KelimeHatasi("Kelime 1 karakterden kısa olamaz..")
        else:
            return deger

class Lugatim:
    def __init__(self):
        self.oturum = Session(
            headers = {
                "User-Agent" : "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36"
            },
            timeout = Timeout(10, connect=10, read=5*60, write=10)
        )
        self.url = "http://lugatim.com"
        self.oturum.get(self.url)

    def arama_yap(self, kelime:str) -> list(SozlukAnlam):
        istek  = self.oturum.get(f"{self.url}/s/{quote(kelime)}")
        secici = Selector(istek.text)

        return [
            SozlukAnlam(
                kelime = sonuc.xpath("normalize-space(./h3/text())").get(),
                anlam  = "\n".join([
                    Selector(veri).xpath("normalize-space(.)").get()
                        for veri in sonuc.xpath(".//p[@class='quota']").get().split("<br>")
                ]),
            )
                for sonuc in secici.xpath("//div[@id='sonuc-left']/div[@class='search-results-div']")
        ]

    def tablo(self, kelime:str, tum_sonuclar:bool=False):
        for sonuc in self.arama_yap(kelime):
            konsol.print()

            tablo = Table(
                title = f"[link={self.url}/s/{quote(sonuc.kelime)}]{sonuc.kelime} » Kubbealtı Lugatı[/link]",
                box   = box.SQUARE
            )
            tablo.add_column(sonuc.kelime)
            tablo.add_row(sonuc.anlam)
            konsol.print(tablo)

            if not tum_sonuclar:
                break

            konsol.print()