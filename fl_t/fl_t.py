import logging

import flet
import flet as ft
from flet_core.alignment import center
from validator.validator import validate_password
from api_manager.api_manager import ApiManager

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
    login_incorrect_label = ft.Text("Login incorrect", visible=False)
    first_name = ft.Ref[ft.TextField]()
    second_name = ft.Ref[ft.TextField]()
    e_mail = ft.Ref[ft.TextField]()
    planet = ft.Ref[ft.TextField]()
    success_field = ft.Ref[ft.Text]()
    api_manager = ApiManager(page)

    def column_with_horizont_alignment(align: ft.CrossAxisAlignment):
        return ft.Column(
            [
                ft.TextField(ref=login,
                             label='Login',
                             autofocus=True,
                             text_align=center,
                             width=200,
                             height=50,
                             ),
                ft.TextField(ref=password,
                             label='Password',
                             autofocus=True,
                             text_align=center,
                             width=200,
                             height=50,
                             ),
                ft.ElevatedButton("To come in",
                                  on_click=button_click,
                                  # url="store",
                                  url_target="_self",
                                  width=200,
                                  height=50,
                                  ),
                ft.ElevatedButton("Registration",
                                  on_click=button_click_registration_form,
                                  # url="store",
                                  url_target="_self",
                                  width=200,
                                  height=50,
                                  )
                #     content=ft.Column(
                #         alignment=ft.MainAxisAlignment.CENTER,
                #         horizontal_alignment=align, )

            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=align.CENTER
        )

    def form_for_user_registration(align: ft.CrossAxisAlignment):
        return ft.Column(
            [
                ft.TextField(ref=login,
                             label='Login',
                             autofocus=True,
                             text_align=center,
                             width=200,
                             height=50,
                             ),
                ft.TextField(ref=first_name,
                             label='First name',
                             autofocus=True,
                             text_align=center,
                             width=200,
                             height=50,
                             ),
                ft.TextField(ref=second_name,
                             label='Second name',
                             autofocus=True,
                             text_align=center,
                             width=200,
                             height=50,
                             ),
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
                ft.TextField(ref=e_mail,
                             label='email',
                             autofocus=True,
                             text_align=center,
                             width=200,
                             height=50,
                             ),
                ft.TextField(ref=password,
                             label='Password',
                             autofocus=True,
                             text_align=center,
                             width=200,
                             height=50,
                             ),
                ft.ElevatedButton("To come in",
                                  on_click=button_click_create_recrut,
                                  # url="store",
                                  url_target="_self",
                                  width=200,
                                  height=50,
                                  visible=False
                                  ),
                #     content=ft.Column(
                #         alignment=ft.MainAxisAlignment.CENTER,
                #         horizontal_alignment=align, )
                ft.Text(
                        ref=success_field,
                        value="Корректный пароль",
                        text_align=center,
                        width=200,
                        height=50,
                        color='RED',
                        disabled=False)
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=align.CENTER,
            visible=True
        )

    def button_submit(e):
        main_answer_to_send = []
        page.views.clear()
        print(f'Распечатываем rows:{rows}')
        for row in rows:
            question_id = row.controls[0].question_id
            main_answer_to_send.append({'question_id': question_id,
                                        'user_answer': row.controls[1].value})
        api_manager.sent_answer_to_back(main_answer_to_send)
        page.go("/test")
        page.update()

    def button_click(e):
        greetings.current.controls.append(
            ft.Text(f'Hello {login.current.value}!')
        )
        result = api_manager.authorize(login.current.value,
                                       password.current.value)
        print(result)
        if result.status_code == 200:
            if api_manager.get_role() == "RECRUT":
                get_user_id_from_answers = api_manager.get_user_id_from_answers()
                data = get_user_id_from_answers
                route_changes("/test")
            elif api_manager.get_role() == "ADMIN":
                print("Зашел админ")
        elif result.status_code == 400:
            # route_changes("/")
            login_incorrect_label.visible = True
        # login.value = ""
        page.update()
        # password.current.focus()

    def button_click_registration_form(e):
        page.views.clear()
        route_changes("/registration")
        page.update()

    # 1. Вынести if в отдельный метод. if route == '/sith' -> def route_sith(page: ft.Page)
    # 2. Добавить пару route_string:method в route_methods

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
                                            on_click=lambda _: page.go("/"),
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
                ft.ElevatedButton("Submit", on_click=button_submit, ),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            vertical_alignment=ft.MainAxisAlignment.CENTER,
        )
        if api_manager.get_user_id_from_answers():
            page.views.append(view_statuses)
        else:
            page.views.append(view_test)

    def route_registration(page: ft.Page):
        page.route = "/registration"
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
                                            on_click=lambda _: page.go("/"))
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
                       # alignment=ft.alignment.center,
                       # vertical_alignment=ft.CrossAxisAlignment.CENTER,
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
