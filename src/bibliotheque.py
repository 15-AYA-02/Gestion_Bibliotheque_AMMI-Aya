import json #pour sauvegarder les liste de livres dans membres.txt...
import csv #pour enregistrer l'historique des emprunts/retours
from datetime import datetime #pour dater chaque emprunt/retour
from exceptions import * #importer les exceptions personnalisées depui exceptions.py
import os

class Livre:
    def __init__(self,ISBN,titre,auteur,annee,genre,status = 'disponible'):
        self.ISBN = ISBN
        self.titre = titre
        self.auteur = auteur
        self.annee = annee
        self.genre = genre
        self.status = status

class Membre:
    def __init__(self,ID,nom):
        self.ID = ID
        self.nom = nom
        self.livres_empruntes = []

class Bibliotheque:
    def __init__(self):
        self.livres = {}
        self.membres = {}
        self.charger_donnees()
        #cette méthode charge automatiquements les livres depuis livres.txt
        #et les membres depuis membres.txt
    
    def add_Livre(self,livre):
        self.livres[livre.ISBN] = livre
    
    def delete_Livre(self,ISBN):
        if ISBN in self.livres:
            del self.livres[ISBN]
        else:
            raise LivreInexistantError("Livre introuvable !")

    def add_membre(self,membre):
        self.membres[membre.ID] = membre
    
    def emprunter_livre(self,ID,ISBN):
        if ID not in self.membres:
            raise MembreInexistantError()
        if ISBN not in self.livres:
            raise LivreInexistantError()
        livre = self.livres[ISBN]
        membre = self.membres[ID]
        if livre.status != 'disponible':
            raise LivreIndisponibleError()
        if len(membre.livres_empruntes) >=3:
            raise QuotaEmpruntDepasseError()
        livre.status = 'emprunte'
        membre.livres_empruntes.append(ISBN)
        self.log_historique(ISBN,ID,"emprunt")# sauvegarder l'historique des actions dans historique.csv
        
    
    def rendre_livre(self,ID,ISBN):
        if ID not in self.membres:
            raise MembreInexistantError()
        if ISBN not in self.livres:
            raise LivreInexistantError()
        membre = self.membres[ID] 
        if ISBN not in membre.livres_empruntes :
            raise Exception("Ce membre n'a pas emprunte ce livre !")
        membre.livres_empruntes.remove(ISBN)
        self.livres[ISBN].status = 'disponible'
        self.log_historique(ISBN,ID,"retour")
    
    def log_historique(self,ISBN,ID,action):
        os.makedirs("data",exist_ok=True)
        with open("data/historique.csv","a",newline="") as f:
            writer = csv.writer(f,delimiter=";")
            date = datetime.now().strftime("%Y-%m-%d")
            writer.writerow([date,ISBN,ID,action])
    
    def sauvegarder_donnees(self):
        with open("data/livres.txt","w") as f:
            for livre in self.livres.values():
                f.write(f"{livre.ISBN};{livre.titre};{livre.auteur};{livre.annee};{livre.genre};{livre.status}\n")
        with open("data/membres.txt","w") as f:
            for membre in self.membres.values():
                f.write(f"{membre.ID};{membre.nom};{json.dumps(membre.livres_empruntes)}\n")    
    
    def charger_donnees(self):
        try:
            with open("data/livres.txt") as f:
                for line in f:
                    line = line.strip()
                    if line:
                        isbn,titre,auteur,annee,genre,status =line.split(";")
                        self.add_Livre(Livre(isbn,titre,auteur,annee,genre,status))
        except FileNotFoundError:
            pass
        except ValueError:
            pass
        try:
            with open("data/membres.txt") as f:
                for line in f:
                    line = line.strip()
                    if line:
                        try:
                            id, nom, emprunts= line.split(";",2)
                            membre = Membre(id,nom)
                            membre.livres_empruntes = json.loads(emprunts)
                            self.add_membre(membre)
                        except (ValueError,json.JSONDecodeError):
                            pass
        except FileNotFoundError:
            pass
            