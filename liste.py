import json
import erreur
import colorama
import datetime
import re

class to_do_liste:
    """
    La classe gérant le gestionnaire de tâches.

    Variables de Classe:
        None
        
    Variable d'Instance:
        None

    Methodes de Classe:
        None

    Methodes d'Instance:
        None
    """

    def __init__(self, nom_fichier:str) -> None:

        self.__taches: dict = {}

        if self.__verifier_fichier(nom_fichier):
            self.__nom_fichier: str = nom_fichier
            self.__taches = dict(sorted(self.__taches.items(), key=lambda item: (item[1]["status"], item[1]["date"])))
        else:
            raise erreur.FichierError("Le fichier fourni n'est pas un fichier json")
        
        self.__num_menu: int = 0
        
        
    def __verifier_fichier(self, nom_fichier: str) -> bool:
        """
        Fonction privée permettant de vérifier si le fichier fourni est un fichier json valide. Si le fichier n'existe pas, il est créé.
        
        Paramètres:
            - nom_fichier (str): Le nom du fichier

        Retourne (bool): True si le fichier fourni est un fichier json valide, False sinon.
        
        """
        try:
            with open(nom_fichier, 'r') as fichier:
                self.__taches: dict = json.loads(fichier.read())
                return True
        except FileNotFoundError:
            return True
        except Exception as e:  
            return False
        
    def menu(self) -> None:
        """
        Fonction permettant d'afficher le menu en fonction des selections de l'utilisateur
        
        Paramètres:
            None

        Retourne: None
        """

        while True:
            
            if self.__num_menu == 0:
                self.__ecran_de_selection()
                continue

            if self.__num_menu == 1:
                self.__visualisation_des_taches()
                continue

            if self.__num_menu == 2:
                self.__ajout_des_taches()
                continue

            if self.__num_menu == 3:
                self.__terminer_tache()
                continue

            if self.__num_menu == 4:
                self.__supprimer_une_tache()
                continue
        
    def __ecran_de_selection(self) -> None:
        """
        Fonction permettant d'écrire le message de bienvenue et la sélection du choix de l'utilisateur.
        
        Paramètres:
            None

        Retourne: None
        """

        while True:
            print("MENU PRINCIPAL\n")
            print("1. Voir les tâches")
            print("2. Ajouter une tâche")
            print("3. Terminer une tâche")
            print("4. Supprimer une tâche")
            str_num_menu: str = input("5. Quitter\n\n")
            print("\n")

            try:
                self.__num_menu = int(str_num_menu)
                if self.__num_menu not in (1,2,3,4,5):
                    raise ValueError
                break
            except Exception:
                print("\n\nErreur, veuillez fournir une valeur entre 1 et 5.\n\n")
                pass

    def __visualisation_des_taches(self) -> None:
        """
        Fonction permettant à l'utilisateur de visualiser les tâches qu'il a en cours et celles qu'il a terminé.

        Paramètres:
            None

        Retourne: None
        """

        if self.__taches == {}:
            print("\nAucune tâche enregistrée pour le moment.\n")
            input()
            self.__num_menu = 0
            return
        
        today = datetime.date.today()
        
        for tache,info in self.__taches.items():
            date = info["date"]
            iso_date = date.split('/')
            iso_date = f"{iso_date[2]}-{iso_date[1]}-{iso_date[0]}"
            
            try:
                date_tache = datetime.date.fromisoformat(iso_date)
            except ValueError:
                print(f"\nLa tache \"{tache}\" a une date invalide: {date}.")
                print("Suppression de la tache.")
                self.__taches.pop(tache)
                self.__num_menu = 0
                with open(self.__nom_fichier, 'w') as fichier:
                    fichier.write(json.dumps(self.__taches, indent=1, ensure_ascii=False))
                return

            if info["status"]:
                print(f"{colorama.Fore.GREEN}{tache} : {date} TERMINEE{colorama.Style.RESET_ALL}")

            elif date_tache > today:
                print(f"{colorama.Fore.LIGHTGREEN_EX}{tache} : {date}{colorama.Style.RESET_ALL}")
            elif date_tache == today:
                print(f"{colorama.Fore.YELLOW}{tache} : {date}{colorama.Style.RESET_ALL}")
            else:
                print(f"{colorama.Fore.RED}{tache} : {date}{colorama.Style.RESET_ALL}")

        input("\n")
        self.__num_menu = 0

    def __ajout_des_taches(self):
        """
        Fonction permettant à l'utilisateur d'ajouter des tâches à sa liste.

        Paramètres:
            None

        Retourne: None
        """

        while True:

            tache = input("Veuillez entrer la tache: ")
            if tache in self.__taches:
                print("\nErreur, cette tâche existe déjà.")
                continue

            date = input("\nVeuillez rentrer la date sous la forme JJ/MM/AAAA: ")
            if not re.fullmatch(r"([0-2][0-9]|3[01])\/(0[1-9]|1[0-2])\/[0-9]{4}", date.strip()):
                print("\nErreur, la date entrée est invalide.")
                continue
            else:
                self.__taches[tache]={"date": date, "status": 0}
                self.__taches = dict(sorted(self.__taches.items(), key=lambda item: (item[1]["status"], item[1]["date"])))
                self.__num_menu = 0
                break

        with open(self.__nom_fichier, 'w') as fichier:
            fichier.write(json.dumps(self.__taches, indent=1, ensure_ascii=False))

    def __terminer_tache(self):
        """
        Fonction permettant de déclarer une tâche comme étant terminée.

        Paramètres:
            None

        Retourne: None
        """

        while True:

            tache = input("Veuillez rentrer la tâche a terminer: ")

            if not tache in self.__taches:
                print("\nErreur: La tâche donnée n'existe pas.\n")
                continue

            self.__taches[tache]["status"] = 1
            self.__taches = dict(sorted(self.__taches.items(), key=lambda item: (item[1]["status"], item[1]["date"])))
            self.__num_menu = 0
            break

        with open(self.__nom_fichier, 'w') as fichier:
            fichier.write(json.dumps(self.__taches, indent=1, ensure_ascii=False))

    def __supprimer_une_tache(self):
        """
        Fonction permettant de supprimer une tâche

        Paramètres:
            None

        Retourne: None
        """

        while True:

            tache = input("Veuillez rentrer la tache à supprimer: ")

            if not tache in self.__taches:
                print("\nErreur: la tache donnée n'existe pas.\n")
                continue

            self.__taches.pop(tache)
            self.__taches = dict(sorted(self.__taches.items(), key=lambda item: (item[1]["status"], item[1]["date"])))
            self.__num_menu = 0
            break

        with open(self.__nom_fichier, 'w') as fichier:
            fichier.write(json.dumps(self.__taches, indent=1, ensure_ascii=False))