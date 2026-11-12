from pathlib import Path
import csv


MAANEDER = [ #loiste med måneder 
    "Januar", "Februar", "Mars", "April", "Mai", "Juni",
    "Juli", "August", "September", "Oktober", "November", "Desember"
]


def parse_tall(verdi):#oppretter funksjon
    if verdi is None:
        return None
    tekst = verdi.strip()
    if tekst in ("", "-", "—", "–", "NA", "N/A"): 
        return None
    tekst = tekst.replace(" ", "").replace(".", "").replace(",", ".")
    try:
        return float(tekst)#teskt om til desimalall
    except ValueError:
        return None


def median(verdi_liste):
    sortert = sorted(verdi_liste)#sorter minst til størst
    n = len(sortert) #hvor mange elemter i listen
    if n % 2 == 1: #sjekker om antall elemter er oddetall, hvis ja returner midterste element
        return sortert[n // 2]#hvsi oddetall returner midterste element
    return (sortert[n // 2 - 1] + sortert[n // 2]) / 2 #hvis partall returner gjennomsnittet av de to midterste elementene


def les_vind_data(csv_path):#lager funksjon for å hente vindmålinger
    maaned_data = {m: [] for m in range(1, 13)} # ein måned om til en liste med 12 elementer, en for hver måned

    with csv_path.open("r", encoding="utf-8", newline="") as fil: #åpner csv filen og leser den, 
        leser = csv.DictReader(fil, delimiter=";") #oppretter en leserekke for å lese csv-filen
        for rad in leser:
            dato = rad.get("Tid(norsk normaltid)") # rad.get henter verdien for nøkkelen "Tid(norsk normaltid)" fra raden i csv-filen
            vind = rad.get("Høyeste middelvind (døgn)")
            if dato is None or vind is None:
                continue

            dato = dato.strip()
            if dato == "": # sjekker om verdien er tom, hvis ja hopper over denne raden
                continue

            deler = dato.split(".") #deler datoen i tre deler basert på punktum, for eksempel "01.01.2020" blir til ["01", "01", "2020"]
            if len(deler) != 3:
                continue

            try:
                maaned = int(deler[1]) #henter måneden fra datoen, som er den andre delen av listen (indeks 1), og konverterer den til et heltall
            except ValueError:
                continue

            verdi = parse_tall(vind) #kaller parse_tall funksjonen for å konvertere vindverdien til et tall, hvis det er mulig
            if verdi is not None:
                maaned_data[maaned].append(verdi) #legger til verdien i listen for den aktuelle måneden i maaned_data dictionaryen

    return maaned_data


def skriv_statistikk(csv_path):
    maaned_data = les_vind_data(csv_path) #kaller les_vind_data funksjonen for å hente vinddataene fra csv-filen og lagrer resultatet i maaned_data

    print(f"\nVindstyrke for {csv_path.stem.replace('_med_makstemperatur', '').replace('_', ' ').title()}\n")
    print(f"{'Måned':<10} {'Min':>8} {'Median':>12} {'Maks':>10}")
    print("-" * 46) # 

    for maaned in range(1, 13): 
        verdier = maaned_data[maaned]
        if not verdier:
            print(f"{MAANEDER[maaned - 1]:<10} {'-':>8} {'-':>12} {'-':>10}")
            continue

        min_verdi = min(verdier)
        med_verdi = median(verdier)
        maks_verdi = max(verdier)

        print(f"{MAANEDER[maaned - 1]:<10} {min_verdi:>8.1f} {med_verdi:>12.1f} {maks_verdi:>10.1f}")


def main():
    katalog = Path(__file__).resolve().parent
    csv_filer = sorted(katalog.glob("*_med_makstemperatur.csv"))

    if not csv_filer:
        print("Fant ingen CSV-filer i denne mappen.")
        return

    print("Velg en værstasjon:")
    for i, fil in enumerate(csv_filer, start=1):
        navn = fil.stem.replace("_med_makstemperatur", "").replace("_", " ").title()
        print(f"{i}. {navn}") # f gjør det mulig å sette inn variabler, i setter inn nummeret på stasjonen og navnet på stasjonen i listen som skrives ut til brukeren

    valg = int(input("Skriv inn nummeret på stasjonen: "))

    if valg < 1 or valg > len(csv_filer):
        print("Ugyldig valg.")
        return

    valgt_fil = csv_filer[valg - 1] 
    skriv_statistikk(valgt_fil) #funkjsonen vi laget tidligere


if __name__ == "__main__":
    main()
