import argparse
from liste import to_do_liste

parser = argparse.ArgumentParser(
    prog="Gestionnaire de tâches",
    usage="python3 main.py [fichier]",
    description="Un programme qui permet d'assister dans la gestion de tâches.\nCe programme permet de créer des tâches et de les marquer comme finies"
)

parser.add_argument('-f', '--fichier', type=str, help="Chemin absolu ou relatif du fichier json contenant la liste", default="liste.json")

args = parser.parse_args()

if __name__ == "__main__":

    liste = to_do_liste(args.fichier)

    liste.menu()