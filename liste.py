import json
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
        __sauvegarde(self) -> None: Permet de sauvegarder les tâches dans le fichier.
        __get_iso_date(self, date: str) -> datetime.date: Permet, à partir de la date en format JJ/MM/AAAA d'obtenir la date en format ISO.
        __visualiser_taches(self) -> None: Permet de visualiser les tâches.
        __ajouter_taches(self): Permet d'ajouter une tâche.
        __terminer_tache(self): Permet de marquer une tâche comme étant terminée.
        __supprimer_tache(self) -> None: Permet de supprimer une tâche.
    """

    def __init__(self, nom_fichier:str) -> None:

        self.__taches: dict = self.__verifier_fichier(nom_fichier)

        if self.__taches == {}:
            self.__nom_fichier: str = nom_fichier

        else:
            self.__nom_fichier: str = nom_fichier
            self.__taches = dict(sorted(self.__taches.items(), key=lambda item: (item[1]["status"], self.__get_iso_date(item[1]["date"]))))
            
        
        self.__num_menu: int = 0
        
        
    def __verifier_fichier(self, nom_fichier: str) -> dict:
        """
        Fonction permettant de vérifier si le fichier fourni est un fichier json valide.
        
        Paramètres:
            - nom_fichier (str): Le nom du fichier

        Retourne (int): 1 si le fichier fourni est un fichier json valide, 2 si le fichier n'existe pas, 0 sinon.
        
        """
        try:
            with open(nom_fichier, 'r') as fichier:
                return json.loads(fichier.read())
        except FileNotFoundError:
            return {}
        except Exception as e:  
            print("Erreur, le fichier donné n'est pas un fichier JSON valide.")
            exit(0)
        
    def menu(self) -> None:
        """
        Fonction permettant d'afficher le menu en fonction des selections de l'utilisateur
        
        Paramètres:
            None

        Retourne: None
        """

        actions = {
                0: self.__ecran_de_selection,
                1: self.__visualiser_taches,
                2: self.__ajouter_taches,
                3: self.__terminer_tache,
                4: self.__supprimer_tache,
                5: self.__quitter_programme
            }

        while True:
            actions[self.__num_menu]()


        
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


 
    def __visualiser_taches(self) -> None:
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
        
        for id,info in self.__taches.items():

            tache = info["tache"]
            date = info["date"]
            date_tache = self.__get_iso_date(date)

            if info["status"]:
                print(f"{colorama.Fore.GREEN}{tache} (ID: {id}) : {date} TERMINEE{colorama.Style.RESET_ALL}")

            elif date_tache > today:
                print(f"{colorama.Fore.LIGHTGREEN_EX}{tache} (ID: {id}) : {date}{colorama.Style.RESET_ALL}")
            elif date_tache == today:
                print(f"{colorama.Fore.YELLOW}{tache} (ID: {id}) : {date}{colorama.Style.RESET_ALL}")
            else:
                print(f"{colorama.Fore.RED}{tache} (ID: {id}) : {date}{colorama.Style.RESET_ALL}")

        input("\n")
        self.__num_menu = 0

    def __ajouter_taches(self):
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

            id = str(max([int(i) for i in self.__taches.keys()] or  [0]) + 1)

            date = input("\nVeuillez rentrer la date sous la forme JJ/MM/AAAA: ")

            try:
                self.__get_iso_date(date)
            except:
                print("\nErreur, la date entrée est invalide.")
                continue

            self.__taches[id]={"tache": tache, "date": date, "status": 0}
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

            id = input("Veuillez rentrer l'ID de la tâche a terminer (menu pour revenir au menu): ")

            if id == "menu":
                self.__num_menu = 0
                return

            if not id in self.__taches:
                print("\nErreur: La tâche donnée n'existe pas.\n")
                continue

            self.__taches[id]["status"] = 1
            self.__num_menu = 0
            break

        self.__sauvegarde()

    def __supprimer_tache(self) -> None:
        """
        Fonction permettant de supprimer une tâche

        Paramètres:
            None

        Retourne: None
        """

        while True:

            id = input("Veuillez rentrer l'ID de la tache à supprimer (menu pour revenir au menu): ")

            if id == "menu":
                self.__num_menu = 0
                return

            if not id in self.__taches:
                print("\nErreur: la tache donnée n'existe pas.\n")
                continue

            self.__taches.pop(id)
            self.__num_menu = 0
            break

        self.__sauvegarde()

    def __quitter_programme(self) -> None:
        """
        Fonction permettant de quitter le programme.
        
        Paramètre:
            None

        Retourne: None
        """

        print("Merci d'avoir utilisé ce programme. A bientôt !")
        exit(0)