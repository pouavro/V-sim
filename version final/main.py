import os
import tkinter as tk
import random
import ctypes

# Fix pour éviter les problèmes de mise à l’échelle sur Windows (sinon flou)
try: ctypes.windll.shcore.SetProcessDpiAwareness(1)
except: pass

# --- Paramètres de base (tu peux changer ça pour tester différents scénarios)
proba_transmission = 0.25
probainfecter_initiaux = 0.02
probasains_initial = 0.10
prob_mort = 0.005
prob_guerison = 0.02
TAILLE_GRILLE = 15
LARGEUR_CANVAS = 800
nombre_de_simulations = 0
auto_running = False
grille = {}
map_affiche = False 
vitesse_sim = 450  # vitesse moyenne au départ

BASE_DIR = os.path.dirname(__file__)

#récupérer les images proprement
def asset(*path):
    return os.path.join(BASE_DIR, "images", *path)

# couleurs utilisées pour les états (plus simple à modifier ici)
COLORS = {
    0: "#d5efbf",
    1: "#0077b6",
    2: "#bc4749",
    3: "#ff8fa3",
    4: "#ade8f4"
}

# toutes les directions possibles (y compris diagonales et sauts)
directions = [
    (0, 0), (-1, 0), (1, 0), (0, -1), (0, 1),
    (-2, 0), (2, 0), (0, -2), (0, 2),
    (-1, -1), (-1, 1), (1, -1), (1, 1)
]

# création de la fenêtre principale
fenetre = tk.Tk()
fenetre.title("V-Sim Pro - Grille et Décor")
fenetre.geometry(f"{LARGEUR_CANVAS + 400}x{LARGEUR_CANVAS}")
fenetre.configure(bg="#2c4260")

# panneau à droite (sliders + boutons)
frame_param = tk.Frame(fenetre, bg="#1d2b3e")
frame_param.pack(side="right", fill="both", expand=True)

tk.Label(frame_param, text="Paramètres", font=("Impact", 24),
         bg="#1d2b3e", fg="#ffffff").pack(pady=10)

# --- fonctions appelées par les sliders
def maj_transmission(val):
    global proba_transmission
    proba_transmission = float(val)

def maj_mort(val): 
    global prob_mort
    prob_mort = float(val)

def maj_guerison(val): 
    global prob_guerison
    prob_guerison = float(val)

def maj_pop_sains(val): 
    global probasains_initial
    probasains_initial = float(val)

def maj_pop_infectes(val): 
    global probainfecter_initiaux
    probainfecter_initiaux = float(val)

def maj_vitesse(val):
    global vitesse_sim
    # slider inversé → plus tu montes, plus ça va vite
    vitesse_sim = int(1050 - (int(val) * 100))

def maj_taille_grille(val):
    global TAILLE_GRILLE
    TAILLE_GRILLE = int(float(val))
    recommencer_simulation()

# reset propre de la simulation avec les nouveaux paramètres
def recommencer_simulation():
    starting_grid()
    if map_affiche:
        afficher_map()
    hitbox()
    mise_a_jour_skins()

# fonction générique pour créer un slider (évite de répéter 10 fois le même code)( aide par un tuto yt)
def creer_slider(parent, texte, command_func, from_, to, resolution, default_val):

    frame = tk.Frame(parent, bg="#1d2b3e")
    frame.pack(fill="x", padx=20, pady=2)
    
    lbl = tk.Label(frame, text=texte, bg="#1d2b3e", fg="#ffffff", font=("Arial", 10, "bold"))
    lbl.pack(side="top", anchor="w")
    
    slider = tk.Scale(frame, from_=from_, to=to, resolution=resolution, orient="horizontal",
                      bg="#1d2b3e", fg="#ffffff", troughcolor="#394867", 
                      activebackground="#ade8f4", highlightthickness=0,
                      command=command_func)
    slider.set(default_val)
    slider.pack(side="top", fill="x")
    return slider

# --- sliders UI
frame_sliders = tk.Frame(frame_param, bg="#1d2b3e")
frame_sliders.pack(fill="both", expand=True, pady=5)

creer_slider(frame_sliders, "Transmission Infection (0 à 1)", maj_transmission, 0.0, 1.0, 0.01, proba_transmission)
creer_slider(frame_sliders, "Chance de Guérison (0 à 0.1)", maj_guerison, 0.0, 0.1, 0.005, prob_guerison)
creer_slider(frame_sliders, "Mortalité (0 à 0.1)", maj_mort, 0.0, 0.1, 0.001, prob_mort)
creer_slider(frame_sliders, "Vitesse Auto (1 à 10)", maj_vitesse, 1, 10, 1, 5)

# petite séparation visuelle
tk.Frame(frame_sliders, bg="#394867", height=2).pack(fill="x", padx=20, pady=10)

creer_slider(frame_sliders, "Pop. Initiale Sains", maj_pop_sains, 0.0, 0.5, 0.01, probasains_initial)
creer_slider(frame_sliders, "Pop. Initiale Infectés", maj_pop_infectes, 0.0, 0.5, 0.01, probainfecter_initiaux)
creer_slider(frame_sliders, "Taille de la Ville (15 à 40)", maj_taille_grille, 15, 40, 1, TAILLE_GRILLE)

# --- boutons
frame_boutons = tk.Frame(frame_param, bg="#1d2b3e")
frame_boutons.pack(pady=10)

bouton_auto = tk.Button(frame_boutons, text="▶▶ Simuler Auto",
                        font=("Arial", 14, "bold"), bg="#81b29a", fg="#ffffff",
                        activebackground="#a8dadc", relief="flat")
bouton_auto.pack(side="top", fill="x", padx=20, pady=5)

bouton_propagation = tk.Button(frame_boutons, text="▶ Simuler 1 Tour",
                                font=("Arial", 14, "bold"), bg="#0077b6", fg="#ffffff",
                                activebackground="#ade8f4", relief="flat")
bouton_propagation.pack(side="top", fill="x", padx=20, pady=5)

bouton_reset = tk.Button(frame_boutons, text="🔄 Recommencer", command=recommencer_simulation,
                         font=("Arial", 12), bg="#bc4749", fg="#ffffff",
                         activebackground="#ff8fa3", relief="flat")
bouton_reset.pack(side="top", fill="x", padx=20, pady=5)

btn_map = tk.Button(frame_boutons, text="🗺  Afficher Map",
                    font=("Arial", 12), bg="#394867", fg="#ffffff", relief="flat")
btn_map.pack(side="top", fill="x", padx=20, pady=5)

# zone principale (la grille)
canvas = tk.Canvas(fenetre, width=LARGEUR_CANVAS, height=LARGEUR_CANVAS,
                   bg="#778DA9", highlightthickness=0)
canvas.pack(side="left")

# charge les images et les adapte à la taille actuelle des cases
def charger_et_adapter_images():
    global img_bonhomme, img_bonhomme2
    taille_case_px = LARGEUR_CANVAS // TAILLE_GRILLE

    try:
        img_sain_orig = tk.PhotoImage(file=asset("Perso 1.png"))
        ratio_sain = max(1, img_sain_orig.width() // (taille_case_px * 1))
        img_bonhomme = img_sain_orig.subsample(int(ratio_sain))
        
        img_infect_orig = tk.PhotoImage(file=asset("Perso 2.png"))
        ratio_infect = max(1, img_infect_orig.width() // (taille_case_px * 1))
        img_bonhomme2 = img_infect_orig.subsample(int(ratio_infect))

        # éviter que Python supprime les images
        canvas.image_perso = img_bonhomme
        canvas.image_perso2 = img_bonhomme2
        
    except Exception as e:
        img_bonhomme = None
        img_bonhomme2 = None
        print(f"Erreur de chargement d'image : {e}")

# chargement de la map (si dispo)
try:
    img_map_originale = tk.PhotoImage(file=asset("map1.png"))
    w = img_map_originale.width()
    ratio_map = max(1, w // LARGEUR_CANVAS)
    img_map = img_map_originale.subsample(ratio_map)
    canvas.image_map = img_map
except Exception as e:
    img_map = None

# remet les bons layers (sinon Tkinter fait n’importe quoi parfois)
def _fix_zorder():
    canvas.tag_lower("sol")
    if map_affiche:
        canvas.tag_raise("map")
    canvas.tag_raise("personnage")

# update visuel des cases
def verification_des_couleur():
    for donnes in grille.values():
        etat = donnes["etat"]
        if etat in COLORS:
            canvas.itemconfig(donnes["id_canvas"], fill=COLORS[etat])
    _fix_zorder()

# création complète de la grille
def starting_grid():
    global nombre_de_simulations
    canvas.delete("sol", "personnage")
    grille.clear()
    
    charger_et_adapter_images()
    
    taille_auto = LARGEUR_CANVAS / TAILLE_GRILLE

    # génération des cases
    for lig in range(TAILLE_GRILLE):
        for col in range(TAILLE_GRILLE):
            x1, y1 = col * taille_auto, lig * taille_auto
            grille[(lig, col)] = {
                "x": x1, "y": y1,
                "etat": 0,
                "type_de_perso": None,
                "immunite": 0,
                "id_canvas": None,
                "id_image_perso": None,
            }
            rect_id = canvas.create_rectangle(
                x1, y1, x1 + taille_auto, y1 + taille_auto,
                fill=COLORS[0], outline="#394867", tags="sol"
            )
            grille[(lig, col)]["id_canvas"] = rect_id

    # spawn des sains
    for coord, donnes in grille.items():
        if random.random() < probasains_initial:
            donnes["etat"] = 1
            donnes["type_de_perso"] = "sain"
            placer_personnage(coord[0], coord[1])

    # spawn des infectés
    for coord, donnes in grille.items():
        if random.random() < probainfecter_initiaux:
            donnes["etat"] = 2
            donnes["type_de_perso"] = "infecte"
            placer_personnage(coord[0], coord[1])

    # sécurité : au moins 3 infectés
    infectes_actuels = [c for c, d in grille.items() if d["etat"] == 2]
    
    while len(infectes_actuels) < 3:
        lig_h = random.randint(0, TAILLE_GRILLE - 1)
        col_h = random.randint(0, TAILLE_GRILLE - 1)
        case_h = grille[(lig_h, col_h)]
        if case_h["etat"] == 0:
            case_h["etat"] = 2
            case_h["type_de_perso"] = "infecte"
            placer_personnage(lig_h, col_h)
            infectes_actuels.append((lig_h, col_h))

    hitbox()
    mise_a_jour_skins()

# dessine un perso sur une case
def placer_personnage(lig, col):
    if (lig, col) in grille:
        case = grille[(lig, col)]
        taille_case = LARGEUR_CANVAS / TAILLE_GRILLE
        cx = case["x"] + taille_case / 2
        cy = case["y"] + taille_case / 2
        
        image_a_utiliser = img_bonhomme
        if case["etat"] == 2:
            image_a_utiliser = img_bonhomme2
            
        if image_a_utiliser:
            id_img = canvas.create_image(cx, cy, image=image_a_utiliser,
                                         anchor="center", tags="personnage")
            case["id_image_perso"] = id_img

# affiche la map en fond
def afficher_map():
    if img_map:
        cx = LARGEUR_CANVAS / 2
        cy = LARGEUR_CANVAS / 2
        canvas.create_image(cx, cy, image=img_map,
                            anchor="center", tags="map")
        _fix_zorder()

def cacher_map():
    canvas.delete("map")

# toggle affichage map
def toggle_map():
    global map_affiche
    map_affiche = not map_affiche

    if map_affiche:
        btn_map.config(text="🗺  Cacher Map", bg="#ef4444")
        afficher_map()
    else:
        btn_map.config(text="🗺  Afficher Map", bg="#394867")
        cacher_map()

# calcule les zones autour des persos
def hitbox():
    for donnes in grille.values():
        if donnes["etat"] in [3, 4]:
            donnes["etat"] = 0

    for (lig, col), donnes in grille.items():
        if donnes["etat"] == 2:
            for dx, dy in directions:
                nl, nc = lig + dx, col + dy
                if (nl, nc) in grille and grille[(nl, nc)]["etat"] in [0, 4]:
                    grille[(nl, nc)]["etat"] = 3
        
        elif donnes["etat"] == 1:
            for dx, dy in directions:
                nl, nc = lig + dx, col + dy
                if (nl, nc) in grille and grille[(nl, nc)]["etat"] == 0:
                    grille[(nl, nc)]["etat"] = 4

    verification_des_couleur()

# déplacement des persos sans collisions
def deplacement():
    mouvements = []
    cases_reservees = set()

    for coord, donnes in grille.items():
        if donnes["etat"] in [1, 2]:
            cases_reservees.add(coord)

    coords_persos = [c for c, d in grille.items() if d["etat"] in [1, 2]]
    random.shuffle(coords_persos)

    for (lig, col) in coords_persos:
        options_directions = directions[1:]
        random.shuffle(options_directions)
        
        for dx, dy in options_directions:
            nl, nc = lig + dx, col + dy
            nouvelle_pos = (nl, nc)
            
            if nouvelle_pos in grille and nouvelle_pos not in cases_reservees:
                mouvements.append(((lig, col), nouvelle_pos))
                cases_reservees.remove((lig, col))
                cases_reservees.add(nouvelle_pos)
                break

    taille_case = LARGEUR_CANVAS / TAILLE_GRILLE

    for depart, arrivee in mouvements:
        case_dep = grille[depart]
        case_arr = grille[arrivee]

        case_arr["etat"] = case_dep["etat"]
        case_arr["type_de_perso"] = case_dep["type_de_perso"]
        case_arr["immunite"] = case_dep.get("immunite", 0)
        case_arr["id_image_perso"] = case_dep["id_image_perso"]

        case_dep["etat"] = 0
        case_dep["type_de_perso"] = None
        case_dep["id_image_perso"] = None

        id_img = case_arr["id_image_perso"]
        if id_img:
            nx = case_arr["x"] + taille_case / 2
            ny = case_arr["y"] + taille_case / 2
            canvas.coords(id_img, nx, ny)

    hitbox()
    verification_des_couleur()

# gestion de l'infection
def gerer_infection():
    for (lig, col), donnes in grille.items():
        if donnes["etat"] == 1:
            for dx, dy in directions:
                nl, nc = lig + dx, col + dy
                if (nl, nc) in grille and grille[(nl, nc)]["etat"] == 2:
                    if random.random() < proba_transmission:
                        donnes["etat"] = 2
                        donnes["type_de_perso"] = "infecte"
                    break

    hitbox()
    verification_des_couleur()

def chance_de_mort():
    for (lig, col), donnes in grille.items():
        if donnes["etat"] == 2:
            if random.random() < prob_mort:
                donnes["etat"] = 0
                donnes["type_de_perso"] = None
                if donnes["id_image_perso"]:
                    canvas.delete(donnes["id_image_perso"])
                    donnes["id_image_perso"] = None

    hitbox()
    verification_des_couleur()

def chance_de_guerison():
    for (lig, col), donnes in grille.items():
        if donnes["etat"] == 2:
            if random.random() < prob_guerison:
                donnes["etat"] = 1
                donnes["type_de_perso"] = "sain"

    hitbox()
    verification_des_couleur()

# update visuel des skins
def mise_a_jour_skins():
    for (lig, col), donnes in grille.items():
        id_img = donnes["id_image_perso"]
        
        if id_img is not None:
            if donnes["etat"] == 2:
                canvas.itemconfig(id_img, image=img_bonhomme2)
            elif donnes["etat"] == 1:
                canvas.itemconfig(id_img, image=img_bonhomme)

# un tour complet de simulation
def tour_de_simulation():
    deplacement()
    gerer_infection()
    chance_de_mort()
    chance_de_guerison()
    mise_a_jour_skins()

# boucle auto
def boucle_automatique():
    if auto_running:
        tour_de_simulation()
        fenetre.after(vitesse_sim, boucle_automatique)

# play / pause
def toggle_auto():
    global auto_running
    auto_running = not auto_running
    
    if auto_running:
        bouton_auto.config(text="⏸  Pause", bg="#e07a5f", fg="#ffffff")
        boucle_automatique()
    else:
        bouton_auto.config(text="▶▶ Simuler Auto", bg="#81b29a", fg="#ffffff")

# connexions boutons
bouton_propagation.config(command=tour_de_simulation)
btn_map.config(command=toggle_map)
bouton_auto.config(command=toggle_auto)

# lancement
starting_grid()
afficher_map()
hitbox()

fenetre.mainloop()