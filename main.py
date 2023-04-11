import tkinter as tk
import tkinter.ttk as ttk
import mysql.connector as mysql

class Product:
    def __init__(self, id, name, description, price, quantity, category):
        self.id = id
        self.name = name
        self.description = description
        self.price = price
        self.quantity = quantity
        self.category = category

class Dashboard:
    def __init__(self, root):
        self.root = root
        self.root.title("Tableau de bord de la boutique")
        
        # Connexion à la base de données
        self.db = mysql.connect(
            host="localhost",
            user="root",
            password="",
            database="boutique"
        )
        self.cursor = self.db.cursor()

        # Liste des produits
        self.product_list = []
        
        # Widgets pour l'affichage des produits
        self.treeview = ttk.Treeview(self.root, columns=("nom", "description", "prix", "quantité", "catégorie"), show="headings")
        self.treeview.heading("nom", text="Nom")
        self.treeview.heading("description", text="Description")
        self.treeview.heading("prix", text="Prix")
        self.treeview.heading("quantité", text="Quantité")
        self.treeview.heading("catégorie", text="Catégorie")
        self.treeview.pack(side="left", fill="both", expand=True)
        
        # Boutons d'actions pour les produits
        self.button_frame = tk.Frame(self.root)
        self.add_button = tk.Button(self.button_frame, text="Ajouter", command=self.add_product_window)
        self.edit_button = tk.Button(self.button_frame, text="Modifier", command=self.edit_product_window)
        self.delete_button = tk.Button(self.button_frame, text="Supprimer", command=self.delete_product)
        self.add_button.pack(side="top", padx=10, pady=10)
        self.edit_button.pack(side="top", padx=10, pady=10)
        self.delete_button.pack(side="top", padx=10, pady=10)
        self.button_frame.pack(side="right", fill="y")
        
        # Chargement des produits depuis la base de données
        self.load_products()

    def load_products(self):
        self.product_list.clear()
        self.treeview.delete(*self.treeview.get_children())
        self.cursor.execute("SELECT p.id, p.nom, p.description, p.prix, p.quantite, c.nom FROM produit p JOIN categorie c ON p.id_categorie = c.id")
        products = self.cursor.fetchall()
        for product in products:
            p = Product(product[0], product[1], product[2], product[3], product[4], product[5])
            self.product_list.append(p)
            self.treeview.insert("", "end", values=(p.name, p.description, p.price, p.quantity, p.category))
    
    def add_product(self, name, description, price, quantity, category):
        # Insertion du nouveau produit dans la base de données
        query = "INSERT INTO produit (nom, description, prix, quantite, id_categorie) VALUES (%s, %s, %s, %s, %s)"
        values = (name, description, price, quantity, category.id)
        self.cursor.execute(query, values)
        self.db.commit()
        
        # Rechargement des produits depuis la base de données
        self.load_products()
    
    def add_product_window(self):
        # Création de la fenêtre pour ajouter
        
class Inventory:
    def __init__(self, master):
        self.master = master
        self.master.title("Tableau de bord")
        self.products = []
        self.categories = []

        # Création de la fenêtre principale
        self.frame = Frame(self.master)
        self.frame.pack()

        # Création de la liste des produits
        self.product_list = Listbox(self.frame)
        self.product_list.pack(side=LEFT)

        # Ajout des boutons pour gérer les produits
        self.add_product_button = Button(self.frame, text="Ajouter un produit", command=self.add_product_window)
        self.add_product_button.pack()

        self.remove_product_button = Button(self.frame, text="Supprimer un produit", command=self.remove_product)
        self.remove_product_button.pack()

        self.edit_product_button = Button(self.frame, text="Modifier un produit", command=self.edit_product_window)
        self.edit_product_button.pack()

        # Ajout d'un bouton pour quitter l'application
        self.quit_button = Button(self.frame, text="Quitter", command=self.master.quit)
        self.quit_button.pack()

    def add_product_window(self):
        # Création de la fenêtre pour ajouter un produit
        self.add_product_frame = Toplevel(self.master)
        self.add_product_frame.title("Ajouter un produit")

        # Ajout des champs pour saisir les informations du produit
        Label(self.add_product_frame, text="Nom").grid(row=0, column=0)
        self.name_entry = Entry(self.add_product_frame)
        self.name_entry.grid(row=0, column=1)

        Label(self.add_product_frame, text="Description").grid(row=1, column=0)
        self.description_entry = Entry(self.add_product_frame)
        self.description_entry.grid(row=1, column=1)

        Label(self.add_product_frame, text="Prix").grid(row=2, column=0)
        self.price_entry = Entry(self.add_product_frame)
        self.price_entry.grid(row=2, column=1)

        Label(self.add_product_frame, text="Quantité").grid(row=3, column=0)
        self.quantity_entry = Entry(self.add_product_frame)
        self.quantity_entry.grid(row=3, column=1)

        Label(self.add_product_frame, text="Catégorie").grid(row=4, column=0)
        self.category_entry = Entry(self.add_product_frame)
        self.category_entry.grid(row=4, column=1)

        # Ajout d'un bouton pour valider l'ajout du produit
        self.add_button = Button(self.add_product_frame, text="Ajouter", command=self.add_product)
        self.add_button.grid(row=5, column=1)

    def add_product(self):
        # Récupération des valeurs saisies par l'utilisateur
        name = self.name_entry.get()
        description = self.description_entry.get()
        price = float(self.price_entry.get())
        quantity = int(self.quantity_entry.get())
        category = self.category_entry.get()

        # Création du produit et ajout dans la liste des produits
        product = Product(len(self.products) + 1, name, description, price, quantity, category)
        self.products.append(product)

        # Mise à jour de la liste des produits affichée dans la fenêtre principale
        self.update_product_list()

        # Fermeture de la fenêtre pour ajouter un produit
        self.add_product_frame.destroy()

    def remove_product(self):
        # Récupération de l'indice du produit sélectionné
        selected_index = self.product_list.cur

    def add_product_window(self):
        # Création de la fenêtre pour ajouter un produit
        self.add_window = Toplevel(self.root)
        self.add_window.title("Ajouter un produit")

        # Création des champs pour le formulaire d'ajout de produit
        name_label = Label(self.add_window, text="Nom du produit:")
        name_label.grid(row=0, column=0, padx=5, pady=5, sticky=W)
        self.name_entry = Entry(self.add_window, width=30)
        self.name_entry.grid(row=0, column=1, padx=5, pady=5)

        description_label = Label(self.add_window, text="Description:")
        description_label.grid(row=1, column=0, padx=5, pady=5, sticky=W)
        self.description_entry = Text(self.add_window, height=5, width=30)
        self.description_entry.grid(row=1, column=1, padx=5, pady=5)

        price_label = Label(self.add_window, text="Prix unitaire:")
        price_label.grid(row=2, column=0, padx=5, pady=5, sticky=W)
        self.price_entry = Entry(self.add_window, width=30)
        self.price_entry.grid(row=2, column=1, padx=5, pady=5)

        quantity_label = Label(self.add_window, text="Quantité:")
        quantity_label.grid(row=3, column=0, padx=5, pady=5, sticky=W)
        self.quantity_entry = Entry(self.add_window, width=30)
        self.quantity_entry.grid(row=3, column=1, padx=5, pady=5)

        category_label = Label(self.add_window, text="Catégorie:")
        category_label.grid(row=4, column=0, padx=5, pady=5, sticky=W)
        self.category_entry = ttk.Combobox(self.add_window, values=self.categories)
        self.category_entry.grid(row=4, column=1, padx=5, pady=5)

        # Bouton pour ajouter le produit
        add_button = Button(self.add_window, text="Ajouter", command=self.add_product)
        add_button.grid(row=5, column=1, padx=5, pady=5, sticky=E)

    def add_product(self):
        # Récupération des données du formulaire
        name = self.name_entry.get()
        description = self.description_entry.get("1.0", END)
        price = self.price_entry.get()
        quantity = self.quantity_entry.get()
        category = self.category_entry.get()

        # Vérification des champs requis
        if name == "" or price == "" or quantity == "" or category == "":
            messagebox.showerror("Erreur", "Veuillez remplir tous les champs.")
            return

        # Conversion des données
        try:
            price = float(price)
            quantity = int(quantity)
        except ValueError:
            messagebox.showerror("Erreur", "Le prix et la quantité doivent être des nombres.")
            return

        # Récupération de l'ID de la catégorie
        category_id = self.db.get_category_id(category)

        # Ajout du produit à la base de données
        self.db.add_product(name, description, price, quantity, category_id)

        # Fermeture de la fenêtre d'ajout
        self.add_window.destroy()

        # Actualisation de la liste des produits
        self.update_product_list()
