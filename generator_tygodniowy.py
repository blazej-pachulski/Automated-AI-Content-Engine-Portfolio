import os
import textwrap
from dotenv import load_dotenv
from openai import OpenAI
from PIL import Image, ImageDraw, ImageFont

load_dotenv()
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

# Przygotowanie zasobów wizualnych
try:
    czcionka_glowna = ImageFont.truetype("arial.ttf", 80)
    czcionka_marki = ImageFont.truetype("arial.ttf", 40)
except IOError:
    czcionka_glowna = czcionka_marki = ImageFont.load_default()

try:
    logo = Image.open("logo.png").convert("RGBA")
    proporcja = 150 / float(logo.size[0])
    nowa_wys = int((float(logo.size[1]) * float(proporcja)))
    logo = logo.resize((150, nowa_wys))
except FileNotFoundError:
    logo = None

# Tworzenie głównego folderu
glowny_folder = "Paczka_Tygodniowa"
os.makedirs(glowny_folder, exist_ok=True)
liczba_dni = 7

print(f"Rozpoczynam generowanie materiałów na {liczba_dni} dni...")

# Pętla generująca materiały na każdy dzień
for dzien in range(1, liczba_dni + 1):
    folder_dnia = os.path.join(glowny_folder, f"Dzien_{dzien}")
    os.makedirs(folder_dnia, exist_ok=True)
    print(f"Tworzenie pakietu: Dzień {dzien}...")

    # Pobieranie tekstów od OpenAI
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Podaj 3 krótkie angielskie hasła motywacyjne i 1 polski opis pod wideo z hashtagami. Rozdziel wszystko znakiem |. Przykład: Hasło 1 | Hasło 2 | Hasło 3 | Gotowy opis i #hashtagi"}
        ]
    )
    
    fragmenty = response.choices[0].message.content.split('|')
    hasla = [tekst.strip() for tekst in fragmenty[:3]]
    opis = fragmenty[3].strip() if len(fragmenty) > 3 else "Brak opisu"

    # Zapis opisu w folderze dziennym
    sciezka_opisu = os.path.join(folder_dnia, "gotowy_opis.txt")
    with open(sciezka_opisu, "w", encoding="utf-8") as plik:
        plik.write(opis)

    # Generowanie 3 slajdów na dany dzień
    for indeks, tresc in enumerate(hasla, start=1):
        obraz = Image.new("RGB", (1080, 1920), color="#FFD1DC")
        rysuj = ImageDraw.Draw(obraz)
        
        zawiniety_tekst = textwrap.fill(tresc, width=22)
        rysuj.text((540, 960), zawiniety_tekst, font=czcionka_glowna, fill="#4A2511", anchor="mm", align="center")
        
        if logo:
            poz_x = int((1080 - logo.width) / 2)
            obraz.paste(logo, (poz_x, 1620), mask=logo)
            
        rysuj.text((540, 1820), "@shemanifestsdesires", font=czcionka_marki, fill="#4A2511", anchor="mm")
        
        sciezka_grafiki = os.path.join(folder_dnia, f"slajd_{indeks}.png")
        obraz.save(sciezka_grafiki)

print("\nSukces! Pełna paczka tygodniowa jest gotowa.")