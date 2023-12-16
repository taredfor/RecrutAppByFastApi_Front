import json

import requests
from flet import Page


class ApiManager():

    def __init__(self, page: Page):
        self.url = "http://127.0.0.1"
        self.port = 8000
        self.host = f'{self.url}:{self.port}'
        self.client_storage = page.client_storage
        self.access_token = self.read_access_token()
        #print(page)

    def save_access_token(self, access_tkn: str):
        print("save_token")
        #print(self.client_storage.get("access_tkn"))
        self.client_storage.clear()
        self.client_storage.set("access_tkn", access_tkn)
        self.access_token = access_tkn

    def save_refresh_token(self, refresh_tkn: str):
        print("save_token")
        #print(self.client_storage.get("access_tkn"))
        self.client_storage.clear()
        self.client_storage.set("refresh_tkn", refresh_tkn)
        self.access_token = refresh_tkn

    def read_access_token(self):
        #print("read_token")
        print(self.client_storage.get("access_tkn"))
        return self.client_storage.get("access_tkn")#[1:-1:1]

    def read_refresh_token(self):
        #print("read_token")
        print(self.client_storage.get("refresh_tkn"))
        return self.client_storage.get("refresh_tkn")#[1:-1:1]


    def authorize(self, login: str, password: str):
        # TODO: валидатор(Логина, Пароля(длина))
        print("read token")
        print(self.read_access_token())
        self.client_storage.clear()
        result = requests.get(f'{self.host}/login', params={"login": login, "pass_wd": password})
        print("pair token: ")
        print(result.json())
        self.save_access_token(result.json()["access_token"])
        self.save_refresh_token(result.json()["refresh_token"])
        print("authorize")
        #self.access_token =result.text
        #print(result.json()["access_token"])
        return result
    #eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJqb2JzIiwiZXhwIjoxNjkxMDY1MDg0fQ.lElm1b7dJ7QpecZQ8SyYVu9zak4F3xHMciKZF2n5Siw
    # def add_question()прикрутить токен

    def get_authorization(self):
        result = requests.get(f'{self.host}/get-questions', headers={"Authorization": f'Bearer {self.access_token}'})
        get_user_id_from_answers = requests.get(f'{self.host}/get_user_id_from_answers',
                                                headers={"Authorization": f'Bearer {self.access_token}'})
        return result, get_user_id_from_answers

    def get_user_id_from_answers(self):
        get_user_id_from_answers = requests.get(f'{self.host}/was_user_tested', headers={"Authorization": f'Bearer {self.access_token}'})
        return get_user_id_from_answers.json()["was_tested"]

    def read_items(self):
        result = requests.get(f'{self.host}/items', headers={"Authorization": f'Bearer {self.access_token}'})
        return result
    def get_question(self):
        result = requests.get(f'{self.host}/get-questions', headers={"Authorization": f'Bearer {self.access_token}'})
        return result.json()
    def get_role(self):
        #print(self.access_token)
        result = requests.get(f'{self.host}/role', headers={"Authorization": f'Bearer {self.access_token}'})
        print("result1")
        print(result)
        #print(result.json().keys())
        print(f'result {result.json()["user_role"]}')
        print(result.json())
        print(result.json()["user_role"])
        return result.json()["user_role"]
    def sent_answer_to_back(self, payload: list):
        print(payload)
        #payload = json.dumps(payload)
        requests.post(f'{self.host}/post_answers', headers={"Authorization": f'Bearer {self.access_token}'}, data=json.dumps(payload))
    def get_user_hire_status(self):
        result = requests.get(f'{self.host}/status', headers={"Authorization": f'Bearer {self.access_token}'})
        return result.json()["recrut_status"]

if __name__ == "__main__":
    api_m = ApiManager(Page())
    #print(api_m.authorize("jobs", "string").json())
    #print(api_m.authorize("jobs", "string").json())
    #print(api_m.get_questions().json())
    print(api_m.read_items().json())
    print(ap)