import flet as ft
import json
import os
from datetime import datetime

# Définir le chemin du fichier de sauvegarde
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TASKS_FILE = os.path.join(BASE_DIR, "..", "storage", "data", "tasks.json")

# Charger les tâches depuis le fichier de sauvegarde
def load_tasks():
    try:
        with open(TASKS_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return []
    
# Sauvegarder les tâches dans le fichier de sauvegarde
def save_tasks(tasks):
    data = [
        {
            "label": task.data["label"],
            "created_at": task.data["created_at"], 
            "done": task.value,
        } for task in tasks
    ]
    os.makedirs(os.path.dirname(TASKS_FILE), exist_ok=True)
    with open(TASKS_FILE, "w") as f:
        json.dump(data, f, indent=4)

# Générer le label affiché avec la date de création
def format_label(label, created_at):
    return f"{label} : {created_at}"


def main(page: ft.Page):
    page.title = "To-Do App"
    page.vertical_alignment = ft.MainAxisAlignment.START
    page.theme_mode = ft.ThemeMode.LIGHT # thème initail

    tasks = []
    task_list = ft.Column()

    def refresh():
        task_list.controls = tasks
        page.update()

    def toggle_theme(e):
        if page.theme_mode == ft.ThemeMode.LIGHT:
            page.theme_mode = ft.ThemeMode.DARK
            theme_button.icon = ft.icons.WB_SUNNY
        else:
            page.theme_mode = ft.ThemeMode.LIGHT
            theme_button.icon = ft.icons.NIGHTLIGHT
        page.update()

    def add_task(e):
        if task_input.value.strip(): # type: ignore
            created_at = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            label_text = task_input.value.strip() # type: ignore
            full_label = format_label(label_text, created_at)

            new_task = ft.Checkbox(label=full_label)
            new_task.data = {
                "label": label_text,
                "created_at": created_at
            }
            new_task.on_change = lambda e: save_tasks(tasks)
            tasks.append(new_task)
            task_input.value = ""
            refresh()
            save_tasks(tasks)

    def delete_completed(e):
        nonlocal tasks
        # Ne garder que les tâches non cochées
        tasks = [task for task in tasks if not task.value]
        refresh()
        save_tasks(tasks)

    # Charger les tâches depuis le fichier de sauvegarde
    def load_saved_tasks():
        existing = load_tasks()
        for item in existing:
            full_label = format_label(item["label"], item["created_at"])
            checkbox = ft.Checkbox(label=full_label, value=item["done"])
            checkbox.data = {
                "label": item["label"],
                "created_at": item["created_at"]
            }
            checkbox.on_change = lambda e: save_tasks(tasks)
            tasks.append(checkbox)
        refresh()
        

    task_input = ft.TextField(
        label="Nouvelle tâche",
        hint_text="Entrez une nouvelle tâche",
        on_submit=add_task,
        expand=True
    )

    add_button = ft.ElevatedButton(
        text="Ajouter", 
        bgcolor="green", 
        color="white", 
        on_click=add_task
    )
    delete_button = ft.OutlinedButton(
        text="Supprimer", 
        on_click=delete_completed, 
        style=ft.ButtonStyle(color="white", bgcolor="red")
    ) 

    theme_button = ft.IconButton(
        icon=ft.icons.DARK_MODE,
        tooltip="Changer de thème",
        on_click=toggle_theme
    )

    page.add(
        ft.Row([task_input, add_button, theme_button]),
        task_list,
        delete_button
    )

    load_saved_tasks()

ft.app(target=main)
