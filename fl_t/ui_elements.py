import flet as ft
from typing import Callable
from flet_core.alignment import center
import schedule
import time


class RegistrationFormTextField(
    ft.TextField):
    def __init__(self, label: str, ref: ft.Ref, incorrect_label: str = None,
                 outside_validator: Callable = None, parent_page: ft.Page = None,
                 good_validate_text: str = None, bad_validate_text: str =None):
        self.incorrect_label = incorrect_label
        self.validated = False
        self.outside_validator = outside_validator
        self.page = parent_page
        self.good_validate_text = good_validate_text
        self.bad_validate_text = bad_validate_text
        super().__init__(ref=ref, label=label, autofocus=True,
                         text_align=center, on_change=self.validate,
                         width=200, height=50)

    def validate(self, _value):
        self.validated = self.outside_validator(self.value)
        self.update_incorrect_label()

    def update_incorrect_label(self):
        if self.incorrect_label == None:
            return
        if self.validated == True:
            self.incorrect_label.color = "Green"
            self.incorrect_label.value = self.good_validate_text
        else:
            self.incorrect_label.color = "Red"
            self.incorrect_label.value = self.bad_validate_text
        self.page.update()


class RegistrationFormSecondPasswordTextField(RegistrationFormTextField):
    def __init__(self, label, ref, ref_main_password, incorrect_label=None,
                 outside_validator=None, parent_page=None,
                 good_validate_text=None, bad_validate_text=None):
        self.ref_main_password = ref_main_password
        super().__init__(label, ref, incorrect_label=incorrect_label,
                         outside_validator=outside_validator,
                         parent_page=parent_page,
                         good_validate_text=good_validate_text,
                         bad_validate_text=bad_validate_text)

    def validate(self, _value):
        if self.value == self.ref_main_password.current.value and self.ref_main_password.current.validated:
            self.validated = True
        else:
            self.validated = False
        self.update_incorrect_label()

    def update_incorrect_label(self):
        if not self.ref_main_password.current.validated:
            self.incorrect_label.value = "Enter correct main password"
            self.page.update()
            return
        super().update_incorrect_label()


class RegistrationFormMainPasswordTextField(RegistrationFormTextField):
    def __init__(self, label, ref, ref_second_password, incorrect_label=None,
                 outside_validator=None, parent_page=None,
                 good_validate_text=None, bad_validate_text=None):
        self.ref_second_password = ref_second_password
        super().__init__(label, ref,
                         incorrect_label=incorrect_label,
                         outside_validator=outside_validator,
                         parent_page=parent_page,
                         good_validate_text=good_validate_text,
                         bad_validate_text=bad_validate_text)

    def validate(self, _value):
        super().validate(_value)
        self.ref_second_password.current.validate(_value)
        #ref_second_password.current - object
        #ref_second_password.current.value - value


# ref_second_password -> ссылка на поле
# во всех методах ua-elements протипизировтаь каждый аргумент


class RegistrationFormTextFieldUserLoginPassword(ft.TextField):
    def __init__(self, label, ref):
        super().__init__(ref=ref, label=label, autofocus=True,
                         text_align=center, width=200, height=50)


class Button(ft.ElevatedButton):
    def __init__(self, text, on_click, visible=True):
        super().__init__(text=text, on_click=on_click, url_target='_self',
                         width=200, height=50, visible=visible)

class RegistrationButton(ft.ElevatedButton):
    def __init__(self, text_fields: list, on_click ):
        self.text_fields = text_fields
        super().__init__("registration", on_click=on_click)

    def update_registration_button(self):
        self.disabled = False
        for item in self.text_fields: # list[ui_elements] + self.validated =
            if item.current.validated == False:
                self.disabled = True
                break



    # 1) Выполнить подвязку шедулл
    # 2) В констурктор передать ссылки на все textField

# 1) кнопка должна быть активной если все поля валидны ->
# login -> RegistrationFormTextField
# validated -> RegistrationFormTextField
# [{login: "TRUE"}]
#
# ссылку на поля должен принимать
# обновлять информацию по по полям каждую 1 секунду
# смотрю все ли validated = true
# def update_button():