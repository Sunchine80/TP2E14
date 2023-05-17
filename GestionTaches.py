from logging import RootLogger
import tkinter.messagebox as messagebox
import tkinter as tk
from datetime import datetime
from tkcalendar import Calendar, DateEntry

taches = []

confirm_button = None
cancel_button = None
cal = None  # définir la variable globale

def load_taches():
    try:
        with open("tac.txt", "r") as file:
            for line in file:
                if " - " in line:
                    tache, date = line.strip().split(" - ")
                    taches.append((tache, date))
    except FileNotFoundError:
        pass

def save_taches():
    with open("tac.txt", "w") as file:
        for tache, date in taches:
            file.write(f"{tache} - {date}\n")    
load_taches()

def add_tache():
    try:
        tache = tache_entree.get()
        date = date_entree.get_date()
        if date is not None:
            date = date.strftime("%Y-%m-%d")
        else:
            date = None
        taches.append((tache, date))
        tache_list.insert(tk.END, f"{date} - {tache}")
        tache_entree.delete(0, tk.END)
        date_entree.set_date(None) # Réinitialisation de la date 
        save_taches()

    except Exception as e:      
        print(f"An error occurred: {e}")

def remove_tache():
    tache = tache_list.get(tk.ACTIVE)
    for i in range(len(taches)):
        if taches[i][1] + " - " + taches[i][0] == tache:
            confirmed = messagebox.askyesno("Confirmation", f"Voulez-vous vraiment supprimer la tâche '{tache}'?")
            if confirmed:
                taches.pop(i)
                tache_list.delete(tk.ACTIVE)
                save_taches()
            break    
    save_taches()  # enregistrer les tâches

def modify_tache():
    global confirm_button, cancel_button

    tache = tache_list.get(tk.ACTIVE)
    tache_entree.delete(0, tk.END)
    tache_entree.insert(tk.END, tache.split(" - ")[1])
    date_entree.delete(0, tk.END)
    date_entree.insert(tk.END, tache.split(" - ")[0])
   
    if confirm_button is None:
        confirm_button = tk.Button(button_frame, text="Confirm", command=confirm_tache)
        confirm_button.pack(pady=5)
    else:
        confirm_button.config(state=tk.NORMAL)      
        
    if cancel_button is None:
        cancel_button = tk.Button(button_frame, text="Cancel", command=cancel_update)
        cancel_button.pack(pady=5)
    else:
        cancel_button.config(state=tk.NORMAL)
        # Désactivez le bouton "Confirmer" et "Annuler" si aucune tâche n'est sélectionnée
    if tache == '':
        confirm_button.config(state=tk.DISABLED)
        cancel_button.config(state=tk.DISABLED)
        # Activez le bouton "Confirmer" et "Annuler" si une tâche est sélectionnée
    else:
        confirm_button.config(state=tk.NORMAL)
        cancel_button.config(state=tk.NORMAL)

def confirm_tache():
    tache = tache_list.get(tk.ACTIVE)
    for i in range(len(taches)):
        if taches[i][1] + " - " + taches[i][0] == tache:
            taches[i] = (tache_entree.get(), date_entree.get())
            break   
    tache_list.delete(tk.ACTIVE)  # supprimer l'ancienne tâche de la liste des tâches
    tache_list.insert(tk.END, taches[i][1] + " - " + taches[i][0])  # ajouter la tâche modifiée à la fin de la liste    
    tache_entree.delete(0, tk.END)
    date_entree.delete(0, tk.END)
    confirm_button.config(state=tk.DISABLED)
    cancel_button.config(state=tk.DISABLED)
    add_button.config(state=tk.NORMAL)
    remove_button.config(state=tk.NORMAL)
    save_taches()  # enregistrer les tâches

def cancel_update():
    tache_entree.delete(0, tk.END)
    date_entree.delete(0, tk.END)
    confirm_button.config(state=tk.DISABLED)
    cancel_button.config(state=tk.DISABLED)
    
def list_taches():
    tache_list.delete(0, tk.END)
    for tache, date in taches:
        tache_list.insert(tk.END, f"{date} - {tache}")

root = tk.Tk()
root.title("Gestion de Tâches")
root.configure(background='white')

menu_frame = tk.Frame(root, bg='white')
menu_frame.pack(fill=tk.BOTH, expand=True)

titre_frame = tk.Frame(menu_frame, bg='white')
titre_frame.pack(fill=tk.X)

title_label = tk.Label(titre_frame, text="Gestion de Tâches", font=("Arial", 40), bg='white', fg='black')
title_label.pack(pady=10)

list_frame = tk.Frame(menu_frame, width=100, bg='white')
list_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

tache_list = tk.Listbox(list_frame, width=50, bg='black', fg='white', font=("Arial" , 14))
tache_list.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

scrollbar = tk.Scrollbar(list_frame)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

tache_list.config(yscrollcommand=scrollbar.set)
scrollbar.config(command=tache_list.yview)

button_frame = tk.Frame(menu_frame, width=40, bg='white')
button_frame.pack(side=tk.RIGHT, fill=tk.Y)

tache_label = tk.Label(button_frame, text="Entrez une tâche à faire", font=("Arial", 14), fg="black")
tache_label.pack()
tache_entree = tk.Entry(button_frame, width=30, bg='white', fg='black', font=("Arial", 12))
tache_entree.pack(pady=5)
tache_entree.config(text="Tâche 1\nTâche 2\nTâche 3")

cal = Calendar(button_frame, selectmode="day", date_pattern="yyyy-mm-dd", show=False)

date_entree = DateEntry(button_frame, width=22, background='darkblue',
                        foreground='white', date_pattern="yyyy-mm-dd", calendar=cal)
date_entree.pack(padx=10, pady=5)
date_entree.focus_set()

add_button = tk.Button(button_frame, text="Ajouter une tâche", command=add_tache, width=18, bg='green', fg='white')
add_button.pack(pady=5)

remove_button = tk.Button(button_frame, text="Supprimer une tâche", command=remove_tache,width=18, bg='red', fg='white')
remove_button.pack(pady=5)

modify_button = tk.Button(button_frame, text="Modifier une tâche", command=modify_tache,width=18, bg='orange', fg='white')
modify_button.pack(pady=5)

list_button = tk.Button(button_frame, text="Liste des tâches", command=list_taches,width=18, bg='blue', fg='white')
list_button.pack(pady=5)

root.mainloop()
