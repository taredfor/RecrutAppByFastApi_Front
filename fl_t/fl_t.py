import flet as ft
from flet_core.alignment import center

from api_manager.api_manager import ApiManager

sith_show_answers = [ft.Text("Эта страница для Ситха")]

admin_panel = [ft.Text("Страница Админа")]

rows = []
def main(page: ft.Page):
    login = ft.Ref[ft.TextField]()
    password = ft.Ref[ft.TextField]()
    greetings = ft.Ref[ft.Column]()
    login_incorrect_label = ft.Text("Login incorrect", visible=False)
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
                                  )
                #     content=ft.Column(
                #         alignment=ft.MainAxisAlignment.CENTER,
                #         horizontal_alignment=align, )

            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=align.CENTER
        )


    def items(l_st: list):
        rows.clear()
        for i in range(len(l_st)):
            dropdowns = ft.Dropdown(options=[
                ft.dropdown.Option("True"),
                ft.dropdown.Option("False")
            ]
            )
            rows.append(
                ft.Row([ft.TextField(value=str(l_st[i] + "?")),
                        dropdowns
                        ],
                       # alignment=ft.alignment.center,
                       # vertical_alignment=ft.CrossAxisAlignment.CENTER,
                       )
            )
        print(f'rows is items {rows}')
        return rows

    def button_submit(e):
        answers_to_send = {}
        print(f'Распечатываем rows:{rows}')
        for row in rows:
            question_text = row.controls[0].value
            answers_to_send[question_text] = row.controls[1].value
        print(answers_to_send)


    def button_click(e):
        greetings.current.controls.append(
            ft.Text(f'Hello {login.current.value}!')
        )
        result = api_manager.authorize(login.current.value, password.current.value)
        if result.status_code == 200:
            if api_manager.get_role() == "USER":
                route_changes("/test")
            elif api_manager.get_role() == "ADMIN":
                print("Зашел админ")
        elif result.status_code == 400:
            # route_changes("/")
            login_incorrect_label.visible = True
        # login.value = ""
        page.update()
        # password.current.focus()

    #
    # page.add(
    #     ft.Row(
    #         [   ft.Text("Первый вход"),
    #             column_with_horizont_alignment(ft.CrossAxisAlignment.CENTER, ""),
    #         ],
    #         spacing=30,
    #         alignment=ft.MainAxisAlignment.CENTER,
    #         vertical_alignment=ft.CrossAxisAlignment.CENTER
    #     ),
    #     ft.Column(ref=greetings, )
    # )

    #### Переход между страницами
    sith_questions_elements = [

    ]

    def route_changes(route):
        page.views.clear()
        if page.route == "/":
            page.views.append(
                ft.View(
                    "/",
                    [
                        ft.Row(
                            [
                                column_with_horizont_alignment(ft.CrossAxisAlignment.CENTER),
                                login_incorrect_label
                            ],
                            spacing=30,
                            alignment=ft.MainAxisAlignment.CENTER,
                            vertical_alignment=ft.CrossAxisAlignment.CENTER,

                        ),
                        ft.Column(ref=greetings, ),
                        # ft.AppBar(title=ft.Text("Flet app"), ),
                        # ft.ElevatedButton("Submit", on_click=lambda _: page.go("/test"))
                    ],
                )
            )
        #     # page.update()
        # elif page.route == "/test":
        #     page.views.append(
        #         ft.View(
        #             "/test",
        #             [
        #                 ft.AppBar(title=ft.Text("Test")),
        #                 ft.ElevatedButton("Go Home", on_click=lambda _: page.go("/")),
        #             ]
        #         )
        #     )
        if route == "/test":
            print("route /test")
            page.route = "/test"
            page.go(page.route)
            elevated_button = ft.ElevatedButton("Go Home", on_click=lambda _: page.go("/"))
            elevated_button.visible = False
            questions = list(api_manager.get_question().values())
            recrut_questions_elements = items(questions)
            print(recrut_questions_elements[1].controls[0].value)
            # recrut_answers_elements = items_id(questions)
            page.views.append(
                ft.View(
                    "/test",
                    # recrut_questions_elements
                    [
                        ft.Column(
                            recrut_questions_elements,
                            spacing=30,
                            alignment=ft.MainAxisAlignment.CENTER,
                            # horizontal_alignment=ft.CrossAxisAlignment.CENTER,

                        ),
                        ft.Row(ref=greetings, ),
                        ft.ElevatedButton("Submit", on_click=button_submit, ),
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    vertical_alignment=ft.MainAxisAlignment.CENTER,
                    # horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    # ft.ElevatedButton("Submit", on_click=lambda _: page.go("/test")),
                    # ft.AppBar(title=ft.Text("Test")),
                    # ft.AppBar(title=ft.Text(api_manager.read_token())),
                    # ft.AppBar(title=ft.Text(api_manager.get_question())),
                    # elevated_button,
                )
            )
        elif route == "/":
            page.route = route
            page.views.append(
                ft.View(
                    "/",
                    [
                        ft.AppBar(title=ft.Text("Flet")),
                    ]
                )
            )
        elif route == "/sith":
            page.route = route
            page.views.append(
                ft.View(
                    "/sith",
                    sith_show_answers
                )
            )
        elif route == "/admin":
            page.route = route
            page.views.append(
                ft.View(
                    "/admin",
                    admin_panel
                )
            )
        page.update()

    def view_pop(view):
        page.views.pop()
        top_view = page.views[-1]
        page.go(top_view.route)

    page.on_route_change = route_changes
    page.on_view_pop = view_pop
    page.go(page.route)


ft.app(port=8002, target=main, view=ft.AppView.WEB_BROWSER)
