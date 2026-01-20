import json
import erreur

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

        if self.__verifier_fichier(nom_fichier):
            self.nom_fichier = nom_fichier
        else:
            raise erreur.FichierError("Le fichier fourni n'est pas un fichier json")
        
        self.__num_menu = 0

        self.__taches = {}
        
        
    def __verifier_fichier(self, nom_fichier: str) -> bool:
        """
        Fonction privée permettant de vérifier si le fichier fourni est un fichier json valide. Si le fichier n'existe pas, il est créé.
        
        Paramètres:
            - nom_fichier (str): Le nom du fichier

        Retourne (bool): True si le fichier fourni est un fichier json valide, False sinon.
        
        """
        try:
            with open(nom_fichier, 'r') as fichier:
                json.loads(fichier.read())
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

        Retourne None
        """

        while True:
            
            if self.__num_menu == 0:
                self.__ecran_de_selection()
                continue

            if self.__num_menu == 1:
                pass
        
    def __ecran_de_selection(self) -> None:
        """
        Fonction permettant d'écrire le message de bienvenue
        
        :param self: Description
        """

        while True:
            print("MENU PRINCIPAL\n")
            print("1. Voir les tâches")
            print("2. Ajouter une tâche")
            print("3. Terminer une tâche")
            print("4. Supprimer une tâche")
            str_num_menu: str = input("5. Quitter\n\n")

            try:
                self.__num_menu = int(str_num_menu)
                if self.__num_menu not in (1,2,3,4,5):
                    raise ValueError
                break
            except Exception:
                print("\n\nErreur, veuillez fournir une valeur entre 1 et 5.\n\n")
                pass

