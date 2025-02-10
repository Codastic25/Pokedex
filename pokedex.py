import tkinter as tk
from PIL import Image, ImageTk
import requests
import io

#ICI LA FENETRE DE POKEDEX
root = tk.Tk()
root.title("Pokedex Aurian")
root.geometry("600x1000")
root.minsize(600, 1000)

# TOUTES LES FONCTIONS

# Pour chercher un pokemon avec son nom ou id
def search_pokemon():
    pokemon = entry_pokemon.get()
    print(f"Recherche du Pokémon : {pokemon}")  # Affiche dans la console (pour l'instant)

# Navigation entre les pages
def next_page():
    global current_page
    current_page += 1
    load_sprite()

def previous_page():
    global current_page
    if current_page > 0:
        current_page -= 1
        load_sprite()

# Ajout des variables globales
current_page = 0
pokemons_per_page = 6

# Charger les Pokémons pour la page actuelle
def load_sprite():
    global current_page

    # Effacer les widgets existants
    for widget in frame_pokemons.winfo_children():
        widget.destroy()

    start_id = current_page * pokemons_per_page + 1
    end_id = start_id + pokemons_per_page

    for poke_id in range(start_id, end_id):
        try:
            url = f"https://pokeapi.co/api/v2/pokemon/{poke_id}"
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()

            pokemon_name = data['name'].capitalize()
            pokemon_number = data['id']
            pokemon_types = [t['type']['name'] for t in data['types']]
            pokemon_types_str = ', '.join(pokemon_types)

            image_url = f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/{poke_id}.png"
            img_data = requests.get(image_url).content

            img = Image.open(io.BytesIO(img_data))
            img = img.resize((100, 100))
            img_tk = ImageTk.PhotoImage(img)

            frame = tk.Frame(frame_pokemons)
            frame.pack(pady=5)

            label_image = tk.Label(frame, image=img_tk)
            label_image.image = img_tk
            label_image.pack(side="left", padx=10)

            label_name = tk.Label(frame, text=f"#{pokemon_number} - {pokemon_name} - Type : {pokemon_types_str}")
            label_name.pack(side="left")

            # Bouton informations
            info_button = tk.Button(frame, text="i", command=lambda poke_id=poke_id: newScreenInfos(poke_id))
            info_button.pack(side="right", padx=5)
            
        except Exception as e:
            print(f"Erreur de chargement pour le Pokémon {poke_id} : {e}")


# la fonction pour la pop-up des infos de chaque pokémon
def newScreenInfos (poke_id):

        url = f"https://pokeapi.co/api/v2/pokemon/{poke_id}"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        pokemon_name = data['name'].capitalize()
        pokemon_number = data['id']
        pokemon_types = [t['type']['name'] for t in data['types']]
        pokemon_types_str = ', '.join(pokemon_types)

        # Chargement des images
        image_url = f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/{poke_id}.png"
        img_data = requests.get(image_url).content

        image_shiny_url = f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/shiny/{poke_id}.png"
        img_data_shiny = requests.get(image_shiny_url).content

        img = Image.open(io.BytesIO(img_data)).resize((100, 100))
        img_tk = ImageTk.PhotoImage(img)

        img_shiny = Image.open(io.BytesIO(img_data_shiny)).resize((100, 100))
        img_tk_shiny = ImageTk.PhotoImage(img_shiny)

        image_back_url = f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/back/{poke_id}.png"
        img_data_back = requests.get(image_back_url).content

        image_back_shiny_url = f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/back/shiny/{poke_id}.png"
        img_data_back_shiny = requests.get(image_back_shiny_url).content

        img_back = Image.open(io.BytesIO(img_data_back)).resize((100, 100))
        img_tk_back = ImageTk.PhotoImage(img_back)

        img_back_shiny = Image.open(io.BytesIO(img_data_back_shiny)).resize((100, 100))
        img_tk_back_shiny = ImageTk.PhotoImage(img_back_shiny)


        # Création de la fenêtre après chargement
        root2 = tk.Toplevel()
        root2.title("Informations Pokémon")
        root2.geometry("600x700")
        root2.minsize(600, 700)

        # Affichage des informations
        
        #les sprites
        tk.Label(root2, image=img_tk).pack(pady=10)
        tk.Label(root2, image=img_tk_shiny).pack(pady=10)
        tk.Label(root2, image=img_tk_back).pack(pady=10)
        tk.Label(root2, image=img_tk_back_shiny).pack(pady=10)

        #les infos globales
        tk.Label(root2, text=f"#{pokemon_number}").pack(pady=5)
        tk.Label(root2, text=f"#{pokemon_name}").pack(pady=5)
        tk.Label(root2, text=f"Types : {pokemon_types_str}").pack(pady=5)

        # Sauvegarde des références des images
        root2.img_tk = img_tk
        root2.img_tk_shiny = img_tk_shiny
        root2.img_tk_back = img_tk_back
        root2.img_tk_back_shiny = img_tk_back_shiny


# Label pour indiquer à l'utilisateur quoi faire
label_instruction = tk.Label(root, text="Entrez le nom ou le numéro du Pokémon :")
label_instruction.pack(pady=10)

# L'input
entry_pokemon = tk.Entry(root, width=30)
entry_pokemon.pack(pady=5)

#pour chercher le pokemon 
bouton_recherche = tk.Button(root, text = "Rechercher", command=search_pokemon)
bouton_recherche.pack(pady=10)

#pour filtrer la recherche de pokemon 
bouton_filtre = tk.Button(root, text = "Trier")
bouton_filtre.pack(pady=10)

# Créer les boutons de navigation
button_previous = tk.Button(root, text="Page précédente", command=previous_page)
button_previous.pack(pady=5)

button_next = tk.Button(root, text="Page suivante", command=next_page)
button_next.pack(pady=5)

# Créer un cadre pour afficher les Pokémons
frame_pokemons = tk.Frame(root)
frame_pokemons.pack(pady=10)

load_sprite()

root.mainloop()