class LivreIndisponibleError(Exception):
    def _str_(self):
        return "ce livre est indisponible !"
    
class QuotaEmpruntDepasseError(Exception):
    def _str_(self):
        return "ce membre a attient le quota d'emprunts !"
    
class MembreInexistantError(Exception):
    def _str_(self):
        return "ce Membre n'existe pas !"
    
class LivreInexistantError(Exception):
    def _str_(self):
        return "Livre introuvable !"