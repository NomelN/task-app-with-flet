import flet as ft
import json
import os
from datetime import datetime

# Chemin du fichier JSON
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TASKS_FILE = os.path.join(BASE_DIR, "..", "storage", "data", "tasks.json")


# Charger les tâches sauvegardées
def load_tasks():
    try:
        with open(TASKS_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return []


# Sauvegarder les tâches
def save_tasks(tasks):
    data = []
    for task in tasks:
        checkbox = task["checkbox"]
        data.append({
            "label": checkbox.data["label"],
            "created_at": checkbox.data["created_at"],
            "done": checkbox.value
        })
    os.makedirs(os.path.dirname(TASKS_FILE), exist_ok=True)
    with open(TASKS_FILE, "w") as f:
        json.dump(data, f, indent=4)


# Format affichage label + date
def format_label(label, created_at):
    return f"{label} : {created_at}"


def main(page: ft.Page):
    page.title = "TASK MANAGER"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.vertical_alignment = ft.MainAxisAlignment.START

    tasks = []
    task_list = ft.Column()

    def refresh():
        task_list.controls = [task["row"] for task in tasks]
        page.update()

    def toggle_theme(e):
        if page.theme_mode == ft.ThemeMode.LIGHT:
            page.theme_mode = ft.ThemeMode.DARK
            theme_button.icon = ft.Icons.WB_SUNNY
        else:
            page.theme_mode = ft.ThemeMode.LIGHT
            theme_button.icon = ft.Icons.NIGHTLIGHT
        page.update()

    def create_task(label, created_at, done=False):
        text_display = ft.Text(format_label(label, created_at), weight="bold", size=16, visible=True) # type: ignore
        text_field = ft.TextField(value=label, visible=False, expand=True, text_size=16) # type: ignore
        checkbox = ft.Checkbox(value=done)

        def toggle_edit(e):
            text_display.visible = not text_display.visible
            text_field.visible = not text_field.visible
            page.update()

        def save_edit(e):
            new_label = text_field.value.strip() # type: ignore
            if new_label:
                text_display.value = format_label(new_label, created_at)
                text_display.visible = True
                text_field.visible = False
                checkbox.data["label"] = new_label # type: ignore
                save_tasks(tasks)
                page.update()

        edit_button = ft.IconButton(icon=ft.Icons.EDIT, tooltip="Modifier", on_click=toggle_edit)
        save_button = ft.IconButton(icon=ft.Icons.SAVE, tooltip="Enregistrer", on_click=save_edit)

        # Séparer le contenu à gauche et les actions à droite
        row = ft.Row(
            [
                ft.Row([checkbox, text_display, text_field], expand=True, alignment=ft.MainAxisAlignment.START),
                ft.Row([edit_button, save_button])
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN
        )

        checkbox.data = {"label": label, "created_at": created_at}
        checkbox.on_change = lambda e: save_tasks(tasks)


        return {"row": row, "checkbox": checkbox}

    def add_task(e):
        if task_input.value.strip(): # type: ignore
            label_text = task_input.value.strip() # type: ignore
            created_at = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            task = create_task(label_text, created_at)
            tasks.append(task)
            task_input.value = ""
            refresh()
            save_tasks(tasks)

    def delete_completed(e):
        nonlocal tasks
        tasks = [task for task in tasks if not task["checkbox"].value]
        refresh()
        save_tasks(tasks)

    def load_saved_tasks():
        for item in load_tasks():
            label = item["label"]
            created_at = item.get("created_at", "Date inconnue")
            done = item["done"]
            task = create_task(label, created_at, done)
            tasks.append(task)
        refresh()

    # UI
    task_input = ft.TextField(label="Nouvelle tâche", hint_text="Entrez une nouvelle tâche", on_submit=add_task, expand=True)

    add_button = ft.ElevatedButton(text="Ajouter", bgcolor="green", color="white", on_click=add_task, style=ft.ButtonStyle(text_style=ft.TextStyle(size=20))) # type: ignore

    delete_button = ft.OutlinedButton(
        text="Supprimer", 
        on_click=delete_completed,
        style=ft.ButtonStyle(color="white", bgcolor="red", overlay_color="pink", text_style=ft.TextStyle(size=18))
    )

    theme_button = ft.IconButton(icon=ft.Icons.DARK_MODE, tooltip="Changer de thème", on_click=toggle_theme)

    page.add(
        ft.Row([task_input, add_button, theme_button]),
        task_list,
        ft.Container(delete_button, alignment=ft.alignment.center),
    )

    load_saved_tasks()


ft.app(target=main)
