import logging

import flet
import flet as ft
from flet_core.alignment import center
from validator.validator import validate_password, validate_email, \
    placeholder_validate
from api_manager.api_manager import ApiManager
from fl_t.ui_elements import RegistrationFormTextField, Button, \
    RegistrationFormTextFieldUserLoginPassword, \
    RegistrationFormSecondPasswordTextField, \
    RegistrationFormMainPasswordTextField, \
    RegistrationButton

sith_show_answers = [ft.Text("Эта страница для Ситха")]

admin_panel = [ft.Text("Страница Админа")]

logging.basicConfig(level=logging.INFO, filename="py_log.log", filemode="w",
                    format="%(asctime)s %(levelname)s %(message)s")
logging.debug("A DEBUG Message")
logging.info("An INFO")
logging.warning("A WARNING")
logging.error("An ERROR")
logging.critical("A message of CRITICAL severity")

rows = []


class AnswerTextField(flet.TextField):
    question_id = -1


api_manager = None


def main(page: ft.Page):
    login = ft.Ref[ft.TextField]()
    password = ft.Ref[ft.TextField]()
    greetings = ft.Ref[ft.Column]()
    # login_incorrect_label = ft.Text("Login incorrect", visible=False)
    first_name = ft.Ref[ft.TextField]()
    second_name = ft.Ref[ft.TextField]()
    e_mail = ft.Ref[ft.TextField]()
    planet = ft.Ref[ft.TextField]()
    success_field = ft.Ref[ft.Text]()
    main_password = ft.Ref[ft.TextField]()
    second_password = ft.Ref[ft.TextField]()
    api_manager = ApiManager(page)
    login_incorrect_label = ft.Text("Add Login", visible=True,
                                    text_align=center)
    password_incorrect_label = ft.Text("Add Password", visible=True,
                                       text_align=center)
    second_password_incorrect_label = ft.Text("Second Password", visible=True,
                                              text_align=center)
    email_incorrect_label = ft.Text("Email", visible=True)

    url_text_fileds = [login, password, e_mail, main_password, second_password]

    def button_submit(e):
        main_answer_to_send = []
        page.views.clear()
        print(f'Распечатываем rows:{rows}')
        for row in rows:
            question_id = row.controls[0].question_id
            main_answer_to_send.append({'question_id': question_id,
                                        'user_answer': row.controls[
                                            1].value})
        api_manager.sent_answer_to_back(main_answer_to_send)
        page.go("/test")
        page.update()

    def button_click_recrut_login(e):
        greetings.current.controls.append(
            ft.Text(f'Hello {login.current.value}!')
        )
        result = api_manager.authorize(login.current.value,
                                       password.current.value)
        if result.status_code == 200:
            if api_manager.get_role() == "RECRUT":
                page.go("/test")
            elif api_manager.get_role() == "ADMIN":
                print("Зашел админ")
        login_incorrect_label.visible = (result.status_code == 400)
        page.update()

    def button_click_registration_form(e):
        page.views.clear()
        page.go("/registration")
        page.update()

    def button_click_logging_after_registration(e):
        page.views.clear()
        page.go("/login")
        page.update()

    def column_with_horizont_alignment(align: ft.CrossAxisAlignment):
        return ft.Column(
            [
                RegistrationFormTextFieldUserLoginPassword('Login', login),
                RegistrationFormTextFieldUserLoginPassword('Password',
                                                           password),
                Button("To come in", button_click_recrut_login),
                Button("Registration", button_click_registration_form),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=align.CENTER
        )

    def form_for_user_registration(align: ft.CrossAxisAlignment):
        return ft.Column(
            [
                ft.Row(
                    [
                        RegistrationFormTextField('Login', login,
                                                  login_incorrect_label,
                                                  api_manager.validate_user_login,
                                                  page, "Login is Free",
                                                  "Login exists"
                                                  ),
                        login_incorrect_label
                    ]
                ),
                RegistrationFormTextField('First name',
                                          first_name,
                                          placeholder_validate),
                RegistrationFormTextField('Second name',
                                          second_name,
                                          placeholder_validate),
                ft.Dropdown(ref=planet,
                            label='Planet',
                            autofocus=True,
                            width=200,
                            height=50,
                            options=[
                                ft.dropdown.Option("MARS"),
                                ft.dropdown.Option("JUPITER")
                            ]
                            ),
                ft.Row(
                    [
                        RegistrationFormTextField('email', e_mail,
                                                  email_incorrect_label,
                                                  validate_email, page,
                                                  "Email is valid",
                                                  "Email isn't valid"
                                                  ),
                        email_incorrect_label
                    ]
                ),
                ft.Row(
                    [
                        RegistrationFormMainPasswordTextField('Main password',
                                                  main_password, second_password,
                                                  password_incorrect_label,
                                                  validate_password, page,
                                                  "Valid password",
                                                  "Password is not correct"
                                                  ),
                        password_incorrect_label
                    ]
                ),
                ft.Row(
                    [
                        RegistrationFormSecondPasswordTextField(
                            'Second password',
                            # TODO: исправить валидацию проверки совпадения паролей
                            second_password, main_password,
                            second_password_incorrect_label,
                            None, page, "Password is equiles",
                            "Password is not equiles"
                            ),
                        second_password_incorrect_label
                    ]
                ),
                ft.Row(
                [
                    RegistrationButton(url_text_fileds, button_click_logging_after_registration)
                ]
            ),
                Button("To come in", button_click_registration_form),
            ],
            alignment=ft.MainAxisAlignment.START,
            horizontal_alignment=align.START,
            visible=True
        )

        # def textbox_changed(e):
        #     if api_manager.validate_user_login(e.control.value):
        #         login_incorrect_label.value = "Login exists"
        #         login_incorrect_label.color = "Red"
        #     else:
        #         login_incorrect_label.value = "Login is Free"
        #         login_incorrect_label.color = "Green"
        #     page.update()

        # def textbox_changed_password(e):
        #     if validate_password(e.control.value):
        #         password_incorrect_label.value = "Valid password"
        #         password_incorrect_label.color = "Green"
        #     else:
        #         password_incorrect_label.value = "Password is not correct"
        #         password_incorrect_label.color = "Red"
        #     textbox_changed_password_second(second_password.current.value)
        #     print(type(e))
        #     page.update()
        #
        # def textbox_changed_password_second(e):
        #     if isinstance(e, ft.ControlEvent):
        #         second_password_str = e.control.value
        #     else:
        #         second_password_str = e
        #     print("main_password_str:", main_password.current.value)
        #     main_password_str = main_password.current.value
        #     print("main_password_str:", main_password.current.value)
        #     if validate_password(main_password_str):
        #         if main_password_str == second_password_str:
        #             second_password_incorrect_label.value = "Password is equiles"
        #             second_password_incorrect_label.color = "Green"
        #         else:
        #             second_password_incorrect_label.value = "Password is not equiles"
        #             second_password_incorrect_label.color = "Red"
        #     else:
        #         second_password_incorrect_label.value = ""
        #     page.update()

        # def textbox_changed_email(e):
        #     if validate_email(e.control.value):
        #         if not api_manager.validate_user_email(e.control.value):
        #             email_incorrect_label.value = "Email is valid"
        #             email_incorrect_label.color = "Green"
        #     else:
        #         email_incorrect_label.value = "Email isn't valid"
        #         email_incorrect_label.color = "Red"
        #     page.update()

        # def button_submit(e):
        #     main_answer_to_send = []
        #     page.views.clear()
        #     print(f'Распечатываем rows:{rows}')
        #     for row in rows:
        #         question_id = row.controls[0].question_id
        #         main_answer_to_send.append({'question_id': question_id,
        #                                     'user_answer': row.controls[
        #                                         1].value})
        #     api_manager.sent_answer_to_back(main_answer_to_send)
        #     page.go("/test")
        #     page.update()

        # def button_click_recrut_login(e):
        #     greetings.current.controls.append(
        #         ft.Text(f'Hello {login.current.value}!')
        #     )
        #     result = api_manager.authorize(login.current.value,
        #                                    password.current.value)
        #     if result.status_code == 200:
        #         if api_manager.get_role() == "RECRUT":
        #             page.go("/test")
        #         elif api_manager.get_role() == "ADMIN":
        #             print("Зашел админ")
        #     login_incorrect_label.visible = (result.status_code == 400)
        #     page.update()
        #
        # def button_click_registration_form(e):
        #     page.views.clear()
        #     page.go("/registration")
        #     page.update()

    def button_click_create_recrut(e):
        # 1)
        # 2) Добавление пользователя в БД
        pass

    def route_default(page: ft.Page):
        page.views.append(
            ft.View(
                "/",
                [
                    ft.Row(
                        [
                            column_with_horizont_alignment(
                                ft.CrossAxisAlignment.CENTER),
                            login_incorrect_label
                        ],
                        spacing=30,
                        alignment=ft.MainAxisAlignment.CENTER,
                        vertical_alignment=ft.CrossAxisAlignment.CENTER,

                    ),
                    ft.Column(ref=greetings, ),
                ],

            )
        )

    def route_test(page: ft.Page):
        page.route = "/test"
        page.go(page.route)
        user_status = api_manager.get_user_hire_status()
        elevated_button = ft.ElevatedButton("Go Home",
                                            on_click=lambda _: page.go(
                                                "/"),
                                            visible=False)
        recrut_questions_elements = __items(api_manager.get_question())
        view_statuses = ft.View(
            "/test",
            [ft.Text(f'Your status: {user_status.lower()}', width=300,
                     color='GREEN' if user_status == "HIRED" else 'RED')])
        view_test = ft.View(
            "/test",
            [
                ft.Column(
                    recrut_questions_elements,
                    spacing=30,
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
                ft.Row(ref=greetings, ),
                ft.ElevatedButton("Submit", on_click=button_submit),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            vertical_alignment=ft.MainAxisAlignment.CENTER,
        )
        if api_manager.get_user_id_from_answers():
            page.views.append(view_statuses)
        else:
            page.views.append(view_test)

    def route_registration(page: ft.Page):
        page.go(page.route)
        page.views.append(
            ft.View(
                "/registration",
                [
                    ft.Row(
                        [
                            form_for_user_registration(
                                ft.CrossAxisAlignment.CENTER),
                        ],
                        spacing=30,
                        alignment=ft.MainAxisAlignment.CENTER,
                        vertical_alignment=ft.CrossAxisAlignment.CENTER,

                    ),
                    ft.Column(ref=greetings, ),
                ],
            )
        )

    def route_sith(page: ft.Page):
        page.route = "/sith"
        page.views.append(
            ft.View(
                "/sith",
                sith_show_answers
            )
        )

    def route_admin(page: ft.Page):
        page.route = "/admin"
        page.views.append(
            ft.View(
                "/admin",
                admin_panel
            )
        )

    def route_took_test(page: ft.Page):
        page.route = "/you_took_this_test"
        elevated_button = ft.ElevatedButton("Go Home",
                                            on_click=lambda _: page.go(
                                                "/"))
        elevated_button.visible = True
        page.go(page.route)
        new_task = ft.Text("Вы уже проходили тестирование", width=300)
        page.views.append(ft.View("/you_took_this_test",
                                  [new_task, elevated_button],
                                  horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                  vertical_alignment=ft.MainAxisAlignment.CENTER,
                                  ))

    def route_changes(event: flet.RouteChangeEvent):
        route_methods = {
            "/": route_default,
            "/test": route_test,
            "/sith": route_sith,
            "/admin": route_admin,
            "/registration": route_registration,
            "/you_took_this_test": route_took_test
        }
        page.views.clear()
        method = route_methods[event.route]
        method(page)
        page.update()

    def __items(l_st: dict):
        rows.clear()
        for question_id in l_st:
            dropdowns = ft.Dropdown(options=[
                ft.dropdown.Option("True"),
                ft.dropdown.Option("False")
            ]
            )
            answer_text_field = AnswerTextField(
                value=str(l_st[question_id] + "?"))
            answer_text_field.question_id = question_id
            rows.append(
                ft.Row([answer_text_field,
                        dropdowns
                        ],
                       )
            )
        print(f'rows is items {rows}')
        return rows

    def view_pop(view):
        page.views.pop()
        top_view = page.views[-1]
        page.go(top_view.route)

    page.on_route_change = route_changes
    page.on_view_pop = view_pop
    page.go(page.route)


ft.app(port=8002, target=main, view=ft.AppView.WEB_BROWSER)
