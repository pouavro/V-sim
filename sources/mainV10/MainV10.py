import os
import tkinter as tk
import random




# --- CONFIGURATION ---
prob = 0.60
probainfecter = 0.01
TAILLE_GRILLE = 15
LARGEUR_CANVAS = 800
nombre_de_simulations = 0
auto_running = False
grille = {}
map_affiche = False  # État d'affichage de la map

BASE_DIR = os.path.dirname(__file__)

def asset(*path):
    return os.path.join(BASE_DIR, "images", *path)

# Couleurs SIR
COLORS = {
    0: "#f4f1de",   # Safe (Beige)
    1: "#a7c957",   # Terrain Sain (Vert)
    2: "#bc4749",   # Infecté (Rouge)
    3: "#b96f70"    # Hitbox Infecté (Rouge clair)
}

# Directions de déplacement
directions = [
    (0, 0), (-1, 0), (1, 0), (0, -1), (0, 1),
    (-2, 0), (2, 0), (0, -2), (0, 2),
    (-1, -1), (-1, 1), (1, -1), (1, 1)
]

# ────────────── FENÊTRE ──────────────
fenetre = tk.Tk()
fenetre.title("V-Sim Pro - Grille et Décor")
fenetre.geometry(f"{LARGEUR_CANVAS + 400}x{LARGEUR_CANVAS}")
fenetre.configure(bg="#2c4260")

# ────────────── Panneau droite ──────────────
frame_param = tk.Frame(fenetre, bg="#1d2b3e")
frame_param.pack(side="right", fill="both", expand=True)

tk.Label(frame_param, text="Paramètres", font=("Impact", 24),
         bg="#1d2b3e", fg="#ffffff").pack(pady=10)

frame_boutons = tk.Frame(frame_param, bg="#1d2b3e")
frame_boutons.pack(pady=10)

bouton_propagation = tk.Button(frame_boutons, text="Simuler",
                                font=("Arial", 15), bg="#394867", fg="#ffffff")
bouton_propagation.pack(side="left", padx=8)

bouton_deplacement = tk.Button(frame_boutons, text="Déplacement",
                                font=("Arial", 15), bg="#394867", fg="#ffffff")
bouton_deplacement.pack(side="left", padx=8)

# Bouton Map (séparé, en dessous)
btn_map = tk.Button(frame_param, text="🗺  Afficher Map",
                    font=("Arial", 12, "bold"), bg="#394867", fg="#ffffff")
btn_map.pack(pady=12)

# ────────────── Canvas (zone de jeu) ──────────────
canvas = tk.Canvas(fenetre, width=LARGEUR_CANVAS, height=LARGEUR_CANVAS,
                   bg="#778DA9", highlightthickness=0)
canvas.pack(side="left")

# ────────────── CHARGEMENT DES IMAGES ──────────────
# Les images doivent être dans le même dossier que ce script.
try:
    # Personnage
    img_bonhomme = tk.PhotoImage(file=asset("Perso 1.png"))
    taille_case_px = LARGEUR_CANVAS // TAILLE_GRILLE   # 30 px
    ratio_perso = max(1, img_bonhomme.width() // taille_case_px)
    img_bonhomme = img_bonhomme.subsample(ratio_perso)
    canvas.image_perso = img_bonhomme  # Empêche le garbage-collector
    print("Perso 1.png chargé.")
except Exception as e:
    img_bonhomme = None
    print(f"Perso 1.png introuvable ({e}) — les infectés seront sans icône.")

try:
    # Map décorative — on la redimensionne pour couvrir exactement le canvas
    img_map_originale = tk.PhotoImage(file=asset("map1.png"))
    w = img_map_originale.width()
    ratio_map = max(1, w // LARGEUR_CANVAS)
    img_map = img_map_originale.subsample(ratio_map)
    canvas.image_map = img_map  # Persistance
    print("map.png chargée.")
except Exception as e:
    img_map = None
    print(f"map.png introuvable ({e}).")

# ═══════════════════════════════════════════════════
#   COUCHES DU CANVAS (ordre z de bas en haut)
#
#   1. "sol"         — rectangles colorés (SIR)
#   2. "map"         — image décorative (optionnelle)
#   3. "personnage"  — icônes des infectés
#
#   Règle : après chaque opération qui pourrait
#   perturber l'ordre, on rappelle _fix_zorder().
# ═══════════════════════════════════════════════════

def _fix_zorder():
    """Garantit : sol < map < personnage."""
    canvas.tag_lower("sol")          # sol tout en bas
    if map_affiche:
        canvas.tag_raise("map")      # map au-dessus du sol
    canvas.tag_raise("personnage")   # persos tout en haut


# ────────────── FONCTIONS GRILLE ──────────────

def verification_des_couleur():
    """Rafraîchit les couleurs des cases selon leur état SIR."""
    for donnes in grille.values():
        etat = donnes["etat"]
        if etat in COLORS:
            canvas.itemconfig(donnes["id_canvas"], fill=COLORS[etat])
    # On remet l'ordre correct après chaque mise à jour visuelle
    _fix_zorder()


def starting_grid():
    """Initialise la grille et place les infectés de départ."""
    global nombre_de_simulations
    nombre_de_simulations = 0

    # On efface uniquement le sol et les persos, PAS la map
    canvas.delete("sol")
    canvas.delete("personnage")
    grille.clear()

    taille_auto = LARGEUR_CANVAS / TAILLE_GRILLE

    for lig in range(TAILLE_GRILLE):
        for col in range(TAILLE_GRILLE):
            x1 = col * taille_auto
            y1 = lig * taille_auto
            x2 = x1 + taille_auto
            y2 = y1 + taille_auto   # ← BUG corrigé (était y2 + taille_auto)

            grille[(lig, col)] = {
                "x": x1, "y": y1,
                "etat": 0,
                "couleur": COLORS[0],
                "id_canvas": None,
                "etats_initial": 0,
                "id_image_perso": None
            }

            # Rectangles semi-transparents via stipple pour laisser voir la map
            rect_id = canvas.create_rectangle(
                x1, y1, x2, y2,
                fill=COLORS[0],
                stipple="gray50",    # ← 50 % transparent : la map transparaît
                outline="#394867",
                width=1,
                tags="sol"
            )
            grille[(lig, col)]["id_canvas"] = rect_id

    # Terrain sain (vert)
    for coord in grille:
        if random.random() < prob:
            grille[coord]["etat"] = 1
            grille[coord]["etats_initial"] = 1

    # Infectés initiaux
    for coord in grille:
        if random.random() < probainfecter:
            grille[coord]["etat"] = 2
            placer_personnage(coord[0], coord[1])

    verification_des_couleur()


def placer_personnage(lig, col):
    """Dessine l'icône d'un infecté sur sa case (tag 'personnage')."""
    if img_bonhomme and (lig, col) in grille:
        taille_case = LARGEUR_CANVAS / TAILLE_GRILLE
        case = grille[(lig, col)]
        cx = case["x"] + taille_case / 2
        cy = case["y"] + taille_case / 2
        id_img = canvas.create_image(cx, cy, image=img_bonhomme,
                                     anchor="center", tags="personnage")
        case["id_image_perso"] = id_img


# ────────────── FONCTION MAP (décor) ──────────────

def afficher_map():
    """
    Dessine la map décorative entre le sol et les personnages.
    Tag utilisé : 'map'
    """
    if img_map:
        cx = LARGEUR_CANVAS / 2
        cy = LARGEUR_CANVAS / 2
        canvas.create_image(cx, cy, image=img_map,
                            anchor="center", tags="map")
        _fix_zorder()   # sol < map < personnage


def cacher_map():
    """Supprime uniquement les éléments taggués 'map'."""
    canvas.delete("map")


def toggle_map():
    """Bascule l'affichage de la map décorative."""
    global map_affiche
    map_affiche = not map_affiche

    if map_affiche:
        btn_map.config(text="🗺  Cacher Map", bg="#ef4444")
        afficher_map()
    else:
        btn_map.config(text="🗺  Afficher Map", bg="#394867")
        cacher_map()


# ────────────── LOGIQUE DE JEU ──────────────

def hitbox():
    """Calcule et colore la zone d'infection autour de chaque infecté."""
    # Réinitialisation des hitbox précédentes
    for donnes in grille.values():
        if donnes["etat"] == 3:
            donnes["etat"] = donnes["etats_initial"]

    # Calcul des cases touchées
    nouveaux_infectes = []
    for (lig, col), donnes in grille.items():
        if donnes["etat"] == 2:
            for dx, dy in directions:
                nl, nc = lig + dx, col + dy
                if (nl, nc) in grille and grille[(nl, nc)]["etat"] != 2:
                    nouveaux_infectes.append((nl, nc))

    for pos in nouveaux_infectes:
        grille[pos]["etat"] = 3

    verification_des_couleur()


def deplacement():
    """Déplace chaque infecté vers une case adjacente valide."""
    mouvements = []
    for (lig, col), donnes in grille.items():
        if donnes["etat"] == 2:
            dx, dy = random.choice(directions[1:])  # Exclut (0,0)
            nl, nc = lig + dx, col + dy
            if (nl, nc) in grille and grille[(nl, nc)]["etat"] in [1, 3]:
                mouvements.append(((lig, col), (nl, nc)))

    taille_case = LARGEUR_CANVAS / TAILLE_GRILLE
    for depart, arrivee in mouvements:
        case_dep = grille[depart]
        case_arr = grille[arrivee]

        # Mise à jour états
        case_arr["etat"] = 2
        case_dep["etat"] = case_dep["etats_initial"]

        # Déplacement visuel de l'icône
        id_img = case_dep["id_image_perso"]
        if id_img:
            nx = case_arr["x"] + taille_case / 2
            ny = case_arr["y"] + taille_case / 2
            canvas.coords(id_img, nx, ny)
            case_arr["id_image_perso"] = id_img
            case_dep["id_image_perso"] = None

    hitbox()
    verification_des_couleur()


# ────────────── CONNEXION BOUTONS ──────────────
bouton_propagation.config(command=hitbox)
bouton_deplacement.config(command=deplacement)
btn_map.config(command=toggle_map)

# ────────────── LANCEMENT ──────────────
starting_grid()
hitbox()


fenetre.mainloop()
