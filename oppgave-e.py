import pandas as pd
import matplotlib.pyplot as plt
import glob

# Leser alle CSV-filene
for fil in glob.glob("innlevering 10/*.csv"):

    df = pd.read_csv(fil, sep=";", decimal=",", na_values="-",
                     encoding="utf-8-sig")

    # Gjør datoene om til datoformat
    df["Dato"] = pd.to_datetime(
        df["Tid(norsk normaltid)"],
        format="%d.%m.%Y"
    )

    # Oktober til april
    df = df[df["Dato"].dt.month.isin([10, 11, 12, 1, 2, 3, 4])].copy()

    # Finner skisesongen
    df["Sesong"] = df["Dato"].dt.year
    df.loc[df["Dato"].dt.month < 10, "Sesong"] -= 1

    # Teller dager med snø
    df["Skiføre"] = df["Snødybde"] > 0

    resultat = df.groupby("Sesong").agg(
        skiføre=("Skiføre", "sum"),
        målinger=("Snødybde", "count")
    )

    # Beholder sesonger med minst halvparten av målingene
    resultat = resultat[resultat["målinger"] >= 106]

    # Lager diagram
    plt.plot(
        resultat.index,
        resultat["skiføre"],
        label=df["Navn"].iloc[0]
    )

plt.xlabel("Skisesong")
plt.ylabel("Antall dager med skiføre")
plt.title("Dager med skiføre per sesong")
plt.legend()
plt.grid()
plt.show()
