import pandas as pd
from conn import HeroeRepo, Heroe


def importar_heroes_csv(ruta_csv="heroes_import.csv"):
    df = pd.read_csv(ruta_csv)
    repo = HeroeRepo()
    for _, fila in df.iterrows():
        repo.create(Heroe(
            nombre=fila["nombre"],
            nivel=int(fila["nivel"]),
            clase=fila["clase"],
            raza=fila["raza"],
            id=None
        ))
    print(f"Se importaron {len(df)} héroes desde {ruta_csv}.")


if __name__ == "__main__":
    importar_heroes_csv()
