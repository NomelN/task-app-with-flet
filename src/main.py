import flet as ft


def main(page: ft.Page):
    page.title = "Task App"
    page.vertical_aligment = ft.MainAxisAlignment.START # type: ignore

    tasks = []

    def add_task(e):
        if task_input.value:
            new_task = ft.Checkbox(label=task_input.value)
            tasks.append(new_task)
            task_list.controls.append(new_task)
            task_input.value = ""
            page.update()

    # Champ de saisie
    task_input = ft.TextField(
        label="Nouvelle tâche",
        hint_text="Entrez une nouvelle tâche",
        on_submit=add_task,
        expand=True,
    )

    # Bouton d'ajout
    add_button = ft.ElevatedButton(text="Ajouter", on_click=add_task, bgcolor="green", color="white")

    # Liste des tâches
    task_list = ft.Column()

    # Ajout des éléments à la page
    page.add(
        ft.Row([task_input, add_button]),
        task_list,
    )

ft.app(target=main)
