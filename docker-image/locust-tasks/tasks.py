from locust import HttpLocust, TaskSet, TaskSequence, seq_task
from random import randrange

random_number = randrange(1000000000,9000000000)

class UserBehavior(TaskSequence):

    @seq_task(1)
    def signup(self):
        data = {
            "login": random_number,
            "password": "embibe1234",
            "password_confirmation": "embibe1234",
            "goal_code": "gl8",
            "org_id": 961,
            "source": "b2b-app"
        }
        response = self.client.post(url = "/user_ms_lt/auth/sign_in", name="Signup",  headers=headers, data=data)
        assert response.json()['success'] == True

    @seq_task(2)
    def login(self):
        data = {
            'user[login]': random_number,
            'user[password]': "embibe1234",
            'app_id': 'NTA--SandwichApp',
            'pack_type': 'PACK-NTA'
        }
        response = self.client.post(url = "http://preprod.embibe.com/mobile/sandwich_app/login?api_version=2", name="Login", headers=headers, data=data)


class WebsiteUser(HttpLocust):
    task_set = UserBehavior