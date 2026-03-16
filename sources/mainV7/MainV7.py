import tkinter as tk
import random

prob = 0.60
prob1 = 1
probainfecter = 0.01
TAILLE_GRILLE = 20  # Tu peux mettre 10, 50, 100...
LARGEUR_CANVAS = 600 # La zone de dessin reste fixe
nombre_de_simulations = 0
auto_running = False
grille = {} #le but est d'avoir une dictionnaire de la forme grille[case1:x,y,etat,couleur, canvas_id: ...] ,
            # case2:x,y,etat,couleur, canvas_id: ...]

directions = [
    (0, 0),   # centre
    (-1, 0),  # haut
    (1, 0),   # bas
    (0, -1),  # gauche
    (0, 1),    # droite
    (-2, 0),  # haut
    (2, 0),   # bas
    (0, -2),  # gauche
    (0, 2),    # droite
    #DIAFONALES
    (-1, -1), # haut-gauche
    (-1, 1),  # haut-droite
    (1, -1),  # bas-gauche
    (1, 1),    # bas-droite
    # (-2, -2), # haut-gauche
    # (-2, 2),  # haut-droite
    # (2, -2),  # bas-gauche
    # (2, 2)    # bas-droite
]

# directions = [
#     (0, 0),   # centre
#     (-1, 0),  # haut
#     (1, 0),   # bas
#     (0, -1),  # gauche
#     (0, 1),    # droite
#    (-1, -1), # haut-gauche
#     (-1, 1),  # haut-droite
#     (1, -1),  # bas-gauche
#     (1, 1)    # bas-droite
# ]

fenetre = tk.Tk()
fenetre.title("Grille cliquable")
fenetre.geometry(f"{LARGEUR_CANVAS + 400}x{LARGEUR_CANVAS}")
fenetre.configure(bg="#2c4260")

# ────────────── Panneau droite ──────────────
frame_param = tk.Frame(fenetre, bg="#1d2b3e")
frame_param.pack(side="right", fill="both", expand=True)

frame_boutons = tk.Frame(frame_param, bg="#1d2b3e")
frame_boutons.pack(pady=20)

titre_param = tk.Label(
    frame_param,
    text="Paramètres",
    font=("Impact", 24),
    bg="#1d2b3e",
    fg="#ffffff"
)
titre_param.pack(pady=0)

bouton_test = tk.Button(
    frame_boutons,
    text="Reset",
    font=("Arial", 16),
    bg="#394867",
    fg="#ffffff"
)
bouton_test.pack(side="left", padx=40)

bouton_propagation = tk.Button(
    frame_boutons,
    text="Simuler",
    font=("Arial", 15),
    bg="#394867",
    fg="#ffffff"
)
bouton_propagation.pack(side="left", padx=40)

bouton_auto = tk.Button(
    frame_boutons,
    text="Auto",
    font=("Arial", 16),
    bg="#394867",
    fg="#ffffff"
)
bouton_auto.pack(side="left", padx=40)

bouton_deplacement = tk.Button(
    frame_boutons,
    text="deplacement",
    font=("Arial", 16),
    bg="#394867",
    fg="#ffffff"
)
bouton_deplacement.pack(side="left", padx=40)

# ────────────── Panneau gauche ──────────────
canvas = tk.Canvas(
    fenetre,
    width=LARGEUR_CANVAS,
    height=LARGEUR_CANVAS,
    bg="#778DA9",
    highlightthickness=0
)
canvas.pack(side="left")



def starting_grid():
    canvas.delete("all")
    grille.clear()
    
    # Calcul automatique de la taille d'une case
    taille_auto = LARGEUR_CANVAS / TAILLE_GRILLE
    
    for lig in range(TAILLE_GRILLE):
        for col in range(TAILLE_GRILLE):
            x1 = col * taille_auto
            y1 = lig * taille_auto
            x2 = x1 + taille_auto
            y2 = y1 + taille_auto
            
            etat = 0 # Par exemple : 0 pour vide, 1 pour plein
            couleur = "#f4f1de"
            
            grille[(lig, col)] = {
                "x": x1,
                "y": y1,
                "etat": etat,
                "couleur": couleur,
                "id_canvas": None,
                "etats initial": 0
            }
            
            rect_id = canvas.create_rectangle(
                x1, y1, x2, y2,
                fill=couleur,
                width=0
            )
            grille[(lig, col)]["id_canvas"] = rect_id

    for lig in range(TAILLE_GRILLE):
        for col in range(TAILLE_GRILLE):
            if random.random() < prob:
                grille[(lig, col)]["etat"] = 1
                grille[(lig, col)]["couleur"] = "#a7c957"
                grille[(lig, col)]["etats initial"] = 1

    #infectee initiaux
    for lig in range(TAILLE_GRILLE):
        for col in range(TAILLE_GRILLE):
            if random.random() < probainfecter:
                grille[(lig, col)]["etat"] = 2
                grille[(lig, col)]["couleur"] = "#bc4749"

    
    verification_des_couleur() # Met à jour les couleurs sur le canvas en fonction des états


def verification_des_couleur():
    for lig in range(TAILLE_GRILLE):
        for col in range(TAILLE_GRILLE):
            etat = grille[(lig, col)]["etat"]
            if etat == 1:
                canvas.itemconfig(grille[(lig, col)]["id_canvas"], fill="#a7c957")  # vert
            elif etat == 2:
                canvas.itemconfig(grille[(lig, col)]["id_canvas"], fill="#bc4749")  # rouge
            elif etat == 3:
                canvas.itemconfig(grille[(lig, col)]["id_canvas"], fill="#b96f70")  # rouge clair
            else:
                canvas.itemconfig(grille[(lig, col)]["id_canvas"], fill="#f4f1de")  # beige


           

def afficher_toutes_les_cartes():
    # 1. CARTE DES ÉTATS (0 ou 1)
    print("\n=== CARTE DES ÉTATS ===")
    for lig in range(TAILLE_GRILLE):
        ligne = ""
        for col in range(TAILLE_GRILLE):
            etat = grille[(lig, col)]["etat"]
            ligne += f"{etat:^3}" # ^3 centre le texte sur 3 espaces
        print(ligne)


    # # 2. CARTE DES COULEURS (Codes Hexa)
    # print("\n=== CARTE DES COULEURS ===")
    # for lig in range(TAILLE_GRILLE):
    #     ligne = ""
    #     for col in range(TAILLE_GRILLE):
    #         coul = grille[(lig, col)]["couleur"]
    #         ligne += f"{coul}  "
    #     print(ligne)

    # # 3. CARTE DES COORDONNÉES (X, Y)
    # print("\n=== CARTE DES COORDONNÉES (X,Y) ===")
    # for lig in range(TAILLE_GRILLE):
    #     ligne = ""
    #     for col in range(TAILLE_GRILLE):
    #         x = grille[(lig, col)]["x"]
    #         y = grille[(lig, col)]["y"]
    #         # On affiche (x,y) de manière compacte
    #         ligne += f"({x},{y}) ".ljust(10) # Aligne à gauche sur 10 caractères
    #     print(ligne)

def cacher_la_grille():
    for lig in range(TAILLE_GRILLE):
        for col in range(TAILLE_GRILLE):
            canvas.itemconfig(grille[(lig, col)]["id_canvas"], fill="#778DA9")  # même couleur que le fond

def hitbox():
    # 1. NETTOYAGE COMPLET des anciennes hitbox
    for pos, donnes in grille.items():
        if donnes["etat"] == 3:
            # On remet l'état initial (1 si c'était vert, 0 si c'était beige)
            donnes["etat"] = donnes["etats initial"]

    # 2. CALCUL DES NOUVELLES HITBOX
    nouveaux_infectes = []
    for (lig, col), donnes in grille.items():
        if donnes["etat"] == 2:  # Pour chaque infecté
            for dx, dy in directions:
                nl, nc = lig + dx, col + dy
                if (nl, nc) in grille:
                    voisin = grille[(nl, nc)]
                    # On ne met une hitbox que sur les cases qui ne sont pas l'infecté lui-même
                    if voisin["etat"] != 2:
                        nouveaux_infectes.append((nl, nc))

    # 3. APPLICATION
    for position in nouveaux_infectes:
        grille[position]["etat"] = 3
    
    verification_des_couleur()

def deplacement():
    # 1. On crée une liste pour stocker les mouvements à faire
    mouvements_a_faire = []

    for (lig, col), donnes in grille.items():
        if donnes["etat"] == 2:  # Si la cellule est infectée
            # On choisit une direction
            dx, dy = random.choice(directions[1:]) 
            nl, nc = lig + dx, col + dy
            
            # 2. On vérifie si la destination est dans la grille
            if (nl, nc) in grille:
                # On autorise le déplacement sur le vert (1) ou la hitbox (3)
                if grille[(nl, nc)]["etat"] in [1, 3]:
                    # On enregistre le mouvement (départ -> arrivée)
                    mouvements_a_faire.append(((lig, col), (nl, nc)))

    # 3. Une fois la boucle finie, on applique les changements
    for depart, arrivee in mouvements_a_faire:
        # L'ancienne case redevient saine (1)
        grille[depart]["etat"] = 1
        # La nouvelle case devient infectée (2)
        grille[arrivee]["etat"] = 2

    # 4. On recalcule la hitbox et on met à jour le dessin
    hitbox()
    verification_des_couleur()



starting_grid()

verification_des_couleur()
hitbox()
afficher_toutes_les_cartes()
bouton_deplacement.config(command=lambda: deplacement())
bouton_propagation.config(command=lambda: hitbox())
afficher_toutes_les_cartes

fenetre.mainloop()

"""""structure de la grille
grille[(lig, col)] = {
    "x": x1,
    "y": y1,
    "etat": etat,
    "couleur": couleur,
    "id_canvas": None # On stockera l'ID de l'objet tkinter ici
}
"""""
"""indication:
etat 0 = nul, non existant
etat 1 = safe
etat 2 = infecté
etat 3 = hitbox infecté
"""
