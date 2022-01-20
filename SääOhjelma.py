# ohjelmalla voi hakea paikkakuntien säät, jos antaa väärän nimen paikkakunnalle ohjelma kaatuu siihen
# värillisin tulosteitesiin: pip install termcolor

import sqlite3
import requests #### Requests kirjastolla http pyynnöt on näppärämpiä Tee pip install requests -komento!
from datetime import datetime
from termcolor import colored

# Funktio joka kirjoittaa lokia
def kirjoita_lokia(parametri):
    aikaleima = datetime.now().strftime('%d.%m.%Y klo %H.%M:%S')
   
    tiedosto = open("lampo_loki.txt", "a")
    rivi = str(aikaleima) + " " + parametri
   
    tiedosto.write(rivi + "\r")
    tiedosto.close()

paikkakunta = ""

print(colored("Säähakusovellus käynnistyy...", "green"))
print()
print(colored('Haluatko vaihtaa haettavia paikkakuntia?', "yellow"))
syöte = input("Vastaa kyllä antamalla K tai ei antamalla X : ")

if syöte.upper() == "K":
    
    conn = sqlite3.connect('Kunnat.db')
    print()
    print("Kunnat tietokantaan yhdistetty.")
    sql2 = """DROP TABLE IF EXISTS Paikkakunnat"""
    kursori = conn.cursor()
    kursori.execute(sql2)
    sql = """CREATE TABLE IF NOT EXISTS Paikkakunnat(
        paikkakunta text)"""
    print()    
    print("Lisätään uusi Paikkakunnat taulu tietokantaan.")    
    kursori = conn.cursor()
    kursori.execute(sql)
    print()
    print("Taulu lisätty tietokantaan.")
    print()

    while paikkakunta.upper() != "X":
        paikkakunta = input("Anna paikkakunta (x lopettaa!) : ")
        if paikkakunta.upper() != "X": 
            sql = f'INSERT INTO Paikkakunnat VALUES ("{paikkakunta}")'
            kursori.execute(sql)
            conn.commit()
            print("Paikkakunta tallennettu.")
            print()
        else:
            continue
            
elif syöte.upper() == "X":
    print("Seuraava kysymys.")
    print()
else:
    print("Annoit väärän vastauksen.")

print(colored("Haluatko hakea lämpötilatiedon ilmatieteenlaitokselta? K (=kyllä) tai X (=ei)", "yellow"))
syöte2 = input("Mikä on vastauksesi? ")
print()

if syöte2.upper() == "K":
    conn = sqlite3.connect('Kunnat.db')
    kursori = conn.cursor()
    print(colored("Tässä tulokset paikkakuntien lämpötiloista!", "green"))
    sql = "SELECT paikkakunta FROM Paikkakunnat"
    for rivi in kursori.execute(sql):
        
        paikkakuntaStr = str(rivi)

        paikkakunta = paikkakuntaStr[2:-3]      
        url = f"https://www.ilmatieteenlaitos.fi/saa/{paikkakunta}"
               
        vastaus = requests.get(url, params={"encoding": "utf-8"})
        vastauksen_status = vastaus.status_code
        laskuri = 0
        if vastauksen_status == 200:
            html = str(vastaus.text)
            indeksi = html.index('Temperature') # Tämä teksti etsitään html sisällöstä
            alku = indeksi + 12 # Tämän verran Temperature sanan alusta niin alkaa lukema
            loppu = alku + 4 # Tässä lukema päättyy
            html2 = html[alku:loppu]
            print(f"Lämpötila {paikkakunta} on {html2}")
            laskuri += 1
            kirjoita_lokia(f"Löydettiin {laskuri} tulosta.")

        elif vastauksen_status == 500:
            kirjoita_lokia(f"{paikkakunta} Hakuvirhe")
        else:
            print("Odottamaton virhe. Ohjelman suoritus päättyy.")
               
        print("Valmis!")
    conn.close()   

elif syöte2.upper() == "X":
    print("Kiitos ja näkemiin!")
    
else:
    print("Vastausmuoto oli virheellinen.")
        
print()
print(colored("Ohjelma päättyy", "cyan"))

