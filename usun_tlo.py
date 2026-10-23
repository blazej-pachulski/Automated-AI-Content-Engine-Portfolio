import requests

klucz_api = "bdUoWCKcc97haf1Rdn22P7bY"
plik_wejsciowy = "surowe_logo.png"
plik_wyjsciowy = "logo.png"

print("Wysyłanie grafiki do serwera...")
with open(plik_wejsciowy, 'rb') as plik:
    odpowiedz = requests.post(
        'https://api.remove.bg/v1.0/removebg',
        files={'image_file': plik},
        data={'size': 'auto'},
        headers={'X-Api-Key': klucz_api},
    )

if odpowiedz.status_code == requests.codes.ok:
    with open(plik_wyjsciowy, 'wb') as wyjscie:
        wyjscie.write(odpowiedz.content)
    print("Gotowe! Zapisano plik logo.png z przezroczystym tłem.")
else:
    print("Błąd API:", odpowiedz.status_code, odpowiedz.text)