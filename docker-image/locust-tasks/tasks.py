from locust import HttpLocust, TaskSet, TaskSequence, seq_task

class UserBehavior(TaskSequence):

    @seq_task(1)
    def signup(self):
        response = self.client.get(url = "/user_auth/healthcheck", name="healthcheck")
        assert response.text == "SUCCESS"

class WebsiteUser(HttpLocust):
    task_set = UserBehavior