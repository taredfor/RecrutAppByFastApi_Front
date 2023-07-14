import requests

class ApiManager():

    def __init__(self):
        self.url = "http://127.0.0.1"
        self.port = 8000
        self.host = f'{self.url}:{self.port}'
        #self.token = load_from_file

    def save_token(self, access_tkn: str):
        f = open("access_tkn.txt", "w")
        w = f.write(access_tkn)
        f.close()

    def authorize(self, login: str, password: str):
        # TODO: валидатор(Логина, Пароля(длина))
        result = requests.get(f'{self.host}/login', params={"login": login, "pass_wd": password})
        self.save_token(result.text)
        #self.token =result.text
        print(result.status_code)
        return result
    # def add_question()прикрутить токен
    def get_questions(self):
        result = requests.get(f'{self.host}/get-questions', headers={"Authorization": Bearer})

api_m = ApiManager()

if __name__ == "__main__":
    #print(api_m.authorize("jobs", "string").json())
     print(api_m.authorize("jobs", "string").json())