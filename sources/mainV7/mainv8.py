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

try:
    img_bonhomme = tk.PhotoImage(file="Perso 1.png")
    ratio = max(1, img_bonhomme.width() // (LARGEUR_CANVAS // TAILLE_GRILLE))
    img_bonhomme = img_bonhomme.subsample(ratio)
    
    # --- LA LIGNE MAGIQUE ---
    canvas.image = img_bonhomme  # On attache l'image au canvas pour qu'elle ne soit pas supprimée
    # ------------------------
except:
    img_bonhomme = None
    print("Attention : Image 'perso 1.png' introuvable.")

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
                "etats_initial": 0,
                "personnage": None,
                "type_de_perso": "sain",
                "immunite": 0,
                "id_image_perso": None
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
                grille[(lig, col)]["etats_initial"] = 1

    #infectee initiaux
    for lig in range(TAILLE_GRILLE):
        for col in range(TAILLE_GRILLE):
            if random.random() < probainfecter:
                grille[(lig, col)]["etat"] = 2
                grille[(lig, col)]["couleur"] = "#bc4749"
                placer_personnage(lig, col)

    
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
            donnes["etat"] = donnes["etats_initial"]

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
    # 1. PRÉPARATION
    # On crée une liste pour stocker les mouvements avant de les appliquer.
    # Si on bougeait les persos un par un dans la boucle principale, certains
    # pourraient bouger deux fois de suite (le fameux effet "téléportation").
    mouvements_a_faire = []

    for (lig, col), donnes in grille.items():
        # On ne déplace que les cases qui ont un infecté (etat 2)
        if donnes["etat"] == 2:
            dx, dy = random.choice(directions[1:]) # Choisit une direction au hasard
            nl, nc = lig + dx, col + dy
            
            # 2. VÉRIFICATION DU VOISINAGE
            if (nl, nc) in grille:
                # On autorise le mouvement seulement si la case est saine (1) ou déjà une hitbox (3)
                if grille[(nl, nc)]["etat"] in [1, 3]:
                    # On enregistre : (position_départ, position_arrivée)
                    mouvements_a_faire.append(((lig, col), (nl, nc)))

    # 3. APPLICATION DES MOUVEMENTS (Logique + Visuel)
    for depart, arrivee in mouvements_a_faire:
        case_dep = grille[depart]
        case_arr = grille[arrivee]

        # --- Partie Logique (Dictionnaire) ---
        # L'infecté quitte la case de départ (elle redevient comme à l'origine)
        case_dep["etat"] = case_dep["etats_initial"]
        # L'infecté arrive sur la nouvelle case
        case_arr["etat"] = 2

        # --- Partie Visuelle (Image sur le Canvas) ---
        # On récupère l'ID de l'image qui se trouve sur la case de départ
        id_img = case_dep.get("id_image_perso")

        if id_img is not None:
            # On calcule le nouveau centre de la case d'arrivée pour placer l'image
            taille_case = LARGEUR_CANVAS / TAILLE_GRILLE
            nouveau_x = case_arr["x"] + (taille_case / 2)
            nouveau_y = case_arr["y"] + (taille_case / 2)

            # COMMANDE MAGIQUE : On déplace l'image existante vers les nouvelles coordonnées
            canvas.coords(id_img, nouveau_x, nouveau_y)

            # On met à jour le dictionnaire : la nouvelle case possède l'image, l'ancienne est vide
            case_arr["id_image_perso"] = id_img
            case_dep["id_image_perso"] = None

    # 4. MISE À JOUR FINALE
    hitbox() # On recalcule les zones rouges autour des nouvelles positions
    verification_des_couleur() # On rafraîchit les couleurs du sol (vert/beige/rouge)

def placer_personnage(lig, col):
    TAILLE_CASE = LARGEUR_CANVAS / TAILLE_GRILLE
    # 1. On calcule le centre de la case pour positionner l'image
    case = grille[(lig, col)]
    centre_x = case["x"] + (TAILLE_CASE / 2)
    centre_y = case["y"] + (TAILLE_CASE / 2)

    # 2. Si l'image a bien été chargée
    if img_bonhomme:
        # 3. On crée l'objet image sur le canvas
        # IMPORTANT : 'anchor="center"' pour que (centre_x, centre_y) soit le milieu de l'image
        id_img = canvas.create_image(
            centre_x, centre_y,
            image=img_bonhomme,
            anchor="center"
        )
        # 4. On range cet ID dans le dictionnaire pour pouvoir le déplacer plus tard
        case["id_image_perso"] = id_img



# 1. On initialise la grille
starting_grid()

# 2. On force la case (10, 10) à être un infecté (état 2)
grille[(10, 10)]["etat"] = 2

# 3. On place le personnage visuel
placer_personnage(10, 10)

# 4. On met à jour les couleurs (pour que la case sous le perso soit rouge/blanche)
verification_des_couleur()
hitbox()
bouton_deplacement.config(command=lambda: deplacement())
bouton_propagation.config(command=lambda: hitbox())
afficher_toutes_les_cartes()


fenetre.mainloop()

"""""structure de la grille
grille[(lig, col)] = {
    "x": x1,
    "y": y1,
    "etat": etat,
    "couleur": couleur,
    "id_canvas": None 
    "etats_initial": etat
    "personnage": None
    "type_de_perso": "infecte" ou "sain"
    "immunite": de 0 a 100
    "id_image_perso": None

}
"""""
"""indication:
etat 0 = nul, non existant
etat 1 = safe
etat 2 = infecté
etat 3 = hitbox infecté
"""
