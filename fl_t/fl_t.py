import flet as ft
from flet_core.alignment import center

from api_manager.api_manager import ApiManager

api_manager = ApiManager()


def main(page: ft.Page):
    login = ft.Ref[ft.TextField]()
    password = ft.Ref[ft.TextField]()
    greetings = ft.Ref[ft.Column]()
    login_incorrect_label = ft.Text("Login incorrect", visible=False)

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

    def button_click(e):
        greetings.current.controls.append(
            ft.Text(f'Hello {login.current.value}!')
        )
        result = api_manager.authorize(login.current.value, password.current.value)
        if result.status_code == 200:
            route_changes("/test")
        elif result.status_code == 401:
            #route_changes("/")
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
                            vertical_alignment=ft.CrossAxisAlignment.CENTER
                        ),
                        ft.Column(ref=greetings, ),
                        # ft.AppBar(title=ft.Text("Flet app"), ),
                        # ft.ElevatedButton("Visit Store", on_click=lambda _: page.go("/store"))
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
            page.route = "/test"
            page.go(page.route)
            elevated_button = ft.ElevatedButton("Go Home", on_click=lambda _: page.go("/"))
            elevated_button.visible = False
            page.views.append(
                    ft.View(
                        "/test",
                        [
                            ft.AppBar(title=ft.Text("Test")),
                            elevated_button,
                        ]
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
        page.update()

    def view_pop(view):
        page.views.pop()
        top_view = page.views[-1]
        page.go(top_view.route)

    page.on_route_change = route_changes
    page.on_view_pop = view_pop
    page.go(page.route)


ft.app(port=8002, target=main, view=ft.AppView.WEB_BROWSER)
