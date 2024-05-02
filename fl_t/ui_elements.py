import flet as ft
from flet_core.alignment import center

class RegistrationFormTextField(ft.TextField):
    def __init__(self, label, ref):
        super().__init__(ref=ref, label=label, autofocus=True, text_align=center, width=200, height=50)


