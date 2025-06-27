import tkinter as tk
from tkinter import ttk, messagebox
from bibliotheque import Bibliotheque, Livre, Membre
from exceptions import *
from PIL import Image,ImageTk
from PIL.Image import Resampling
from visualisations import genre_pie_chart,top_auteurs_barchart,activite_emprunt_courbe
import os



class Application:
    def __init__(self,root):
        self.biblio = Bibliotheque()
        self.root = root
        self.root.title("Système de Gestion de Bibliothèque")
        self.root.geometry("1000x600")
        self.root.configure(bg="#f4f4f4")

        self.style = ttk.Style()
        self.style.configure("TButton",font=("Arial",10),padding=6)
        self.style.map("TButton",foreground=[('pressed',"white"),('active','#003366')],background=[('pressed','#003366'),('active','#006699')])

        self.menu_frame = tk.Frame(root,bg='#003366',width=200)
        self.menu_frame.pack(side="left",fill="y")

        self.content_frame = tk.Frame(root,bg="white")
        self.content_frame.pack(side="right",fill="both",expand=True)

        self.pages = {}
        menu_items = [
            ("Livres",self.init_tab_livres),
            ("Membres",self.init_tab_membres),
            ("Emprunts",self.init_tab_emprunts),
            ("Statistiques",self.init_tab_stats),
            ("Quitter",self.root.quit)
        ]
        
        for label,command in menu_items:
            btn = tk.Button(self.menu_frame,text = label,font =("Arial",12),
                            bg = "#003366",fg="white",relief="flat",
                            activebackground="#005580",activeforeground="white",
                            command=lambda c=command: self.show_page(c))
            btn.pack(fill="x",pady=2,padx=10)
        self.show_page(self.init_tab_livres)

    def show_page(self,init_function):
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        init_function()
        
    
    def init_tab_livres(self):
        frame = ttk.Frame(self.content_frame)
        frame.pack(fill="both",expand=True)
        
        #FORMULAIRE D'AJOUT D'UN LIVRE
        
        entries = {}
        labels = ["ISBN","Titre","Auteur","Année","Genre"]
        for i,label in enumerate(labels):
            ttk.Label(frame,text=label).grid(row=i,column=0,padx=5,pady=2,sticky="w")
            entries[label] = ttk.Entry(frame)
            entries[label].grid(row=i,column=1,padx=5,pady=2)

        def add_livre():
            try:
                livre = Livre(
                    entries["ISBN"].get(),
                    entries["Titre"].get(),
                    entries["Auteur"].get(),
                    entries["Année"].get(),
                    entries["Genre"].get()
                )
                self.biblio.add_Livre(livre)
                self.biblio.sauvegarder_donnees()
                messagebox.showinfo("Succes","Livre ajouté")
            except Exception as e:
                messagebox.showerror("Error",str(e))
        ttk.Button(frame,text="Ajouter Livre",command=add_livre).grid(row=6,columnspan=2,pady=5)
    
    def init_tab_membres(self):
        frame = ttk.Frame(self.content_frame)
        frame.pack(fill="both",expand=True)
        
        #FORMULAIRE D'AJOUT D'UN MEMBRE
        ttk.Label(frame,text="ID Membre").grid(row=0,column=0,padx=5,pady=2)
        id_entry = ttk.Entry(frame)
        id_entry.grid(row=0,column=1,padx=5,pady=2)

        ttk.Label(frame,text="Nom du Membre").grid(row=1,column=0,padx=5,pady=2)
        nom_entry = ttk.Entry(frame)
        nom_entry.grid(row=1,column=1,padx=5,pady=2)

        def add_membre():
            try:
                membre = Membre(id_entry.get(),nom_entry.get())
                self.biblio.add_membre(membre)
                self.biblio.sauvegarder_donnees()
                messagebox.showinfo("Succes","Membre ajouté")
            except Exception as e:
                messagebox.showerror("Error",str(e))
        ttk.Button(frame,text="Ajouter Membre",command=add_membre).grid(row=2,columnspan=2,pady=5)
    
    def init_tab_emprunts(self):
        frame = ttk.Frame(self.content_frame)
        frame.pack(fill="both",expand=True)
        
        #FORMULAIRE D'AJOUT D'UN EMPRUNT
        ttk.Label(frame,text="ID de Membre").grid(row=0,column=0,padx=5,pady=2)
        id_entry = ttk.Entry(frame)
        id_entry.grid(row=0,column=1,padx=5,pady=2)

        ttk.Label(frame,text="ISBN de Livre").grid(row=1,column=0,padx=5,pady=2)
        isbn_entry = ttk.Entry(frame)
        isbn_entry.grid(row=1,column=1,padx=5,pady=2)

        def emprunter():
            try:
                self.biblio.emprunter_livre(id_entry.get(),isbn_entry.get())
                self.biblio.sauvegarder_donnees()
                messagebox.showinfo("Succes","Livre emprunté")
            except Exception as e:
                messagebox.showerror("Error",str(e))
        def rendrer():
            try:
                self.biblio.rendre_livre(id_entry.get(),isbn_entry.get())
                self.biblio.sauvegarder_donnees()
                messagebox.showinfo("Succes","Livre retourné")
            except Exception as e:
                messagebox.showerror("Error",str(e))
        ttk.Button(frame,text="Emprunter",command=emprunter).grid(row=2,column=0,pady=5)
        ttk.Button(frame,text="Rendre",command=rendrer).grid(row=2,column=1,pady=5)
    
    def init_tab_stats(self):
        frame = ttk.Frame(self.content_frame)
        frame.pack(fill="both",expand=True)
        self.images = {}

        container = ttk.Frame(frame)
        container.pack(fill="both",expand=True,padx=10,pady=10)
        

        def generer_stats():
            genre_pie_chart(self.biblio)
            top_auteurs_barchart(self.biblio)
            activite_emprunt_courbe()
            messagebox.showinfo("Succes","Graphiques générés")
            afficher_images()
    
        def afficher_images():
            for widget in container.winfo_children():
                widget.destroy()

            paths = [
                ("Répartition par genre","assets/stats_genres.png"),
                ("Top 10 auteurs","assets/stats_auteurs.png"),
                ("Activité des emprunts","assets/stats_emprunts.png")
            ]

            top_row= ttk.Frame(container)
            top_row.pack(pady=10)
            for titre, path in paths[:2]:
                col = ttk.Frame(top_row)
                col.pack(side="left",padx=10)
                if os.path.exists(path):
                    try:
                        img = Image.open(path)
                        img = img.resize((320,240),Resampling.LANCZOS)
                        photo = ImageTk.PhotoImage(img)
                        self.images[path] = photo

                        ttk.Label(col,text=titre,font=("Arial",12,"bold")).pack(pady=(0,5))
                        ttk.Label(col,image=photo).pack()
                    except Exception as e:
                        ttk.Label(col,text=f"Error :{e}").pack()
                else:
                    ttk.Label(col,text=f"Image non trouvée :{path}").pack()
            bottom_row=ttk.Frame(container)
            bottom_row.pack(pady=10)

            titre,path = paths[2]
            col=ttk.Frame(bottom_row)
            col.pack()
            if os.path.exists(path):
                try:
                    img = Image.open(path)
                    img = img.resize((640,300),Resampling.LANCZOS)
                    photo = ImageTk.PhotoImage(img)
                    self.images[path] = photo

                    ttk.Label(col,text=titre,font=("Arial",12,"bold")).pack(pady=(0,5))
                    ttk.Label(col,image=photo).pack()
                except Exception as e:
                    ttk.Label(col,text=f"Error :{e}").pack()
            else:
                ttk.Label(col,text=f"Image non trouvée :{path}").pack()
        ttk.Button(frame,text="Refraichir les stats",command=generer_stats).pack(pady=10)
        

if __name__ == "__main__":
    root = tk.Tk()
    application = Application(root)
    root.mainloop()