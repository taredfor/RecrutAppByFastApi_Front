import flet as ft
from flet_core.alignment import center

class RegistrationFormTextField(ft.TextField):
    def __init__(self, label, ref):
        super().__init__(ref=ref, label=label, autofocus=True, text_align=center, width=200, height=50)

class Button(ft.ElevatedButton):
    def __init__(self, text, on_click, visible=True):
        super().__init__(text=text, on_click=on_click, url_target='_self', width=200, height=50, visible=visible)