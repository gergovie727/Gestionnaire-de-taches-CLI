import json
import erreur
import colorama
import datetime

class ToDoList:
    """
    La classe gérant le gestionnaire de tâches.

    Variables de Classe:
        None
        
    Variable d'Instance:
        __taches (dict): Contient les tâches en cours
        __nom_fichier (str): Contient le nom du fichier json où stocker les tâches.
        __num_menu (int): Contient là où en est l'utilisateur dans ses actions.

    Methodes de Classe:
        None
        
    Methodes d'Instance:
        __init__(self, nom_fichier:str) -> None: L'initialisation de la classe.
        __verifier_fichier(self, nom_fichier: str) -> bool: Vérifie si le fichier fourni est bien un fichier json bien formé. Renvoie True s'il l'est ou si le fichier n'existe pas. Renvoie False sinon.
        menu(self) -> None: Permet la sélection de la fonction à utiliser en fonction de __num_menu.
        __ecran_de_selection(self) -> None: Affiche l'écran de sélection des menus.
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
        Fonction permettant de vérifier si le fichier fourni est un fichier json valide.
        
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

            else:
                print("Merci d'avoir utilisé ce programme. A bientôt !")
                exit(0)


        
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

    def __sauvegarde(self) -> None:
        """
        Fonction permettant la sauvegarde des données dans le fichier json.

        Paramètres:
            None

        Retourne: None
        """

        with open(self.__nom_fichier, 'w') as fichier:
            self.__taches = dict(sorted(self.__taches.items(), key=lambda item: (item[1]["status"], self.__get_iso_date(item[1]["date"]))))
            fichier.write(json.dumps(self.__taches, indent=1, ensure_ascii=False))

    def __get_iso_date(self, date: str) -> datetime.date:
        """
        Fonction permettant de retourner la date au standard iso à partir de la date en français.
        
        Paramètres:
            date (str): La date en français.

        Retourne: x(datetime.date) la date en format iso.
        """

        iso_date = date.split('/')
        iso_date = f"{iso_date[2]}-{iso_date[1]}-{iso_date[0]}"
        return datetime.date.fromisoformat(iso_date)


 
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
            date_tache = self.__get_iso_date(date)

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

            tache = input("Veuillez entrer la tache (menu pour revenir au menu): ")

            if tache == "menu":
                self.__num_menu = 0
                return

            if tache in self.__taches:
                print("\nErreur, cette tâche existe déjà.")
                continue

            date = input("\nVeuillez rentrer la date sous la forme JJ/MM/AAAA: ")

            try:
                self.__get_iso_date(date)
            except:
                print("\nErreur, la date entrée est invalide.")
                continue

            self.__taches[tache]={"date": date, "status": 0}
            self.__num_menu = 0
            break

        self.__sauvegarde()

    def __terminer_tache(self):
        """
        Fonction permettant de déclarer une tâche comme étant terminée.

        Paramètres:
            None

        Retourne: None
        """

        while True:

            tache = input("Veuillez rentrer la tâche a terminer (menu pour revenir au menu): ")

            if tache == "menu":
                self.__num_menu = 0
                return

            if not tache in self.__taches:
                print("\nErreur: La tâche donnée n'existe pas.\n")
                continue

            self.__taches[tache]["status"] = 1
            self.__num_menu = 0
            break

        self.__sauvegarde()

    def __supprimer_une_tache(self) -> None:
        """
        Fonction permettant de supprimer une tâche

        Paramètres:
            None

        Retourne: None
        """

        while True:

            tache = input("Veuillez rentrer la tache à supprimer (menu pour revenir au menu): ")

            if tache == "menu":
                self.__num_menu = 0
                return

            if not tache in self.__taches:
                print("\nErreur: la tache donnée n'existe pas.\n")
                continue

            self.__taches.pop(tache)
            self.__num_menu = 0
            break

        self.__sauvegarde()