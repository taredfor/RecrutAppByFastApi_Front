import requests
from flet import Page


class ApiManager():

    def __init__(self, page: Page):
        self.url = "http://127.0.0.1"
        self.port = 8000
        self.host = f'{self.url}:{self.port}'
        self.client_storage = page.client_storage
        self.token = self.read_token()
        #print(page)

    def save_token(self, access_tkn: str):
        print("save_token")
        print(self.client_storage.get("access_tkn"))
        self.client_storage.clear()
        self.client_storage.set("access_tkn", access_tkn)

    def read_token(self):
        #print("read_token")
        print(self.client_storage.get("access_tkn"))
        return self.client_storage.get("access_tkn")#[1:-1:1]


    def authorize(self, login: str, password: str):
        # TODO: валидатор(Логина, Пароля(длина))
        print("read token")
        print(self.read_token())
        result = requests.get(f'{self.host}/login', params={"login": login, "pass_wd": password})
        self.save_token(result.json()["access_token"])
        print("authorize")
        #self.token =result.text
        print(result.json()["access_token"])
        return result
    #eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJqb2JzIiwiZXhwIjoxNjkxMDY1MDg0fQ.lElm1b7dJ7QpecZQ8SyYVu9zak4F3xHMciKZF2n5Siw
    # def add_question()прикрутить токен
    def get_authorization(self):
        result = requests.get(f'{self.host}/get-questions', headers={"Authorization": f'Bearer {self.token}'})
        return result
    def read_items(self):
        result = requests.get(f'{self.host}/items', headers={"Authorization": f'Bearer {self.token}'})
        return result
    def get_question(self):
        result = requests.get(f'{self.host}/get-questions', headers={"Authorization": f'Bearer {self.token}'})
        return result.json()
    def get_role(self):
        print(self.token)
        result = requests.get(f'{self.host}/role', headers={"Authorization": f'Bearer {self.token}'})
        print("result1")
        print(result)
        print(f'result{result.json()["user_role"]}')
        #print(result.json())
        print(result.json()["user_role"])
        return result.json()["user_role"]
    def sent_answer_to_back(self, payload: dict):
        requests.post(f'{self.host}/post_answers', json={'questions': payload})
#api_m = ApiManager()

if __name__ == "__main__":
    #print(api_m.authorize("jobs", "string").json())
    #print(api_m.authorize("jobs", "string").json())
    #print(api_m.get_questions().json())
    print(api_m.read_items().json())