import sys
import os
import datetime
import googlemaps


apikey = "Add your API key here"


def datos_google(Direcciones: list, apikey: str, origen: str):
    gmaps = googlemaps.Client(key=apikey)
    matrix = gmaps.distance_matrix(
        origins=origen, destinations=Direcciones, mode="driving")
    return matrix


if len(sys.argv) == 2:
    if ".txt" in sys.argv[1]:
        if os.path.exists(sys.argv[1]):
            Info = {}
            Direcciones = []
            with open(sys.argv[1], encoding="utf-8") as file:
                rawdata = list(map(lambda x: x.strip("\n"), file.readlines()))
                data = rawdata[1:]
                origen = rawdata[0]+", Cali, Colombia"

                for i in range(0, len(data), 2):
                    Info[data[i+1]+", Cali, Colombia"] = data[i]
                    Direcciones.append(data[i+1]+", Cali, Colombia")

                file.close()

            x = datos_google(Direcciones, apikey, origen)
            num_destinos = len(Direcciones)
            elem = x["rows"][0]["elements"]
            matriz = {}

            for destino, valores in zip(Direcciones, elem):
                distancia = valores["duration"]["value"]
                matriz[destino] = distancia

            Direccionesord = Direcciones[:]
            destinos = []
            destinos.append(min(matriz, key=lambda x: matriz[x]))
            Direccionesord.remove(min(matriz, key=lambda x: matriz[x]))
            print("Procesando...")

            while len(destinos) < num_destinos:
                paso = destinos[-1]
                direccions = datos_google(Direccionesord, apikey, paso)
                new = direccions["rows"][0]["elements"]
                matriz = {}

                for destino, valores in zip(Direccionesord, new):
                    distancia = valores["duration"]["value"]
                    matriz[destino] = distancia

                rutaoptima = min(matriz, key=lambda x: matriz[x])
                destinos.append(rutaoptima)
                Direccionesord.remove(rutaoptima)

            print("Datos Obtenidos")

            archivo = "Entregas/entrega"+"_" + \
                str(datetime.date.today().strftime("%d-%m-%y"))+".txt"

            with open(archivo, mode="w+", encoding="utf-8") as file:
                for pos in range(len(destinos)):
                    file.write(
                        f"Entrega # {pos+1}, datos cliente: {Info[destinos[pos]]}, dirección: {destinos[pos]}\n")
                file.close()

            print("Información guardada exitosamente en "+archivo[9:])
