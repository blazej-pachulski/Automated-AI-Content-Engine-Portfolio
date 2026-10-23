import textwrap
from PIL import Image, ImageDraw, ImageFont

wymiary = (1080, 1920)
tlo_jasnorozowe = "#FFD1DC"
tekst_czekoladowy = "#4A2511"

hasla = [
    "becoming HER is easy with us",
    "everyone knows HER",
    "Twój mindset to Twój największy zasób, dlatego każdego dnia pracuj nad swoją wizją i nie pozwól, aby ktokolwiek zakłócił Twój spokój."
]

try:
    czcionka = ImageFont.truetype("arial.ttf", 80)
except IOError:
    czcionka = ImageFont.load_default()

for indeks, tresc in enumerate(hasla, start=1):
    obraz = Image.new("RGB", wymiary, color=tlo_jasnorozowe)
    rysuj = ImageDraw.Draw(obraz)
    
    # Łamanie tekstu co 22 znaki
    zawiniety_tekst = textwrap.fill(tresc, width=22)
    
    # Rysowanie wyśrodkowanego tekstu (anchor="mm" oraz align="center")
    rysuj.text((540, 960), zawiniety_tekst, font=czcionka, fill=tekst_czekoladowy, anchor="mm", align="center")
    
    nazwa_pliku = f"karuzela_slajd_{indeks}.png"
    obraz.save(nazwa_pliku)
    print(f"Gotowe: {nazwa_pliku}")