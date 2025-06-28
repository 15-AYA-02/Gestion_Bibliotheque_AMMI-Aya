import matplotlib.pyplot as plt
import csv
from datetime import datetime
from collections import Counter
import os


plt.rcParams.update({
    "axes.facecolor":"#ffffff",
    "axes.edgecolor":"#000000",
    "axes.labelcolor":"#000000",
    "xtick.color":"#000000",
    "ytick.color":"#000000",
    "text.color":"#000000",
})

#Diagramme circulaire : % de livres par genre
def genre_pie_chart(bibliotheque):
    genres = [livre.genre for livre in bibliotheque.livres.values()]
    os.makedirs("assets",exist_ok=True)
    plt.figure(figsize=(6,6))
    if not genres:
        plt.title("pourcentage de livres par genre")
        plt.axis('off')
    else:
        counts = Counter(genres)
        plt.pie(list(counts.values()),labels=list(counts.keys()),autopct='%1.1f%%')
        plt.title("pourcentage de livres par genre")
    
    plt.savefig("assets/stats_genres.png")
    plt.close()

#Histogramme : Top 10 des auteurs les plus populaires
def top_auteurs_barchart(bibliotheque):
    auteurs = [livre.auteur for livre in bibliotheque.livres.values()]
    os.makedirs("assets",exist_ok=True)
    plt.figure(figsize=(8,4))
    if not auteurs:
        plt.title("Top 10 des auteurs populaires")
        plt.axis('off')

    else :
        counts = Counter(auteurs).most_common(10)
        noms= [auteur for auteur, _ in counts]
        nb = [c for _,c in counts]
    
        plt.bar(noms,nb,color="#3366cc")
        plt.xticks(rotation=30)
    
    
    plt.savefig("assets/stats_auteurs.png")
    plt.close()


#Courbe temporelle : Activité des emprunts (30 derniers jours)
def activite_emprunt_courbe():
    jours = []
    
    with open("data/historique.csv") as f:
        reader = csv.reader(f,delimiter=";")
        for row in reader:
            if len(row)<1 or not row[0].strip():
                continue
            try :
                date = datetime.strptime(row[0],"%Y-%m-%d")
                jours.append(date.date())
            except ValueError:
                continue
    
    counts = Counter(jours)
    sorted_dates = sorted(counts.keys())
    valeurs =[counts[d] for d in sorted_dates]
    plt.figure(figsize=(10,5))
    plt.plot(sorted_dates,valeurs,marker="o")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.title("Activité des emprunts")
    os.makedirs("assets",exist_ok=True)
    plt.savefig("assets/stats_emprunts.png")
    plt.close()