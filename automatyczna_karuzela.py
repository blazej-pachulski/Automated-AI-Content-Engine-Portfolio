import os
import textwrap
from dotenv import load_dotenv
from openai import OpenAI
from PIL import Image, ImageDraw, ImageFont

load_dotenv()
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

print("Pobieranie danych z OpenAI...")
response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": "Podaj 3 krótkie angielskie hasła motywacyjne i 1 polski opis pod wideo z hashtagami. Rozdziel wszystko znakiem |. Przykład: Hasło 1 | Hasło 2 | Hasło 3 | Gotowy opis i #hashtagi"}
    ]
)

fragmenty = response.choices[0].message.content.split('|')
hasla = [tekst.strip() for tekst in fragmenty[:3]]
opis = fragmenty[3].strip() if len(fragmenty) > 3 else "Brak opisu"

# Zapis opisu do pliku
with open("gotowy_opis.txt", "w", encoding="utf-8") as plik:
    plik.write(opis)
print("Zapisano: gotowy_opis.txt")

try:
    czcionka_glowna = ImageFont.truetype("arial.ttf", 80)
    czcionka_marki = ImageFont.truetype("arial.ttf", 40)
except IOError:
    czcionka_glowna = czcionka_marki = ImageFont.load_default()

print("Tworzenie obrandowanych slajdów...")
for indeks, tresc in enumerate(hasla, start=1):
    obraz = Image.new("RGB", (1080, 1920), color="#FFD1DC")
    rysuj = ImageDraw.Draw(obraz)
    
    # Rysowanie haseł i znaku wodnego
    zawiniety_tekst = textwrap.fill(tresc, width=22)
    rysuj.text((540, 960), zawiniety_tekst, font=czcionka_glowna, fill="#4A2511", anchor="mm", align="center")
    rysuj.text((540, 1820), "@shemanifestsdesires", font=czcionka_marki, fill="#4A2511", anchor="mm")
    
    nazwa = f"ai_karuzela_slajd_{indeks}.png"
    obraz.save(nazwa)
    print(f"Zapisano: {nazwa}")