import matplotlib.pyplot as plt

filnavn = [
    "øvingsoppgave 10/oslo_blindern_1954_2025_med_makstemperatur.csv",
    "øvingsoppgave 10/roeros_1954_2025_med_makstemperatur.csv",
    "øvingsoppgave 10/tromsoe_1954_2025_med_makstemperatur.csv",
    "øvingsoppgave 10/vaernes_1954_2025_med_makstemperatur.csv",
    "øvingsoppgave 10/venabu_1954_2025_med_makstemperatur.csv"
]

# Dictionary for å lagre temperaturdata
temperatur_data = {}

for filnavn in filnavn:
    with open(filnavn, "r", encoding="UTF-8") as fil:
        fil.readline()  # Hopper over overskriften

        for linje in fil:
            kolonner = linje.strip().split(";")

            # Henter informasjon fra filen
            stasjon = kolonner[0]
            dato = kolonner[2]
            temperatur = kolonner[4]

            # Finner årstallet fra datoen
            deler = dato.split(".")
            if len(deler) != 3:
                continue

            år = deler[2]

            # Hopper over manglende temperaturdata
            if temperatur == "-":
                continue

            temperatur = float(temperatur.replace(",", "."))

            # Oppretter dictionary for stasjonen hvis den ikke finnes
            if stasjon not in temperatur_data:
                temperatur_data[stasjon] = {}

            # Oppretter dictionary for året hvis det ikke finnes
            if år not in temperatur_data[stasjon]:
                temperatur_data[stasjon][år] = [0, 0]

            # Legger til temperatur og øker antall dager
            temperatur_data[stasjon][år][0] += temperatur
            temperatur_data[stasjon][år][1] += 1


# Plotter temperaturene
for stasjon in temperatur_data:
    årstall = []
    gjennomsnitt = []

    for år in sorted(temperatur_data[stasjon]):
        sum_temperatur = temperatur_data[stasjon][år][0]
        antall_dager = temperatur_data[stasjon][år][1]

        # Krever minst 300 dager med temperaturdata
        if antall_dager >= 300:
            årstall.append(int(år))
            gjennomsnitt.append(sum_temperatur / antall_dager)

    plt.plot(årstall, gjennomsnitt, marker="o", label=stasjon)


plt.xlabel("År")
plt.ylabel("Gjennomsnittstemperatur (°C)")
plt.title("Gjennomsnittstemperatur per år for hver værstasjon")
plt.legend()
plt.grid()
plt.show()
