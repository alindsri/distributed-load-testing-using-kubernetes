from locust import HttpLocust, TaskSet, TaskSequence, seq_task
from random import randrange
import json


headers = {
	'embibe-token': ''
}

user_name = {
	"user_name": f"{randrange(1000000,9999999)}@hotmail.com"
}



class UserBehavior(TaskSequence):

	@seq_task(1)
	def guest_signup(self):
		data = {
			"flag" : "gsp"
		}
		response = self.client.post('/user_auth/auth/sign_in', name="guest_signup" ,headers=headers, data=json.dumps(data))
		assert response.json()['success'] == True
	
	@seq_task(2)
	def normal_signup(self):
		data = {
			"login":user_name["user_name"],
			"password":"embibe1234",
			"password_confirmation":"embibe1234",
			"goal_code":"gl8",
			"flag":"sp"
		}
		response = self.client.post('/user_auth/auth/sign_in', name="normal_signup", headers=headers, data=json.dumps(data))
		assert response.json()['success'] == True
	
	@seq_task(3)
	def signin(self):
		data = {
			"login":user_name["user_name"],
			"password":"embibe1234",
			"password_confirmation":"embibe1234"
		}
		response = self.client.post('/user_auth/auth/sign_in',name="signin",headers=headers, data=json.dumps(data))
		assert response.json()['success'] == True

class WebsiteUser(HttpLocust):
	task_set = UserBehavior