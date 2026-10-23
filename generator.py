import os
import openai
from dotenv import load_dotenv

load_dotenv()
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

with open("baza_pomyslow.txt", "r", encoding="utf-8") as plik:
    tematy = plik.readlines()

for numer, temat in enumerate(tematy, 1):
    temat = temat.strip()
    if not temat:
        continue

    nazwa_folderu = f"Post_{numer}_{temat.replace(' ', '_')}"
    os.makedirs(nazwa_folderu, exist_ok=True)
    
    print(f"Tworzę teksty i prompty dla: {temat}...")
    
    instrukcja_systemowa = (
        "Jesteś ekspertką od manifestacji w estetyce IT GIRL. Dla podanego tematu stwórz:\n"
        "1. Scenariusz wideo i krótki opis z hasłem 'becoming HER is easy with us'.\n"
        "2. Prompt po angielsku dla Midjourney/DALL-E na minimalistyczną grafikę tytułową (pastel baby pink background, chocolate brown typography)."
    )
    
    odpowiedz = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": instrukcja_systemowa},
            {"role": "user", "content": temat}
        ]
    )
    
    sciezka_pliku = os.path.join(nazwa_folderu, "gotowy_pakiet.txt")
    with open(sciezka_pliku, "w", encoding="utf-8") as plik_wyjsciowy:
        plik_wyjsciowy.write(odpowiedz.choices[0].message.content)
        
print("Gotowe! Wygenerowano pakiety tekstowe wraz z promptami.")