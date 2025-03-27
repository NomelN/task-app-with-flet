import flet as ft
import json
import os

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
    data = [{"label": task.label, "done": task.value} for task in tasks]
    os.makedirs(os.path.dirname(TASKS_FILE), exist_ok=True)
    with open(TASKS_FILE, "w") as f:
        json.dump(data, f, indent=4)


def main(page: ft.Page):
    page.title = "To-Do App"
    page.vertical_alignment = ft.MainAxisAlignment.START

    tasks = []
    task_list = ft.Column()

    def refresh():
        task_list.controls = tasks
        page.update()

    def add_task(e):
        if task_input.value.strip(): # type: ignore
            new_task = ft.Checkbox(label=task_input.value)
            tasks.append(new_task)
            task_list.controls.append(new_task)
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
            checkbox = ft.Checkbox(label=item["label"], value=item["done"])
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

    page.add(
        ft.Row([task_input, add_button]),
        task_list,
        delete_button
    )

    load_saved_tasks()

ft.app(target=main)
