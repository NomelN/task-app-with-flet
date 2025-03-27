import flet as ft

def main(page: ft.Page):
    page.title = "To-Do App"
    page.vertical_alignment = ft.MainAxisAlignment.START

    tasks = []

    def add_task(e):
        if task_input.value.strip(): # type: ignore
            new_task = ft.Checkbox(label=task_input.value)
            tasks.append(new_task)
            task_list.controls.append(new_task)
            task_input.value = ""
            page.update()

    def delete_completed(e):
        nonlocal tasks
        # Ne garder que les tâches non cochées
        tasks = [task for task in tasks if not task.value]
        task_list.controls = tasks
        page.update()

    task_input = ft.TextField(
        label="Nouvelle tâche",
        hint_text="Entrez une nouvelle tâche",
        on_submit=add_task,
        expand=True
    )

    add_button = ft.ElevatedButton(text="Ajouter", bgcolor="green", color="white", on_click=add_task)
    delete_button = ft.OutlinedButton(text="Supprimer", on_click=delete_completed, style=ft.ButtonStyle(color="white", bgcolor="red")) 

    task_list = ft.Column()

    page.add(
        ft.Row([task_input, add_button]),
        task_list,
        delete_button
    )

ft.app(target=main)
